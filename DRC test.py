import time
import serial
import math


ser = serial.Serial()

ser.baudrate = 115200
ser.port = 'COM4'
ser.timeout = 0.5
ser.open()

print(ser.name)

time.sleep(3)

while True:
    ser.write(b'@')
    time.sleep(1.5)

    ser.write(b'0')
    ser.write(' '.encode('ascii'))

    time.sleep(1)

    ser.write(b'0')
    ser.write('z'.encode('ascii'))

    time.sleep(1)

    ser.write(b'@')
    time.sleep(1.5)

    ser.write(b'1')
    ser.write(' '.encode('ascii'))

    time.sleep(1)

    ser.write(b'1')
    ser.write('z'.encode('ascii'))

    time.sleep(1)

