/********************************************************
  Feed function.  This turns the stepper forward and backwards to dispense a pellet,
  stopping once pellet is dispensed.
********************************************************/
void Feed() {
  while (dispense == true) {
    // Move pellet disk to dispense a pellet
    // Blink (14, 1, 1);
    stepper.step(5);
    delay (5);
    if (digitalRead(PHOTODETECTOR) == LOW) {
      // Blink (LED_BUILTIN, 1, 1);
      dispense = false;
      ReleaseMotor();
    }
  }
}

/********************************************************
   Power off Stepper so it doesn't overheat
********************************************************/
void ReleaseMotor () {
  digitalWrite (10, LOW);
  digitalWrite (6, LOW);
  digitalWrite (9, LOW);
  digitalWrite (5, LOW);
}
