from time import sleep
import serial

def readresponse():
        b = bytearray(b"                   ");
        ser.readinto(b)  #beware of timing issues here
        print(b)

def readbinaryresponse():
        b = bytearray(b"                   ");
        ser.readinto(b)  #beware of timing issues here
        print(b[0]*256 + b[1]   )
        #print(b[1])
def setup():
        #setup serial connection
        ser = serial.Serial('COM3',115200,timeout=0.5)  # open serial port USB
        #ser = serial.Serial('/dev/ttyAMA0',115200,timeout=0.5)  # open serial port on gpio
        print(ser.name)         # check which port was really used
        sleep(3)
        #when the serial connection is initialized the usb-power is "flicked"
        #causing the arduino to boot and thereby iddentify itself
        readresponse()

def ping():
        print("Pinging the arduino to see if the connection is established")
        ser.write(':'.encode('ascii'))
        ser.write('y'.encode('ascii'))
        ser.write('@'.encode('ascii'))
        readresponse()

