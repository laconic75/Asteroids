
import math
import random
import pyglet
from utils import angle_to_vector
from utils import dist
from pyglet.sprite import Sprite


class MovingSprite(Sprite):
    def __init__(self, img, 
                 x=0,
                 y=0,
                 x_vel=None,
                 y_vel=None,
                 angle=None,
                 ang_vel=None,
                 sound=None,
                 radius=0,
                 lifespan=None,
                 diff=None,
                 batch=None):
        super(MovingSprite, self).__init__(img, x, y, batch=batch)

        if x_vel is None:
            x_vel = random.randrange(0, diff)/50.0 - diff/2.0/50.0
        self.x_vel = x_vel

        if y_vel is None:
            y_vel = random.randrange(0, diff)/50.0 - diff/2.0/50.0
        self.y_vel = y_vel

        if angle is None:
            angle = random.randrange(0, 360)
        self.rotation = angle

        if ang_vel is None:
            ang_vel = (random.randrange(0, 60) - 30) * .2
        self._angle_vel = ang_vel

        if lifespan is None:
            lifespan = float('inf')
        self._lifespan = lifespan


        self.image = img
        self.age = 0
        self._radius = radius
        self.sound = sound
        # TODO Handle sound
        # TODO Explosion Animations

    @property
    def radius(self):
        return self._radius
    
    @property
    def lifespan(self):
        return self._lifespan

    @property
    def center(self):
        return (self.x, self.y)

    def collide(self, other_object):
        sum_radii = self.radius + other_object.radius
        other_pos = other_object.center
        if dist(self.center, other_pos) < sum_radii:
            return True
        else: 
            return False
        
    def update(self, width, height):
        self.rotation += self._angle_vel
        self.x += self.x_vel
        self.x = self.x % width 
        self.y += self.y_vel
        self.y = self.y % height 
        # lifespan logic
        self.age += 1
        if self.age > self._lifespan:
            return False
        else:
            return True
        return True

class PlayerSprite(MovingSprite):
    def __init__(self, 
                 image_grid, 
                 sound,
                 x=0, 
                 y=0, 
                 x_vel=0, 
                 y_vel=0, 
                 angle=0, 
                 radius=0, 
                 batch=None,
                 missile_batch=None):

        super(PlayerSprite, self).__init__(image_grid[0], x, y, x_vel, y_vel, radius=radius, batch=batch)
        self.image_grid = image_grid
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.rotation  = angle
        self._thrusters = False
        self._angle_vel = 0
        self.thruster_snd = pyglet.media.Player()
        self.thruster_snd.queue(sound)

        # Sound and images for firing missiles
        self.missile_snd = pyglet.media.load('static/sounds/laser7.wav', streaming=False)
        self.missile_img = pyglet.image.load('static/images/shot2.png')
        self.missile_batch = missile_batch

    @property
    def position(self):
        """Return tuple of ships position"""
        return self.x, self.y

    @position.setter
    def position(self, coordinates):
        self.x, self.y = coordinates

    @property
    def thrusters(self):
        """Thrusters on or off"""
        return self._thrusters

    @thrusters.setter
    def thrusters(self, thrusters_on):
        self._thrusters = thrusters_on

        if self._thrusters:
            # Trusters on
            self.image = self.image_grid[1]
            # Play thrusters sound
            self.thruster_snd.play()
        else:
            self.image = self.image_grid[0]
            self.thruster_snd.pause()

    @property
    def angle_vel(self):
        return self._angle_vel

    @angle_vel.setter
    def angle_vel(self, ang_vel):
        self._angle_vel = ang_vel

    def accel(self):
        if self._thrusters:
           x_vel, y_vel = tuple([vel * .1 for vel in angle_to_vector(self.rotation)]) 
           self.x_vel += x_vel 
           self.y_vel += y_vel

    def shoot(self, missiles_set):
        """
        Shoot missile and make missile sound
        Callback a Set.add to missile_group in Window class
        to add new missile to Window
        """
        forward_vector = angle_to_vector(self.rotation)
        ship_nose = [self.x + ((self.height/2)* forward_vector[0]),
                     self.y + ((self.height/2)* forward_vector[1])]
        firing_vel = [self.x_vel + (5*forward_vector[0]), 
                      self.y_vel + (5*forward_vector[1])]
        missiles_set.add(MovingSprite(self.missile_img, 
                                           ship_nose[0], ship_nose[1], 
                                           firing_vel[0], firing_vel[1], 
                                           lifespan=60, batch= self.missile_batch))
        self.missile_snd.play()

    def friction(self):
            self.x_vel = self.x_vel * .995
            self.y_vel = self.y_vel * .995

    def update(self, width, height):
        self.accel()
        self.friction()
        self.rotation += self._angle_vel
        self.x += self.x_vel
        self.y += self.y_vel
        self.x = self.x % width 
        self.y = self.y % height 
