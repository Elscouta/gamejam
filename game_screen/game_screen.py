import pygame as pg
from pygame import Surface, SRCALPHA
from pygame.color import Color

from game_screen import player, monsters, map, asset
from screen import Screen


class GameScreen(Screen):
    def __init__(self):
        asset.init()
        map.init()
        map.print()
        player.init()
        monsters.init()

    def draw(self, screen: Surface, clock: pg.time.Clock, player_speed: int) -> bool:
        player.handle_keys()

        light_mask = Surface((screen.get_width(), screen.get_height()), flags=SRCALPHA)
        light_mask.fill(Color(0, 0, 0))

        # Draw stuff and fill the light mask with light sources
        map.draw(screen, light_mask)
        player.draw(screen, light_mask)
        screen.blit(light_mask, (0, 0))

        monsters.draw_all(screen)

        pg.display.update()
        clock.tick(60)
        fps = clock.get_fps()
        if fps > 0:
            player_speed = player_speed * (60 / fps)
            pg.display.set_caption(f"FPS: {clock.get_fps()}, player speed : {player_speed}")

        return False
