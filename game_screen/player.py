import os
from itertools import product

from pygame import time
from pygame.mixer import SoundType

from game_screen import map, lighting

import pygame as pg

from config import TILE_WIDTH, TILE_HEIGHT, PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_HEIGHT, PLAYER_WIDTH, \
    PLAYER_FRAME_ROTATION
from game_screen.lighting import draw_light_source
from utils import sprite_sheet


PLAYER_FRAME_LENGTH = PLAYER_FRAME_ROTATION // 3


class _state:
    x = None
    y = None
    current_horizontal_cycle = None
    image = None
    remaining_millipixels = 0
    last_tick = None

sprites = None
footstep_sound: SoundType = None

def draw(screen, light_mask):
    player_screen_x = SCREEN_WIDTH / 2
    player_screen_y = SCREEN_HEIGHT / 2
    screen.blit(_state.image, (player_screen_x, player_screen_y))
    draw_light_source(light_mask, _state.x + PLAYER_WIDTH // 2,
                      _state.y + PLAYER_HEIGHT // 2, lighting.player_lightning_radius)


def _valid_position(x, y):
    rel_x = x % TILE_WIDTH
    rel_y = y % TILE_HEIGHT

    return not any(map.get_tile(x + dx, y + dy).is_collision(rel_x - dx, rel_y - dy)
                   for (dx, dy) in product({0, TILE_WIDTH}, {0, TILE_HEIGHT}))


def increment_cycle():
    _state.current_horizontal_cycle = (_state.current_horizontal_cycle + 1) % PLAYER_FRAME_ROTATION


def handle_keys():
    key = pg.key.get_pressed()
    dist = 1

    new_tick = time.get_ticks()
    tick_since_last = new_tick - _state.last_tick
    _state.last_tick = new_tick

    millipixels = (tick_since_last * PLAYER_SPEED) + _state.remaining_millipixels
    pixel_moves = millipixels // 1000
    _state.remaining_millipixels = pixel_moves % 1000


    for _ in range(0, pixel_moves):
        new_x = _state.x
        new_y = _state.y
        moving = False

        if key[pg.K_DOWN]:
            new_y = new_y + dist
            _state.image = sprites[0][_state.current_horizontal_cycle // PLAYER_FRAME_LENGTH]
            moving = True
        elif key[pg.K_UP]:
            new_y = new_y - dist
            _state.image = sprites[3][_state.current_horizontal_cycle // PLAYER_FRAME_LENGTH]
            moving = True

        if _valid_position(new_x, new_y):
            _state.x = new_x
            _state.y = new_y
        else:
            new_x = _state.x
            new_y = _state.y

        if key[pg.K_RIGHT]:
            new_x = new_x + dist
            _state.image = sprites[2][_state.current_horizontal_cycle // PLAYER_FRAME_LENGTH]
            moving = True
        elif key[pg.K_LEFT]:
            new_x = new_x - dist
            moving = True
            _state.image = sprites[1][_state.current_horizontal_cycle // PLAYER_FRAME_LENGTH]

        if _valid_position(new_x, new_y):
            _state.x = new_x
            _state.y = new_y

        if moving:
            increment_cycle()
            pg.mixer.Channel(1).play(footstep_sound)


def get_x():
    return _state.x


def get_y():
    return _state.y


def get_pos():
    return _state.x, _state.y


def init():
    global sprites
    global footstep_sound
    footstep_sound = pg.mixer.Sound(os.path.join('assets', 'sfx_footsteps.wav'))
    footstep_sound.set_volume(0.02)
    _state.x, _state.y = map.initial_room.get_initial_position()
    _state.last_tick = time.get_ticks()

    sprites = sprite_sheet(os.path.join('assets', 'children.png'), (48, 48))
    _state.current_horizontal_cycle = 0
    _state.image = sprites[0][0]
