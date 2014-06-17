#!/usr/bin/python2
import math
import random
import pyglet
from pyglet.window import key
from pyglet.sprite import Sprite

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
batch = pyglet.graphics.Batch()

# Images
background = pyglet.image.load('static/images/nebula_blue.s2014.png')
rock_img = pyglet.image.load('static/images/asteroid_blue.png')
rock_img.anchor_x = rock_img.height/2
rock_img.anchor_y = rock_img.width/2
ship_sequence = pyglet.image.load('static/images/double_ship.png')
ship_imgs = pyglet.image.ImageGrid(ship_sequence, 1, 2)
ship_imgs[0].anchor_x = ship_imgs[0].height/2
ship_imgs[0].anchor_y = ship_imgs[0].width/2
ship_imgs[1].anchor_x = ship_imgs[1].height/2
ship_imgs[1].anchor_y = ship_imgs[1].width/2

# ship = Sprite(ship_imgs[0], 50, 100)

# #############################################################################
# TODO                                                                        #
# We need two Sprite subclasses Moving_Sprite and Player_Sprite               #
# Moving_Sprite should interit from Sprite and Player_Sprite should inherit   #
# Moving_Sprite                                                               #
# #############################################################################


class MovingSprite(Sprite):
    def __init__(self, img,
                 x=None,
                 y=None,
                 x_vel=None,
                 y_vel=None,
                 angle=None,
                 ang_vel=None,
                 sound=None,
                 batch=None):
        if x is None:
            x = random.randrange(0, WIDTH)
        if y is None:
            y = random.randrange(0, HEIGHT)
        super(MovingSprite, self).__init__(img, x, y, batch=batch)

        if x_vel is None:
            x_vel = random.randrange(0, difficulty)/50.0 - difficulty/2.0/50.0
        self.x_vel = x_vel

        if y_vel is None:
            y_vel = random.randrange(0, difficulty)/50.0 - difficulty/2.0/50.0
        self.y_vel = y_vel

        if angle is None:
            angle = random.randrange(0, 360)
        self.rotation = angle

        if ang_vel is None:
            ang_vel = (random.randrange(0, 60) - 30) * .2
        self._angle_vel = ang_vel


        self.image = img
        self.age = 0
        # TODO Handle sound

    def update(self):
        self.rotation += self._angle_vel
        self.x += self.x_vel
        self.x = self.x % WIDTH
        self.y += self.y_vel
        self.y = self.y % HEIGHT
        # TODO add lifespan logic
        return True


class PlayerSprite(MovingSprite):
    def __init__(self, img, x=0, y=0, x_vel=0, y_vel=0, angle=0, batch=None):
        super(PlayerSprite, self).__init__(img, x, y, batch=batch)
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.rotation  = angle
        self._thrusters = False
        self._angle_vel = 0

    @property
    def position(self):
        """Return tuple of ships position"""
        return self.x, self.y
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
            self.imgage = ship_imgs[0]

    @property
    def angle_vel(self):
        return self._angle_vel

    @angle_vel.setter
    def angle_vel(self, ang_vel):
        self._angle_vel = ang_vel

    def accel(self):
        if self._thrusters:
            self.x_vel += math.cos(self.rotation/180*math.pi) * .1
            self.y_vel += math.sin(self.rotation/180*math.pi) * .1
            
    def friction(self):
            self.x_vel = self.x_vel * .99
            self.y_vel = self.y_vel * .99

    def update(self):
        self.accel()
        self.friction()
        self.rotation += self._angle_vel
        self.x += self.x_vel
        self.y += self.y_vel
        self.x = self.x % WIDTH
        self.y = self.y % HEIGHT


ship = PlayerSprite(ship_imgs[0], 50, 100, batch=batch)
rock = MovingSprite(rock_img, batch=batch)

def accel():
    ship.thrusters = True
    
def decel():
    ship.thrusters = False

def left():
    ship.angle_vel -= 10

def right():
    ship.angle_vel += 10
    
def fire():
    ship.shoot()
    
key_downs = {key.UP:accel, key.LEFT:left, key.RIGHT:right, key.SPACE:fire}
key_ups = {key.UP:decel,key.LEFT:right, key.RIGHT:left}

@window.event
def on_key_press(symbol, modifiers):
    #if symbol == key.RIGHT:
    #    ship.x += 50
    #if symbol == key.LEFT:
    #    ship.x -= 50
    #if symbol == key.UP:
    for key in key_downs:
        if key == symbol:
            key_downs[symbol]()

@window.event
def on_key_release(symbol, modifiers):
    for key in key_ups:
        if key == symbol:
            key_ups[symbol]()

@window.event
def on_draw():
    window.clear()
    background.blit(0, 0)
    batch.draw()

def update(dt):
    rock.update()
    ship.update()

pyglet.clock.schedule_interval(update, 1/60.0)  # update at 60Hz
pyglet.app.run()
