#include <Arduino.h>
#include <Bounce2.h>

// Define Buttons
#define TRIGGER_PIN 13

// Debounce Object
Bounce trigger = Bounce();

void setup() {
  // Initialize Serial Comms
  Serial.begin(115200);
  Serial.setTimeout(1);

  trigger.attach(TRIGGER_PIN, INPUT);
  trigger.interval(25);
}

void loop() {

  // Update Debounced Button Object
  trigger.update();

  if(trigger.rose()){
    // Send trigger event to the PC
    Serial.println("T");
  }
}