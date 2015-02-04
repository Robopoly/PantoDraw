// Sweep
// by BARRAGAN <http://barraganstudio.com> 
// This example code is in the public domain.


#include <Servo.h> 
#define MOTOR1_PIN 5
#define MOTOR2_PIN 6
#define TABLE_PIN 10
#define M1M2_OFFSET 67
#define BAUDRATE 9600
Servo M1;  // create servo object to control a servo 
Servo M2;                // a maximum of eight servo objects can be created 
Servo T;
int pos1 = 0;    // variable to store the servo position 
int pos2 = 0; 
int tablePos = 0;
void setup() 
{ 
  Serial.begin(BAUDRATE);
  M1.attach(MOTOR1_PIN);  // attaches the servo on pin 5 to the servo object 
  M2.attach(MOTOR2_PIN);
  T.attach(TABLE_PIN);  // attaches the servo on pin 5 to the servo object
} 
 
 
void loop() 
{ 
  if (Serial.available() > 0)
  {
    byte inByte = Serial.read();
    if(inByte == 'P')
    {
      pos1 = Serial.read() - M1M2_OFFSET;
      pos2 = Serial.read() - M1M2_OFFSET;
      tablePos = Serial.read();
      pos2 = 180-pos2;
      //echo
      Serial.write('P');
      Serial.write(pos1);
      Serial.write(180-pos2);
      Serial.write(tablePos);
      
      M1.write(pos1);
      M2.write(pos2);
      T.write(tablePos);
    }
  }
} 
