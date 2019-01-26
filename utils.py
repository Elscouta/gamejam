import pygame
from pygame.surface import Surface
from typing import List, Tuple


def sprite_sheet(file, sprite_size, pos=(0, 0)) -> List[List[Surface]]:
    sheet = pygame.image.load(file).convert_alpha()  # Load the sheet
    len_sprt_x, len_sprt_y = sprite_size
    sprt_rect_x, sprt_rect_y = pos  # where to find first sprite on sheet

    sheet_rect = sheet.get_rect()

    sprites: List[List[Surface]] = [[0 for _ in range(0, int(sheet_rect.width / len_sprt_x))] for _ in range(0, int(sheet_rect.height / len_sprt_y))]
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


def display_text_bubble(screen: Surface, content, size: Tuple[int, int], where: Tuple[int, int],
                        color=(255, 255, 255)):
    for current_column in range(0, size[0]):
        for current_row in range(0, size[1]):
            if 2 < current_column < size[0] - 2 and (current_row == 0 or current_row == size[1] - 1):
                screen.set_at((where[0] + current_column, where[1] + current_row), color)
            if (current_column == 1 and (current_row == 1 or current_row == size[1] - 1)) or (current_column == size[0] - 1 and (current_row == size[1] - 1 or current_row == 1)):
                screen.set_at((where[0] + current_column, where[1] + current_row), color)
            if 2 < current_row < size[1] - 2 and (current_column == 0 or current_column == size[0] - 1):
                screen.set_at((where[0] + current_column, where[1] + current_row), color)
