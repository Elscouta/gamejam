import os
from random import randint
from typing import Optional

import pygame as pg

from events import schedule_event, clear_event
from screen import Screen, ScreenType


class TitleScreen(Screen):
    def __init__(self):
        self.font = pg.font.Font(os.path.join('assets', 'ButterflyKids-Regular.ttf'), 70)
        self.red = 255
        self.green = 215
        self.blue = 185
        self.update_event = schedule_event(self.update_colors, 1, oneshot=False)

    def update_colors(self):
        self.red -= randint(0, 20)
        if self.red <= 5:
            self.red = 255
        self.green -= randint(0, 20)
        if self.green <= 5:
            self.green = 255
        self.blue -= randint(0, 20)
        if self.blue <= 5:
            self.blue = 255

    def cleanup(self):
        clear_event(self.update_event)

    def draw(self, screen: pg.Surface, clock: pg.time.Clock) -> Optional[ScreenType]:
        surface = self.font.render('A Loo In the Dark', False, (self.red, self.green, self.blue))
        text_rec = surface.get_rect(center=(screen.get_size()[0] // 2, screen.get_size()[1] // 2))
        screen.blit(surface, text_rec)

        return None
