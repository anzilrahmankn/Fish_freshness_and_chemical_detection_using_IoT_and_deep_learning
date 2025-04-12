
# Fish Freshness and Formaldehyde Detection System

## Overview

This project aims to automate fish freshness detection and formaldehyde (formalin) monitoring using IoT technology. The system utilizes an **ESP32-WROOM** module integrated with sensors such as **HX711 (Load Cell)** for weight measurement and the **MQ-138** sensor for formaldehyde detection. The system generates dynamic pricing for fish based on freshness and weight, alongside QR and barcode generation for each transaction.

### Features:
- **Formalin Detection:** Alerts if formaldehyde levels exceed safe limits.
- **Weight Measurement:** Accurate weight calculation using the HX711 and load cell.
- **Dynamic Pricing Algorithm:** Calculates price based on weight and freshness.
- **QR and Barcode Generation:** Automatically generates QR codes and barcodes for fish purchases.
- **No Barcode for Unsafe Fish:** No barcode is printed if formalin levels are detected or if the fish is deemed not fresh.

---

## Requirements

### Hardware:
- **ESP32-WROOM** (or compatible)
- **HX711 Load Cell** for weight measurement
- **MQ-138 Sensor** for formaldehyde detection
- **LED (optional)** for formalin alerts
- **Tare Button** (optional) for resetting weight

### Software:
- **Python 3.x**
- **Flask** (Web framework)
- **TensorFlow** (For freshness prediction)
- **Git** for version control
- **Git LFS** for large file management

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/anzilrahmankn/Fish_freshness_and_chemical_detection_using_IoT_and_deep_learning.git
cd Fish_freshness_and_chemical_detection_using_IoT_and_deep_learning
```

### 2. Create a Virtual Environment
To set up a Python virtual environment, run:
```bash
python -m venv venv
```

### 3. Install Dependencies
Activate the virtual environment and install the necessary dependencies:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 4. Download Model File (Fish Freshness Model)
- Download the pre-trained `.h5` model file from [Google Drive](<Google-Drive-Link>).
- Place it in the `/model/` directory of the project.

### 5. Configure Wi-Fi and Upload to ESP32
1. Edit the Wi-Fi credentials in the `config.h` file:
```cpp
#define WIFI_SSID "your-SSID"
#define WIFI_PASSWORD "your-PASSWORD"
```

2. Compile and upload the code to the ESP32 using the Arduino IDE or PlatformIO:
```cpp
#define FORMALDEHYDE_PIN 34
#define DT 14
#define SCK 27
#define TARE_BUTTON_PIN 5
#define FORMALIN_LED_PIN 2  // Connected to formaldehyde detection LED
```

### 6. Run the Flask Application
Run the Flask app to start the web server:
```bash
python app.py
```
This will start a local server, and you can access the web interface to view freshness results and barcode/QR code generation.

### 7. Monitor ESP32 Output
Open a serial monitor or use a terminal to view the ESP32 outputs. It will print weight and formaldehyde readings in real-time.

### 8. Testing and Debugging
- Ensure the sensors are correctly connected and calibrated.
- Use the `TARE_BUTTON_PIN` to reset the weight measurement.
- Formalin levels above the set threshold will trigger the formalin LED and stop barcode generation.

---

## Contact

For any questions or further assistance, feel free to contact:  
**Email:** anzilrahmankn@gmail.com
