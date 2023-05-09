import pygame
import numpy as np
import pandas as pd
from pygame.locals import *

import asteroid_gan

sun_diameter = 1400000  # suns diameter is 1.4 million km
earth_diameter = 12742  # earths diameter is 12742 km


def calculate_scaling(perihelion):
    perihelion = int(round(perihelion))
    if perihelion > 30:
        scale = 20
    else:
        scale = 30
    return scale


def km_to_au(km):
    # 1km = 6.685*10-9 au
    au = km * (6.685E-9)
    return au


def determine_color(albedo):
    color_level = albedo / 10

    color_level = round(color_level)

    color = ()

    match color_level:
        case 0:
            color = (220, 220, 200)
            return color
        case 1:
            color = (220, 220, 200)
            return color
        case 2:
            color = (211, 211, 211)
            return color
        case 3:
            color = (192, 192, 192)
            return color
        case 4:
            color = (169, 169, 169)
            return color
        case 5:
            color = (128, 128, 128)
            return color
        case 6:
            color = (105, 105, 105)
            return color
        case 7:
            color = (119, 136, 153)
            return color
        case 8:
            color = (112, 128, 144)
            return color
        case 9:
            color = (47, 79, 79)
            return color
        case 10:
            color = (0, 0, 0)
            return color


def determine_dimensions(diameter):
    diameter = int(round(diameter)) * 10
    half_diameter = diameter / 2

    if diameter >= 400:  # objects become spherical when diameter >= 400km
        return WIDTH_CENTRE - half_diameter, HEIGHT_CENTRE - half_diameter, WIDTH_CENTRE + half_diameter, HEIGHT_CENTRE + half_diameter
    else:
        print(WIDTH_CENTRE - half_diameter, HEIGHT_CENTRE - diameter / 4)
        print(WIDTH_CENTRE + half_diameter, HEIGHT_CENTRE + diameter / 4)
        return (WIDTH_CENTRE - half_diameter, HEIGHT_CENTRE - diameter / 4, diameter, half_diameter)


def draw_asteroid(values_dict):
    color = determine_color(values_dict.get('albedo'))
    dimensions = determine_dimensions(values_dict.get('diameter'))

    target_rect = pygame.Rect(dimensions)
    shape_surface = pygame.Surface(target_rect.size, pygame.SRCALPHA)

    pygame.draw.ellipse(surface=shape_surface, color=color, rect=(0, 0, *target_rect.size))
    rotated_surface = pygame.transform.rotate(shape_surface, values_dict.get('e'))
    screen.blit(rotated_surface, rotated_surface.get_rect(center=target_rect.center))


def draw_sun(scale):
    diameter = km_to_au(sun_diameter)
    pygame.draw.ellipse(surface=screen, color=pygame.Color('orange'),
                        rect=(SCREEN_WIDTH / 2 - diameter * scale / 2, SCREEN_HEIGHT / 2 - diameter * scale / 2,
                              diameter * scale, diameter * scale))


def draw_asteroid_orbit(diameter, q, a, e, scale):
    # q is perihelion
    # a is semi-major axis
    # e is eccentricity

    perihelion = q * scale
    semi_major = a * scale

    # if semi major > perihelion, swap them over (improves viewing as screen is wider than it is tall)
    if semi_major > perihelion:
        old_perihelion = perihelion
        perihelion = semi_major
        semi_major = old_perihelion

    au_diameter = km_to_au(int(round(diameter)))

    pygame.draw.ellipse(surface=screen, color=pygame.Color('gray'),
                        rect=(
                        SCREEN_WIDTH / 2 - perihelion / 2, SCREEN_HEIGHT / 2 - semi_major / 2, perihelion, semi_major),
                        width=1)
    pygame.draw.ellipse(surface=screen, color=pygame.Color('gray'), rect=(
    SCREEN_WIDTH / 2 - au_diameter * scale, SCREEN_HEIGHT / 2 - au_diameter * scale, au_diameter * scale,
    au_diameter * scale))


def draw_earth(scale):
    # earths orbit
    diameter = km_to_au(earth_diameter)
    pygame.draw.ellipse(surface=screen, color=pygame.Color('blue'),
                        rect=(SCREEN_WIDTH / 2 - scale / 2, SCREEN_HEIGHT / 2 - scale / 2, scale, scale), width=1)
    # earth itself
    pygame.draw.ellipse(surface=screen, color=pygame.Color('blue'), rect=(
    SCREEN_WIDTH / 2 - diameter * scale, SCREEN_HEIGHT / 2 - diameter * scale, diameter * scale, diameter * scale))


# following function taken from Mangs, 2022 (https://devpress.csdn.net/python/63045a4a7e6682346619a614.html)
def blit_text(surface, text, pos, font, color=pygame.Color('yellow')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def visualise_orbit():
    screen.fill((0, 0, 0))
    to_asteroid_button_text = font.render('view asteroid', True, pygame.Color('yellow'))

    scale = calculate_scaling(values_dict.get('q'))

    screen.blit(bg_img, (0, 0))

    orbit = True
    while orbit:
        mouse = pygame.mouse.get_pos()

        draw_sun(scale)
        draw_earth(scale)
        draw_asteroid_orbit(values_dict.get('diameter'), values_dict.get('q'), values_dict.get('a'),
                            values_dict.get('e'), scale)

        screen.blit(to_asteroid_button_text, (9 * SCREEN_WIDTH / 10, 9 * SCREEN_HEIGHT / 10))

        blit_text(screen, text, (20, 20), font)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                orbit = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (9 * SCREEN_WIDTH / 10) <= mouse[0] <= (9 * SCREEN_WIDTH / 10) + 140 and (9 * SCREEN_HEIGHT / 10) <= \
                        mouse[1] <= (9 * SCREEN_HEIGHT / 10) + 40:
                    orbit = False


values = asteroid_gan.run_program()

values *= 255

values = values.reshape(16, 1)
values = values.flatten()
values = np.around(values, decimals=2)

keys = ["neo", "pha", "H", "diameter", "albedo", "e", "a", "q", "i", "om", "w", "ad", "n", "tp_cal", "per", "moid"]

values_dict = {}

for i in range(16):
    values_dict[keys[i]] = values[i]

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 680

WIDTH_CENTRE = SCREEN_WIDTH / 2
HEIGHT_CENTRE = SCREEN_HEIGHT / 2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('AsteroidGAN')

font = pygame.font.SysFont('timesnewroman', 20)

bg_img = pygame.image.load("resources/stars-sky-night.jpg")
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

text = 'Diameter : ' + str(values_dict.get('diameter')) + 'm' \
                                                          '\nAlbedo : ' + str(values_dict.get('albedo')) + \
       '\nAbsolute Magnitude Parameter : ' + str(values_dict.get('H')) + \
       '\nSemi-major axis : ' + str(values_dict.get('a')) + 'au' + \
       '\nPerihelion distance : ' + str(values_dict.get('q')) + 'au' + \
       '\nInclination : ' + str(values_dict.get('i')) + 'degrees' + \
       '\nEarth minimum orbit intersection distance : ' + str(values_dict.get('moid')) + 'au'

to_orbit_button_text = font.render('view orbit', True, pygame.Color('yellow'))

running = True
while running:
    mouse = pygame.mouse.get_pos()

    screen.blit(bg_img, (0, 0))

    draw_asteroid(values_dict)

    blit_text(screen, text, (20, 20), font)

    screen.blit(to_orbit_button_text, (9 * SCREEN_WIDTH / 10, 9 * SCREEN_HEIGHT / 10))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (9 * SCREEN_WIDTH / 10) <= mouse[0] <= (9 * SCREEN_WIDTH / 10) + 140 and (9 * SCREEN_HEIGHT / 10) <= \
                    mouse[1] <= (9 * SCREEN_HEIGHT / 10) + 40:
                visualise_orbit()

pygame.quit()
