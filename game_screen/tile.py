from pygame.rect import Rect

from asset import NW_CORNER, N_WALL, NE_CORNER, W_WALL, FLOOR, E_WALL, SW_CORNER, S_WALL, SE_CORNER, N_DOOR, \
    W_DOOR, \
    E_DOOR, S_DOOR, N_DOORWAY, W_DOORWAY, E_DOORWAY, S_DOORWAY, BEDSIDE_LAMP, BED_TOP, BED_BOTTOM, BPAINT_NW, BPAINT_NE, \
    BPAINT_SW, BPAINT_SE, PORCELAIN_NW_CORNER, PORCELAIN_N_WALL, PORCELAIN_N_DOOR, PORCELAIN_N_DOORWAY, \
    PORCELAIN_NE_CORNER, PORCELAIN_W_WALL, PORCELAIN_W_DOOR, PORCELAIN_W_DOORWAY, PORCELAIN_FLOOR, PORCELAIN_E_WALL, \
    PORCELAIN_E_DOOR, PORCELAIN_E_DOORWAY, PORCELAIN_SW_CORNER, PORCELAIN_S_WALL, PORCELAIN_S_DOOR, PORCELAIN_S_DOORWAY, \
    PORCELAIN_SE_CORNER, OPAINT_NW, OPAINT_NE, OPAINT_SW, OPAINT_SE, GPAINT_NW, GPAINT_NE, GPAINT_SW, GPAINT_SE
from config import WALL_WIDTH, TILE_WIDTH, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_CROP_BOTTOM, \
    PLAYER_CROP_TOP, PLAYER_CROP_RIGHT, PLAYER_CROP_LEFT
from game_screen import player


def _player_bounding_box(x, y):
    return Rect(x + PLAYER_CROP_LEFT, y + PLAYER_CROP_TOP,
                PLAYER_WIDTH - PLAYER_CROP_LEFT - PLAYER_CROP_RIGHT,
                PLAYER_HEIGHT - PLAYER_CROP_TOP - PLAYER_CROP_BOTTOM)


class Tile:
    def __init__(self, sprite_id, bboxs, solid=True, event=lambda: None):
        self.bboxs = bboxs
        self.solid = solid
        self.event = event
        self.sprite_id = sprite_id

    def is_collision(self, x, y):
        player_bbox = _player_bounding_box(x, y)

        if any(player_bbox.colliderect(bbox) for bbox in self.bboxs):
            self.event()
            return self.solid

        return False

top_wall_bbox = Rect(0, 0, TILE_WIDTH, WALL_WIDTH)
left_wall_bbox = Rect(0, 0, 24, 64)
bottom_wall_bbox = Rect(0, TILE_WIDTH - WALL_WIDTH, TILE_WIDTH, WALL_WIDTH)
right_wall_bbox = Rect(40, 0, 24, 64)


NorthWestCorner = Tile(NW_CORNER, bboxs=(top_wall_bbox, left_wall_bbox))
NorthWall = Tile(N_WALL, bboxs=(top_wall_bbox,))
NorthClosedDoor = Tile(N_DOOR, bboxs=(top_wall_bbox,))
NorthOpenDoor = Tile(N_DOORWAY, bboxs=())
NorthEastCorner = Tile(NE_CORNER, bboxs=(top_wall_bbox, right_wall_bbox))
WestWall = Tile(W_WALL, bboxs=(left_wall_bbox,))
WestClosedDoor = Tile(W_DOOR, bboxs=(left_wall_bbox,))
WestOpenDoor = Tile(W_DOORWAY, bboxs=())
Floor = Tile(FLOOR, bboxs=())
EastWall = Tile(E_WALL, bboxs=(right_wall_bbox,))
EastClosedDoor = Tile(E_DOOR, bboxs=(right_wall_bbox,))
EastOpenDoor = Tile(E_DOORWAY, bboxs=())
SouthWestCorner = Tile(SW_CORNER, bboxs=(bottom_wall_bbox, left_wall_bbox))
SouthWall = Tile(S_WALL, bboxs=(bottom_wall_bbox,))
SouthClosedDoor = Tile(S_DOOR, bboxs=(bottom_wall_bbox,))
SouthOpenDoor = Tile(S_DOORWAY, bboxs=())
SouthEastCorner = Tile(SE_CORNER, bboxs=(bottom_wall_bbox, right_wall_bbox))
PorcelainNorthWestCorner = Tile(PORCELAIN_NW_CORNER, bboxs=(top_wall_bbox, left_wall_bbox))
PorcelainNorthWall = Tile(PORCELAIN_N_WALL, bboxs=(top_wall_bbox,))
PorcelainNorthClosedDoor = Tile(PORCELAIN_N_DOOR, bboxs=(top_wall_bbox,))
PorcelainNorthOpenDoor = Tile(PORCELAIN_N_DOORWAY, bboxs=())
PorcelainNorthEastCorner = Tile(PORCELAIN_NE_CORNER, bboxs=(top_wall_bbox, right_wall_bbox))
PorcelainWestWall = Tile(PORCELAIN_W_WALL, bboxs=(left_wall_bbox,))
PorcelainWestClosedDoor = Tile(PORCELAIN_W_DOOR, bboxs=(left_wall_bbox,))
PorcelainWestOpenDoor = Tile(PORCELAIN_W_DOORWAY, bboxs=())
PorcelainFloor = Tile(PORCELAIN_FLOOR, bboxs=())
PorcelainEastWall = Tile(PORCELAIN_E_WALL, bboxs=(right_wall_bbox,))
PorcelainEastClosedDoor = Tile(PORCELAIN_E_DOOR, bboxs=(right_wall_bbox,))
PorcelainEastOpenDoor = Tile(PORCELAIN_E_DOORWAY, bboxs=())
PorcelainSouthWestCorner = Tile(PORCELAIN_SW_CORNER, bboxs=(bottom_wall_bbox, left_wall_bbox))
PorcelainSouthWall = Tile(PORCELAIN_S_WALL, bboxs=(bottom_wall_bbox,))
PorcelainSouthClosedDoor = Tile(PORCELAIN_S_DOOR, bboxs=(bottom_wall_bbox,))
PorcelainSouthOpenDoor = Tile(PORCELAIN_S_DOORWAY, bboxs=())
PorcelainSouthEastCorner = Tile(PORCELAIN_SE_CORNER, bboxs=(bottom_wall_bbox, right_wall_bbox))
BedsideLamp = Tile(BEDSIDE_LAMP, bboxs=(Rect(0, 0, 64, 64),))
BedTop = Tile(BED_TOP, bboxs=(Rect(0, 0, 64, 64),))
BedBottom = Tile(BED_BOTTOM, bboxs=(Rect(0, 0, 64, 45),))

def add_paint(color):
    from game_screen import player
    player.add_paint(color)

BPaintNW = Tile(BPAINT_NW, bboxs=(Rect(44, 54, 20, 10),), solid=False, event=lambda: add_paint('blue'))
BPaintNE = Tile(BPAINT_NE, bboxs=(Rect(0, 54, 20, 10),), solid=False, event=lambda: add_paint('blue'))
BPaintSW = Tile(BPAINT_SW, bboxs=(Rect(44, 0, 20, 5),), solid=False, event=lambda: add_paint('blue'))
BPaintSE = Tile(BPAINT_SE, bboxs=(Rect(0, 0, 20, 5),), solid=False, event=lambda: add_paint('blue'))
OPaintNW = Tile(OPAINT_NW, bboxs=(Rect(44, 54, 20, 10),), solid=False, event=lambda: add_paint('orange'))
OPaintNE = Tile(OPAINT_NE, bboxs=(Rect(0, 54, 20, 10),), solid=False, event=lambda: add_paint('orange'))
OPaintSW = Tile(OPAINT_SW, bboxs=(Rect(44, 0, 20, 5),), solid=False, event=lambda: add_paint('orange'))
OPaintSE = Tile(OPAINT_SE, bboxs=(Rect(0, 0, 20, 5),), solid=False, event=lambda: add_paint('orange'))
GPaintNW = Tile(GPAINT_NW, bboxs=(Rect(44, 54, 20, 10),), solid=False, event=lambda: add_paint('green'))
GPaintNE = Tile(GPAINT_NE, bboxs=(Rect(0, 54, 20, 10),), solid=False, event=lambda: add_paint('green'))
GPaintSW = Tile(GPAINT_SW, bboxs=(Rect(44, 0, 20, 5),), solid=False, event=lambda: add_paint('green'))
GPaintSE = Tile(GPAINT_SE, bboxs=(Rect(0, 0, 20, 5),), solid=False, event=lambda: add_paint('green'))
