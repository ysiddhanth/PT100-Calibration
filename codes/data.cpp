#include "Arduino.h"

void setup() { 
	Serial.begin(9600);
}

void loop() { 
	int sensorValue = analogRead(A0);
	double voltage = (5*sensorValue/1023);
	Serial.println(voltage);
	delay(1000);
}
