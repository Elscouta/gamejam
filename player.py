import os
from itertools import product

import map

import pygame as pg

from config import TILE_WIDTH, TILE_HEIGHT, PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT
from utils import sprite_sheet


class Player(pg.sprite.Sprite):

    def __init__(self, surface: pg.Surface):
        super().__init__()
        self.surface = surface
        self.current_horizontal_cycle = 0
        self.sprites = sprite_sheet(os.path.join('assets', 'children.png'), (48, 48))
        self.image = self.sprites[0][0]
        self.x = 75
        self.y = 75

    def draw(self):
        self.surface.blit(self.image, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    def valid_position(self, x, y):
        rel_x = x % TILE_WIDTH
        rel_y = y % TILE_HEIGHT

        return not any(map.get_tile(x+dx, y+dy).is_collision(rel_x-dx, rel_y-dy)
                       for (dx, dy) in product({0, TILE_WIDTH}, {0, TILE_HEIGHT}))

    def increment_cycle(self):
        self.current_horizontal_cycle += 1
        if self.current_horizontal_cycle == 3:
            self.current_horizontal_cycle = 0

    def handle_keys(self):
        key = pg.key.get_pressed()
        dist = 1

        for _ in range(0, PLAYER_SPEED):
            new_x = self.x
            new_y = self.y

            if key[pg.K_DOWN]:
                new_y = self.y + dist
                self.image = self.sprites[0][self.current_horizontal_cycle]
                self.increment_cycle()
            elif key[pg.K_UP]:
                new_y = self.y - dist
                self.image = self.sprites[3][self.current_horizontal_cycle]
                self.increment_cycle()
            if key[pg.K_RIGHT]:
                new_x = self.x + dist
                self.image = self.sprites[2][self.current_horizontal_cycle]
                self.increment_cycle()
            elif key[pg.K_LEFT]:
                new_x = self.x - dist
                self.image = self.sprites[1][self.current_horizontal_cycle]
                self.increment_cycle()

            if self.valid_position(new_x, new_y):
                self.x = new_x
                self.y = new_y

