import os
import sys

import pygame as pg
from pygame.constants import DOUBLEBUF
from pygame.locals import *

import asset
import events
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from game_screen.game_screen import GameScreen
from victory_screen.end_screen import EndScreen
from screen import Screen
from title_screen.title_screen import TitleScreen

pg.init()

pg.mouse.set_visible(False)

pg.mixer_music.load(os.path.join('assets', 'music.ogg'))
pg.mixer_music.play(-1)
pg.mixer_music.set_volume(1)

screen: pg.Surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)

events.init()
asset.init()

pg.display.set_caption("A loo in the dark!")

currentDisplayScreen: Screen = TitleScreen()

clock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pg.quit()
            sys.exit()
        if (type(currentDisplayScreen) == TitleScreen or type(currentDisplayScreen) == EndScreen) \
                and event.type == KEYDOWN and event.key == K_RETURN:
            currentDisplayScreen = GameScreen()

        if event.type == USEREVENT:
            events.tick()

    screen.fill((0, 0, 0))

    screenChange = currentDisplayScreen.draw(screen, clock)
    if screenChange:
        currentDisplayScreen = screenChange()

    pg.display.flip()
