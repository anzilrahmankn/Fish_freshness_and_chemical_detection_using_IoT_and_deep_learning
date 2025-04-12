# Fish Freshness and Chemical Detection Using IoT and Deep Learning

This project utilizes IoT technologies and deep learning to detect fish freshness and formalin contamination. It employs the **ESP32-WROOM** microcontroller, an **HX711 load cell** for weight measurement, and an **MQ-138** sensor for formalin (formaldehyde) detection. The system communicates wirelessly with a **Flask web application** running on a local server to process the data and provide results.

## Features
- **ESP32-WROOM** for weight and formalin detection.
- **HX711 load cell** for accurate weight measurements.
- **MQ-138 sensor** for detecting formalin levels.
- **Flask web app** for processing data and generating results.
- **Machine learning** integration for freshness prediction.
- **WiFi-based communication** for easy integration with web applications.

## Requirements

### Software Requirements
- **Python 3.x**
- **Flask** (For running the web app)
- **TensorFlow** (For deep learning model)
- **Git LFS** (For tracking large files)

### Hardware Requirements
- **ESP32-WROOM** microcontroller
- **HX711 load cell**
- **MQ-138 formaldehyde sensor**

## Setting Up the Project

### Step 1: Create a Virtual Environment

1. Open a terminal (or Command Prompt).
2. Navigate to your project directory:
    ```bash
    cd path/to/project/folder
    ```
3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On **Windows**:
      ```bash
      .\venv\Scripts\activate
      ```
    - On **Linux/macOS**:
      ```bash
      source venv/bin/activate
      ```

### Step 2: Install Project Dependencies

1. Ensure your virtual environment is activated.
2. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

### Step 3: Download the Deep Learning Model

The deep learning model file (`model.h5`) is used for freshness prediction. You can download the model from Google Drive:

- [Download fish freshness model](https://drive.google.com/file/d/1VNAx5jCe_s0v-Si6zXJPVBwuxUni-acZ/view?usp=drive_link)

Once downloaded, place the `.h5` file in the root directory of your project.

### Step 4: Configure WiFi for ESP32

1. Open the **ESP32** source code and update the WiFi credentials in the `config.cpp` file.
2. Set your WiFi SSID and password:
    ```cpp
    const char* ssid = "your_wifi_ssid";
    const char* password = "your_wifi_password";
    ```

### Step 5: Upload Code to ESP32

1. Use the **Arduino IDE** or **PlatformIO** to upload the `esp32_code.cpp` (or equivalent) to the ESP32 microcontroller.
2. Ensure that the **HX711 load cell** and **MQ-138 sensor** are correctly connected to the ESP32.

### Step 6: Run the Flask Web App

1. Open another terminal window in the project directory.
2. Run the Flask web app:
    ```bash
    python app.py
    ```
3. The web app should now be running on your local server, and you can access it through `http://127.0.0.1:5000` or the specified host address.

### Step 7: Test the System

1. Open the **serial terminal** for the ESP32. It will send data regarding the fish weight and formalin levels.
2. The Flask app will display the fish freshness and pricing on the result page, based on the data received from the ESP32.

## Contributing

Feel free to contribute by reporting issues or submitting pull requests. Any help to improve the project is appreciated!

## Contact

For further assistance or queries, feel free to contact me at **anzilrahmankn@gmail.com**.
