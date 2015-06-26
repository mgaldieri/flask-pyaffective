#include <SPI.h>

#include <RF24.h>
#include <nRF24L01.h>
#include <RF24_config.h>

#define BAUD_RATE 9600

#define CE_PIN   8
#define CSN_PIN 10

RF24 radio(CE_PIN, CSN_PIN);

const uint64_t pipe = 0xE8E8F0F0E1LL;

void setup() {
  Serial.begin(BAUD_RATE);
  while(!Serial){;}

  radio.begin();
  radio.openReadingPipe(1, pipe);
  radio.startListening();
}

void loop() {
  radio.printDetails();
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
  delay(100);
}
