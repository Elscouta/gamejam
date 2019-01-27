import os
import time
from typing import Optional

import pygame as pg

import asset
from config import SCREEN_HEIGHT
from screen import Screen, ScreenType


class EndScreen(Screen):
    def __init__(self):
        self.tmp = 0
        self.player_sprites = asset.get_player_sprites()
        self.font = pg.font.Font(os.path.join('assets', 'ButterflyKids-Regular.ttf'), 70)
        self.stop = False
        self.current_sprite = 1
        self.sprite_speed_delta = 0
        self.time = None
        self.isPlayingPeeSound = False
        self.toilet_scene: pg.Surface = pg.image.load(os.path.join('assets', 'bathroom_scene.png')).convert_alpha()
        self.character_scene: pg.Surface = pg.image.load(os.path.join('assets', 'happy_child.png')).convert_alpha()
        self.rect = pg.rect.Rect(0, SCREEN_HEIGHT - self.toilet_scene.get_size()[1], self.toilet_scene.get_size()[0],
                                 SCREEN_HEIGHT)

    def show_ending(self, screen):
        screen.fill((0, 0, 0))
        if self.isPlayingPeeSound is False:
            self.isPlayingPeeSound = True
            pee_sound = pg.mixer.Sound(os.path.join('assets', 'sfx_pee.wav'))
            pee_sound.set_volume(0.5)
            pee_sound.play()

        surface = self.font.render('Thank you for playing', False, (255, 255, 255))
        text_rec = surface.get_rect(center=(screen.get_size()[0] // 2, screen.get_size()[1] // 2))
        screen.blit(surface, text_rec)

    def draw_scene(self, screen, rect):
        screen.blit(self.toilet_scene, rect)

        character_rec = (self.player_sprites[3][self.current_sprite]).get_rect(center=(screen.get_size()[0] // 2,
                                                                                       screen.get_size()[1] - (45 + self.sprite_speed_delta))
                                                                               )
        screen.blit(self.player_sprites[3][self.current_sprite], character_rec)
        self.sprite_speed_delta += 1
        self.current_sprite += 1
        if self.current_sprite == 3:
            self.current_sprite = 0

    def draw(self, screen: pg.Surface, clock: pg.time.Clock) -> Optional[ScreenType]:
        if not self.time or time.time() - self.time > 20:
            if self.rect.y == -400:
                if self.tmp < 50:
                    screen.blit(self.character_scene, screen.get_rect())
                    self.tmp += 1
                else:
                    self.draw_scene(screen, self.rect)
                    self.rect.y += 3
            else:
                self.draw_scene(screen, self.rect)
                self.rect.y += 3
                if self.rect.y >= 0:
                    self.time = time.time()
        else:
            self.show_ending(screen)

        return None
