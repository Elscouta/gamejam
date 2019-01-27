import os
from typing import Tuple

import pygame as pg
from game_screen import map

from asset import get_sprite, BURGER, BUBBLE_FF, BUBBLE_OO, BUBBLE_OF, BUBBLE_FO
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class ThreatBubble(pg.sprite.Sprite):


    def __init__(self, monster_position: Tuple[int, int]):
        pg.sprite.Sprite.__init__(self)
        self.image_orig: pg.Surface = pg.image.load(os.path.join('assets', 'speech_bubble.png')).convert_alpha()
        self.images = [
            [
                get_sprite(BUBBLE_OO),
                get_sprite(BUBBLE_OF)
            ],
            [
                get_sprite(BUBBLE_FO),
                get_sprite(BUBBLE_FF)
            ]
        ]
        self.monster_position = monster_position
        self.set_image(monster_position)
        self.rect = self.image.get_rect()
        self.burger: pg.Surface = get_sprite(BURGER)


    def set_image(self, monster_position: Tuple[int, int]):
        self.offset = (37, 15)
        self.x_burger_offset = 5
        self.image = self.image_orig

        qsw, qsh = SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4
        mpx, mpy = map.to_screen_coords(*monster_position)

        if qsw <= mpx < 2*qsw or 3*qsw <= mpx:
            reverse_x = 1
            self.x_burger_offset *= -1
            self.offset = (-self.offset[0], self.offset[1])
        else:
            reverse_x = 0

        if mpy < qsh or 2*qsh <= mpy < 3*qsh:
            reverse_y = 1
            self.offset = (self.offset[0], -self.offset[1])
        else:
            reverse_y = 0

        self.image = self.images[reverse_x][reverse_y]

    def draw(self, screen: pg.Surface):
        from game_screen import map

        x, y = map.to_screen_coords(self.monster_position[0], self.monster_position[1])
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        minx, maxx = self.rect.w, SCREEN_WIDTH - self.rect.w
        miny, maxy = self.rect.h, SCREEN_HEIGHT - self.rect.h

        if x < minx:
            k = (minx - cx) / (x - cx)
            x = minx
            y = int(k * (y - cy) + cy)

        if y < miny:
            k = (miny - cy) / (y - cy)
            y = miny
            x = int(k * (x - cx) + cx)

        if x > maxx:
            k = (maxx - cx) / (x - cx)
            x = maxx
            y = int(k * (y - cy) + cy)

        if y > maxy:
            k = (maxy - cy) / (y - cy)
            y = maxy
            x = int(k * (x - cx) + cx)

        screen.blit(self.image, (x + self.offset[0] - self.rect.w // 2, y + self.offset[1] - self.rect.h // 2))
        screen.blit(self.burger, (x + self.offset[0] + self.x_burger_offset - (self.burger.get_size()[0] // 2),
                                  y + self.offset[1] - 2 - (self.burger.get_size()[1] // 2)))
