/********************************************************
  FED++, version 1.04 for dispensing M&Ms
  Written by Lex Kravitz during a pandemic
  Washington University in St Louis
  alexxai@wustl.edu
  May 2020

  This code includes code from:
  *** Adafruit, who made the hardware breakout boards and associated code we used in FED ***

  This project is released under the terms of the Creative Commons - Attribution - ShareAlike 3.0 license:
  human readable: https://creativecommons.org/licenses/by-sa/3.0/
  legal wording: https://creativecommons.org/licenses/by-sa/3.0/legalcode
  Copyright (c) 2020 Lex Kravitz

********************************************************/

/********************************************************
  Setup code
********************************************************/
#include "a_header.h" //See "a_Header.h" for #defines and other constants 

void setup() {
  StartUpCommands();
}

/********************************************************
  Main loop
********************************************************/
void loop() {
  CheckInputs();
  Feed();
  Timeout();
}
