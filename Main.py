import cv2, time, pandas
import numpy as np
from datetime import datetime

#Importing the servoc pan tilt controls

import servoc

servoc.setup()
servoc.setpantilt(90,20)
time.sleep(2)

tiltew = 90
tiltns = 20


static_back = None

#List of any face apearing
motion_list = [None, None]

start = time.time()

# Initializing DataFrame, one column is start
# time and other column is end time
df = pandas.DataFrame(columns=["Start", "End"])

# Capturing video
video = cv2.VideoCapture(1)

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
