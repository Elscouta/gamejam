import pygame as pg
import sys

from pygame.locals import *

from player import Player

pg.init()

screen = pg.display.set_mode((640, 480))

pg.display.set_caption("Popo")

# all_sprites = pg.sprite.Group()

player = Player()

# all_sprites.add(player)

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    player.handle_keys()
    player.draw(screen)

    pg.display.update()
    # all_sprites.draw(DISPLAYSURF)
