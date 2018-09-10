""""Testing te tilt pan functionality from python (adjust the serial port-name) """

import time
import math
import serial

def setup():
    ser.baudrate = 115200
    ser.port = 'COM3'
    ser.open()
    time.sleep(2)


def setpantilt(x,y):
    ser.write(bytearray([48, x]))
    ser.write(bytearray([49, y]))


ser = serial.Serial()

setup()

setpantilt(0,0)
print('nu 1')
time.sleep(10)
setpantilt(20,0)
print('nu 2')

print("send @")
ser.write(bytearray([64]))
time.sleep(1)

print("pos 10")
ser.write(bytearray([48,10]))
time.sleep(1)

print("pos 150")
ser.write(bytearray([48,150]))
time.sleep(1)

print("pos 10")
ser.write(bytearray([48,10]))
time.sleep(1)

print("pos 150")
ser.write(bytearray([48,150]))
time.sleep(1)




for pos in range (10,150,5):
    ser.write(bytearray([49,pos]))
    time.sleep(0.1)

for pos in range(0,360,10):
    ser.write(bytearray([48,bytes (150*(1+math.cos(3.14*pos/180)))]))
    ser.write(bytearray([49,bytes (150*(1+math.sin(3.14*pos/180)))]))
    time.sleep(0.1)
