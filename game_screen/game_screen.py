from typing import Optional

import pygame as pg
from pygame import Surface, SRCALPHA
from pygame.color import Color

from defeat_screen.defeat_screen import DefeatScreen
from game_screen import player, monsters, map, logic, lighting
from game_screen.logic import GameOverEx, WonEx
from screen import Screen, ScreenType
from victory_screen.end_screen import EndScreen


class GameScreen(Screen):
    def __init__(self):
        map.init()
        map.print_map()
        player.init()
        lighting.init()
        logic.init()

    def draw(self, screen: Surface, clock: pg.time.Clock) -> Optional[ScreenType]:
        player.handle_keys()

        light_mask = Surface((screen.get_width(), screen.get_height()), flags=SRCALPHA)
        light_mask.fill(Color(0, 0, 0))

        # Draw stuff and fill the light mask with light sources
        map.draw(screen, light_mask)
        player.draw(screen, light_mask)
        screen.blit(light_mask, (0, 0))

        monsters.draw_all(screen)

        clock.tick(60)
        try:
            logic.tick()
        except GameOverEx:
            return DefeatScreen
        except WonEx:
            return EndScreen

        fps = clock.get_fps()
        if fps > 0:
            pg.display.set_caption(f"FPS: {clock.get_fps()}")

        return None
