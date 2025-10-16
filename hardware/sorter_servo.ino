#include <Servo.h>

Servo sorterServo;

int servoPin = 9;  // signal wire to pin 9

void setup() {
  Serial.begin(9600);
  sorterServo.attach(servoPin);
  sorterServo.write(90);  // start centered
  Serial.println("Ready for servo commands!");
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();

    if (command == '1') {
      sorterServo.write(30);     // move left
      Serial.println("Moved to position 1 (Left)");
    }
    else if (command == '2') {
      sorterServo.write(90);    // center
      Serial.println("Moved to position 2 (Center)");
    }
    else if (command == '3') {
      sorterServo.write(150);   // move right
      Serial.println("Moved to position 3 (Right)");
    }

    delay(1000); // pause briefly before accepting next command
  }
}