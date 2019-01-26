import pygame as pg
from pygame import Surface

from game_screen import player, monsters, map, asset


class GameScreen:
    def __init__(self):
        asset.init()
        player.init()
        map.init()
        map.print()
        monsters.init()

    def draw(self, screen: Surface, clock: pg.time.Clock, player_speed: int):
        player.handle_keys()

        # Draw stuff
        map.draw(screen, player.get_x(), player.get_y())
        player.draw(screen)
        monsters.draw_all(screen)

        pg.display.update()
        clock.tick(60)
        fps = clock.get_fps()
        if fps > 0:
            player_speed = player_speed * (60 / fps)
            pg.display.set_caption(f"FPS: {clock.get_fps()}, player speed : {player_speed}")
