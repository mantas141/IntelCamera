# WebCam Motion Detector

# importing OpenCV, time and Pandas library
import cv2, time, pandas
import numpy as np
# importing datetime class from datetime library
from datetime import datetime

import tiltpan

tiltpan.setup()
tiltpan.setpantilt(90,20)  # 0..180, 0..60
time.sleep(2)

tilteastwest = 90
tiltnorthsouth=20

# Assigning our static_back to None
static_back = None

# List when any moving object appear
motion_list = [None, None]

# Time of movement
#time = []

start = time.time()

# Initializing DataFrame, one column is start
# time and other column is end time
df = pandas.DataFrame(columns=["Start", "End"])

# Capturing video
video = cv2.VideoCapture(0)

nbframes=0
actiontime=0.30

# Infinite while loop to treat stack of image as video
while True:
    # Reading frame(image) from video
    check, frame = video.read()

    # Initializing motion = 0(no motion)
    motion = 0

    # Converting color image to gray_scale image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Converting gray scale image to GaussianBlur
    # so that change can be find easily
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # In first iteration we assign the value
    # of static_back to our first frame
    if static_back is None:
        static_back = gray
        continue

    if (abs( start - time.time())>actiontime):
        static_back = gray
        print(time.time())
        start = time.time()

    # Difference between static background
    # and current frame(which is GaussianBlur)
    diff_frame = cv2.absdiff(static_back, gray)

    # If change in between static background and
    # current frame is greater than 30 it will show white color(255)
    thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Finding contour of moving object
    (_, cnts, _) = cv2.findContours(thresh_frame.copy(),
                                    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #for contour in cnts:
       # if cv2.contourArea(contour) < 1000:
       #     continue
        #motion = 1

        #(x, y, w, h) = cv2.boundingRect(contour)
        # making green rectangle arround the moving object
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        #print (x,y)
        #nbframes = nbframes+1
        #framename = 'frame' + str(nbframes) + '.jpg'
        #cv2.imwrite(framename, frame)

    # Find the index of the largest contour
    if len(cnts)>0:
       areas = [cv2.contourArea(c) for c in cnts]
       max_index = np.argmax(areas)
       cnt = cnts[max_index]
       if cv2.contourArea(cnt) < 1000:
           continue
       (x, y, w, h) = cv2.boundingRect(cnt)
       # making green rectangle arround the moving object
       cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
       print (x,y)

       displaytext=''
       if (x>400):
           displaytext = 'West'
           print('West ' + str(tilteastwest))
           if tilteastwest>20:
               tilteastwest -= 20
               print('West 1 ' + str(tilteastwest))
               tiltpan.setpantilt(tilteastwest, tiltnorthsouth)
           print('West 2 ' + str(tilteastwest))
           time.sleep(actiontime)
       if (x < 100):
           displaytext = 'East'
           print('East  ' + str(tilteastwest))
           if tilteastwest<160:
               tilteastwest += 20
               print('East 1 ' + str(tilteastwest))
               tiltpan.setpantilt(tilteastwest, tiltnorthsouth)
           print('East 2 ' + str(tilteastwest))
           time.sleep(actiontime)

       if (y < 100):
           displaytext = displaytext +'North'
           print('North ' + str(tiltnorthsouth))
           if (tiltnorthsouth < 60):
               tiltnorthsouth += 10
               print('tilt 8 ' + str(tiltnorthsouth))
               tiltpan.setpantilt(tilteastwest, tiltnorthsouth)
               time.sleep(actiontime)
           print('North 2 ' + str(tiltnorthsouth))

       if (y > 200 ):
           displaytext = displaytext + 'South'
           print('South ' + str(tiltnorthsouth))
           if (tiltnorthsouth > 10):
               tiltnorthsouth -= 10
               print('tilt 11 ' + str(tiltnorthsouth))
               tiltpan.setpantilt(tilteastwest, tiltnorthsouth)
               time.sleep(actiontime)
           print('South 2 ' + str(tiltnorthsouth))

       cv2.putText(frame, displaytext, (205, 205), cv2.FONT_HERSHEY_COMPLEX_SMALL, .7, (225, 0, 0))

    # Appending status of motion
    #motion_list.append(motion)

    #motion_list = motion_list[-2:]

    # Appending Start time of motion
    #if motion_list[-1] == 1 and motion_list[-2] == 0:
    #    time.append(datetime.now())

    # Appending End time of motion
    #if motion_list[-1] == 0 and motion_list[-2] == 1:
     #   time.append(datetime.now())

    # Displaying image in gray_scale
    #cv2.imshow("Gray Frame", gray)

    # Displaying the difference in currentframe to
    # the staticframe(very first_frame)
    #cv2.imshow("Difference Frame", diff_frame)

    # Displaying the black and white image in which if
    # intencity difference greater than 30 it will appear white
    #cv2.imshow("Threshold Frame", thresh_frame)

    # Displaying color frame with contour of motion of object
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)
    # if q entered whole process will stop
    if key == ord('q'):
        # if something is movingthen it append the end time of movement
        if motion == 1:
            time.append(datetime.now())
        break

# Appending time of motion in DataFrame
#for i in range(0, len(time), 2):
#    df = df.append({"Start": time[i], "End": time[i + 1]}, ignore_index=True)

# Creating a csv file in which time of movements will be saved
#df.to_csv("Time_of_movements.csv")

video.release()

# Destroying all the windows
cv2.destroyAllWindows()