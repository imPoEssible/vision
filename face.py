# -*- coding: utf-8 -*-
"""
@author: sophiali
"""

import pygame, random, math, time
from pygame.locals import *
from math import pi
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
            ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2)
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
            if len(faces) == 0:
                ser.write("2")
                continue
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

class Model:
    def __init__(self):
        self.faces = {}
        self.populate_faces()

        self.face = self.faces["smile"]
        self.expression = "smile"

        self.define_colors()
        self.color = self.BLACK

    def define_colors(self):
        # Define the colors we will use in RGB format
        self.BLACK = (  0,   0,   0)
        self.WHITE = (255, 255, 255)
        self.BLUE =  (  0,   0, 255)
        self.GREEN = (  0, 255,   0)
        self.RED =   (255,   0,   0)
        self.PINK = (240, 128, 128)
    
    def populate_faces(self):
        self.faces["hello"] = u'ヽ(･∀･)ﾉ'
        self.faces["glitter"] = u'(ﾉ´ヮ´)ﾉ*･ﾟ✧'
        self.faces["excite"] = u'(o((*ﾟ▽ﾟ*))o)'
        self.faces["d_left"] = u'〜(￣▽￣〜)'
        self.faces["d_right"] = u'(〜￣▽￣)〜'
        self.faces["blush"] = u'(〃・ω・〃)'
        self.faces["smile"] = u'( ・ω・ )'
        self.faces["question"] = u'( ・◇・)？'
        self.faces["wtf"] = u'щ(ﾟﾛﾟщ)'

    def update(self):
        self.face = self.faces[self.expression]  

class View:
    """ Draws our game in a Pygame window """
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
        self.font = pygame.font.Font("kochi.tff", 50)

    def draw(self):
        self.screen.fill(self.model.WHITE)

        face_print = self.font.render(self.model.face, 3, self.model.color)
        face_pos = face_print.get_rect(bottomleft = (20,160))
        self.screen.blit(face_print, face_pos)

        pygame.display.update()

class Controller:
    """ Manipulate game state based on keyboard input """
    def __init__(self, model):
        self.model = model

    def handle_pygame_key(self):
        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_LEFT]:
            print "key!"
            self.model.expression = "blush"

    def handle_pygame_mouse(self, event):
        x, y = event.pos
        self.model.expression = "blush"
        self.model.color = self.model.PINK

def run_screen():
    pass

if __name__ == '__main__':
    pygame.init()
    walls = []
    size = (320, 240)
    screen = pygame.display.set_mode(size)
    model = Model()
    view = View(model,screen)
    controller = Controller(model)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                controller.handle_pygame_mouse(event)
            elif event.type == MOUSEBUTTONUP:
                model.expression = "smile"
                model.color = model.BLACK
        controller.handle_pygame_key()
        model.update()
        view.draw()
        time.sleep(0.001)

    pygame.quit()