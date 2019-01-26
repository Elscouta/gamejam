import pygame as pg
import sys

from pygame.locals import *

import map
from player import Player

pg.init()

screen = pg.display.set_mode((640, 480))

pg.display.set_caption("Popo")

# all_sprites = pg.sprite.Group()

player = Player(screen)
map.create_map()
map.print_map()

# all_sprites.add(player)
clock = pg.time.Clock()


while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    player.handle_keys()
    player.draw()

    pg.display.update()
    clock.tick(60)
    pg.display.set_caption(str(clock.get_fps()))
    # all_sprites.draw(DISPLAYSURF)
