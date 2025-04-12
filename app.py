from flask import Flask, request, render_template, jsonify
import tensorflow as tf
import numpy as np
import os
from keras.preprocessing import image

app = Flask(__name__)

# Load trained model
MODEL_PATH = "fish_freshness_model.h5"
if os.path.exists(MODEL_PATH):
    model = tf.keras.models.load_model(MODEL_PATH)
else:
    raise FileNotFoundError("❌ Model file not found at " + MODEL_PATH)

# Globals to store latest ESP32 data
latest_sensor_data = {
    "weight": None,
    "formaldehyde_ppm": None,
    "formalin_status": "Unknown"
}

# Price chart (per kg)
price_per_kg = {
    "Sardine": 80,
    "Mackerel": 60,
    "Silver Pomfret": 40,
    "Tilapia": 30
}

# Mapping form input to known fish types
fish_type_mapping = {
    "sardine": "Sardine",
    "mackerel": "Mackerel",
    "silver promfret": "Silver Pomfret",
    "tilapia": "Tilapia"
}

# Predict freshness from uploaded image
def predict_freshness(img_path):
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    prediction = model.predict(img_array)[0][0]
    return "Fresh" if prediction < 0.5 else "Not Fresh"

# Route: Upload page
@app.route('/')
def home():
    return render_template('upload.html')

# Route: Handle image + fish type form submission
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return render_template('result.html', prediction="No file uploaded")

    file = request.files['file']
    if file.filename == '':
        return render_template('result.html', prediction="No selected file")

    # Get fish type and map to known format
    raw_fish_type = request.form.get("fish_type", "Unknown").strip().lower()
    fish_type = fish_type_mapping.get(raw_fish_type, "Unknown")

    # Save uploaded image
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    # Run prediction
    prediction = predict_freshness(file_path)

    # Fetch latest sensor values
    weight = latest_sensor_data["weight"] if prediction == "Fresh" else None
    formaldehyde_ppm = latest_sensor_data["formaldehyde_ppm"] if prediction == "Fresh" else "N/A"
    formalin_status = latest_sensor_data["formalin_status"] if prediction == "Fresh" else "Not Applicable"

    # Price calculation
    if weight and fish_type in price_per_kg:
        price_per_gram = price_per_kg[fish_type] / 1000
        total_price = f"\u20B9{round(weight * price_per_gram, 2)}"
    else:
        total_price = "N/A"

    return render_template(
        'result.html',
        prediction=prediction,
        fish_type=fish_type,
        weight=weight,
        formaldehyde_ppm=formaldehyde_ppm,
        formalin=formalin_status,
        total_price=total_price
    )

# Route: ESP32 POSTs sensor values here
@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()

    if not data or 'weight' not in data or 'formaldehyde' not in data:
        return jsonify({"error": "Invalid data format"}), 400

    try:
        weight = float(data['weight'])
        formaldehyde = float(data['formaldehyde'])

        latest_sensor_data["weight"] = round(weight, 2)
        latest_sensor_data["formaldehyde_ppm"] = round(formaldehyde, 2)
        latest_sensor_data["formalin_status"] = "Detected" if formaldehyde < 15.5 else "Not Detected"

        print(f"📡 Data received: {weight}g, {formaldehyde} ppm → {latest_sensor_data['formalin_status']}")
        return jsonify({"message": "Data received successfully"}), 200

    except ValueError:
        return jsonify({"error": "Invalid number format"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
