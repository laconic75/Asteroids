"""
Helper function for asteroids game
"""
import random
import math

# Helper functions
def angle_to_vector(degrees):
    """
    Input: angle in degrees
    Output: unit vector for angle
    """
    rad_ang = math.radians(degrees)
    return math.cos(rad_ang), -math.sin(rad_ang)

def dist(p,q):
    """
    return distance between two points
    """
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def group_collide(sprite_group, other_object):
    """
    Check is a sprite collides with a sprite in a group of sprites
    """
    sprites = set(sprite_group)
    for sprite in sprites:
        if sprite.collide(other_object):
            sprite_group.remove(sprite)
            sprite.delete()
            return True
    return False

def group_group_collide(sprite_group, o_sprite_group):
    """
    Check if sprites in two groups collide
    """
    sprites = set(sprite_group)
    for sprite in sprites:
        if group_collide(o_sprite_group, sprite):
            sprite_group.remove(sprite)
            sprite.delete()
            return True
    return False

def random_position(width, height):
    """
    Generate a random set of coordinates
    """
    x = random.randrange(0, width)
    y = random.randrange(0, height)
    return x,y

def center_image_anchor(image):
    """
    Center anchors for pyglet images
    """
    image.anchor_x = image.height/2
    image.anchor_y = image.height/2

def center_image_grid_anchors(image_grid):
    """
    Center anchors for images in image grid
    """
    for image in image_grid:
        center_image_anchor(image)

def circular_movement(sprite, width, height):
    """
    Allows sprite to leave one side of the screen and return on the other side
    """
    sprite.x = sprite.x % width
    sprite.y = sprite.y % height
