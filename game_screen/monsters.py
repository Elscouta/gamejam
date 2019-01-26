import os

import pygame
import random

from config import MIN_MONSTER_DISTANCE, MONSTER_SPEED, MONSTER_MOVE_INTERVAL, MONSTER_ANNOUNCE_INTERVAL, \
    MONSTER_RANDOM_WALK, MONSTER_WARNING_INTERVAL, MONSTER_SPAWN_INTERVAL
from events import schedule_event, clear_event
from game_screen import player, map
from game_screen.asset import get_sprite, WARNING
from threat_bubble import ThreatBubble
from utils import distance

PHASE_EXPLORATION = 0
PHASE_RUNAWAY = 1

cycle_number = 0
phase = PHASE_EXPLORATION
spawn_rate = 40
spawn_event = None

_monsters = set()


class Monster:
    def __init__(self):
        self._events = set()
        self.monster_sound = pygame.mixer.Sound(os.path.join('assets', 'sfx_scream.wav'))
        self.monster_sound.set_volume(0.1)

        self._events.add(schedule_event(self.announce_itself, MONSTER_ANNOUNCE_INTERVAL*10, oneshot=False))
        self._events.add(schedule_event(self.move, MONSTER_MOVE_INTERVAL*10, oneshot=False))
        self._events.add(schedule_event(self.switch_warning_sign, MONSTER_WARNING_INTERVAL*10 + 1, oneshot=False))

        self.threat_bubble = None
        self.warning_sign_active = 0

        while True:
            self.x, self.y = map.random_point()
            if distance((self.x, self.y), (player.get_x(), player.get_y())) > MIN_MONSTER_DISTANCE:
                break

        self.announce_itself()

    def switch_warning_sign(self):
        self.warning_sign_active = self.warning_sign_active + 1 % 3

    def destroy(self):
        for e in self._events:
            clear_event(e)
        self._events.clear()

    def draw(self, screen):
        if self.threat_bubble:
            self.threat_bubble.draw(screen)

        if self.warning_sign_active == 2:
            screen.blit(get_sprite(WARNING), map.to_screen_coords(self.x, self.y))

    def move(self):
        from game_screen import player

        px, py = player.get_x(), player.get_y()
        dst = distance((px, py), (self.x, self.y))

        ms = MONSTER_MOVE_INTERVAL * MONSTER_SPEED

        dx = int(ms * (self.x - px) / dst)
        dy = int(ms * (self.y - py) / dst)

        self.x += dx + int(random.uniform(-ms * MONSTER_RANDOM_WALK, ms * MONSTER_RANDOM_WALK))
        self.y += dy + int(random.uniform(-ms * MONSTER_RANDOM_WALK, ms * MONSTER_RANDOM_WALK))

    def announce_itself(self):
        self.threat_bubble = ThreatBubble((self.x, self.y))
        self.monster_sound.play()
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
    schedule_event(spawn, MONSTER_SPAWN_INTERVAL * 10, oneshot=False)
    schedule_event(map.close_door, 45 * 10, oneshot=False)