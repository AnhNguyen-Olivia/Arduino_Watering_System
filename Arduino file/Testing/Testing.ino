#include <Arduino.h>

const int SENSOR_PIN = A0;
const int RELAY_PIN = 4;

void setup() {
  Serial.begin(9600); // Use the hardware Serial over USB
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);
}

void loop() {
  // Read sensor and send data to computer
  int soil_moisture = analogRead(SENSOR_PIN);
  Serial.print("SOIL:");
  Serial.println(soil_moisture);

  // Check for commands from computer
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim(); 
    
    if (command == "RELAY_ON") {
      digitalWrite(RELAY_PIN, HIGH);
    } else if (command == "RELAY_OFF") {
      digitalWrite(RELAY_PIN, LOW);
    }
  }

  delay(1000);
}