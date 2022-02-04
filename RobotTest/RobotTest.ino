/* Sweep
  by BARRAGAN <http://barraganstudio.com>
  This example code is in the public domain.

  modified 8 Nov 2013
  by Scott Fitzgerald
  https://www.arduino.cc/en/Tutorial/LibraryExamples/Sweep
*/

#include <Servo.h>
Servo myservo9;  // create servo object to control a servo
Servo myservo10;
Servo myservo11;
Servo myservo12;
Servo myservo13;
float mg(float ar[3]){
  float mag = 0;
  for (int i = 0; i < 3; i++) {
    mag = mag + ar[i]*ar[i];
  }
  return(sqrt(mag));
}
float servoSmoothed9;
float switchPrevious9;
float servo9;
float servoSmoothed10;
float switchPrevious10;
float servo10;
float servoSmoothed11;
float switchPrevious11;
float servo11;
float servoSmoothed12;
float switchPrevious12;
float servo12;
float servoSmoothed13;
float switchPrevious13;
float servo13;
//Varing:
float robtDm[5] = {5.5,6.25,22.25,22.25,6.25};
float TP[3] = {0,30,30};
float TRA[2] = {90,0};
//Math Start
float O[3] = {0,0,robtDm[4]};
float TRV[3] = {cos(TRA[0])*cos(TRA[1]),sin(TRA[0])*cos(TRA[1]),sin(TRA[1])};
float P1[3] = {TRV[0]*robtDm[0]/mg(TRV)+TP[0],TRV[1]*robtDm[0]/mg(TRV)+TP[1],TRV[2]*robtDm[0]/mg(TRV)+TP[2]};
float OP1[3] = {P1[0]-O[0],P1[1]-O[1],P1[2]-O[2]};
float N[3] = {-TRV[2]*OP1[0]/(OP1[0]*TRV[0]+OP1[1]*TRV[1]),-TRV[2]/(OP1[0]*TRV[0]/OP1[1]+TRV[1]),1};
float Q[3] = {-N[2]*OP1[0]/(OP1[0]*N[0]+OP1[1]*N[1]),-N[2]/(OP1[0]*N[0]/OP1[1]+N[1]),1};
float P2[3] = {Q[0]*robtDm[1]/mg(Q)+P1[0],Q[1]*robtDm[1]/mg(Q)+P1[1],Q[2]*robtDm[1]/mg(Q)+P1[2]};
//Math End
int VRx1 = A0;
int VRy1 = A1;
int VRx2 = A2;
int VRy2 = A3;
int VRx3 = A4;
int VRy3 = A5;s

int xPosition1 = 0;
int yPosition1 = 0;
int xPosition2 = 0;
int yPosition2 = 0;
int xPosition3 = 0;
int yPosition3 = 0;
int mapX1 = 0;
int mapY1 = 0;
int mapX2 = 0;
int mapY2 = 0;
int mapX3 = 0;
int mapY3 = 0;
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

void setup() {
  Serial.begin(9600);
  pinMode(VRx1, INPUT);
  pinMode(VRy1, INPUT);
  pinMode(VRx2, INPUT);
  pinMode(VRy2, INPUT);
  pinMode(VRx3, INPUT);
  pinMode(VRy3, INPUT);
  myservo9.attach(9);
  myservo10.attach(10);
  myservo11.attach(11);
  myservo12.attach(12);
  myservo13.attach(13);
}

void loop() {
  xPosition1 = analogRead(VRx1);
  yPosition1 = analogRead(VRy1);
  xPosition2 = analogRead(VRx2);
  yPosition2 = analogRead(VRy2);
  xPosition3 = analogRead(VRx3);
  yPosition3 = analogRead(VRy3);
  mapX1 = map(xPosition1, 0, 1023, -180, 180);
  mapY1 = map(yPosition1, 0, 1023, -180, 180);
  mapX2 = map(xPosition2, 0, 1023, -180, 180);
  mapY2 = map(yPosition2, 0, 1023, -180, 180);
  mapX3 = map(xPosition3, 0, 1023, -180, 180);
  mapY3 = map(yPosition3, 0, 1023, -180, 180);
  servo9 = (-mapX2 / 2.75 + 95);
  servo10 = (mapY2 / 2.75 + 90);
  servo11 = (mapY1 / 4 + 95);
  servo12 = (-mapY3 / 4 + 100);
  servo13 = (mapX3 / 4 + 90);
//  servoSmoothed9 = (servo9*0.02)+(switchPrevious9*0.98);
//  switchPrevious9 = servoSmoothed9;
//  servoSmoothed10 = (servo10*0.02)+(switchPrevious10*0.98);
//  switchPrevious10 = servoSmoothed10;
//  servoSmoothed11 = (servo11*0.05)+(switchPrevious11*0.99);
//  switchPrevious11 = servoSmoothed11;
//  servoSmoothed12 = (servo12*0.01)+(switchPrevious12*0.99);
//  switchPrevious12 = servoSmoothed12;
//  servoSmoothed13 = (servo13*0.01)+(switchPrevious13*0.99);
//  switchPrevious13 = servoSmoothed13;
//  myservo9.write(servoSmoothed9);
//  myservo10.write(servoSmoothed10);
//  myservo11.write(servoSmoothed11);
//  myservo12.write(servoSmoothed12);
//  myservo13.write(servoSmoothed13);
  myservo9.write(servo9);
  myservo10.write(servo10);
  myservo11.write(servo11);
  myservo12.write(servo12);
  myservo13.write(servo13);
//  delay(5);
//  myservo13.write(90);
  //  for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
  //    // in steps of 1 degree 
  //    myservo.write(pos);              // tell servo to go to position in variable 'pos'
  //    delay(15);                       // waits 15 ms for the servo to reach the position
  //  }
  //  for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
  //    myservo.write(pos);              // tell servo to go to position in variable 'pos'
  //    delay(15);                       // waits 15 ms for the servo to reach the position
  //  }
}
