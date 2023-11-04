#include <Arduino.h>
#include <Bounce2.h>

// Define Buttons
#define TRIGGER_PIN 18

// Debounce Object
Bounce trigger = Bounce();

// // Pin Status
// bool trigger = false;

// // Debounce Timer
// unsigned long debounceTimer = 0;

// // Debounce Delay Time
// unsigned int delayTime = 150;

// // GPIO Interrupt Function
// // Sends trigger pull signal to the PC
// void IRAM_ATTR ISR() {
//   if(millis() - debounceTimer > delayTime){
//     debounceTimer = millis();
//     trigger = true;
//   }
// }


void setup() {
  // Initialize Serial Comms
  Serial.begin(115200);
  Serial.setTimeout(1);

  // Setup Trigger Interrupt
  // pinMode(18, INPUT_PULLDOWN);
  // attachInterrupt(18, ISR, RISING);

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

  // if(trigger){
  //   // Send trigger event to the PC
  //   Serial.print("Trigger");

  //   // Reset Trigger
  //   trigger = false;
  // }
}

// Computer Vision Detected a Bullet Firing, Fire the Bullet
void fire(){
  Serial.print("Firing");
}