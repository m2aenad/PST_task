#include <Adafruit_MotorShield.h>

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
// to motor port #1 (M3 and M4)
Adafruit_StepperMotor *myMotor = AFMS.getStepper(516, 1); 
#define PHOTODETECTOR 27 //define Beambreaker port
int x = 0;  //var for motor state
int incomingByte = 0; // var for incoming data

void setup() {
  Serial.begin(9600);           // set up the serial library at 9600 bps
  while (!Serial);
  Serial.println("Stepper test!");
  if (!AFMS.begin()) {         // set the default frequency 1.6KHz
   if (!AFMS.begin(1000)) {  // OR a different frequency, say 1KHz
    Serial.println("Could not find Motor Shield. Check wiring.");
   while (1);
  // myMotor->setSpeed(5);
  // myMotor->run(RELEASE);
  }
  Serial.println("Motor Shield found.");
 
 // myMotor->setSpeed(5);
}
 pinMode(PHOTODETECTOR, INPUT_PULLUP);  // define beambreaker port mode
}

void loop() {
 //this block is responsible for receiving data from the com port, for now it launches the motor with any data input
 if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();    
    // prints the input:
    Serial.print("Input received: ");
    Serial.println(incomingByte, DEC);
    if (incomingByte == 'T')
    x=1; //change motor state
    if (incomingByte == 'F')
    x=0;
  }

  //to launch the motor 
  if (x == 1) {
     myMotor->step(1, FORWARD, SINGLE);
     // Timeout(3); 
  }


  //to stop the motor when the beam breaks
  if (digitalRead(PHOTODETECTOR) == LOW) { 
     Serial.println("PHOTODETECTOR LOW");       // control message in com port 
     x = 0;              //change motor state
     myMotor->release();
     delay(500);    
    }

     if (x == 0) {
     Serial.println("x=0");       // control message in com port 
     x = 0;              //change motor state
     myMotor->release();
     delay(500);    
    }
    
}
