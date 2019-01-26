import os
from itertools import product

import gamelogic
import map

import pygame as pg

from asset import get_light_halo
from config import TILE_WIDTH, TILE_HEIGHT, PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_HEIGHT, PLAYER_WIDTH
from utils import sprite_sheet


class Player(pg.sprite.Sprite):

    def __init__(self, screen: pg.Surface):
        super().__init__()
        self.screen = screen
        self.current_horizontal_cycle = 0
        self.sprites = sprite_sheet(os.path.join('assets', 'children.png'), (48, 48))
        self.image = self.sprites[0][0]
        self.x = 75
        self.y = 75

    def draw(self):
        player_x = SCREEN_WIDTH / 2
        player_y = SCREEN_HEIGHT / 2
        self.screen.blit(self.image, (player_x, player_y))
        self.screen.blit(get_light_halo(gamelogic.lightning_radius),
                         gamelogic.get_player_light_area(player_x, player_y))

    def valid_position(self, x, y):
        rel_x = x % TILE_WIDTH
        rel_y = y % TILE_HEIGHT

        return not any(map.get_tile(x+dx, y+dy).is_collision(rel_x-dx, rel_y-dy)
                       for (dx, dy) in product({0, TILE_WIDTH}, {0, TILE_HEIGHT}))

    def increment_cycle(self, update_cycle: bool):
        if update_cycle:
            self.current_horizontal_cycle += 1
            if self.current_horizontal_cycle == 3:
                self.current_horizontal_cycle = 0
            return False
        return True

    def handle_keys(self):
        key = pg.key.get_pressed()
        dist = 1

        update_cycle = True

        for _ in range(0, PLAYER_SPEED):
            new_x = self.x
            new_y = self.y

            if key[pg.K_DOWN]:
                new_y = self.y + dist
                self.image = self.sprites[0][self.current_horizontal_cycle]
            elif key[pg.K_UP]:
                new_y = self.y - dist
                self.image = self.sprites[3][self.current_horizontal_cycle]
            if key[pg.K_RIGHT]:
                new_x = self.x + dist
                self.image = self.sprites[2][self.current_horizontal_cycle]
            elif key[pg.K_LEFT]:
                new_x = self.x - dist
                self.image = self.sprites[1][self.current_horizontal_cycle]

            update_cycle = self.increment_cycle(update_cycle)

            if self.valid_position(new_x, new_y):
                self.x = new_x
                self.y = new_y

