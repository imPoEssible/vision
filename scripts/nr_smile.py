#!/usr/bin/env python

"""
* Using OpenCV, this script detects a face and a
* smile within the face. It also draws rectangles
* around the face. It uses two haarcascade for each
* feature detected
"""

import cv2
import numpy as np
import serial
import time

class SerialConnection:
    def __init__(self):
        self.addr = '/dev/ttyACM0'
        self.baud = 9600
        self.port = serial.Serial(self.addr, self.baud, timeout=2)


class SmileDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml') #face xml
        self.mouth_cascade = cv2.CascadeClassifier('haarcascade_smile.xml') #smile xml

    def run(self):
        try:
            ser = SerialConnection()
        except:
            raise Exception("Serial port not open, connect Arduino?")
        cap = cv2.VideoCapture(0)
        i = 0
        while True:
            ret, self.frame = cap.read()
            if i == 15:
                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minSize=(20,20))
                print len(faces)
                for (x,y,w,h) in faces:
                    print "FACE"
                    cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,0,255),2)
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = self.frame[y:y+h, x:x+w]

                    mouth = self.mouth_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=20, minSize=(10,10), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
                    for (mp,mq,mr,ms) in mouth:
                        cv2.rectangle(roi_color,(mp,mq),(mp+mr,mq+ms), (255,0,0),1)
                        print "SMILE"
                        ser.write("1")
                i = 0
            i += 1

            cv2.imshow("output", self.frame)
            c = cv2.waitKey(1)

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    smile = SmileDetector()
    smile.run()
