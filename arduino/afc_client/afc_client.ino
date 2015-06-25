#include <SPI.h>

#include <RF24_config.h>
#include <nRF24L01.h>
#include <RF24.h>

#define PIPE_ID  0

#define TRIG_PIN 7
#define ECHO_PIN 6

#define CE_PIN   9
#define CSN_PIN 10

#define MAX_RUN   10
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

int readUltrasonicDistance() {
  int duration, distance;
  
  // emit an ultrasonic pulse
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  // read the duration of the returned pulse w/ a HIGH trigger
  duration = pulseIn(ECHO_PIN, HIGH);
  
  // roughly calculate the distance in cm based on the duration
//  distance = (duration/2) / 29.1;
  
  return duration;
}

FastRunningMedian<int, MAX_RUN, 0> distMedian;
int distVal;

const uint64_t talking_pipes[3]   = {0xf0f0f0f0c2LL, 0xf0f0f0f0b3LL, 0xf0f0f0f0a4ll};
const uint64_t listening_pipes[3] = {0x3a3a3a3ac2LL, 0x3a3a3a3ab3LL, 0x3a3a3a3aa4LL};

RF24 radio(CE_PIN, CSN_PIN);

void setup() {
  // put your setup code here, to run once:
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  
  Serial.begin(9600);
  while(!Serial){;}
  
  radio.begin();
  
  radio.openWritingPipe(talking_pipes[0]);
  radio.openReadingPipe(1, listening_pipes[0]);
  
  radio.startListening();
}

void loop() {
  // put your main code here, to run repeatedly:
  /****
   DISTANCE SENSOR
   ****/
  int dist = (int)readUltrasonicDistance();
  if (dist < 300) { dist = 300; }
  if (dist > 7000) { dist = 7000; }
  distMedian.addValue(dist);
  
  distVal = map(distMedian.getMedian(), 300, 7000, 0, 1023);
  
  /****
   RADIO STUFF
   ****/
  // stop listening and send info
  radio.stopListening();
  radio.write(&distVal, sizeof(int));
  Serial.println(distVal);
  // resume listening
  radio.startListening();
  
  // wait for a response
  unsigned long started_waiting_at = millis();
  bool timeout;
  while(!radio.available() && !timeout) {
    if (millis() - started_waiting_at > RADIO_TIMEOUT) {
      timeout = true;
    }
  }
  
  if (timeout) {
//    Serial.println("Response timeout");
  } else {
    char response;
    radio.read(&response, sizeof(char));
    Serial.println("Server acknowledged");
  }
  
  // rest a little while
  delay(10);
}
