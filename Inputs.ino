// Grace edits

void CheckInputs() {
  if (serial.available() > 0 {
    incomingByte = Serial.read();

    if (incomingByte == 'G'){
    dispense == true;  
    }
    if (incomingByte == 'S'){
    dispense == false;  
      }
  }
  // pixels.show();
  // digitalWrite (LED_BUILTIN, LOW);
  // digitalWrite (14, LOW);

  //If button is pushed
  // if (digitalRead(18) == LOW or digitalRead(19) == LOW) {
  //  for (int i = 0; i < num_pixels; i++) {
  //    pixels.setPixelColor(i, pixels.Color(2, 0, 2));
  //  }
  //  pixels.show();
  //  dispense = true;
 // }

  //If input A2 is triggered           
//  if (digitalRead(16) == LOW) {
//    for (int i = 0; i < num_pixels; i++) {
//      pixels.setPixelColor(i, pixels.Color(2, 2, 2));
//    }
//    pixels.show();
//    dispense = true;
//  }

}
