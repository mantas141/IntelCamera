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



#setup serial connection
ser = serial.Serial()  # open serial port USB
ser.baudrate = 115200
ser.port = 'COM3'
ser.timeout = 0.5
print(ser.name)
ser.open()
sleep(3)
#when the serial connection is initialized the usb-power is "flicked"
#causing the arduino to boot and thereby iddentify itself
readresponse()

sleep(3)

print("Pinging the arduino to see if the connection is established")
ser.write(bytearray([58,121,64]))
readresponse()
sleep(1)
ser.write(bytearray([58,121,105,55]))

while True:
        ser.write(bytearray([58,121,114,55]))
        readresponse()
        sleep(1)