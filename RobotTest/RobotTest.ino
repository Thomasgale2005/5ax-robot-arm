/* Sweep
  by BARRAGAN <http://barraganstudio.com>
  This example code is in the public domain.

  modified 8 Nov 20b b13
  by Scott Fitzgerald
  https://www.arduino.cc/en/Tutorial/LibraryExamples/Sweep
*/

#include <Servo.h>
Servo myservo9;  // create servo object to control a servo
Servo myservo10;
Servo myservo11;
Servo myservo12;
Servo myservo13;
extern Servo myservo9;
extern Servo myservo10;
extern Servo myservo11;
extern Servo myservo12;
extern Servo myservo13;
float mg(float ar[3]) {
  float mag = 0;
  for (int i = 0; i < 3; i++) {
    mag = mag + ar[i] * ar[i];
  }
  return (sqrt(mag));
}
//(a[0]*b[0]+a[1]*b[1]+a[2]*b[2])/(sqrt(a[0]*a[0]+a[1]*a[1]+a[2]*a[2])*sqrt(b[0]*b[0]+b[1]*b[1]+b[2]*b[2]))
float qd(float a, float b, float c, int d) {
  float out = {(-b + d * sqrt(b * b - 4 * a * c)) / (2 * a)};
  return (out);
}
void moveBot(float L[5], float TP[3], float TRA[2]) {
  float O[3] = {0, 0, L[4]};
  float TRV[3] = {cos(TRA[0]*PI / 180)*cos(TRA[1]*PI / 180), sin(TRA[0]*PI / 180)*cos(TRA[1]*PI / 180), sin(TRA[1]*PI / 180)};
  float P1[3] = {TRV[0]*L[0] / mg(TRV) + TP[0], TRV[1]*L[0] / mg(TRV) + TP[1], TRV[2]*L[0] / mg(TRV) + TP[2]};
  float OP1[3] = {P1[0], P1[1], P1[2] - O[2]};
  float N[3] = { -TRV[2]*P1[0] / (P1[0]*TRV[0] + P1[1]*TRV[1]), -TRV[2] / (P1[0]*TRV[0] / P1[1] + TRV[1]), 1};
  float Q[3] = { -N[2]*OP1[0] / (OP1[0]*N[0] + OP1[1]*N[1]), -N[2] / (OP1[0]*N[0] / OP1[1] + N[1]), 1};
  float P2[3] = {Q[0]*L[1] / mg(Q) + P1[0], Q[1]*L[1] / mg(Q) + P1[1], Q[2]*L[1] / mg(Q) + P1[2]};
  float P3[3] = {0, 0, 0};
  float P4[3] = {0, 0, L[4]};
  int options[8] = {1, 1, 1, -1, -1, -1, -1, 1};
  for (int i = 0; i < 4; i++) {
    float P3Z = qd((2 * P2[2] - 2 * L[4]) * (2 * P2[2] - 2 * L[4]) + 4 * (P2[0] * P2[0] + P2[1] * P2[1]),
                   4 * (L[4] - P2[2]) * (-L[2] * L[2] + L[3] * L[3] - L[4] * L[4] + mg(P2) * mg(P2)) - 8 * L[4] * (P2[0] * P2[0] + P2[1] * P2[1]),
                   (-L[2] * L[2] + L[3] * L[3] - L[4] * L[4] + mg(P2) * mg(P2)) * (-L[2] * L[2] + L[3] * L[3] - L[4] * L[4] + mg(P2) * mg(P2)) - 4 * (P2[0] * P2[0] + P2[1] * P2[1]) * (L[3] * L[3] - L[4] * L[4]), options[2 * i]);
    float P3Y = options[2 * i + 1] * sqrt((L[3] * L[3] - (P3Z - L[4]) * (P3Z - L[4])) / (((P2[0] * P2[0]) / (P2[1] * P2[1])) + 1));
    float P3X = P3Y * P2[0] / P2[1];
    float tempP3P2[3] = {P3X - P2[0], P3Y - P2[1], P3Z - P2[2]};
    if ((round(mg(tempP3P2) * 10000) == L[2] * 10000) and (round(mg(tempP3P2) * 10000) == L[3] * 10000)) {
      if (P3X >= 0) {
        if (P2[2] <= (P2[0]*P3Z / P3X + P4[2])) {
          P3[0] = P3X;
          P3[1] = P3Y;
          P3[2] = P3Z;
        }
      } else {
        if (P2[2] >= (P2[0]*P3Z / P3X + P4[2])) {
          P3[0] = P3X;
          P3[1] = P3Y;
          P3[2] = P3Z;
        }
      }
    }
  }
  float P1TP[3] = {TP[0] - P1[0], TP[1] - P1[1], TP[2] - P1[2]};
  float TPP1[3] = {P1[0] - TP[0], P1[1] - TP[1], P1[2] - TP[2]};
  float P1P2[3] = {P2[0] - P1[0], P2[1] - P1[1], P2[2] - P1[2]};
  float P2P1[3] = {P1[0] - P2[0], P1[1] - P2[1], P1[2] - P2[2]};
  float P2P3[3] = {P3[0] - P2[0], P3[1] - P2[1], P3[2] - P2[2]};
  float P3P2[3] = {P2[0] - P3[0], P2[1] - P3[1], P2[2] - P3[2]};
  float P3P4[3] = {P4[0] - P3[0], P4[1] - P3[1], P4[2] - P3[2]};
  float P4P3[3] = {P3[0] - P4[0], P3[1] - P4[1], P3[2] - P4[2]};
  float angles[5] = {
    acos((P1TP[0]*P1P2[0] + P1TP[1]*P1P2[1] + P1TP[2]*P1P2[2]) / (sqrt(P1TP[0]*P1TP[0] + P1TP[1]*P1TP[1] + P1TP[2]*P1TP[2])*sqrt(P1P2[0]*P1P2[0] + P1P2[1]*P1P2[1] + P1P2[2]*P1P2[2]))) * 180 / PI,
    acos((P2P3[0]*P2P1[0] + P2P3[1]*P2P1[1] + P2P3[2]*P2P1[2]) / (sqrt(P2P3[0]*P2P3[0] + P2P3[1]*P2P3[1] + P2P3[2]*P2P3[2])*sqrt(P2P1[0]*P2P1[0] + P2P1[1]*P2P1[1] + P2P1[2]*P2P1[2]))) * 180 / PI,
    acos((P3P4[0]*P3P2[0] + P3P4[1]*P3P2[1] + P3P4[2]*P3P2[2]) / (sqrt(P3P4[0]*P3P4[0] + P3P4[1]*P3P4[1] + P3P4[2]*P3P4[2])*sqrt(P3P2[0]*P3P2[0] + P3P2[1]*P3P2[1] + P3P2[2]*P3P2[2]))) * 180 / PI,
    acos((P4P3[2] * -1) / sqrt(P4P3[0]*P4P3[0] + P4P3[1]*P4P3[1] + P4P3[2]*P4P3[2])) * 180 / PI,
    acos(-P3[0]/sqrt(P3[0]*P3[0]+P3[1]*P3[1])) * 180 / PI
  };
  if (P1[0] >= 0) {
    if (TPP1[0]*P1[1] / P1[0] - TPP1[1] >= 0) {
      angles[0] = 360 - angles[0];
    }
  } else {
    if (TPP1[0]*P1[1] / P1[0] - TPP1[1] <= 0) {
      angles[0] += 180;
    }
  }
  if (P3[0] <= 0) {
    angles[3] = 360 - angles[3];
    if (P3[1] <= 0) {
      angles[4] = acos(P3[0]/sqrt(P3[0]*P3[0]+P3[1]*P3[1])) * 180 / PI;
    } else {
      angles[4] = 360 - acos(P3[0]/sqrt(P3[0]*P3[0]+P3[1]*P3[1])) * 180 / PI;
    }
  } else {
    if (P3[1] <= 0) {
      angles[4] = 360 - angles[4];
    }
  }
  if (P2[0] - P3[0] >= 0) {
    if (P1[2] >= P2[2] + (P1[0] - P2[0]) * (P2[2] - P3[2]) / (P2[0] - P3[0])) {
      angles[1] = 360 - angles[1];
    }
  } else {
    if (P1[2] <= P2[2] + (P1[0] - P2[0]) * (P2[2] - P3[2]) / (P2[0] - P3[0])) {
      angles[1] = 360 - angles[1];
    }
  }
  float servo10 = (360-angles[0]); //A1
  float servo9 = (angles[1]); //A2
  float servo11 = (angles[2]); //A3
  float servo12 = (360-angles[3]); //A4
  float servo13 = (360-angles[4]); //A5
  myservo9.write(2*servo9/3-27);
  myservo10.write(2*servo10/3-27);
  myservo11.write(2*servo11/3-27);
  myservo12.write(2*servo12/3-27);
  myservo13.write(2*servo13/3-27);
}
void moveBotLinePath(float a[3],float b[3],float angs[2],float L[5],int split) {
  float ab[3] = {b[0]-a[0],b[1]-a[1],b[2]-a[2]};
  float TP[3] = {0,0,0};
  for (int i = 0; i < split; i++) {
    TP[0] = a[0]+ab[0]*i/split;
    TP[1] = a[1]+ab[1]*i/split;
    TP[2] = a[2]+ab[2]*i/split;
    moveBot(L,TP,angs);
  }
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
float L[5] = {6, 7.5, 22.25, 22.25, 3.75};
float TP[3] = {15.000001, 5.000001, 25.0000001};
float TRA[2] = {0.5, 135.5};

float VRx1 = A0;
float VRy1 = A1;
float VRx2 = A2;
float VRy2 = A3;
float VRx3 = A4;
float VRy3 = A5;

float xPosition1 = 0;
float yPosition1 = 0;
float xPosition2 = 0;
float yPosition2 = 0;
float xPosition3 = 0;
float yPosition3 = 0;
float mapX1 = 0;
float mapY1 = 0;
float mapX2 = 0;
float mapY2 = 0;
float mapX3 = 0;
float mapY3 = 0;
float a[3] = {0,0,0};
float b[3] = {0,0,0};
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
  mapX1 = map(xPosition1, 0, 1023, -511.5, 511.5);
  mapY1 = map(yPosition1, 0, 1023, -511.5, 511.5);
  mapX2 = map(xPosition2, 0, 1023, -511.5, 511.5);
  mapY2 = map(yPosition2, 0, 1023, -511.5, 511.5);
  mapX3 = map(xPosition3, 0, 1023, -511.5, 511.5);
  mapY3 = map(yPosition3, 0, 1023, -511.5, 511.5);
  float TP[3] = {25, 0, 17.5};
  float TRA[2] = {359.9, 179.9};
  moveBot(L, TP, TRA);
//  TP[0] += mapX1/10000;
//  TP[1] += mapY1/10000;
//  TP[2] += mapX2/10000;
//  TRA[0] += mapY3/10000;
//  TRA[1] += mapX3/10000;
//  if (TRA[0] > 360) {
//    TRA[0] = 1.5;
//  } else if (TRA[0]<0) {
//    TRA[0] = 358.5;
//  }
//  if (TRA[1] > 360) {
//    TRA[1] = 1.5;
//  } else if (TRA[1]<0) {
//    TRA[1] = 358.5;
//  }
  delay(1500);
  a[0] = 25;
  a[1] = 0;
  a[2] = 17.5;
  b[0] = 25;
  b[1] = 0;
  b[2] = 25;
  moveBotLinePath(a,b,TRA,L,5);
  delay(1500);
  a[0] = 25;
  a[1] = 0;
  a[2] = 25;
  b[0] = 25;
  b[1] = 7.5;
  b[2] = 25;
  moveBotLinePath(a,b,TRA,L,5);
  delay(1500);
  a[0] = 25;
  a[1] = 0;
  a[2] = 25;
  b[0] = 25;
  b[1] = 7.5;
  b[2] = -5;
  moveBotLinePath(a,b,TRA,L,15);
  delay(2000);
  a[0] = 25;
  a[1] = 7.5;
  a[2] = -5;
  b[0] = 25;
  b[1] = 15;
  b[2] = -5;
  moveBotLinePath(a,b,TRA,L,5);
  delay(1500);
  a[0] = 25;
  a[1] = 15;
  a[2] = -5;
  b[0] = 25;
  b[1] = 15;
  b[2] = -15;
  moveBotLinePath(a,b,TRA,L,5);
  delay(1500);
  a[0] = 25;
  a[1] = 15;
  a[2] = -15;
  b[0] = 25;
  b[1] = -15;
  b[2] = -15;
  moveBotLinePath(a,b,TRA,L,15);
  delay(2000);
  a[0] = 25;
  a[1] = -15;
  a[2] = -15;
  b[0] = 25;
  b[1] = -15;
  b[2] = -5;
  moveBotLinePath(a,b,TRA,L,5);
  delay(1500);
  a[0] = 25;
  a[1] = -15;
  a[2] = -5;
  b[0] = 25;
  b[1] = -7.5;
  b[2] = -5;
  moveBotLinePath(a,b,TRA,L,5);
  delay(1500);
  a[0] = 25;
  a[1] = -7.5;
  a[2] = -5;
  b[0] = 25;
  b[1] = -7.5;
  b[2] = 25;
  moveBotLinePath(a,b,TRA,L,15);
  delay(2000);
  a[0] = 25;
  a[1] = -7.5;
  a[2] = 25;
  b[0] = 25;
  b[1] = 0;
  b[2] = 25;
  moveBotLinePath(a,b,TRA,L,5);
  delay(1500);
  a[0] = 25;
  a[1] = 0;
  a[2] = 25;
  b[0] = 25;
  b[1] = 0;
  b[2] = 17.5;
  moveBotLinePath(a,b,TRA,L,5);
  delay(1500);
//  moveBot(L, {15, 5, 25}, {340.5, 135.5});
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
