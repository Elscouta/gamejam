import pygame
from pygame.surface import Surface


def sprite_sheet(file, sprite_size, pos=(0, 0)) -> [Surface]:
    sheet = pygame.image.load(file).convert_alpha()  # Load the sheet
    len_sprt_x, len_sprt_y = sprite_size
    sprt_rect_x, sprt_rect_y = pos  # where to find first sprite on sheet

    sheet_rect = sheet.get_rect()
    sprites = []
    for _ in range(0, sheet_rect.height - len_sprt_y, sprite_size[1]):  # rows
        for _ in range(0, sheet_rect.width - len_sprt_x, sprite_size[0]):  # columns
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y))  # find sprite you want
            sprite = sheet.subsurface(sheet.get_clip())  # grab the sprite you want
            sprites.append(sprite)
            sprt_rect_x += len_sprt_x

        sprt_rect_y += len_sprt_y
        sprt_rect_x = 0
    print(sprites)
    return sprites
