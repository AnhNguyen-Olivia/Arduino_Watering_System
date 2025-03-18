#include <iostream>;
#include <Arduino.h>
using namespace std;
// Define the pins
int sensorPin = A0;

// Variables to store sensor value
int sensorValue = 0;

void setup() {
  // Initialize serial communication at 9600 baud rate
  Serial.begin(9600);
  
  pinMODE(A0,INPUT);
  pinMODE(PIN_WIRE_SCL, OUTPUT);
}

void loop() {
  // Read the analog value from the sensor
  sensorValue = analogRead(A0);
  
  // Print the sensor value to the Serial Monitor
  Serial.print("Soil Moisture Value: ");
  Serial.println(sensorValue);
  
  // Check if the soil is dry
  if (sensorValue > 450) {
    serial.println("Soil Moisture is low, turning on the relay");


  } else {
    serial.println("Soil Moisture is high, turning off the relay");
  }
  
  // Wait for a second before taking another reading
  delay(10000);
}

