#!/usr/bin/env python

"""
* Using OpenCV, this script detects a face and a
* smile within the face. It also draws rectangles
* around the face. It uses two haarcascade for each
* feature detected
"""
import roslib; roslib.load_manifest('poe_vision')
import cv2
import numpy as np
import rospy
from std_msgs.msg import String, Int16, Bool
from sensor_msgs.msg import Image
import pytesseract
from matplotlib import cm
from cv_bridge import CvBridge, CvBridgeError

class SmileDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml') #face xml
        self.mouth_cascade = cv2.CascadeClassifier('haarcascade_smile.xml') #smile xml
        self.bridge = CvBridge()

        rospy.init_node("vision_detection", anonymous = True)
        self.sub = rospy.Subscriber("/camera/rgb/image_raw_drop", Image, self.callback)
        self.pub_face = rospy.Publisher("/smile_detected", Bool, queue_size=10) #subscribing to detected gestures from detectfinger

    def callback(self, data):
        try:
            self.frame = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError, e:
            print e

        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minSize=(20,20))
        for (x,y,w,h) in faces:
            print "FACE"
            cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,0,255),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = self.frame[y:y+h, x:x+w]

            mouth = self.mouth_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=20, minSize=(10,10), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
            for (mp,mq,mr,ms) in mouth:
                cv2.rectangle(roi_color,(mp,mq),(mp+mr,mq+ms), (255,0,0),1)
                self.pub_face.publish(True)
                print "SMILE"

        cv2.imshow("output", self.frame)
        c = cv2.waitKey(1)

    def run(self):
        r = rospy.Rate(10)
        while not rospy.is_shutdown():
            r.sleep()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    smile = SmileDetector()
    smile.run()