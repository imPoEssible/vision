#!/usr/bin/env python
import roslib; roslib.load_manifest('poe_vision')
from PIL import Image
import pytesseract
import cv2
from cv2 import cv
import numpy as np
from matplotlib import cm
import rospy
from std_msgs.msg import String

def main():
	rospy.init_node("vision_ocr", anonymous = True)
	pub = rospy.Publisher("/ocr_detected", String, queue_size=10) #subscribing to detected gestures from detectfinger

	cap = cv2.VideoCapture(0)
	i = 0
	while not rospy.is_shutdown():
		ret, frame = cap.read()
		bw_img = cv2.cvtColor(frame, cv.CV_BGR2GRAY)
		if i == 15:
			im = Image.fromarray(np.uint8(cm.gist_earth(bw_img)*255))
			detected_string = pytesseract.image_to_string(im)
			print detected_string
			pub.publish(detected_string)
			i = 0
		i += 1
		cv2.imshow("camera", bw_img)
		c = cv2.waitKey(1)

if __name__ == '__main__':
	main()