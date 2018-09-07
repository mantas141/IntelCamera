import time
import serial
import math


ser = serial.Serial()

ser.baudrate = 115200
ser.port = 'COM4'
ser.open()

# Servo No.1 PWM pin should be on pin2
# Servo No. 2 PWM pin should be on pin3

time.sleep(3)
ser.write(b'o')
time.sleep(2)
ser.write(b'9')
time.sleep(2)
ser.write(b'p')
time.sleep(2)
ser.write(b'9')
time.sleep(2)


while True:
    ser.write(b'v')
    time.sleep(2)
    ser.write(b'0')
    time.sleep(2)
    ser.write(b'v')
    time.sleep(2)
    ser.write(b'100')
    time.sleep(2)
