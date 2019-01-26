import pygame as pg
import sys

from pygame.locals import *

import asset
import monsters
import map
from config import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_SPEED
import player
import events

pg.init()

screen: pg.Surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pg.display.set_caption("Popo")

# all_sprites = pg.sprite.Group()
asset.init()

events.init()
player.init()
map.init()
map.print()
monsters.init()

# all_sprites.add(player)
clock = pg.time.Clock()


while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

        if event.type == USEREVENT:
            events.tick()

    screen.fill((0, 0, 0))

    player.handle_keys()

    # Draw stuff
    map.draw(screen, player.get_x(), player.get_y())
    player.draw(screen)
    monsters.draw_all(screen)

    pg.display.update()
    clock.tick(60)
    fps = clock.get_fps()
    if fps > 0:
        PLAYER_SPEED = PLAYER_SPEED * (60 / fps)
        pg.display.set_caption(f"FPS: {clock.get_fps()}, player speed : {PLAYER_SPEED}")
