/*
  Adressable extension of the DRC protocol.(by Kaj Norman Nielsen knn@eaaa.dk)
  (Originally Copyright (c) 2012 Gordon Henderson
  Full details at:
  http://projects.drogon.net/drogon-remote-control/drc-protocol-arduino/
  )
  packet:
  +---+------+-------+---------+
  |':'|Addres|command|parameter|
  +---+------+-------+---------+
  Address :
  The hard-coded number of the actual arduino (coded in the program)
  ( 0-255  or   0x00-0xFF )
  commands:
  @: 0x40 Ping          Send back #: 0x40
  0: 0x30 0xNN  Set Pin NN OFF
  1: 0x31 0xNN  Set Pin NN ON
  i: 0x69 0xNN  Set Pin NN as Input
  o: 0x6F 0xNN  Set Pin NN as Output
  p: 0x6F 0xNN  Set Pin NN as PWM
  v: 0x6F 0xNN  Set PWM value on Pin NN
  r: 0x72 0xNN  Read back digital Pin NN  Send back 0: 0x30 or 1: 0x31
  a: 0x61 0xNN  Read back analogue pin NN Send back binary 2 bytes, Hi
  s: 0x73 0xNN  Set servo position NN is in the range from 0 to 180
  d: 0x64 0xNN  Set servo position NN in the range 0 to 180
  A servo is set on a fixed pin number 2
  The second servo is fixed to pin number 3
*************************************************************************
********
  This is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  drcAduino is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  You should have received a copy of the GNU General Public License
  along with drcAduino.  If not, see <http://www.gnu.org/licenses/>.
*************************************************************************
********
*/
// Serial commands
#include <Servo.h>
Servo pan,tilt;  // create servo object to control a servo
int mode = 0;
#define START_MARK      ':'
#define ADDR_THIS       'y'  //This excact Arduino (individual number on the network)
#define CMD_PING        '@'
#define CMD_SETSERVO_1  's'
#define CMD_SETSERVO_2  'd'
#define CMD_PIN_0       '0'
#define CMD_PIN_1       '1'
#define CMD_PIN_I       'i'
#define CMD_PIN_O       'o'
#define CMD_RD_PIN      'r'
#define CMD_RA_PIN      'a'
#define CMD_PWM_PIN     'p'
#define CMD_PWM_VAL_PIN  'v'
#define CMD_DEBUG_DIGITAL       'D'
#define CMD_DEBUG_ANALOGUE      'A'
// Arduino with a 168 or 328 chip
//      ie. Arduino Classic, Demi, Uno.
#define MIN_APIN         0
#define MAX_APIN         5
#define MIN_DPIN         2
#define MAX_DPIN        13
#define STD_BY            0
#define AWAIT_ADDR        1
#define AWAIT_COMMAND     2
void setup ()
{
  int pin ;
  Serial.begin (115200) ;
  Serial.println ("Addr DRC Arduino 1.0") ;
  pinMode (13, OUTPUT) ;
  digitalWrite (13, HIGH) ;
  for (pin = 2 ; pin < 13 ; ++pin)
  {
    digitalWrite (pin, LOW) ;
    pinMode (pin, INPUT) ;
  }
  analogReference (DEFAULT) ;
  pan.attach(2);  // attaches the servo on pin 2 to the servo object
  tilt.attach(3);  // attaches the servo on pin 3 to the servo object
}
int myGetchar ()
{
  int x ;
  while ((x = Serial.read ()) == -1)
    ;
  return x ;
}
void loop ()
{
  unsigned int pin ;
  unsigned int aVal, dVal ;
  char lastchar;
  for (;;)
  {
    while (Serial.available () < 0); //wait for char
    lastchar = myGetchar ();
    if ((mode == STD_BY) && (lastchar == START_MARK ))
    {
      mode = AWAIT_ADDR ;
      continue;  //for loop
    }
    if ((mode == AWAIT_ADDR))
    {
      if (lastchar == ADDR_THIS )
      {
        mode = AWAIT_COMMAND ;
        continue; //forloop
      }
      else
      {
        mode = STD_BY;
        continue; //forloop
      }
    }
    if (mode == AWAIT_COMMAND)
    {
      switch (lastchar)
      {
        case CMD_PING:
          Serial.write (CMD_PING) ;
          mode = STD_BY;
          continue ;
        case CMD_PIN_O:
          //          pin = Serial.read () ;  OLD VERSION
          pin = myGetchar () ;
          if ((pin >= MIN_DPIN) && (pin <= MAX_DPIN))
            pinMode (pin, OUTPUT) ;
          mode = STD_BY;
          continue ;
        case CMD_SETSERVO_1:
          aVal = myGetchar () ;
          if ((aVal >= 0) && (aVal <= 180))
            pan.write(aVal);
          mode = STD_BY;
          continue ;
        case CMD_SETSERVO_2:
            aVal = myGetchar () ;
            if ((aVal >= 0) && (aVal <= 180))
                tilt.write(aVal);
            mode = STD_BY;
            continue;
        case CMD_PIN_I:
          pin = myGetchar () ;
          if ((pin >= MIN_DPIN) && (pin <= MAX_DPIN))
            pinMode (pin, INPUT) ;
          mode = STD_BY;
          continue ;
        case CMD_PIN_0:
          pin = myGetchar () ;
          if ((pin >= MIN_DPIN) && (pin <= MAX_DPIN))
            digitalWrite (pin, LOW) ;
          mode = STD_BY;
          continue ;
        case CMD_PIN_1:
          pin = myGetchar () ;
          if ((pin >= MIN_DPIN) && (pin <= MAX_DPIN))
            digitalWrite (pin, HIGH) ;
          mode = STD_BY;
          continue ;
        case CMD_RD_PIN:
          pin = myGetchar () ;
          if ((pin >= MIN_DPIN) && (pin <= MAX_DPIN))
            dVal = digitalRead (pin) ;
          else
            dVal = LOW ;
          Serial.write ((dVal == HIGH) ? '1' : '0') ;
          mode = STD_BY;
          continue ;
        case CMD_RA_PIN:
          pin = myGetchar () ;
          if ((pin >= MIN_APIN) && (pin <= MAX_APIN))
            aVal = analogRead (pin) ;
          else
            aVal = 0 ;
          Serial.write ((aVal & 0xFF00) >> 8) ;        // High byte    first
          Serial.write ( aVal & 0x00FF      ) ;
          mode = STD_BY;
          continue ;
        case CMD_PWM_PIN:
          pin = myGetchar () ;
          if ((pin >= MIN_DPIN) && (pin <= MAX_DPIN))
            pinMode (pin, OUTPUT) ;
          mode = STD_BY;
          continue ;
        case CMD_PWM_VAL_PIN:
          pin  = myGetchar () ;
          dVal = myGetchar () ;
          if ((pin >= MIN_DPIN) && (pin <= MAX_DPIN))
            analogWrite (pin, dVal) ;
          mode = STD_BY;
          continue ;
        default :
          mode = STD_BY;
      } //switch
    } // if AWAIT_COMMAND
  } //for
} //loop
