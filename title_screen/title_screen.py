import os

import pygame as pg
from pygame.constants import *

from screen import Screen
from random import randint

class TitleScreen(Screen):
    def __init__(self):
        self.font = pg.font.Font(os.path.join('assets', 'ButterflyKids-Regular.ttf'), 70)
        self.red = 255
        self.green = 255
        self.blue = 255

    def update_colors(self):
        self.red -= randint(0, 10)
        if self.red <= 5:
            self.red = 255
        self.green -= randint(0, 10)
        if self.green <= 5:
            self.green = 255
        self.blue -= randint(0, 10)
        if self.blue <= 5:
            self.blue = 255

    def draw(self, screen: pg.Surface, clock: pg.time.Clock, player_speed: int) -> bool:
        surface = self.font.render('Poop for Glory!', False, (self.red, self.green, self.blue))
        text_rec = surface.get_rect(center=(screen.get_size()[0] // 2, screen.get_size()[1] // 2))
        screen.blit(surface, text_rec)
        self.update_colors()

        return False
