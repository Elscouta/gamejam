import os
from typing import Optional

import pygame as pg

from config import SCREEN_HEIGHT
from screen import Screen, ScreenType


class EndScreen(Screen):
    def __init__(self):
        self.tmp = 0
        self.font = pg.font.Font(os.path.join('assets', 'ButterflyKids-Regular.ttf'), 70)
        self.stop = False
        self.isPlayingPeeSound = False
        self.toilet_scene: pg.Surface = pg.image.load(os.path.join('assets', 'bathroom_scene.png'))
        self.character_scene: pg.Surface = pg.image.load(os.path.join('assets', 'happy_child.png'))
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

    def draw(self, screen: pg.Surface, clock: pg.time.Clock) -> Optional[ScreenType]:
        if self.stop is False:
            if self.rect.y == -400:
                if self.tmp < 50:
                    screen.blit(self.character_scene, screen.get_rect())
                    self.tmp += 1
                else:
                    self.tmp = 0
                    screen.blit(self.toilet_scene, self.rect)
                    self.rect.y += 1
            elif self.rect.y < -200:
                if self.tmp < 25:
                    screen.blit(self.character_scene, screen.get_rect())
                    self.tmp += 1
                else:
                    screen.blit(self.toilet_scene, self.rect)
                    self.rect.y += 1
            else:
                screen.blit(self.toilet_scene, self.rect)
                self.rect.y += 3
                if self.rect.y <= 0:
                    self.stop = True
        else:
            self.show_ending(screen)

        return None
