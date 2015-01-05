#!/usr/bin/python2
import pyglet
import utils
from pyglet.window import key
from utils import group_collide, group_group_collide
from sprites import MovingSprite, PlayerSprite
from pyglet.sprite import Sprite

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
        self.splash_img = pyglet.image.load('static/images/splash.png') 

        # Sounds
        thruster_snd = pyglet.media.load('static/sounds/rocket.ogg', streaming=False)
        self.explosion_snd = pyglet.media.load('static/sounds/explosion.ogg', streaming=False)
        self.background_music = pyglet.media.load('static/sounds/space1.mp3', streaming=False)
        self.background_music.play()

        # Sprite Groups
        self.rock_group = set()
        self.missile_group = set()

        # Spites 
        self.ship = PlayerSprite(ship_imgs, thruster_snd, 400, 250, 0, 0, 270, 35, self.ships, self.missiles)
        self.splash = Sprite(self.splash_img, 200, 125)

        # Screen Text
        self.text_lives = pyglet.text.Label('Lives=' + str(self.lives),
                                            font_name='Times New Roman',
                                            font_size=36, x=10, y=10)
        self.text_score = pyglet.text.Label('Score=' + str(self.score),
                                            font_name='Times New Roman',
                                            font_size=36, x=10, y=60)

        # Keymaps
        self.key_downs = {key.UP:self.accel, key.LEFT:self.left, key.RIGHT:self.right, key.SPACE:self.fire, key.ESCAPE:pyglet.app.exit}
        self.key_ups = {key.UP:self.decel, key.LEFT:self.right, key.RIGHT:self.left}

        pyglet.clock.schedule_interval(self.update, 1/60.0)  # update at 60Hz
    def game_reset(self):
        self.started = False
        rock_group = set()
        # sountrack.pause()
        self.lives = 3
        self.score = 0
        # intro screen 
        # self.splash.draw()

    def display_score(self):
        self.text_lives = pyglet.text.Label('Lives=' + str(self.lives),
                                            font_name='Times New Roman',
                                            font_size=36, x=10, y=10)
        self.text_score = pyglet.text.Label('Score=' + str(self.score),
                                            font_name='Times New Roman',
                                            font_size=36, x=10, y=60)
    def start_game(self):
        #Function to start game on initial mouse click
        self.splash.delete()
        self.started = True

    def accel(self):
        self.ship.thrusters = True
    
    def decel(self):
        self.ship.thrusters = False

    def left(self):
        self.ship.angle_vel -= 5

    def right(self):
        self.ship.angle_vel += 5
    
    def fire(self):
        self.ship.shoot(self.missile_group)

    def on_mouse_press(self, x, y, button, modifiers):
        self.start_game()

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
    # TODO Implement Missile-Rock Colisons
    # TODO Implement Sheilds
    # TODO Display Spash Screen
    def on_draw(self):
        self.clear()
        self.background.blit(0, 0)
        self.ships.draw()
        self.rocks.draw()
        self.missiles.draw()
        self.text_lives.draw()
        self.text_score.draw()
        if not self.started:
           self.splash = Sprite(self.splash_img, 200, 125)
           self.splash.draw()

    def update(self, dt):
        if self.started:
            self.trigger_put_rock()
            for rock in self.rock_group:
                rock.update(WIDTH, HEIGHT) 
            self.ship.update(WIDTH, HEIGHT) 

            local_missiles = set(self.missile_group)
            for missile in local_missiles:
                if not missile.update(WIDTH, HEIGHT):
                    self.missile_group.remove(missile)
                    missile.delete()

            if group_collide(self.rock_group, self.ship):
                self.lives -= 1
                self.explosion_snd.play()

            if group_group_collide(self.missile_group, self.rock_group):
                self.score += 10
                self.difficulty  += self.score + 50
                self.explosion_snd.play()

            self.display_score()
        
        if self.lives < 0:
            self.game_reset()


def main():
    window = Window(WIDTH, HEIGHT)
    pyglet.app.run()

main()
