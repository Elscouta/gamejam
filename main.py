import os
import sys

import pygame as pg
from pygame.locals import *

import events
from config import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_SPEED
from end_screen.end_screen import EndScreen
from game_screen.game_screen import GameScreen
from screen import Screen
from title_screen.title_screen import TitleScreen


def get_next_screen(current_displayed_screen: Screen) -> Screen:
    if not current_displayed_screen:
        return TitleScreen()
    if type(current_displayed_screen) is TitleScreen:
        return GameScreen()
    if type(current_displayed_screen) is GameScreen:
        return EndScreen()


pg.init()

pg.mixer_music.load(os.path.join('assets', 'music.ogg'))
# pg.mixer_music.play(-1)
pg.mixer_music.set_volume(0.1)

currentDisplayScreen: Screen = None

screen: pg.Surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#, FULLSCREEN)

pg.display.set_caption("A loo in the dark!")

events.init()

clock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pg.quit()
            sys.exit()
        if type(currentDisplayScreen) == TitleScreen and event.type == KEYDOWN and event.key == K_RETURN:
            currentDisplayScreen = get_next_screen(currentDisplayScreen)

        if event.type == USEREVENT:
            events.tick()

    screen.fill((0, 0, 0))

    if not currentDisplayScreen or currentDisplayScreen.draw(screen, clock, PLAYER_SPEED):
        currentDisplayScreen = get_next_screen(currentDisplayScreen)

    pg.display.update()
