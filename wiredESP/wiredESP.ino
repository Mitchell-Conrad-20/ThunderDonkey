#include <Arduino.h>

// Pin Status
int lastValue = LOW;
bool triggerSend = false;
bool triggerReleased = false;

// Debounce Timer
unsigned long debounceTimer = 0;

// Debounce Delay Time
unsigned int delayTime = 20;

// GPIO Interrupt Function
// Sends trigger pull signal to the PC
void IRAM_ATTR ISR() {
  if(millis() - debounceTimer > delayTime){
    debounceTimer = millis();

    if (digitalRead(18) == HIGH && lastValue == LOW){
      triggerSend = true;
      lastValue = HIGH;      
    }
    else if (digitalRead(18) == LOW && lastValue == HIGH){
      triggerReleased = true;
      lastValue = LOW;
    }
  }
}


void setup() {
  // Initialize Serial Comms
  Serial.begin(115200);
  Serial.setTimeout(1);

  // Setup Trigger Interrupt
  pinMode(18, INPUT_PULLDOWN);
  attachInterrupt(18, ISR, CHANGE);
}

void loop() {
  // Computer Vision Detected a Bullet Fired 
  //while (!Serial.available());
  if (Serial.readString() == "Detected"){
    fire();
  }

  if(triggerSend){
    // Send trigger event to the PC
    Serial.print("Trigger");

    // Reset Trigger
    triggerSend = false;
  }

  else if(triggerReleased){
    // Send trigger event to the PC
    Serial.print("Trigger Released");

    // Reset Trigger
    triggerReleased = false;
  }
}

// Computer Vision Detected a Bullet Firing, Fire the Bullet
void fire(){
  Serial.print("Firing");
}