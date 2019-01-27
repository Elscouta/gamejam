from config import TILE_WIDTH
from events import clear_event, schedule_event
from game_screen import player, map, lighting, monsters
from utils import distance

PHASE_EXPLORATION = 0
PHASE_SAFE = 1
PHASE_RUNAWAY = 2

closing_door_event = None


class _state:
    phase = None


_triggers = []
def trigger(cls):
    _triggers.append(cls())


def init():
    _state.phase = PHASE_SAFE
    lighting.player_lightning_radius = 6 * 64


def tick():
    for t in _triggers:
        if _state.phase in t.eligible_states and t.condition():
            t.action()


def is_player_safe():
    return _state.phase == PHASE_SAFE


class GameOverEx(Exception):
    pass


@trigger
class BackToBed:
    eligible_states = (PHASE_EXPLORATION, PHASE_RUNAWAY)

    def condition(self):
        px, py = player.get_pos()
        return distance((px, py), map.initial_room.get_initial_position()) < 2.4 * TILE_WIDTH

    def action(self):
        _state.phase = PHASE_SAFE
        lighting.player_lightning_radius = 6 * 64
        monsters.destroy_all()
        if closing_door_event:
            clear_event(closing_door_event)


@trigger
class OutOfBed:
    eligible_states = (PHASE_SAFE,)

    def condition(self):
        px, py = player.get_pos()
        return distance((px, py), map.initial_room.get_initial_position()) > 2.4 * TILE_WIDTH

    def action(self):
        global closing_door_event

        _state.phase = PHASE_EXPLORATION
        monsters.start_spawning()
        closing_door_event = schedule_event(map.close_door, 45 * 10, oneshot=False)


@trigger
class GameOver:
    eligible_states = (PHASE_EXPLORATION, PHASE_RUNAWAY)

    def condition(self):
        return lighting.player_lightning_radius <= 1

    def action(self):
        raise GameOverEx()