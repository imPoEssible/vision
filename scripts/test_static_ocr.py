#!/usr/bin/env python
from PIL import Image
import pytesseract
import cv2
from cv2 import cv
import numpy as np
from matplotlib import cm

def main():
  cap = cv2.VideoCapture(0)
  i = 0
  while True:
	ret, frame = cap.read()
	bw_img = cv2.cvtColor(frame, cv.CV_BGR2GRAY)
	if i == 15:
		im = Image.fromarray(np.uint8(cm.gist_earth(bw_img)*255))
		print pytesseract.image_to_string(im)
		i = 0
	i += 1
	cv2.imshow("camera", bw_img)
	c = cv2.waitKey(1)

if __name__ == '__main__':
  main()