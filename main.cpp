#include <WiFi.h>
#include <HTTPClient.h>
#include "HX711.h"
#include <math.h>

// WiFi credentials
#define WIFI_SSID "your wifi name"
#define WIFI_PASSWORD "passcode"

// Pin configuration
#define FORMALDEHYDE_PIN 34
#define DT 14
#define SCK 27
#define TARE_BUTTON_PIN 5
#define FORMALIN_LED_PIN 2

// HX711 instance
HX711 scale;

// Calibration constants
const float Ro = 3720.0;               // MQ-138 clean air resistance
const float calibration_factor = 215.0; // HX711 scale factor

// Connect to WiFi with debug output
void connectToWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  int attempts = 0;

  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ WiFi Connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n❌ WiFi Connection Failed. Check SSID/password or switch to 2.4GHz.");
  }
}

// Read formaldehyde concentration from MQ-138
float readFormaldehydePPM() {
  int analogValue = analogRead(FORMALDEHYDE_PIN);
  float voltage = analogValue * (3.3 / 4095.0);
  float Rs = (3.3 - voltage) * 10000.0 / voltage;
  float ratio = Rs / Ro;
  float ppm = pow(10, (-1.522 * log10(ratio) + 2.096));

  digitalWrite(FORMALIN_LED_PIN, ppm <= 15.5 ? HIGH : LOW); // Turn on LED if high ppm
  return ppm;
}

// Read weight from HX711
float readWeight() {
  if (scale.is_ready()) {
    return abs(scale.get_units(10)); // Average over 10 readings
  }
  return 0.0;
}

// Send sensor data to Flask server
void sendSensorData() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin("http://192.168.81.223:5000/data");   // LAPTOP'S IP

  // Update with your Flask server IP
    http.addHeader("Content-Type", "application/json");

    float weight = readWeight();
    float formaldehydePPM = readFormaldehydePPM();

    if (weight > 0.0) {
      String jsonPayload = "{\"weight\": " + String(weight, 2) +
                           ", \"formaldehyde\": " + String(formaldehydePPM, 2) + "}";

      Serial.println("Sending JSON: " + jsonPayload);
      int httpResponseCode = http.POST(jsonPayload);

      if (httpResponseCode > 0) {
        Serial.println("✅ Data sent! Response: " + String(httpResponseCode));
      } else {
        Serial.println("❌ Error sending data: " + String(http.errorToString(httpResponseCode)));
      }
    }

    http.end();
  } else {
    Serial.println("WiFi disconnected. Reconnecting...");
    connectToWiFi();
  }
}

void setup() {
  Serial.begin(115200);
  delay(3000);  // Allow time for mobile hotspot to stabilize

  pinMode(TARE_BUTTON_PIN, INPUT_PULLUP);
  pinMode(FORMALIN_LED_PIN, OUTPUT);

  connectToWiFi();

  scale.begin(DT, SCK);
  scale.set_scale(calibration_factor);
  scale.tare();
  Serial.println("HX711 initialized. Taring...");
}

void loop() {
  if (digitalRead(TARE_BUTTON_PIN) == LOW) {
    scale.tare();
    Serial.println("Tare button pressed");
    delay(300);
  }

  sendSensorData();
  delay(1000);  // Delay before next reading
}
