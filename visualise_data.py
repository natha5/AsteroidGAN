import pygame
import numpy as np
import pandas as pd
from pygame.locals import *

import asteroid_gan


# create screen simply showing asteroid

def determine_color(albedo):
    color_level = albedo / 10
    print(color_level)

    color_level = round(color_level)

    print(color_level)

    color = ()

    match color_level:
        case 0, 1:
            color = (220, 220, 200)
        case 2:
            color = (211, 211, 211)
        case 3:
            color = (192, 192, 192)
        case 4:
            color = (169, 169, 169)
        case 5:
            color = (128, 128, 128)
        case 6:
            color = (105, 105, 105)
        case 7:
            color = (119, 136, 153)
        case 8:
            color = (112, 128, 144)
        case 9:
            color = (47, 79, 79)
        case 10:
            color = (0, 0, 0)

    return color


def determine_dimensions(diameter):
    if diameter >= 400:  # objects become spherical when diameter >= 400km
        return (0,0,diameter, diameter)
    else:
        return (0,0,diameter / 10, (diameter / 2) / 10)


def draw_asteroid(values_dict):
    color = determine_color(values_dict.get('albedo'))
    dimensions = determine_dimensions(values_dict.get('diameter'))

    pygame.draw.ellipse(surface=screen, color=color, rect=dimensions)


values = asteroid_gan.run_program()

values *= 255

print(values)
print(values.shape)

values = values.reshape(16,1)
values = values.flatten()

print(values)
print(values.shape)

values = np.around(values, decimals=2)

print(values)

keys = ["neo", "pha", "H", "diameter", "albedo",  "e", "a", "q", "i", "om", "w", "ad", "n", "tp_cal", "per", "moid"]

values_dict = {}

for i in range(16):
    values_dict[keys[i]] = values[i]

print(values_dict)

pygame.init()

# handle import of gan output here

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))

bg_img = pygame.image.load("resources/stars-sky-night.jpg")
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_WIDTH))

running = True
while running:
    screen.blit(bg_img, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    draw_asteroid(values_dict)
    pygame.display.update()
pygame.quit()
