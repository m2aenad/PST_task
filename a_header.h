/********************************************************
  Include these libraries
********************************************************/
#include <Wire.h>
#include <SPI.h>
#include <Stepper.h>
#include <Adafruit_NeoPixel.h>

/********************************************************
  Initialize variables
********************************************************/
bool PelletJam = false;
bool dispense = false;
bool jammed = false;
float greenTimer = millis();

/********************************************************
  Set up the NeoPixel
********************************************************/
// int num_pixels = 12;
// Adafruit_NeoPixel pixels = Adafruit_NeoPixel(num_pixels, 14, NEO_GRB + NEO_KHZ800);

/********************************************************
  Feather pins being used
********************************************************/
#define PHOTODETECTOR 11

/********************************************************
  Setup stepper object
********************************************************/
// Create the stepper object
#define STEPS 2038
Stepper stepper(STEPS, 10, 6, 9, 5);
