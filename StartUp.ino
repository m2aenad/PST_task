/********************************************************
  Start Up Commands
********************************************************/
void StartUpCommands () {
  Serial.begin(115200);

  /********************************************************
    Setting digital pin modes
  ********************************************************/
  pinMode(14, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(15, INPUT_PULLUP); //A1
  pinMode(16, INPUT_PULLUP); //A2
  pinMode(17, INPUT_PULLUP); //A3
  pinMode(18, INPUT_PULLUP); //Button B
  pinMode(19, INPUT_PULLUP); //Button A
  pinMode(PHOTODETECTOR, INPUT_PULLUP);

  /********************************************************
    Start Neopixel
  ********************************************************/
  // pixels.begin();

  /********************************************************
    Set up stepper
  ********************************************************/
  stepper.setSpeed(12);  //rpm
}
