import os

import pygame as pg

from config import SCREEN_HEIGHT
from screen import Screen


class EndScreen(Screen):
    def __init__(self):
        self.scene: pg.Surface = pg.image.load(os.path.join('assets', 'bathroom_scene.png'))
        self.rect = pg.rect.Rect(0, SCREEN_HEIGHT - self.scene.get_size()[1], self.scene.get_size()[0], SCREEN_HEIGHT)

    def draw(self, screen: pg.Surface, clock: pg.time.Clock) -> bool:
        screen.blit(self.scene, self.rect)
        return False
