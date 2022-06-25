// Flowshutter
// Copyright (C) 2021  Hugo Chiang

// Flowshutter is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published
// by the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// Flowshutter is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.

// You should have received a copy of the GNU Affero General Public License
// along with flowshutter.  If not, see <https://www.gnu.org/licenses/>.
const int LANCPin = 11;
const int CMDPin = 7;
const int buttonPin = 2;
const int ledPin =  13;

byte ADDRESS = B00011000;   // byte 0 
byte REC = B00110011;       // byte 1

int buttonState = 0;
int record = 0;
int blocktime = 1500;       // block 1500ms
bool recording = 0;
bool block = 0;
unsigned long blockstart = millis();
unsigned long now;

int writeInterval = 8; // it taks 8us to write to the digital port

int bitDuration = 96; /// 104 - 8
void sendCMD(unsigned char cmd1, unsigned char cmd2) 
{
    for (int cmdRepeatCount = 0; cmdRepeatCount < 5; cmdRepeatCount++) {
        //repeat 5 times

        // byte 0
        while (pulseIn(LANCPin, HIGH) < 5000) {
            // block reading after 5ms of last byte 1
        }
        delayMicroseconds(bitDuration);
        // bitbang byte 0
        for( int i=0; i<8; i++){
            digitalWrite(CMDPin, (cmd1 & (1<<i) ) ? HIGH : LOW);
            delayMicroseconds(bitDuration);
        }
        digitalWrite(CMDPin, LOW);
        delayMicroseconds(10);

        // byte 1
        while (digitalRead(LANCPin)) {
        }
        delayMicroseconds(bitDuration);  //wait START bit duration
        // bitbang byte 1
        for( int i=0; i<8; i++){
            digitalWrite(CMDPin, (cmd2 & (1<<i) ) ? HIGH : LOW);
            delayMicroseconds(bitDuration);
        }
        digitalWrite(CMDPin, LOW);
    }
}

void setup() {
    Serial.begin(9600, SERIAL_8E2);
    Serial.print("LANC controller initialized");
    pinMode(ledPin, OUTPUT);
    pinMode(buttonPin, INPUT);
    delay(3000);
}

void loop() {
    // read the state of the button value:
    buttonState = digitalRead(buttonPin);

    if (buttonState == 0){

        if ((record == 0) and (!block) and (!recording)) {
            Serial.print("START");
            record=1;
            block=1;
            recording=1;
            blockstart=millis();
            digitalWrite(ledPin, HIGH); 
            sendCMD(ADDRESS, REC); // REC 
        }

        if ((record == 1) and (!block) and (recording)) {
            Serial.print("STOP");
            record=0;
            block=1;
            recording = 0;
            blockstart=millis();
            digitalWrite(ledPin, LOW); 
            sendCMD(ADDRESS, REC); // REC
        }

        now=millis();
        if (now-blockstart>blocktime){
            block=0;
        }
    }
} 
