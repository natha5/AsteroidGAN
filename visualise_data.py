import pygame
import numpy as np
import pandas as pd
from pygame.locals import *

pygame.init()

# handle import of gan output here

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))

values = {
    "neo": 0,
    "pha": 0,
    "H": 0.013,
    "diameter": 3.68,
    "albedo": 0.000353,
    "e": 0.0003,
    "a": 0.0108,
    "q": 0.010034,
    "i": 0.414,
    "om": 0.315,
    "w": 0.2886,
    "ad": 0.0117,
    "n": 0.000839,
    "tp_cal": 79138.937500,
    "per": 6.600572,
    "moid": 0.006
}

bg_img = pygame.image.load("resources/stars-sky-night.jpg")
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_WIDTH))


# create screen simply showing asteroid

def determine_color(albedo):
    color_level = albedo * 10000
    color_level = round(color_level)
    match color_level:
        case 0,1:
            color = (220,220,200)
        case 2:
            color = (211,211,211)
        case 3:
            color = (192,192,192)
        case 4:
            color = (169,169,169)
        case 5:
            color = (128,128,128)
        case 6:
            color = (105,105,105)
        case 7:
            color = (119,136,153)
        case 8:
            color = (112,128,144)
        case 9:
            color = (47,79,79)
        case 10:
            color = (0,0,0)

    return color


def determine_dimensions(diameter):
    adjusted_diameter = diameter * 1000
    if diameter >= 400:  # objects become spherical when diameter >= 400km
        return diameter/10, diameter/10
    else:
        return diameter/10, (diameter/2)/10


def draw_asteroid(values):
    color = determine_color(values.get('albedo'))
    dimensions = determine_dimensions(values.get('diameter'))

    pygame.draw.ellipse(surface=screen, color=color, rect=dimensions)


running = True
while running:
    screen.blit(bg_img, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    draw_asteroid(values)
    pygame.display.update()
pygame.quit()
