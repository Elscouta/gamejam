import os
from itertools import product

import lightning
import map

import pygame as pg

from asset import get_light_halo
from config import TILE_WIDTH, TILE_HEIGHT, PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_HEIGHT, PLAYER_WIDTH
from utils import sprite_sheet


class _state:
    x = None
    y = None
    current_horizontal_cycle = None
    image = None

sprites = None


def draw(screen):
    player_x = SCREEN_WIDTH / 2
    player_y = SCREEN_HEIGHT / 2
    screen.blit(_state.image, (player_x, player_y))
    screen.blit(get_light_halo(lightning.lightning_radius),
                     lightning.get_player_light_area(player_x, player_y))

def _valid_position(x, y):
    rel_x = x % TILE_WIDTH
    rel_y = y % TILE_HEIGHT

    return not any(map.get_tile(x+dx, y+dy).is_collision(rel_x-dx, rel_y-dy)
                   for (dx, dy) in product({0, TILE_WIDTH}, {0, TILE_HEIGHT}))


def increment_cycle(update_cycle: bool):
    if update_cycle:
        _state.current_horizontal_cycle += 1
        if _state.current_horizontal_cycle == 3:
            _state.current_horizontal_cycle = 0
        return False
    return True


def handle_keys():
    key = pg.key.get_pressed()
    dist = 1

    update_cycle = True

    for _ in range(0, PLAYER_SPEED):
        new_x = _state.x
        new_y = _state.y

        if key[pg.K_DOWN]:
            new_y = new_y + dist
            _state.image = sprites[0][_state.current_horizontal_cycle]
        elif key[pg.K_UP]:
            new_y = new_y - dist
            _state.image = sprites[3][_state.current_horizontal_cycle]
        if key[pg.K_RIGHT]:
            new_x = new_x + dist
            _state.image = sprites[2][_state.current_horizontal_cycle]
        elif key[pg.K_LEFT]:
            new_x = new_x - dist
            _state.image = sprites[1][_state.current_horizontal_cycle]

        update_cycle = increment_cycle(update_cycle)

        if _valid_position(new_x, new_y):
            _state.x = new_x
            _state.y = new_y


def get_x():
    return _state.x


def get_y():
    return _state.y


def init():
    global sprites
    _state.x = 75
    _state.y = 75
    sprites = sprite_sheet(os.path.join('assets', 'children.png'), (48, 48))
    _state.current_horizontal_cycle = 0
    _state.image = sprites[0][0]
