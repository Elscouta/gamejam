from typing import Optional

import pygame as pg

from abc import ABC, abstractmethod, ABCMeta


class ScreenType(ABCMeta):
    pass


class Screen(ABC, metaclass=ScreenType):

    @abstractmethod
    def draw(self, screen: pg.Surface, clock: pg.time.Clock) -> Optional[ScreenType]:
        pass
