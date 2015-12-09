# -*- coding: utf-8 -*-
"""
@author: sophiali
"""

import pygame, random, math, time
from pygame.locals import *
from math import pi

class Model:
    def __init__(self):
        self.faces = {}
        self.populate_faces()

        self.face = self.faces["smile"]
        self.expression = "smile"

    
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
        self.define_colors()
        self.font = pygame.font.Font("kochi.tff", 50)

    def define_colors(self):
        # Define the colors we will use in RGB format
        self.BLACK = (  0,   0,   0)
        self.WHITE = (255, 255, 255)
        self.BLUE =  (  0,   0, 255)
        self.GREEN = (  0, 255,   0)
        self.RED =   (255,   0,   0)
        self.PINK = (240, 128, 128)

    def draw(self):
        self.screen.fill(self.WHITE)

        face_print = self.font.render(self.model.face, 3, self.BLACK)
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
        controller.handle_pygame_key()
        model.update()
        view.draw()
        time.sleep(0.001)

    pygame.quit()