#!/usr/bin/python2
import pyglet
import utils
from pyglet.window import key
from utils import group_collide, group_group_colide
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
        self.started = False
        self.rock_trigger = 0

        # Images
        self.background = pyglet.image.load('static/images/nebula_blue.s2014.png')

        self.rock_img = pyglet.image.load('static/images/asteroid_blue.png')
        utils.center_image_anchor(self.rock_img)

        ship_sequence = pyglet.image.load('static/images/double_ship.png')
        ship_imgs = pyglet.image.ImageGrid(ship_sequence, 1, 2)
        utils.center_image_grid_anchors(ship_imgs)

        # Sounds
        thruster_snd = pyglet.media.load('static/sounds/rocket.ogg', streaming=False)
        self.explosion_snd = pyglet.media.load('static/sounds/explosion.ogg', streaming=False)

        # Sprite Groups
        self.rock_group = set()
        self.missile_group = set()

        # Spites 
        self.ship = PlayerSprite(ship_imgs, thruster_snd, 50, 100, 0, 0, 0, 35,
                                 self.ships, self.missiles)

        # Screen Text
        self.text_lives = pyglet.text.Label('Lives=' + str(self.lives),
                                            font_name='Times New Roman',
                                            font_size=36, x=10, y=10)

        # Keymaps
        self.key_downs = {key.UP:self.accel, key.LEFT:self.left, 
                          key.RIGHT:self.right, key.SPACE:self.fire}
        self.key_ups = {key.UP:self.decel, key.LEFT:self.right, 
                        key.RIGHT:self.left}

        pyglet.clock.schedule_interval(self.update, 1/60.0)  # update at 60Hz

    def game_over(self):
        self.started = False
        rock_group = set()
        # sountrack.pause()
        self.lives = 3
        self.score = 0
        # intro screen 

    def display_score(self):
        self.text_lives = pyglet.text.Label('Lives=' + str(self.lives), 
                                            font_name='Times New Roman',
                                            font_size=36,                                                                                                       x=10, y=10)

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

    def put_rock(self):
        rock_position = utils.random_position(WIDTH, HEIGHT)
        rock = MovingSprite (self.rock_img, rock_position[0], rock_position[1], 
                             sound=self.explosion_snd, diff=self.difficulty, 
                             radius=40, batch=self.rocks)
        self.rock_group.add(rock)

    def trigger_put_rock(self):
        self.rock_trigger += 1
        if self.rock_trigger > 60 and len(self.rock_group) < 10:
            self.put_rock()
            self.rock_trigger = 0
            
    # TODO Implement Colisons
    # TODO Implement Sheilds
    # TODO Display Spash Screen
    def on_draw(self):
        self.clear()
        self.background.blit(0, 0)
        self.ships.draw()
        self.rocks.draw()
        self.missiles.draw()
        self.text_lives.draw()

    def update(self, dt):
        self.trigger_put_rock()
        for rock in self.rock_group:
            rock.update(WIDTH, HEIGHT) 
        self.ship.update(WIDTH, HEIGHT) 

        local_missiles = set(self.ship.missiles_fired)
        for missile in local_missiles:
            if not missile.update(WIDTH, HEIGHT):
                self.ship.missiles_fired.remove(missile)
                missile.delete()

        if group_collide(self.rock_group, self.ship):
                    self.lives -= 1

        if group_group_colide(self.rock_group, local_missiles):
            self.score += 10
            self.diff = self.score + 50

        self.display_score()



def main():
    window = Window(WIDTH, HEIGHT)
    pyglet.app.run()

main()
