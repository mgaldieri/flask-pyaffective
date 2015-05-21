#include <SPI.h>

#include <RF24_config.h>
#include <nRF24L01.h>
#include <RF24.h>

#define TRIG_PIN 7
#define ECHO_PIN 6

#define CE_PIN   8 // leonardo only, otherwise 9
#define CSN_PIN 10


//const uint64_t talking_pipes[3]   = {0xf0f0f0f0d2LL, 0xf0f0f0f0c3LL, 0xf0f0f0f0b4ll};
//const uint64_t listening_pipes[3] = {0x3a3a3a3ad2LL, 0x3a3a3a3ac3LL, 0x3a3a3a3ab4LL};
const uint64_t talking_pipe   = 0xf0f0f0f0d2LL;
const uint64_t listening_pipe = 0x3a3a3a3ad2LL;

RF24 radio(CE_PIN, CSN_PIN);


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while(!Serial){;}
  
  radio.begin();
  
//  for (uint8_t i=0; i<sizeof(talking_pipes); i++) {
//    radio.openReadingPipe(i+1, talking_pipes[i]);
//  }
  radio.openReadingPipe(1, talking_pipe);
  
  radio.startListening();
}

void loop() {
  // listen on all available pipes
//  for (uint8_t pipe_num=0; pipe_num<sizeof(talking_pipes); pipe_num++) {
    uint8_t i = 1;
    if (radio.available(&i) > 0) {
      unsigned long request = 100;
      bool done = false;
      while(!done) {
        done = radio.read(&request, sizeof(unsigned long));
      }
      
      // debug value
      Serial.println(request);
      
      // send response back
      // first, stop listening so we can talk
      radio.stopListening();
      // open pipe for communicating
      radio.openWritingPipe(listening_pipe);
      // send info
      char response = 'A';
      radio.write(&response, sizeof(char));
      // resume listening
      radio.startListening();
    }
//  }
  
  delay(10);
}
