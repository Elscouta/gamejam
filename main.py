import pygame as pg
import sys

from pygame.locals import *

import asset
import gamelogic
import map
from config import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_SPEED
import player
from threat_bubble import ThreatBubble

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

# threat_bubble = ThreatBubble((10, 50))

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    player.handle_keys()

    # Draw stuff
    map.draw(screen, player.get_x(), player.get_y())
    player.draw(screen)
    threat_bubble.draw(screen)

    pg.display.flip()
    gamelogic.tick()
    clock.tick(60)
    fps = clock.get_fps()
    if fps > 0:
        PLAYER_SPEED = PLAYER_SPEED * (60 / fps)
        pg.display.set_caption(f"FPS: {clock.get_fps()}, player speed : {PLAYER_SPEED}")
