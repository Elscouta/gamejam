from abc import abstractmethod, ABC

from game_screen.tile import BPaintNW, BPaintSW, BPaintNE, BPaintSE, OPaintNW, OPaintSW, OPaintNE, OPaintSE, GPaintSE, \
    GPaintNE, GPaintSW, GPaintNW


class Furniture(ABC):
    width: int = None
    height: int = None

    def __init__(self, room_x, room_y):
        self.room_x = room_x
        self.room_y = room_y

    def in_furniture(self, room_i, room_j):
        return self.room_x <= room_i < self.room_x + self.width and \
               self.room_y <= room_j < self.room_y + self.height

    def room_coords_to_furniture_coords(self, room_i, room_j):
        return room_i - self.room_x, room_j - self.room_y

    @abstractmethod
    def get_tile(self, x, y):
        ...


class BPaint(Furniture):
    width = 2
    height = 2

    def get_tile(self, x, y):
        return {
            (0, 0): BPaintNW,
            (0, 1): BPaintSW,
            (1, 0): BPaintNE,
            (1, 1): BPaintSE
        }[x, y]

class OPaint(Furniture):
    width = 2
    height = 2

    def get_tile(self, x, y):
        return {
            (0, 0): OPaintNW,
            (0, 1): OPaintSW,
            (1, 0): OPaintNE,
            (1, 1): OPaintSE
        }[x, y]

class GPaint(Furniture):
    width = 2
    height = 2

    def get_tile(self, x, y):
        return {
            (0, 0): GPaintNW,
            (0, 1): GPaintSW,
            (1, 0): GPaintNE,
            (1, 1): GPaintSE
        }[x, y]
