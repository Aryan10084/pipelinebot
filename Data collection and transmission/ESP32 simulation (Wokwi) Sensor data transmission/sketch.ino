#include <WiFi.h>
#include <HTTPClient.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>

// Pin Definitions
#define DHTPIN 4
#define MQ2PIN 35
#define POTENTIOMETER_PIN 34 // Analog pin for the potentiometer
#define DHTTYPE DHT22

// Sensor Objects
DHT dht(DHTPIN, DHTTYPE);

// WiFi credentials
const char* ssid = "Wokwi-GUEST";  // Replace with your WiFi SSID
const char* password = "";        // Replace with your WiFi password

// Cloudflare Tunnel URL
const char* serverUrl = "https://filename-hobbies-expansion-techniques.trycloudflare.com/data"; // Ensure the /data endpoint is used

void setup() {
  Serial.begin(115200);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi!");

  // Initialize DHT sensor
  dht.begin();
}

void loop() {
  // Read Sensor Data
  float temperature = dht.readTemperature();  // in Celsius (°C)
  float humidity = dht.readHumidity();        // in Percentage (%)
  
  // Read MQ2 gas sensor (in voltage) and simulate gas concentration in ppm (parts per million)
  float gasLevel = analogRead(MQ2PIN) * (3.3 / 4095.0);  // Convert analog reading to voltage

  // Read potentiometer as pressure sensor and simulate pressure (in Pascals)
  float simulatedPressure = analogRead(POTENTIOMETER_PIN) * (3.3 / 4095.0);  // Convert to voltage
  float pressure = simulatedPressure * 100000; // Simulating pressure (1V corresponds to 100 kPa)

  // Check if sensor readings are valid
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Print data for debugging
  Serial.print("Temperature: "); Serial.print(temperature); Serial.print(" °C, ");
  Serial.print("Humidity: "); Serial.print(humidity); Serial.print(" %, ");
  Serial.print("Gas Level: "); Serial.print(gasLevel); Serial.print(" V, ");
  Serial.print("Pressure: "); Serial.print(pressure); Serial.println(" Pa");

  // Send Data to Server
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Prepare JSON payload
    String jsonData = "{";
    jsonData += "\"temperature\":" + String(temperature, 2) + ","; // in °C
    jsonData += "\"humidity\":" + String(humidity, 2) + ",";       // in %
    jsonData += "\"gasLevel\":" + String(gasLevel, 2) + ",";       // in V (Voltage)
    jsonData += "\"pressure\":" + String(pressure, 2);              // in Pa (Pascals)
    jsonData += "}";

    // Send POST request
    int httpResponseCode = http.POST(jsonData);

    // Check response
    if (httpResponseCode > 0) {
      Serial.print("Server Response Code: ");
      Serial.println(httpResponseCode);
    } else {
      Serial.print("Error Sending Data: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi Disconnected!");
  }

  delay(5000); // Wait for 5 seconds before sending the next data
}
