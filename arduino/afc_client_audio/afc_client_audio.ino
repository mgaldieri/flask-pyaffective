#include <SPI.h>

#include <RF24_config.h>
#include <nRF24L01.h>
#include <RF24.h>

#define DEBUG true

#define PIPE_ID 0
#define BAUD_RATE 9600

#define R_PIN 3
#define G_PIN 5
#define B_PIN 6

// radio defines
#define CE_PIN   9
#define CSN_PIN 10

// audio defines
#define AUDIO_PIN A0

#define MAX_RUN        10
#define RADIO_TIMEOUT 250 // milliseconds

template <typename T, uint8_t N, T default_value> class FastRunningMedian {

public:
	FastRunningMedian() {
		_buffer_ptr = N;
		_window_size = N;
		_median_ptr = N/2;

		// Init buffers
		uint8_t i = _window_size;
		while( i > 0 ) {
			i--;
			_inbuffer[i] = default_value;
			_sortbuffer[i] = default_value;
		}
	};

	T getMedian() {
		// buffers are always sorted.
		return _sortbuffer[_median_ptr];
	}

	
	void addValue(T new_value) {
		// comparision with 0 is fast, so we decrement _buffer_ptr
		if (_buffer_ptr == 0)
			_buffer_ptr = _window_size;
		
		_buffer_ptr--;
		
		T old_value = _inbuffer[_buffer_ptr]; // retrieve the old value to be replaced
		if (new_value == old_value) 		  // if the value is unchanged, do nothing
			return;
		
		_inbuffer[_buffer_ptr] = new_value;  // fill the new value in the cyclic buffer
			
		// search the old_value in the sorted buffer
		uint8_t i = _window_size;
		while(i > 0) {
			i--;
			if (old_value == _sortbuffer[i])
				break;
		}
		
		// i is the index of the old_value in the sorted buffer
		_sortbuffer[i] = new_value; // replace the value 

		// the sortbuffer is always sorted, except the [i]-element..
		if (new_value > old_value) {
			//  if the new value is bigger than the old one, make a bubble sort upwards
			for(uint8_t p=i, q=i+1; q < _window_size; p++, q++) {
				// bubble sort step
				if (_sortbuffer[p] > _sortbuffer[q]) {
					T tmp = _sortbuffer[p];
					_sortbuffer[p] = _sortbuffer[q];
					_sortbuffer[q] = tmp;
				} else {
					// done ! - found the right place
					return;
				}
			}
		} else {
			// else new_value is smaller than the old one, bubble downwards
			for(int p=i-1, q=i; q > 0; p--, q--) {
				if (_sortbuffer[p] > _sortbuffer[q]) {
					T tmp = _sortbuffer[p];
					_sortbuffer[p] = _sortbuffer[q];
					_sortbuffer[q] = tmp;
				} else {
					// done !
					return;
				}
			}
		}
	}
	
private:
	// Pointer to the last added element in _inbuffer
	uint8_t _buffer_ptr;
	// sliding window size
	uint8_t _window_size;
	// position of the median value in _sortbuffer
	uint8_t _median_ptr;

	// cyclic buffer for incoming values
	T _inbuffer[N];
	// sorted buffer
	T _sortbuffer[N];
};

/*****
 CONSTANTS
 *****/

/*****
 VARS
 *****/
FastRunningMedian<int, MAX_RUN, 0> audioMedian;
int audioVal;

byte bytesToWrite[2];
byte rgb[3] = {0, 0, 0};
char ackResponse;    
boolean acknowledged = false;

/*****
 RADIO STUFF
 *****/
// define communication pipes
const uint64_t talking_pipes[3]   = { 0xF0F0F0F0D2LL, 0xF0F0F0F0C3LL, 0xF0F0F0F0B4LL };//, 0xF0F0F0F0A5LL, 0xF0F0F0F096LL };
const uint64_t listening_pipes[3] = { 0x3A3A3A3AD2LL, 0x3A3A3A3AC3LL, 0x3A3A3A3AB4LL };//, 0x3A3A3A3AA5LL, 0x3A3A3A3A96LL };

// init radio
RF24 radio(CE_PIN, CSN_PIN);

/*****
 HELPER FUNCTIONS
 *****/
// pack int value to byte array
void packValue(byte pack[], int value)
{
  pack[0] = (byte)value;
  pack[1] = (byte)(value >> 8);
}

// set rgb led colors
void setRGB()
{
  analogWrite(R_PIN, rgb[0]);
  analogWrite(G_PIN, rgb[1]);
  analogWrite(B_PIN, rgb[2]);
}

/*****
 SETUP
 *****/
void setup() {
  // set rgb pin modes
  pinMode(R_PIN, OUTPUT);
  pinMode(G_PIN, OUTPUT);
  pinMode(B_PIN, OUTPUT);
  
#ifdef DEBUG
  // for debugging purposes only
  Serial.begin(BAUD_RATE);
  while(!Serial){;}
#endif

  // start radio communication
  radio.begin();
  
  // open writing and reading pipes
  radio.openWritingPipe(talking_pipes[PIPE_ID]);
  radio.openReadingPipe(PIPE_ID+1, listening_pipes[PIPE_ID]);
  
  // start listening for incoming data on the radio
  radio.startListening();
}

/*****
 LOOP
 *****/
void loop() {
  /*****
   SENSOR STUFF
   *****/
  // read sensor data
  //accelMedian.addValue(accel.getTotalVector());
  // put the value in a global, just in case...
  audioVal = analogRead(AUDIO_PIN);
  
  // pack data into byte array
  packValue(bytesToWrite, audioVal);
  
  /****
   RADIO STUFF
   ****/
  // stop listening and send info
  radio.stopListening();
  Serial.println("Now sending...");
  bool ok = radio.write(&bytesToWrite, sizeof(bytesToWrite));
  if (ok) {
    Serial.println("Data sent.");
  } else {
    Serial.println("Failed sending data...");
  }
  // resume listening
  radio.startListening();

#ifdef DEBUG
  /*****
   DEBUG POINT
   *****/
  Serial.print("Audio level: ");
  Serial.print(audioVal);
  Serial.print(" - Lower: ");
  Serial.print(bytesToWrite[0]);
  Serial.print(" - Upper: ");
  Serial.println(bytesToWrite[1]);
#endif
  
//  // wait for a response
//  unsigned long started_waiting_at = millis();
//  bool timeout;
//  while(!radio.available() && !timeout) {
//    if (millis() - started_waiting_at > RADIO_TIMEOUT) {
//      timeout = true;
//    }
//  }
//  
//  if (timeout) {
//#ifdef DEBUG
//    /*****
//     DEBUG POINT
//     *****/
//    Serial.println("Response timed out");
//#endif
//  } else {
//    char response;
//    radio.read(&response, sizeof(char));
//#ifdef DEBUG
//    /*****
//     DEBUG POINT
//     *****/
//    Serial.println("Server acknowledged");
//  }
  
  // listen for incoming rgb data
  if (radio.available()) {
    // read data int rgb array
    radio.read(&rgb, sizeof(rgb));
  }
  
  // keep the lights on
  setRGB();
  
  // take a nap...
  delay(10);
}
