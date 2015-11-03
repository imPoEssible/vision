#!/usr/bin/env python

import roslib; roslib.load_manifest('poe_vision')
from std_msgs.msg import String, Int16, Bool
import rospy
import time

class VisualChecker():
	def __init__(self):
		rospy.init_node("vision_master", anonymous=True)
		rospy.Subscriber("/ocr_detected", String, self.ocr_callback)
		rospy.Subscriber("/smile_detected", Bool, self.smile_callback)

	def ocr_callback(self, data):
		pass
		# print data.data

	def smile_callback(self, data):
		print data.data

	def run(self):
		while not rospy.is_shutdown():
			time.sleep(1)


if __name__ == "__main__":
	vc = VisualChecker()
	vc.run()