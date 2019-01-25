import pygame as pg
import os


class Player(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.image.load(os.path.join('assets', 'children.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
