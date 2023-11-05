int val = 0;  // variable to store the value rea
int air_piston_pin = 4;// pin for controlling the air piston
bool flag = false;
int taser_pin = 12;
int x;
bool debug = true; // Debug Flag

void punish_player(int time_){
  digitalWrite(taser_pin, HIGH);
  delay(time_);
  digitalWrite(taser_pin, LOW);
}

void fire_shot(int time_) {
  int reset_factor = 1.2;
  digitalWrite(air_piston_pin, HIGH);
  delay(time_);
  digitalWrite(air_piston_pin, LOW);
  delay(int(time_ * reset_factor));
}