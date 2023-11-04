#include <Arduino.h>
#include <Bounce2.h>

// Define Buttons
#define TRIGGER_PIN 18

// Debounce Object
Bounce trigger = Bounce();

void setup() {
  // Initialize Serial Comms
  Serial.begin(115200);
  Serial.setTimeout(1);

  trigger.attach(TRIGGER_PIN, INPUT_PULLUP);
  trigger.interval(25);
}

void loop() {
  // Computer Vision Detected a Bullet Fired 
  //while (!Serial.available());
  if (Serial.readString() == "Detected"){
    fire();
  }

  // Update Debounced Button Object
  trigger.update();

  if(trigger.fell()){
    // Send trigger event to the PC
    Serial.print("Trigger");
  }
}

// Computer Vision Detected a Bullet Firing, Fire the Bullet
void fire(){
  Serial.print("Firing");
}