#!/usr/bin/python2
import math
import random
import pyglet
import utils
from pyglet.window import key
from utils import group_collide
from sprites import MovingSprite, PlayerSprite
# Global constants
WIDTH = 800
HEIGHT = 600
SCREEN_SIZE = [WIDTH, HEIGHT]
DIMENSIONS = 2

# Global varibles
score = 0
difficulty = score + 50
lives = 3
time = 0.5
window = pyglet.window.Window(WIDTH, HEIGHT)
ships = pyglet.graphics.Batch()
rocks = pyglet.graphics.Batch()
missiles = pyglet.graphics.Batch()

# Images
background = pyglet.image.load('static/images/nebula_blue.s2014.png')

rock_img = pyglet.image.load('static/images/asteroid_blue.png')
utils.center_image_anchor(rock_img)

ship_sequence = pyglet.image.load('static/images/double_ship.png')
ship_imgs = pyglet.image.ImageGrid(ship_sequence, 1, 2)
utils.center_image_grid_anchors(ship_imgs)

# Sounds
thruster_snd = pyglet.media.load('static/sounds/rocket.ogg', streaming=False)
explosion_snd = pyglet.media.load('static/sounds/explosion.ogg', streaming=False)

# Global Varibles that need to be moved into a class. 
ship = PlayerSprite(ship_imgs, thruster_snd, 50, 100, 0, 0, 0, 35, ships, missiles)
# Temporary 
rock_position = utils.random_position(WIDTH, HEIGHT)
# Temporary
rock = MovingSprite(rock_img, sound=explosion_snd, diff=difficulty, radius=40, batch=rocks)

def accel():
    ship.thrusters = True
    
def decel():
    ship.thrusters = False

def left():
    ship.angle_vel -= 5

def right():
    ship.angle_vel += 5
    
def fire():
    ship.shoot()
    
key_downs = {key.UP:accel, key.LEFT:left, key.RIGHT:right, key.SPACE:fire}
key_ups = {key.UP:decel,key.LEFT:right, key.RIGHT:left}

@window.event
def on_key_press(symbol, modifiers):
    for key in key_downs:
        if key == symbol:
            key_downs[symbol]()

@window.event
def on_key_release(symbol, modifiers):
    for key in key_ups:
        if key == symbol:
            key_ups[symbol]()

# TODO Implement Colisons
# TODO Implement Sheilds
# TODO Implement Spontaneos Rock Spawning
# TODO Display Spash Screen

@window.event
def on_draw():
    window.clear()
    background.blit(0, 0)
    ships.draw()
    rocks.draw()
    missiles.draw()

def update(dt):
    rock.update(WIDTH, HEIGHT) 
    ship.update(WIDTH, HEIGHT) 
    local_missiles = set(ship.missiles_fired)
    for missile in local_missiles:
        if not missile.update(WIDTH, HEIGHT):
            ship.missiles_fired.remove(missile)
            missile.delete()

pyglet.clock.schedule_interval(update, 1/60.0)  # update at 60Hz
pyglet.app.run()
