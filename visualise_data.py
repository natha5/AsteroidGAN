import pygame
from pygame.locals import *
pygame.init()

# handle import of gan output here

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_WIDTH))


values = {
    "neo" : 0,
    "pha" : 0,
    "H" : 0.013,
    "diameter" : 3.68,
    "albedo" : 0.000353,
    "e" : 0.0003,
    "a" : 0.0108,
    "q" : 0.010034,
    "i" : 0.414,
    "om" : 0.315,
    "w" : 0.2886,
    "ad" : 0.0117,
    "n" : 0.000839,
    "tp_cal" : 79138.937500,
    "per" : 6.600572,
    "moid" : 0.006
}


bg_img = pygame.image.load("resources/stars-sky-night.jpg")
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH,SCREEN_WIDTH))

running = True
while running:
    screen.blit(bg_img,(0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    pygame.display.update()
pygame.quit()
