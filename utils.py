import pygame
from pygame.surface import Surface


def sprite_sheet(file, sprite_size, pos=(0, 0)) -> [Surface]:
    sheet = pygame.image.load(file).convert_alpha()  # Load the sheet
    len_sprt_x, len_sprt_y = sprite_size
    sprt_rect_x, sprt_rect_y = pos  # where to find first sprite on sheet

    sheet_rect = sheet.get_rect()

    number_of_rows = range(0, sheet_rect.height - len_sprt_y, sprite_size[1])
    number_of_columns = range(0, sheet_rect.width - len_sprt_x, sprite_size[0])

    sprites = [[0 for _ in range(0, int(sheet_rect.width / len_sprt_x))] for _ in range(0, int(sheet_rect.height / len_sprt_y))]
    current_row = 0
    current_column = 0

    for _ in number_of_rows:  # rows
        for _ in number_of_columns:  # columns
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
