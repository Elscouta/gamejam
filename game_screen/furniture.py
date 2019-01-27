from abc import abstractmethod, ABC

from game_screen.tile import PaintNW, PaintSW, PaintNE, PaintSE


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


class Paint(Furniture):
    width = 2
    height = 2

    def get_tile(self, x, y):
        return {
            (0, 0): PaintNW,
            (0, 1): PaintSW,
            (1, 0): PaintNE,
            (1, 1): PaintSE
        }[x, y]
