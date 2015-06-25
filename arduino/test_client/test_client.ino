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

  radio.begin();
//  radio.openReadingPipe(1, listening_pipes[0]);
//  radio.openWritingPipe(talking_pipes[0]);
  radio.openWritingPipe(talking_pipe);

//  radio.startListening();
  radio.printDetails();
}

void loop() {
  // put your main code here, to run repeatedly:
//  radio.stopListening();
  char data = 'A';
//  data[0] = 1;
//  data[1] = 2;

  radio.powerUp();
  delay(3);
  bool ok = radio.write(&data, sizeof(data));

  if (ok) {
    Serial.println("Ok!");
  } else {
    Serial.println("Failed...");
  }

//  radio.startListening();
}
