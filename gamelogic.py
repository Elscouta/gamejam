import random

from config import MIN_MONSTER_DISTANCE
from events import schedule_event, clear_event
import map
import player
from utils import distance

PHASE_EXPLORATION = 0
PHASE_RUNAWAY = 1

cycle_number = 0
phase = PHASE_EXPLORATION

_monsters = set()


class Monster:
    def __init__(self):
        self.announce_event = schedule_event(self.announce_itself, 20*10, oneshot=False)
        self.move_event = schedule_event(self.move, 5*10, oneshot=False)
        while True:
            self.x, self.y = map.random_point()
            if distance((self.x, self.y), (player.get_x(), player.get_y())) > MIN_MONSTER_DISTANCE:
                break

    def destroy(self):
        clear_event(self.announce_event)
        clear_event(self.move_event)

    def draw(self):
        pass

    def move(self):
        pass

    def announce_itself(self):
        print("I'm hungry!!!")


def spawn_monster():
    _monsters.add(Monster())


def destroy_monsters():
    for m in _monsters:
        m.destroy()
    _monsters.clear()


def init():
    schedule_event(spawn_monster, 30*10, oneshot=False)
    schedule_event(map.close_door, 45*10, oneshot=False)