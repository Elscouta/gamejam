import pygame as pg
import sys

from pygame.locals import *

from player import Player

pg.init()

DISPLAYSURF = pg.display.set_mode((640, 480))

pg.display.set_caption("My First Game")

player = Player((0, 50))

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

    pg.display.update()
