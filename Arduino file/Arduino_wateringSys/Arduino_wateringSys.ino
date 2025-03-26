#include <Arduino.h>

const int SENSOR_PIN = A0;  // Analog pin 0
const int RELAY_PIN = 4;    // Use pin 4 (not conflicting with Serial)

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH); // Start with relay OFF (active-low)
  Serial.begin(9600);

}

void loop() {
  int moisture = analogRead(SENSOR_PIN);
  
  Serial.print("Moisture: ");
  Serial.print(moisture);
  
  if (moisture > 450) {
    digitalWrite(RELAY_PIN, HIGH);  // Activate relay (active-low)
    Serial.println(" → PUMP ON");
  } else {
    digitalWrite(RELAY_PIN, LOW); // Deactivate relay
    Serial.println(" → PUMP OFF");
  }
  
  delay(1000);
}