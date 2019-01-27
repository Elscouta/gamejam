import functools
import os
from itertools import product

import pygame as pg
from pygame import time

from pygame.color import Color
from pygame.constants import SRCALPHA, BLEND_RGBA_MULT
from pygame.mixer import SoundType
from pygame.surface import Surface

import asset
from config import TILE_WIDTH, TILE_HEIGHT, PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_HEIGHT, PLAYER_WIDTH, \
    PLAYER_FRAME_ROTATION, PAINT_POWER
from game_screen import map, lighting
from game_screen.lighting import draw_light_source

PLAYER_FRAME_LENGTH = PLAYER_FRAME_ROTATION // 3


class _state:
    x = None
    y = None
    current_horizontal_cycle = None
    current_paint_cycle = None
    image = None
    remaining_millipixels = 0
    last_tick = None
    current_dir = 0
    paint_level = None
    paint_color = None



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

    return not any(any(t.is_collision(rel_x - dx, rel_y - dy)
                       for t in map.get_tile(x + dx, y + dy))
                   for (dx, dy) in product({0, TILE_WIDTH}, {0, TILE_HEIGHT}))


def draw_footstep(sprite):
    @functools.lru_cache(maxsize=None)
    def get_rotated(sprite, cd):
        return pg.transform.rotate(sprite, cd)

    rotated_sprite = get_rotated(sprite, _state.current_dir)
    rect = rotated_sprite.get_rect()

    if _state.paint_level < 1000:
        alpha_mask = Surface((rotated_sprite.get_width(), rotated_sprite.get_height()), flags=SRCALPHA)
        alpha_mask.fill(Color(255, 255, 255, int(255*_state.paint_level/1000)))
        rotated_sprite = rotated_sprite.copy()
        rotated_sprite.blit(alpha_mask, (0, 0), special_flags=BLEND_RGBA_MULT)

    map.map_surface.blit(rotated_sprite, (_state.x - rect.x // 2,
                                          _state.y + PLAYER_HEIGHT // 2 - rect.y // 2))




FOOTPRINTS = {
    'blue': (asset.BFOOTPRINT_LEFT, asset.BFOOTPRINT_RIGHT),
    'orange': (asset.OFOOTPRINT_LEFT, asset.OFOOTPRINT_RIGHT),
    'green': (asset.GFOOTPRINT_LEFT, asset.GFOOTPRINT_RIGHT)
}

def increment_cycles():
    _state.current_horizontal_cycle = (_state.current_horizontal_cycle + 1) % PLAYER_FRAME_ROTATION
    _state.current_paint_cycle = (_state.current_paint_cycle + 1) % (24 * 2)
    _state.paint_level = max(_state.paint_level - 1, 0)
    if _state.paint_level:
        fleft, fright = FOOTPRINTS[_state.paint_color]
        if _state.current_paint_cycle == 0:
            draw_footstep(asset.get_sprite(fleft))
        if _state.current_paint_cycle == 24:
            draw_footstep(asset.get_sprite(fright))


def add_paint(color):
    _state.paint_level = PAINT_POWER
    _state.paint_color = color


def handle_keys():
    key = pg.key.get_pressed()
    dist = 1

    new_tick = time.get_ticks()
    tick_since_last = new_tick - _state.last_tick
    _state.last_tick = new_tick

    millipixels = (tick_since_last * PLAYER_SPEED) + _state.remaining_millipixels
    pixel_moves = millipixels // 1000
    _state.remaining_millipixels = millipixels % 1000

    for _ in range(0, pixel_moves):
        new_x = _state.x
        new_y = _state.y
        moving = False

        if key[pg.K_DOWN]:
            new_y = new_y + dist
            _state.image = asset.get_player_sprites()[0][_state.current_horizontal_cycle // PLAYER_FRAME_LENGTH]
            moving = True
            y_axis = -1
        elif key[pg.K_UP]:
            new_y = new_y - dist
            _state.image = asset.get_player_sprites()[3][_state.current_horizontal_cycle // PLAYER_FRAME_LENGTH]
            moving = True
            y_axis = 1
        else:
            y_axis = 0

        if _valid_position(new_x, new_y):
            _state.x = new_x
            _state.y = new_y
        else:
            new_x = _state.x
            new_y = _state.y

        if key[pg.K_RIGHT]:
            new_x = new_x + dist
            _state.image = asset.get_player_sprites()[2][_state.current_horizontal_cycle // PLAYER_FRAME_LENGTH]
            moving = True
            x_axis = 1
        elif key[pg.K_LEFT]:
            new_x = new_x - dist
            moving = True
            _state.image = asset.get_player_sprites()[1][_state.current_horizontal_cycle // PLAYER_FRAME_LENGTH]
            x_axis = -1
        else:
            x_axis = 0

        _state.current_dir = {
            (-1, 1): 45,
            (-1, 0): 90,
            (-1, -1): 135,
            (0, -1): 180,
            (1, -1): 225,
            (1, 0): 270,
            (1, 1): 315,
            (0, 1): 360,
            (0, 0): 0
        }[x_axis, y_axis]

        if _valid_position(new_x, new_y):
            _state.x = new_x
            _state.y = new_y

        if moving:
            increment_cycles()
            pg.mixer.Channel(1).play(footstep_sound)


def get_x():
    return _state.x


def get_y():
    return _state.y


def get_pos():
    return _state.x, _state.y


def init():
    global footstep_sound
    footstep_sound = pg.mixer.Sound(os.path.join('assets', 'sfx_footsteps.wav'))
    footstep_sound.set_volume(0.02)
    _state.x, _state.y = map.initial_room.get_initial_position()
    _state.last_tick = time.get_ticks()
    _state.current_horizontal_cycle = 0
    _state.current_paint_cycle = 0
    _state.image = asset.get_player_sprites()[0][0]
    _state.paint_level = 0
