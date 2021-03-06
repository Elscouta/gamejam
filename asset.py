import functools
import os

import pygame as pg
from pygame import transform

from config import TILE_WIDTH, TILE_HEIGHT
from utils import sprite_sheet

MAP_TILESHEET = 0
LIGHT_TILESHEET = 1
FURNITURE_TILESHEET = 2
OHNOES_TILESHEET = 3
BUBBLE_TILESHEET = 4
PAINT_TILESHEET = 5
FOOTPRINT_TILESHEET = 6

NW_CORNER = (MAP_TILESHEET, 0, 0)
N_WALL = (MAP_TILESHEET, 0, 1)
N_DOOR = (MAP_TILESHEET, 5, 1)
N_DOORWAY = (MAP_TILESHEET, 5, 0)
NE_CORNER = (MAP_TILESHEET, 0, 2)
W_WALL = (MAP_TILESHEET, 1, 0)
W_DOOR = (MAP_TILESHEET, 7, 1)
W_DOORWAY = (MAP_TILESHEET, 7, 0)
FLOOR = (MAP_TILESHEET, 1, 1)
E_WALL = (MAP_TILESHEET, 1, 2)
E_DOOR = (MAP_TILESHEET, 8, 1)
E_DOORWAY = (MAP_TILESHEET, 8, 0)
SW_CORNER = (MAP_TILESHEET, 2, 0)
S_WALL = (MAP_TILESHEET, 2, 1)
S_DOOR = (MAP_TILESHEET, 6, 1)
S_DOORWAY = (MAP_TILESHEET, 6, 0)
SE_CORNER = (MAP_TILESHEET, 2, 2)
PORCELAIN_NW_CORNER = (MAP_TILESHEET, 0, 3)
PORCELAIN_N_WALL = (MAP_TILESHEET, 0, 4)
PORCELAIN_N_DOOR = (MAP_TILESHEET, 5, 3)
PORCELAIN_N_DOORWAY = (MAP_TILESHEET, 5, 2)
PORCELAIN_NE_CORNER = (MAP_TILESHEET, 0, 5)
PORCELAIN_W_WALL = (MAP_TILESHEET, 1, 3)
PORCELAIN_W_DOOR = (MAP_TILESHEET, 7, 3)
PORCELAIN_W_DOORWAY = (MAP_TILESHEET, 7, 2)
PORCELAIN_FLOOR = (MAP_TILESHEET, 1, 4)
PORCELAIN_E_WALL = (MAP_TILESHEET, 1, 5)
PORCELAIN_E_DOOR = (MAP_TILESHEET, 8, 3)
PORCELAIN_E_DOORWAY = (MAP_TILESHEET, 8, 2)
PORCELAIN_SW_CORNER = (MAP_TILESHEET, 2, 3)
PORCELAIN_S_WALL = (MAP_TILESHEET, 2, 4)
PORCELAIN_S_DOOR = (MAP_TILESHEET, 6, 3)
PORCELAIN_S_DOORWAY = (MAP_TILESHEET, 6, 2)
PORCELAIN_SE_CORNER = (MAP_TILESHEET, 2, 5)
HALO = (LIGHT_TILESHEET, 0, 0)
SHADOW = (LIGHT_TILESHEET, 0, 1)
WARNING = (MAP_TILESHEET, 3, 0)
BEDSIDE_LAMP = (FURNITURE_TILESHEET, 4, 3)
BED_TOP = (FURNITURE_TILESHEET, 4, 5)
BED_BOTTOM = (FURNITURE_TILESHEET, 5, 5)
OHNOES1 = (OHNOES_TILESHEET, 0, 0)
OHNOES2 = (OHNOES_TILESHEET, 0, 1)
BUBBLE_OO = (BUBBLE_TILESHEET, 0, 0)
BUBBLE_OF = (BUBBLE_TILESHEET, 0, 1)
BUBBLE_FO = (BUBBLE_TILESHEET, 0, 2)
BUBBLE_FF = (BUBBLE_TILESHEET, 0, 3)
BURGER = (BUBBLE_TILESHEET, 0, 4)
BPAINT_NW = (PAINT_TILESHEET, 2, 0)
BPAINT_NE = (PAINT_TILESHEET, 2, 1)
BPAINT_SW = (PAINT_TILESHEET, 3, 0)
BPAINT_SE = (PAINT_TILESHEET, 3, 1)
BFOOTPRINT_LEFT = (FOOTPRINT_TILESHEET, 0, 0)
BFOOTPRINT_RIGHT = (FOOTPRINT_TILESHEET, 0, 1)
OPAINT_NW = (PAINT_TILESHEET, 2, 2)
OPAINT_NE = (PAINT_TILESHEET, 2, 3)
OPAINT_SW = (PAINT_TILESHEET, 3, 2)
OPAINT_SE = (PAINT_TILESHEET, 3, 3)
OFOOTPRINT_LEFT = (FOOTPRINT_TILESHEET, 1, 0)
OFOOTPRINT_RIGHT = (FOOTPRINT_TILESHEET, 1, 1)
GPAINT_NW = (PAINT_TILESHEET, 4, 0)
GPAINT_NE = (PAINT_TILESHEET, 4, 1)
GPAINT_SW = (PAINT_TILESHEET, 5, 0)
GPAINT_SE = (PAINT_TILESHEET, 5, 1)
GFOOTPRINT_LEFT = (FOOTPRINT_TILESHEET, 2, 0)
GFOOTPRINT_RIGHT = (FOOTPRINT_TILESHEET, 2, 1)

_tilesheets = {}
_player_sprites = None


def _load_bubble_tilesheet():
    bubble_orig = pg.image.load(os.path.join('assets', 'speech_bubble.png')).convert_alpha()
    bubble_orig = pg.transform.scale(bubble_orig, (75, 50))
    bubble_rect = bubble_orig.get_rect()
    burger_orig = pg.image.load(os.path.join('assets', 'pixel_burger.png')).convert_alpha()

    return [[
        bubble_orig,
        pg.transform.flip(bubble_orig, False, True),
        pg.transform.flip(bubble_orig, True, False),
        pg.transform.flip(bubble_orig, True, True),
        pg.transform.scale(burger_orig, (int(bubble_rect.w / 2), int(bubble_rect.h / 2)))
    ]]


def init():
    global _player_sprites

    _tilesheets[MAP_TILESHEET] = sprite_sheet(os.path.join('assets', 'tilesetHouse.png'), (TILE_WIDTH, TILE_HEIGHT))
    _tilesheets[LIGHT_TILESHEET] = sprite_sheet(os.path.join('assets', 'halo.png'), (640, 640))
    _tilesheets[FURNITURE_TILESHEET] = sprite_sheet(os.path.join('assets', 'house_objects.png'), (TILE_WIDTH, TILE_HEIGHT))
    _tilesheets[OHNOES_TILESHEET] = sprite_sheet(os.path.join('assets', 'ohnoes.png'), (2*TILE_WIDTH, 2*TILE_HEIGHT))
    _tilesheets[PAINT_TILESHEET] = sprite_sheet(os.path.join('assets', 'ohnoes.png'), (TILE_WIDTH, TILE_HEIGHT))
    _tilesheets[BUBBLE_TILESHEET] = _load_bubble_tilesheet()
    _tilesheets[FOOTPRINT_TILESHEET] = sprite_sheet(os.path.join('assets', 'footprints.png'), (32, 32))
    _player_sprites = sprite_sheet(os.path.join('assets', 'children.png'), (48, 48))


def get_sprite(sprite_id):
    return _tilesheets[sprite_id[0]][sprite_id[1]][sprite_id[2]]


def get_player_sprites():
    return _player_sprites


@functools.lru_cache(maxsize=256)
def get_light_halo(radius):
    big_light_halo = get_sprite(HALO)
    return transform.scale(big_light_halo, (2 * radius, 2 * radius))


@functools.lru_cache(maxsize=256)
def get_shadow_halo(radius):
    big_shadow = get_sprite(SHADOW)
    return transform.scale(big_shadow, (2 * radius, 2 * radius))
