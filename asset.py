import os

from config import TILE_WIDTH, TILE_HEIGHT
from utils import sprite_sheet

MAP_TILESHEET = 0

NW_CORNER = (MAP_TILESHEET, 0, 0)
N_WALL = (MAP_TILESHEET, 0, 1)
N_DOOR = (MAP_TILESHEET, 0, 3)
NE_CORNER = (MAP_TILESHEET, 0, 2)
W_WALL = (MAP_TILESHEET, 1, 0)
W_DOOR = (MAP_TILESHEET, 0, 3)
FLOOR = (MAP_TILESHEET, 1, 1)
E_WALL = (MAP_TILESHEET, 1, 2)
E_DOOR = (MAP_TILESHEET, 0, 3)
SW_CORNER = (MAP_TILESHEET, 2, 0)
S_WALL = (MAP_TILESHEET, 2, 1)
S_DOOR = (MAP_TILESHEET, 0, 3)
SE_CORNER = (MAP_TILESHEET, 2, 2)

_tilesheets = {}


def init():
    _tilesheets[MAP_TILESHEET] = sprite_sheet(os.path.join('assets', 'tilesetHouse.png'), (TILE_WIDTH, TILE_HEIGHT))


def get_sprite(sprite_id):
    return _tilesheets[sprite_id[0]][sprite_id[1]][sprite_id[2]]