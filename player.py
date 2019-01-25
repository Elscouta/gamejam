import os

import pygame as pg

from utils import sprite_sheet


class Player(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.current_horizontal_cycle = 0
        self.sprites = sprite_sheet(os.path.join('assets', 'children.png'), (48, 48))
        self.image = self.sprites[0][0]
        self.x = 0
        self.y = 0

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def increment_cycle(self):
        self.current_horizontal_cycle += 1
        if self.current_horizontal_cycle == 3:
            self.current_horizontal_cycle = 0

    def handle_keys(self):
        key = pg.key.get_pressed()
        dist = 10

        if key[pg.K_DOWN]:
            self.y += dist
            self.image = self.sprites[0][self.current_horizontal_cycle]
            self.increment_cycle()
        elif key[pg.K_UP]:
            self.y -= dist
            self.image = self.sprites[3][self.current_horizontal_cycle]
            self.increment_cycle()
        if key[pg.K_RIGHT]:
            self.x += dist
            self.image = self.sprites[2][self.current_horizontal_cycle]
            self.increment_cycle()
        elif key[pg.K_LEFT]:
            self.x -= dist
            self.image = self.sprites[1][self.current_horizontal_cycle]
            self.increment_cycle()
