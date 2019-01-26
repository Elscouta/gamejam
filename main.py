import pygame as pg
import sys

from pygame.locals import *

import asset
import map
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pg.display.set_caption("Popo")

# all_sprites = pg.sprite.Group()
asset.init()

player = Player(screen)
map.init()
map.print()

# all_sprites.add(player)
clock = pg.time.Clock()


while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    player.handle_keys()
    map.draw(screen, player.x, player.y)
    player.draw()

    pg.display.update()
    clock.tick(60)
    pg.display.set_caption(str(clock.get_fps()))
    # all_sprites.draw(DISPLAYSURF)
