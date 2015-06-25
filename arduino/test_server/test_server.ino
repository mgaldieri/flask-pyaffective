#include <SPI.h>

#include <RF24.h>
#include <nRF24L01.h>
#include <RF24_config.h>

#define BAUD_RATE 9600

#define CE_PIN   9
#define CSN_PIN 10

RF24 radio(CE_PIN, CSN_PIN);

const uint64_t talking_pipes[3]   = { 0xF0F0F0F0D2LL, 0xF0F0F0F0C3LL, 0xF0F0F0F0B4LL };//, 0xF0F0F0F0A5LL, 0xF0F0F0F096LL };
const uint64_t listening_pipes[3] = { 0x3A3A3A3AD2LL, 0x3A3A3A3AC3LL, 0x3A3A3A3AB4LL };//, 0x3A3A3A3AA5LL, 0x3A3A3A3A96LL };

const uint64_t talking_pipe = 0xF0F0F0F0D2LL;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(BAUD_RATE);
  while(!Serial){;}

  radio.begin();

//  radio.openReadingPipe(1, talking_pipes[0]);
//  radio.openWritingPipe(listening_pipes[0]);
  radio.openReadingPipe(1, talking_pipe);

  radio.startListening();
  radio.printDetails();
}

void loop() {
  // put your main code here, to run repeatedly:
  uint8_t pipe_num;
  if (radio.available()) {
    Serial.println("Data available");
    bool ok;
    char buf;
    ok = radio.read(&buf, sizeof(buf));
    if (ok) {
      Serial.println("Data succesfully read");
    } else {
      Serial.println("Read failed...");
    }
  } else {
    Serial.println("No data available...");
  }
}
