import os
from typing import Tuple

import pygame as pg

from config import SCREEN_WIDTH, SCREEN_HEIGHT


class ThreatBubble(pg.sprite.Sprite):
    def __init__(self, monster_position: Tuple[int, int]):
        pg.sprite.Sprite.__init__(self)
        self.image: pg.Surface = None
        self.monster_position = monster_position
        self.orient_image(pg.image.load(os.path.join('assets', 'speech_bubble.png')).convert_alpha(), monster_position)
        self.rect = self.image.get_rect()
        self.burger: pg.Surface = pg.transform.scale(
            pg.image.load(os.path.join('assets', 'pixel_burger.png')).convert_alpha(),
            (int(self.rect.w / 2), int(self.rect.h / 2))
        )

    def orient_image(self, image, monster_position: Tuple[int, int]):
        if monster_position[0] > SCREEN_WIDTH / 2:
            self.image = pg.transform.flip(image, True, False)
        if monster_position[1] < SCREEN_HEIGHT / 2:
            self.image = pg.transform.flip(image, False, True)
        if self.image is None:
            self.image = image
        self.image = pg.transform.scale(self.image, (75, 50))

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, self.monster_position)
        screen.blit(self.burger, ((self.monster_position[0] + self.rect.w / 2) - ((self.burger.get_size()[0] / 2) - 5),
                                  (self.monster_position[1] + self.rect.h / 2) - (self.burger.get_size()[1] / 2)))
