#include <Arduino.h>
#include <Bounce2.h>
#include"functions.h"

// Define Pins
#define TRIGGER_PIN 13
#define AIR_PISTON_PIN 4
#define TASER_PIN 12

// Debounce Object
Bounce trigger = Bounce();

// Zap Timer
unsigned long zap = millis();
bool notZapped = true;

void setup() {
  // Initialize Serial Comms
  Serial.begin(115200);
  Serial.setTimeout(1);

  // Setup Trigger Pin
  trigger.attach(TRIGGER_PIN, INPUT);
  trigger.interval(25);

  // Setup Air Piston Pin
  pinMode(AIR_PISTON_PIN, OUTPUT);

  // Setup Taser Pin
  pinMode(TASER_PIN, OUTPUT);
}

void loop() {

  // Update Debounced Button Object
  trigger.update();

  // Check for Trigger Press
  if(trigger.rose()){
    // Send trigger event to the PC
    Serial.println(1);

    // Shoot -- Temporary, Remove When Connected to Computer and Comms Work
    fire_shot(70);  
  }

  // Hardcoded zap
  if(((millis() - zap) > 10000) && notZapped){
    notZapped = false;
    punish_player(4);
  }

  // Get Trigger Data
  //while (!Serial.available()); // Breaks everything, never leaves loop
  x = Serial.readString().toInt();
  if (x == 3) { // shot denied, do nothing  `!qqqq  `!Q@Q!! ``````````````````1Q2
    if (debug == true) { 
      //Serial.flush();
      Serial.print(x);
    }
  }
  else if (x == 556) { // shot confirmed fire! (AR recoil)
    fire_shot(70);  
    if (debug == true) {
      Serial.print(x);
    }
  }
  else if (x == 308) { // shot confirmed fire! (308 recoil)
    fire_shot(70);  
    if (debug == true) {
      Serial.print(x);
    }
  }
  else if (x == 9) { // shot confirmed fire! (9mm SMG recoil)
    fire_shot(25);  
    if (debug == true) {
      Serial.print(x);
    }
  }
  else if (x == 22) { // shot confirmed fire! (Pistol recoil)
    fire_shot(15); // cant feel much with pistols
    if (debug == true) {
      Serial.print(x);
    }
  }
  else if (x == 44) { // if dead tazer time
    punish_player(5);  // taze the bastard
    if (debug == true) {
      Serial.print(x);
    }
  }
  Serial.flush();
}