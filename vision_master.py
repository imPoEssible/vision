#!/usr/bin/env python

import roslib; roslib.load_manifest('poe_vision')
from std_msgs.msg import String, Int16, Bool
# from sensor_msgs.msg import Image
# from stereo_msgs.msg import DisparityImage
from poe_kinect.msg import *
import rospy
import time
import cv2
# from cv_bridge import CvBridge, CvBridgeError
import serial
import time

class SerialConnection:
	def __init__(self):
		self.addr = '/dev/ttyACM0'
		self.baud = 9600
		self.port = serial.Serial(self.addr, self.baud, timeout=2)


class VisualChecker():
	def __init__(self):
		rospy.init_node("vision_master", anonymous=True)
		rospy.Subscriber("/ocr_detected", String, self.ocr_callback)
		rospy.Subscriber("/smile_detected", Bool, self.smile_callback)
		rospy.Subscriber("/point_location", pointerpos, self.location_callback)
		rospy.Subscriber("/detected_gestures", gestures, self.gesture_callback)
		self.mode = 0
		self.interaction = 0

	def ocr_callback(self, data):
		pass
		# print data.data

	def smile_callback(self, data):
		print data.data
		if data.data:
			self.interaction = 1

	def location_callback(self, data):
		xpos = data.positionx
		if xpos != 0:
			if -300 < xpos < -200:
				self.mode = 2
			elif -200 < xpos < -100:
				self.mode = 3
			elif -100 < xpos < 100:
				self.mode = 4
			elif 100 < xpos < 200:
				self.mode = 5
			elif 200 < xpos < 300:
				self.mode = 1
			# print xpos

	def gesture_callback(self, data):
		if data.wave == True:
			self.interaction = 1
			print "hello there!"
		# print data

	def run(self):
		try:
			ser = SerialConnection()
		except:
			raise Exception("Serial port not open, connect Arduino?")
		r = rospy.Rate(20)
		self.prev_mode = 0
		while not rospy.is_shutdown():
			if self.interaction != 0:
				self.port.write(str(self.interaction))
				self.interaction = 0
			elif self.mode != self.prev_mode:
				ser.port.write(str(self.mode))
				print "write mode " + str(self.mode)
				self.prev_mode = self.mode
				# time.sleep(2)
			r.sleep()


if __name__ == "__main__":
	vc = VisualChecker()
	vc.run()