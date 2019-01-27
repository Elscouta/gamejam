import math
import time
from typing import List

import pygame
from pygame.surface import Surface


def distance(pos1, pos2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return math.sqrt(dx * dx + dy * dy)


def fade_in(screen: Surface, surface: Surface, fade_time_in_s):
    starting_time = time.time()

    while time.time() - starting_time <= fade_time_in_s:
        state_time = time.time() - starting_time
        # last_state_change = time.time() - state_time
        alpha = 1.0 * state_time / fade_time_in_s
        surface.set_alpha(alpha * 255)
        screen.blit(surface, screen.get_rect())
        pygame.display.update()


def fade_out(screen: Surface, surface: Surface, fade_time_in_s, starting_time):
    state_time = time.time() - starting_time
    # last_state_change = time.time() - state_time
    alpha = 1 - (1.0 * state_time / fade_time_in_s)
    surface.set_alpha(alpha * 255)
    screen.blit(surface, screen.get_rect())
    pygame.display.update()


def sprite_sheet(file, sprite_size, pos=(0, 0)) -> List[List[Surface]]:
    sheet = pygame.image.load(file).convert_alpha()  # Load the sheet
    len_sprt_x, len_sprt_y = sprite_size
    sprt_rect_x, sprt_rect_y = pos  # where to find first sprite on sheet

    sheet_rect = sheet.get_rect()

    sprites: List[List[Surface]] = [[0 for _ in range(0, int(sheet_rect.width / len_sprt_x))] for _ in
                                    range(0, int(sheet_rect.height / len_sprt_y))]
    current_row = 0
    current_column = 0

    for _ in range(0, len(sprites)):  # rows
        for _ in range(0, len(sprites[0])):  # columns
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y))  # find sprite you want
            sprite = sheet.subsurface(sheet.get_clip())  # grab the sprite you want
            sprites[current_row][current_column] = sprite
            sprt_rect_x += len_sprt_x
            current_column += 1

        current_row += 1
        current_column = 0

        sprt_rect_y += len_sprt_y
        sprt_rect_x = 0

    return sprites
