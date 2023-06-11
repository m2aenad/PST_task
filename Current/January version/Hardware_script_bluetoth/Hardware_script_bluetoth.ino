#include <Adafruit_MotorShield.h>
#include <bluefruit.h>
#include <Adafruit_LittleFS.h>
#include <InternalFileSystem.h>

// BLE Service
BLEDfu  bledfu;  // OTA DFU service
BLEDis  bledis;  // device information
BLEUart bleuart; // uart over ble
BLEBas  blebas;  // battery

//Motorshields var
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); // Create the motor shield object with the default I2C address
Adafruit_StepperMotor *myMotor = AFMS.getStepper(516, 1); // to motor port #1 (M3 and M4)

//utility var
#define PHOTODETECTOR 27 //define Beambreaker port
int x = 0;  //var for motor state
int incomingByte = 0; // var for incoming data
int Beam_count = 0; //delay time from beambreakers

void setup() {
  Serial.begin(9600);           // set up the serial library at 9600 bps
  while (!Serial);
  Serial.println("Stepper test!");
    if (!AFMS.begin()) {         // set the default frequency 1.6KHz
        if (!AFMS.begin(1000)) {  // OR a different frequency, say 1KHz
            Serial.println("Could not find Motor Shield. Check wiring.");
            while (1);
        }
      Serial.println("Motor Shield found."); 
    }
    
  pinMode(PHOTODETECTOR, INPUT_PULLUP);  // define beambreaker port mode

  Serial.println("Bluetooth BLEUART initialization");
  Serial.println("---------------------------\n");
  Bluefruit.autoConnLed(true);  // Setup the BLE LED to be enabled on CONNECT
  Bluefruit.configPrphBandwidth(BANDWIDTH_MAX); // Config the peripheral connection with maximum bandwidth 
  Bluefruit.begin();
  Bluefruit.setTxPower(4);   
  Bluefruit.Periph.setConnectCallback(connect_callback);
  Bluefruit.Periph.setDisconnectCallback(disconnect_callback);
  bledfu.begin();     // To be consistent OTA DFU should be added first if it exists
  bledis.setManufacturer("Adafruit Industries");     // Configure and Start Device Information Service
  bledis.setModel("CANDY MACHINE (Bluefruit Feather52)");
  bledis.begin();
  bleuart.begin();     // Configure and Start BLE Uart Service
  blebas.begin();   // Start BLE Battery Service
  blebas.write(100);
  startAdv();   // Set up and start advertising
}

void startAdv(void)
{
  // Advertising packet
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();

  // Include bleuart 128-bit uuid
  Bluefruit.Advertising.addService(bleuart);

  // Secondary Scan Response packet (optional)
  // Since there is no room for 'Name' in Advertising packet
  Bluefruit.ScanResponse.addName();
  
  /* Start Advertising
   * - Enable auto advertising if disconnected
   * - Interval:  fast mode = 20 ms, slow mode = 152.5 ms
   * - Timeout for fast mode is 30 seconds
   * - Start(timeout) with timeout = 0 will advertise forever (until connected)
   * 
   * For recommended advertising interval
   * https://developer.apple.com/library/content/qa/qa1931/_index.html   
   */
  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(32, 244);    // in unit of 0.625 ms
  Bluefruit.Advertising.setFastTimeout(30);      // number of seconds in fast mode
  Bluefruit.Advertising.start(0);                // 0 = Don't stop advertising after n seconds  
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
  
  Beam_count = Beam_count + 1; //this line counts the beamcount
  //the part below launches when someone connects to the feather bluetooth
  while ( bleuart.available() )
  {
    uint8_t ch; //a variable to store the data received from python
    ch = (uint8_t) bleuart.read(); //read this data and store it in this variable
    Serial.println(ch); //print this data to the serial monitor
    x=1; //x=1 is the condition which is, when satisfied, launches the motor 
    Beam_count = 0; //restart the beamcount
  }

  //to launch the motor 
  if (x == 1) {
     myMotor->step(1, FORWARD, SINGLE);
  }
 

  //to stop the motor when the beam breaks
  if (digitalRead(PHOTODETECTOR) == LOW) { 
     Serial.println("PHOTODETECTOR LOW");       // control message in com port 
     x = 0;              //change motor state
     myMotor->release();
     char cstr[16]; //creating a var to send bytearray to python //no idea what's 16 
     itoa(Beam_count, cstr, 10); //a function to convert beamcount into bytearray 
     bleuart.write(cstr); //sends the bytearray variable to bluetooth
     Serial.println(String(Beam_count)); //prints bytearray in serial monitor
     Serial.println(cstr); //to check if the cnvertation is right 
     //to match the content in beamcount and cstr variables
     delay(500);
    }

     if (x == 0) {
   //  Serial.println("x=0");       // control message in com port 
   //  x = 0;              //change motor state
     myMotor->release();
     delay(1) //to convert beamcount (from arduino cycles to ms (millliseconds))  
    }
} 

// callback invoked when central connects
void connect_callback(uint16_t conn_handle)
{
  // Get the reference to current connection
  BLEConnection* connection = Bluefruit.Connection(conn_handle);

  char central_name[32] = { 0 };
  connection->getPeerName(central_name, sizeof(central_name));

  Serial.print("Connected to ");
  Serial.println(central_name);
}

/**
 * Callback invoked when a connection is dropped
 * @param conn_handle connection where this event happens
 * @param reason is a BLE_HCI_STATUS_CODE which can be found in ble_hci.h
 */
void disconnect_callback(uint16_t conn_handle, uint8_t reason)
{
  (void) conn_handle;
  (void) reason;

  Serial.println();
  Serial.print("Disconnected, reason = 0x"); Serial.println(reason, HEX);
}
