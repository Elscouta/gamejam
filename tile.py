from asset import NW_CORNER, N_WALL, NE_CORNER, W_WALL, FLOOR, E_WALL, SW_CORNER, S_WALL, SE_CORNER, N_DOOR, W_DOOR, \
    E_DOOR, S_DOOR
from config import WALL_WIDTH, TILE_WIDTH, PLAYER_CROP_X, PLAYER_WIDTH, PLAYER_CROP_Y, PLAYER_HEIGHT


class Tile:
    def __init__(self, sprite_id, top_wall, right_wall, bottom_wall, left_wall):
        self.top_wall = top_wall
        self.right_wall = right_wall
        self.bottom_wall = bottom_wall
        self.left_wall = left_wall
        self.sprite_id = sprite_id

    def is_collision(self, x, y):
        if self.top_wall and y < WALL_WIDTH - PLAYER_CROP_X:
            print("ctop")
            return True

        if self.right_wall and x > TILE_WIDTH - PLAYER_WIDTH + PLAYER_CROP_X - WALL_WIDTH:
            print("cright")
            return True

        if self.bottom_wall and y > TILE_WIDTH - PLAYER_HEIGHT + PLAYER_CROP_Y - WALL_WIDTH:
            print("cbottom")
            return True

        if self.left_wall and x < WALL_WIDTH - PLAYER_CROP_Y:
            print("cleft")
            return True

        return False


NorthWestCorner = Tile(NW_CORNER, True, False, False, True)
NorthWall = Tile(N_WALL, True, False, False, False)
NorthDoor = Tile(N_DOOR, True, False, False, False)
NorthEastCorner = Tile(NE_CORNER, True, True, False, False)
WestWall = Tile(W_WALL, False, False, False, True)
WestDoor = Tile(W_DOOR, False, False, False, True)
Floor = Tile(FLOOR, False, False, False, False)
EastWall = Tile(E_WALL, False, True, False, False)
EastDoor = Tile(E_DOOR, False, True, False, False)
SouthWestCorner = Tile(SW_CORNER, False, False, True, True)
SouthWall = Tile(S_WALL, False, False, True, False)
SouthDoor = Tile(S_DOOR, False, False, True, False)
SouthEastCorner = Tile(SE_CORNER, False, True, True, False)
