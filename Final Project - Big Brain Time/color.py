# --------------------------------------------------------------------
# Program: Colours constants class
# Author: Alex Hyde
# Date: Nov 11 2019
# Description: Colour constants to be imported into any program.
# --------------------------------------------------------------------

import random

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 150)
LIGHT_BLUE = (80, 80, 255)
SKY_BLUE = (150, 150, 255)
LIGHT_RED = (255, 100, 100)
GREEN = (0, 255, 0)
PURPLE = (200, 0, 200)
LIGHT_GREEN = (200, 255, 200)
DARK_GREEN = (50, 150, 50)
DARKER_GREEN = (0, 50, 0)
YELLOW = (255, 255, 0)
THE_BLUE = (130, 220, 226)
DARK_GREY = (50, 50, 50)
GREY = (100, 100, 100)
LIGHT_GREY = (200, 200, 200)
MEDIUM_GREY = (150, 150, 150)
BROWN = (48, 29, 2)
LIGHT_BROWN = (60, 35, 4)
ORANGE = (255, 150, 0)
DARK_ORANGE = (200, 100, 0)
SKY = (130, 220, 226)


def random_any_color(start=0, stop=255):
    r = random.randrange(start, stop)
    g = random.randrange(start, stop)
    b = random.randrange(start, stop)
    return r, g, b


def random_color(start, stop, color, saturation=100):
    c = random.randrange(start, stop)
    return basic_color(c, color, saturation)


def basic_color(strength, color, saturation=100):
    c = strength
    dark = c * (1 - saturation / 100)
    if "r" in color:
        r = c
    else:
        r = dark
    if "g" in color:
        g = c
    else:
        g = dark
    if "b" in color:
        b = c
    else:
        b = dark
    return r, g, b


def grey(darkness):
    return darkness, darkness, darkness

