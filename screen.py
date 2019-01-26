import pygame as pg

from abc import ABC, abstractmethod


class Screen(ABC):

    @abstractmethod
    def draw(self, screen: pg.Surface, clock: pg.time.Clock, player_speed: int) -> bool:
        pass
