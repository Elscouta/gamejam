from pygame.rect import Rect

from asset import NW_CORNER, N_WALL, NE_CORNER, W_WALL, FLOOR, E_WALL, SW_CORNER, S_WALL, SE_CORNER, N_DOOR, W_DOOR, \
    E_DOOR, S_DOOR
from config import WALL_WIDTH, TILE_WIDTH, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_CROP_BOTTOM, \
    PLAYER_CROP_TOP, PLAYER_CROP_RIGHT, PLAYER_CROP_LEFT


def _player_bounding_box(x, y):
    return Rect(x + PLAYER_CROP_LEFT, y + PLAYER_CROP_TOP,
                PLAYER_WIDTH - PLAYER_CROP_LEFT - PLAYER_CROP_RIGHT,
                PLAYER_HEIGHT - PLAYER_CROP_TOP - PLAYER_CROP_BOTTOM)


class Tile:
    def __init__(self, sprite_id, top_wall, right_wall, bottom_wall, left_wall):
        self.top_wall = top_wall
        self.right_wall = right_wall
        self.bottom_wall = bottom_wall
        self.left_wall = left_wall
        self.sprite_id = sprite_id

    def is_collision(self, x, y):
        player_bbox = _player_bounding_box(x, y)

        if self.top_wall and player_bbox.colliderect(Rect(0, 0, TILE_WIDTH, WALL_WIDTH)):
            return True

        if self.right_wall and player_bbox.colliderect(Rect(TILE_WIDTH - WALL_WIDTH, 0, WALL_WIDTH, TILE_WIDTH)):
            return True

        if self.bottom_wall and player_bbox.colliderect(Rect(0, TILE_WIDTH - WALL_WIDTH, TILE_WIDTH, WALL_WIDTH)):
            return True

        if self.left_wall and player_bbox.colliderect(Rect(0, 0, WALL_WIDTH, TILE_WIDTH)):
            return True

        return False

    def is_collision_ur(self, x, y):
        if self.top_wall and y < WALL_WIDTH - PLAYER_CROP_TOP:
            return True

        if self.right_wall and x > TILE_WIDTH - PLAYER_WIDTH + PLAYER_CROP_RIGHT - WALL_WIDTH:
            return True

        if self.left_wall and x < WALL_WIDTH - PLAYER_CROP_LEFT:
            return True

        return False

    def is_collision_bl(self, x, y):
        if self.right_wall and y > TILE_WIDTH - PLAYER_HEIGHT + PLAYER_CROP_BOTTOM and x > TILE_WIDTH - PLAYER_WIDTH + PLAYER_CROP_RIGHT - WALL_WIDTH:
            return True

        if self.left_wall and y > TILE_WIDTH - PLAYER_HEIGHT + PLAYER_CROP_BOTTOM and x < WALL_WIDTH - PLAYER_CROP_LEFT:
            return True

        if self.bottom_wall and y > 2 * TILE_WIDTH - PLAYER_HEIGHT + PLAYER_CROP_BOTTOM - WALL_WIDTH:
            return True

        return False

NorthWestCorner = Tile(NW_CORNER, True, False, False, True)
NorthWall = Tile(N_WALL, True, False, False, False)
NorthOpenDoor = Tile(N_DOOR, False, False, False, False)
NorthEastCorner = Tile(NE_CORNER, True, True, False, False)
WestWall = Tile(W_WALL, False, False, False, True)
WestOpenDoor = Tile(W_DOOR, False, False, False, False)
Floor = Tile(FLOOR, False, False, False, False)
EastWall = Tile(E_WALL, False, True, False, False)
EastOpenDoor = Tile(E_DOOR, False, False, False, False)
SouthWestCorner = Tile(SW_CORNER, False, False, True, True)
SouthWall = Tile(S_WALL, False, False, True, False)
SouthOpenDoor = Tile(S_DOOR, False, False, False, False)
SouthEastCorner = Tile(SE_CORNER, False, True, True, False)
