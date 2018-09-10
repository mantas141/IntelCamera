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

def setpantilt(x,y):
        ser.write(bytearray([115, x])) #First servo s - 115
        ser.write(bytearray[100, y]) #First servo d - 100

print("Testing the servos movement")

print("Both servos position 0")
setpantilt(0,0)
time.sleep(5)

print("First servo position to 10")
setpantilt(10,0)
time.sleep(1)

print("Position 10")
ser.write(bytearray([115,10]))
time.sleep(1)

print("Position 120")
ser.write(bytearray([115,120]))
time.sleep(1)

print("2nd position 50")
ser.write(bytearray[100,50])
time.sleep(1)