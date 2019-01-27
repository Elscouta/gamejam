import os
from random import randint
from typing import Optional

import pygame as pg

from events import schedule_event, clear_event
from screen import Screen, ScreenType


class TitleScreen(Screen):
    def __init__(self):
        self.font = pg.font.Font(os.path.join('assets', 'ButterflyKids-Regular.ttf'), 70)
        self.small_font = pg.font.Font(os.path.join('assets', 'ButterflyKids-Regular.ttf'), 35)
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
        main_text = self.font.render('A Loo In the Dark', False, (self.red, self.green, self.blue))
        main_text_rec = main_text.get_rect(center=(screen.get_size()[0] // 2, screen.get_size()[1] // 2))
        screen.blit(main_text, main_text_rec)
        creator_text = self.small_font.render('A JJ/RB/JJ Game', False, (255, 255, 255))
        creator_text_rec = creator_text.get_rect(center=(screen.get_size()[0] // 2, screen.get_size()[1] // 2 + 70))
        screen.blit(creator_text, creator_text_rec)

        return None
