#!/usr/bin/python2
import math
import random
import pyglet
from pyglet.window import key
from pyglet.sprite import Sprite

# Global constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Global varibles
score = 0
difficulty = score + 50
lives = 3
time = 0.5
window = pyglet.window.Window(800, 600)

# Images
background = pyglet.image.load('static/images/nebula_blue.s2014.png')
ship_sequence = pyglet.image.load('static/images/double_ship.png')
ship_imgs = pyglet.image.ImageGrid(ship_sequence, 1, 2)

#ship = Sprite(ship_imgs[0], 50, 100)

###############################################################################o
# TODO                                                                         #
# We need two Sprite subclasses Moving_Sprite and Player_Sprite                #
# Moving_Sprite should interit from Sprite and PLayer_Sprite should inherit    #
# Moving_Sprite                                                                #
################################################################################
class Ship(Sprite):
    def __init__(self, img, x=0, y=0, x_vel=0, y_vel=0, angle=0):
        super(Ship, self).__init__(img, x, y)
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.angle = angle
        self._thrusters = False
        self.angle_vel = 0
    
    def accel(self):
        if self.thrusters:
           self.x_vel += math.cos(self.angle) * .1
           self.y_vel += math.sin(self.angle) * .1

    @property
    def thrusters(self):
        """Thrusters on or off"""
        return self._thrusters

    @thrusters.setter
    def thrusters(self, thrusters_on):
        self._thrusters = thrusters_on
        
        if self._thrusters:
            # Trusters on
            self.image = ship_imgs[1]
            # need to play thrusters sound
        else:
            self.img = ship_imgs[0]

ship = Ship(ship_imgs[0], 50, 100)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.RIGHT:
        ship.x += 50
    if symbol == key.LEFT:
        ship.x -= 50
    if symbol == key.UP:
        ship.thrusters = True

@window.event
def on_draw():
    window.clear()
    background.blit(0, 0)
    ship.draw()

pyglet.app.run()

