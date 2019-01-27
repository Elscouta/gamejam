import pygame as pg

from asset import FLOOR, get_sprite, get_player_sprites, OHNOES1, OHNOES2, get_light_halo
from config import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_WIDTH, TILE_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT
from events import schedule_event
from screen import Screen


class DefeatScreen(Screen):
    def __init__(self):
        self.step = 0
        schedule_event(lambda: self.set_step(1), 8, oneshot=True)
        schedule_event(lambda: self.set_step(2), 13, oneshot=True)
        schedule_event(lambda: self.set_step(3), 21, oneshot=True)
        self.light = 128

    def set_step(self, step):
        if step == 3:
            schedule_event(self.decrease_light, 1, oneshot=False)
        else:
            self.step = step

    def decrease_light(self):
        if self.light > 8:
            self.light -= 8

    def draw(self, screen: pg.Surface, clock: pg.time.Clock):
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        for i in range(-2, 3):
            for j in range(-2, 3):
                screen.blit(get_sprite(FLOOR), (cx + i*TILE_WIDTH, cy + j * TILE_HEIGHT))

        if self.step == 1:
            screen.blit(get_sprite(OHNOES1), (cx - TILE_WIDTH // 2, cy - TILE_HEIGHT // 2))
        if self.step == 2:
            screen.blit(get_sprite(OHNOES2), (cx - TILE_WIDTH // 2, cy - TILE_HEIGHT // 2))

        screen.blit(get_player_sprites()[3][0], (cx, cy))

        light_mask = pg.Surface((screen.get_width(), screen.get_height()), flags=pg.SRCALPHA)
        light_mask.fill(pg.Color(0, 0, 0))

        halo = get_light_halo(self.light)
        light_mask.blit(halo, (cx - self.light + PLAYER_WIDTH // 2,
                               cy - self.light + PLAYER_HEIGHT // 2),
                        special_flags=pg.BLEND_RGBA_MIN)
        screen.blit(light_mask, (0, 0))

        if self.light <= 8:
            from title_screen.title_screen import TitleScreen
            return TitleScreen
