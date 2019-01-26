import os
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
        self.x = 15
        self.y = 15

    def draw(self):
        self.surface.blit(self.image, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    def valid_position(self, x, y):
        if map.get_tile(x, y).is_collision(x % TILE_WIDTH, y % TILE_HEIGHT):
            return False

        if map.get_tile(x+TILE_WIDTH, y).is_collision(x % TILE_WIDTH, y % TILE_HEIGHT):
            return False

        if map.get_tile(x, y+TILE_HEIGHT).is_collision(x % TILE_WIDTH, y % TILE_HEIGHT):
            return False

        if map.get_tile(x+TILE_WIDTH, y+TILE_HEIGHT).is_collision(x % TILE_WIDTH, y % TILE_HEIGHT):
            return False

        return True

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

