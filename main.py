import pygame as pg
import sys

from pygame.locals import *

import asset
import gamelogic
import map
from config import SCREEN_HEIGHT, SCREEN_WIDTH
import player
from utils import display_text_bubble

pg.init()

screen: pg.Surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pg.display.set_caption("Popo")

# all_sprites = pg.sprite.Group()
asset.init()

player.init()
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
    map.draw(screen, player.get_x(), player.get_y())
    player.draw(screen)

    display_text_bubble(screen, None, (64, 56), (40, 40))

    pg.display.update()
    gamelogic.tick()
    clock.tick(60)
    pg.display.set_caption(str(clock.get_fps()))
    # all_sprites.draw(DISPLAYSURF)
