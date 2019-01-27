import os
from typing import Optional

import pygame as pg

import asset
from config import SCREEN_HEIGHT
from events import schedule_event
from screen import Screen, ScreenType


class EndScreen(Screen):
    def __init__(self):
        self.tmp = 0
        self.player_sprites = asset.get_player_sprites()
        self.font = pg.font.Font(os.path.join('assets', 'ButterflyKids-Regular.ttf'), 70)
        self.stop = False
        self.event_scheduled = False
        self.do_not_redraw_char_scene = False
        self.should_draw_toilets = False
        self.current_sprite = 1
        self.sprite_speed_delta = 0
        self.remaining_millipixels = 0
        self.last_tick = pg.time.get_ticks()
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

        character_rec = (self.player_sprites[3][self.current_sprite]) \
            .get_rect(center=(
            screen.get_size()[0] // 2,
            screen.get_size()[1] - (45 + self.sprite_speed_delta)
        )
        )
        screen.blit(self.player_sprites[3][self.current_sprite], character_rec)
        self.sprite_speed_delta += 1
        self.current_sprite += 1
        if self.current_sprite == 3:
            self.current_sprite = 0

    def draw_toilets(self, screen):
        if self.rect.y > 0:
            self.show_ending(screen)
        else:
            screen.blit(self.toilet_scene, self.rect)
            for _ in range(0, self.get_pixels_to_move(15)):
                if self.rect.y < 0:
                    self.draw_scene(screen, self.rect)
                    self.rect.y += 3

    def set_variables(self):
        self.should_draw_toilets = True
        self.do_not_redraw_char_scene = True

    def draw(self, screen: pg.Surface, clock: pg.time.Clock) -> Optional[ScreenType]:
        if not self.event_scheduled:
            schedule_event(self.set_variables, 15, True)
            self.event_scheduled = True
        if not self.do_not_redraw_char_scene:
            screen.blit(self.character_scene, screen.get_rect())
        if self.should_draw_toilets:
            self.draw_toilets(screen)

        return None

    def get_pixels_to_move(self, item_speed) -> int:
        new_tick = pg.time.get_ticks()
        tick_since_last = new_tick - self.last_tick
        self.last_tick = new_tick

        millipixels = (tick_since_last * item_speed) + self.remaining_millipixels
        pixel_moves = millipixels // 1000
        self.remaining_millipixels = pixel_moves % 1000
        return pixel_moves
