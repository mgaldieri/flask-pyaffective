#include <SPI.h>

#include <RF24.h>
#include <nRF24L01.h>
#include <RF24_config.h>

#define BAUD_RATE 9600

#define CE_PIN   9
#define CSN_PIN 10

RF24 radio(CE_PIN, CSN_PIN);

const uint64_t pipe = 0xE8E8F0F0E1LL;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(BAUD_RATE);

  radio.begin();
  radio.openWritingPipe(pipe);
  radio.printDetails();
}

void loop() {
  radio.powerUp();
  radio.printDetails();
  char data = 'A';

  bool ok = radio.write(&data, sizeof(data));

  if (ok) {
    Serial.println("Ok!");
  } else {
    Serial.println("Failed...");
  }
  delay(100);
}
