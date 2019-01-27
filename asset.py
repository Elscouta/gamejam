import functools
import os

from pygame import transform

from config import TILE_WIDTH, TILE_HEIGHT
from utils import sprite_sheet

MAP_TILESHEET = 0
LIGHT_TILESHEET = 1
FURNITURE_TILESHEET = 2
OHNOES_TILESHEET = 3

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
HALO = (LIGHT_TILESHEET, 0, 0)
SHADOW = (LIGHT_TILESHEET, 0, 1)
WARNING = (MAP_TILESHEET, 3, 0)
BEDSIDE_LAMP = (FURNITURE_TILESHEET, 4, 3)
BED_TOP = (FURNITURE_TILESHEET, 4, 5)
BED_BOTTOM = (FURNITURE_TILESHEET, 5, 5)
OHNOES1 = (OHNOES_TILESHEET, 0, 0)
OHNOES2 = (OHNOES_TILESHEET, 0, 1)

_tilesheets = {}
_player_sprites = None


def init():
    global _player_sprites

    _tilesheets[MAP_TILESHEET] = sprite_sheet(os.path.join('assets', 'tilesetHouse.png'), (TILE_WIDTH, TILE_HEIGHT))
    _tilesheets[LIGHT_TILESHEET] = sprite_sheet(os.path.join('assets', 'halo.png'), (640, 640))
    _tilesheets[FURNITURE_TILESHEET] = sprite_sheet(os.path.join('assets', 'house_objects.png'), (TILE_WIDTH, TILE_HEIGHT))
    _tilesheets[OHNOES_TILESHEET] = sprite_sheet(os.path.join('assets', 'ohnoes.png'), (2*TILE_WIDTH, 2*TILE_HEIGHT))
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
