#!/usr/bin/python2
import pyglet
from pyglet.window import key
from pyglet.sprite import Sprite

window = pyglet.window.Window(800, 600)
background = pyglet.image.load('nebula_blue.s2014.png')
ship_sequence = pyglet.image.load('double_ship.png')
ship_imgs = pyglet.image.ImageGrid(ship_sequence, 1, 2)
#ship = Sprite(ship_imgs[0], 50, 100)

class Ship(Sprite):
    def __init__(self, img, x=0, y=0, x_vel=0, y_vel=0, angle=0):
        super(Ship, self).__init__(img, x, y)
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.angle = angle

ship = Ship(ship_imgs[0], 50, 100)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.RIGHT:
        ship.x += 50

@window.event
def on_draw():
    window.clear()
    background.blit(0, 0)
    ship.draw()

pyglet.app.run()

