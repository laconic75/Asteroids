#!/usr/bin/python2
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

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        self.score = 0
        self.difficulty = self.score + 50
        self.lives = 3
        self.time = 0.5
        self.ships = pyglet.graphics.Batch()
        self.rocks = pyglet.graphics.Batch()
        self.missiles = pyglet.graphics.Batch()

        # Images
        self.background = pyglet.image.load('static/images/nebula_blue.s2014.png')

        rock_img = pyglet.image.load('static/images/asteroid_blue.png')
        utils.center_image_anchor(rock_img)

        ship_sequence = pyglet.image.load('static/images/double_ship.png')
        ship_imgs = pyglet.image.ImageGrid(ship_sequence, 1, 2)
        utils.center_image_grid_anchors(ship_imgs)

        # Sounds
        thruster_snd = pyglet.media.load('static/sounds/rocket.ogg', streaming=False)
        explosion_snd = pyglet.media.load('static/sounds/explosion.ogg', streaming=False)

        # Spites 
        self.ship = PlayerSprite(ship_imgs, thruster_snd, 50, 100, 0, 0, 0, 35, self.ships, self.missiles)
        # Temporary 
        rock_position = utils.random_position(WIDTH, HEIGHT)
        # Temporary
        self.rock = MovingSprite(rock_img, sound=explosion_snd, diff=self.difficulty, radius=40, batch=self.rocks)

        # Keymaps
        self.key_downs = {key.UP:self.accel, key.LEFT:self.left, key.RIGHT:self.right, key.SPACE:self.fire}
        self.key_ups = {key.UP:self.decel, key.LEFT:self.right, key.RIGHT:self.left}

        pyglet.clock.schedule_interval(self.update, 1/60.0)  # update at 60Hz

    def accel(self):
        self.ship.thrusters = True
    
    def decel(self):
        self.ship.thrusters = False

    def left(self):
        self.ship.angle_vel -= 5

    def right(self):
        self.ship.angle_vel += 5
    
    def fire(self):
        self.ship.shoot()

    def on_key_press(self, symbol, modifiers):
        for key in self.key_downs:
            if key == symbol:
                self.key_downs[symbol]()

    def on_key_release(self, symbol, modifiers):
        for key in self.key_ups:
            if key == symbol:
                self.key_ups[symbol]()

    # TODO Implement Colisons
    # TODO Implement Sheilds
    # TODO Implement Spontaneos Rock Spawning
    # TODO Display Spash Screen
    def on_draw(self):
        self.clear()
        self.background.blit(0, 0)
        self.ships.draw()
        self.rocks.draw()
        self.missiles.draw()

    def update(self, dt):
        self.rock.update(WIDTH, HEIGHT) 
        self.ship.update(WIDTH, HEIGHT) 
        self.local_missiles = set(self.ship.missiles_fired)
        for missile in self.local_missiles:
            if not missile.update(WIDTH, HEIGHT):
                self.ship.missiles_fired.remove(missile)
                missile.delete()




def main():
    window = Window(WIDTH, HEIGHT)
    pyglet.app.run()

main()
