import random

from config import MIN_MONSTER_DISTANCE
from events import schedule_event, clear_event
import map
import player
from threat_bubble import ThreatBubble
from utils import distance

PHASE_EXPLORATION = 0
PHASE_RUNAWAY = 1

cycle_number = 0
phase = PHASE_EXPLORATION

_monsters = set()


class Monster:
    def __init__(self):
        self._events = set()
        self._events.add(schedule_event(self.announce_itself, 3*10, oneshot=False))
        self._events.add(schedule_event(self.move, 5*10, oneshot=False))

        self.threat_bubble = None

        while True:
            self.x, self.y = map.random_point()
            if distance((self.x, self.y), (player.get_x(), player.get_y())) > MIN_MONSTER_DISTANCE:
                break

    def destroy(self):
        for e in self._events:
            clear_event(e)
        self._events.clear()

    def draw(self, screen):
        if self.threat_bubble:
            self.threat_bubble.draw(screen)

    def move(self):
        pass

    def announce_itself(self):
        self.threat_bubble = ThreatBubble((self.x, self.y))
        self._events.add(schedule_event(self.silence_itself, 1*10, oneshot=True))

    def silence_itself(self):
        self.threat_bubble = None


def spawn():
    _monsters.add(Monster())


def destroy_all():
    for m in _monsters:
        m.destroy()
    _monsters.clear()


def draw_all(screen):
    for m in _monsters:
        m.draw(screen)


def init():
    schedule_event(spawn, 5 * 10, oneshot=False)
    schedule_event(map.close_door, 45*10, oneshot=False)