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
from PIL import Image
import pytesseract
from matplotlib import cm


def main():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml') #face xml
    mouth_cascade = cv2.CascadeClassifier('haarcascade_smile.xml') #smile xml

    kernel = np.ones((21,21),'uint8')

    rospy.init_node("vision_detection", anonymous = True)
    pub_ocr = rospy.Publisher("/ocr_detected", String, queue_size=10) #subscribing to detected gestures from detectfinger
    pub_face = rospy.Publisher("/smile_detected", Bool, queue_size=10) #subscribing to detected gestures from detectfinger

    cap = cv2.VideoCapture(0)
    i = 0

    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if i == 15:
            bw_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            im = Image.fromarray(np.uint8(cm.gist_earth(bw_img)*255))
            detected_string = pytesseract.image_to_string(im)
            if detected_string:
                print detected_string
            pub_ocr.publish(detected_string)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minSize=(20,20))
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]

                mouth = mouth_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=20, minSize=(10,10), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

                for (mp,mq,mr,ms) in mouth:
                    cv2.rectangle(roi_color,(mp,mq),(mp+mr,mq+ms), (255,0,0),1)
                    pub_face.publish(True)
            i = 0

        i += 1
        cv2.imshow("output", frame)
        c = cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':

    main()