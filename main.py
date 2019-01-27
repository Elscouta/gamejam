import os
import sys

import pygame as pg
from pygame.locals import *

import asset
import events
from config import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_SPEED
from defeat_screen.defeat_screen import DefeatScreen
from victory_screen.end_screen import EndScreen
from screen import Screen
from title_screen.title_screen import TitleScreen

pg.init()

pg.mixer_music.load(os.path.join('assets', 'music.ogg'))
# pg.mixer_music.play(-1)
pg.mixer_music.set_volume(0.1)

currentDisplayScreen: Screen = EndScreen()

screen: pg.Surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)

pg.display.set_caption("A loo in the dark!")

events.init()
asset.init()

clock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pg.quit()
            sys.exit()
        if type(currentDisplayScreen) == TitleScreen and event.type == KEYDOWN and event.key == K_RETURN:
            currentDisplayScreen = DefeatScreen()

        if event.type == USEREVENT:
            events.tick()

    screen.fill((0, 0, 0))

    screenChange = currentDisplayScreen.draw(screen, clock)
    if screenChange:
        currentDisplayScreen = screenChange()

    pg.display.update()
