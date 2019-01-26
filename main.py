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
        return GameScreen()
    if type(current_displayed_screen) is TitleScreen:
        return GameScreen()
    if type(current_displayed_screen) is GameScreen:
        return EndScreen()


pg.init()

currentDisplayScreen: Screen = None

screen: pg.Surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pg.display.set_caption("Poop for Glory!")

events.init()

clock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pg.quit()
            sys.exit()

        if event.type == USEREVENT:
            events.tick()

    screen.fill((0, 0, 0))

    if not currentDisplayScreen or currentDisplayScreen.draw(screen, clock, PLAYER_SPEED):
        currentDisplayScreen = get_next_screen(currentDisplayScreen)
