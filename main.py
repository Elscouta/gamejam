import pygame as pg
import sys

from pygame.locals import *

from config import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_SPEED
import events
from game_screen.game_screen import GameScreen

pg.init()

screen: pg.Surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)

pg.display.set_caption("Popo")

events.init()

clock = pg.time.Clock()

currentScreen = GameScreen()

while True:
    for event in pg.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pg.quit()
            sys.exit()

        if event.type == USEREVENT:
            events.tick()

    screen.fill((0, 0, 0))

    if type(currentScreen) is GameScreen:
        currentScreen.draw(screen, clock, PLAYER_SPEED)
