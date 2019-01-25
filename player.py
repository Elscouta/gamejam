import pygame as pg
import os

from utils import sprite_sheet


class Player(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        tmp = sprite_sheet(os.path.join('assets', 'children.png'), (45, 50))
        self.image = tmp[0]
        self.rect = self.image.get_rect(center=pos)
