#include <SPI.h>

#include <RF24_config.h>
#include <nRF24L01.h>
#include <RF24.h>

#define DEBUG true

#define BAUD_RATE 9600

// radio defines
#define CE_PIN   9
#define CSN_PIN 10

typedef enum { AUDIO=0, CAP, ACCEL } sensors_e;

/*****
 RADIO STUFF
 *****/
// define communication pipes
const uint64_t talking_pipes[3]   = { 0xF0F0F0F0D2LL, 0xF0F0F0F0C3LL, 0xF0F0F0F0B4LL };//, 0xF0F0F0F0A5LL, 0xF0F0F0F096LL };
const uint64_t listening_pipes[3] = { 0x3A3A3A3AD2LL, 0x3A3A3A3AC3LL, 0x3A3A3A3AB4LL };//, 0x3A3A3A3AA5LL, 0x3A3A3A3A96LL };

// init radio
RF24 radio(CE_PIN, CSN_PIN);

/*****
 CONSTANTS
 *****/
//sensors_e SENSORS;

/*****
 VARS
 *****/
int audioVal;
int capVal;
int accelVal;

byte bytesToRead[2];
byte bytesToWrite[sizeof(talking_pipes)];
byte rgb[3] = {0, 0, 255};

/*****
 HELPER FUNCTIONS
 *****/
// pack int value to byte array
void packValue(byte pack[], int value)
{
  pack[0] = (byte)value;
  pack[1] = (byte)(value >> 8);
}

// unpack byte array to int value
int unpackValue(byte pack[2])
{
  int value;
  value = 0xff & pack[1];
  value = (value << 8) | pack[0];
  return value;
}

/*****
 SETUP
 *****/
void setup() {
  Serial.begin(BAUD_RATE);
  while(!Serial){;}
  
  radio.begin();
  
  for (uint8_t i=0; i<sizeof(talking_pipes); i++) {
    radio.openReadingPipe(i+1, talking_pipes[i]);
  }
  
  radio.startListening();
}

/*****
 LOOP
 *****/
void loop() {
  /*****
   RADIO STUFF
   *****/
  // listen on all available pipes
  uint8_t pipe_num;
  if (radio.available(&pipe_num)) {
    Serial.println("Data available");
    // read data from pipe
    bool done = false;
    while(!done) {
      done = radio.read(&bytesToRead, sizeof(bytesToRead));
    }
    
    // unpack data
    sensors_e currSensor = static_cast<sensors_e>(pipe_num);
    switch(currSensor) {
      case AUDIO:
        audioVal = unpackValue(bytesToRead);
        break;
      case CAP:
        capVal = unpackValue(bytesToRead);
        break;
      case ACCEL:
        accelVal = unpackValue(bytesToRead);
        break;
      default:
        break;
    }
#ifdef DEBUG
    /*****
     DEBUG POINT
     *****/
    Serial.print("Pipe num: ");
    Serial.print(pipe_num);
    Serial.print(" - Lower: ");
    Serial.print(bytesToRead[0]);
    Serial.print(" - Upper: ");
    Serial.println(bytesToRead[1]);
#endif
  } else {
    Serial.println("No data available...");
  }
  
  /*****
   SERIAL STUFF
   *****/
  // map sensor data to byte size
  audioVal = map(audioVal, 0, 1023, 0, 255);
  capVal = map(capVal, 0, 1023, 0, 255);
  accelVal = map(accelVal, 0, 1023, 0, 255);
  
#ifdef DEBUG
  /*****
   DEBUG POINT
   *****/
//  Serial.print("Audio value: ");
//  Serial.print(audioVal);
//  Serial.print(" - Capacitance value: ");
//  Serial.print(capVal);
//  Serial.print(" - Accelerometer value: ");
//  Serial.println(accelVal);
#endif

  // pack data for sending
  bytesToWrite[0] = audioVal;
  bytesToWrite[1] = capVal;
  bytesToWrite[2] = accelVal;

#ifndef DEBUG
  // send values to server
//  Serial.write(bytesToWrite, sizeof(bytesToWrite));
#endif

  radio.stopListening();
  for(uint8_t pipe_num=0; pipe_num<sizeof(listening_pipes); pipe_num++) {
    radio.openWritingPipe(listening_pipes[pipe_num]);
    radio.write(&rgb, sizeof(rgb));
  }
  radio.startListening();
  
//  // first, stop listening so we can talk
//  radio.stopListening();
//  // open pipe for communicating
//  radio.openWritingPipe(listening_pipe);
//  // send rgb data
//  radio.write(&rgb, sizeof(rgb));
//  // resume listening
//  radio.startListening();
   
  // take a nap...
  delay(10);
}
