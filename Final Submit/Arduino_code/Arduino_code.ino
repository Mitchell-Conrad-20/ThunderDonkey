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

bool trigger_hold_flag = true;
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

unsigned long buttonPressStartTime = 0;
bool flag_auto = false;
bool fullAuto = false;
int shot_counter = 0;
void loop() {
trigger.update();

  if (trigger.rose()) {
    fire_shot(56);
    shot_counter++;
    buttonPressStartTime = 0;
    //delay(20);
  } else if (trigger.read() == HIGH) {
    if (buttonPressStartTime == 0) {
      buttonPressStartTime = millis();
    }
    
    if (millis() - buttonPressStartTime >= 400) {
      fullAuto = true;
    }
  } else if (trigger.fell()) {
    buttonPressStartTime = 0;
    fullAuto = false;
    // Optionally, you can add code here to stop full-auto firing
  }

  if (fullAuto) {
    shot_counter++;
    fire_shot(38);
    //delay(20); // Adjust this delay as needed for full-auto mode
  }
  // tazer
//  if(shot_counter == 2){
//    shot_counter++;
//    Serial.println("taser time!");
//     digitalWrite(taser_pin, HIGH);
//    delay(5);
//    digitalWrite(taser_pin, LOW);
//    Serial.println("DONE!");
//  }




}
