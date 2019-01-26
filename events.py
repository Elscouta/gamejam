from pygame.constants import USEREVENT, NUMEVENTS
from pygame.time import set_timer

_events = set()

class Event:
    def __init__(self, callback, oneshot, timer):
        self.callback = callback
        self.oneshot = oneshot
        self.original_timer = timer
        self.remaining_timer = timer

def schedule_event(callback, timer_in_ticks, oneshot=True):
    event = Event(callback, oneshot=oneshot, timer=timer_in_ticks)
    _events.add(event)

def clear_event(event):
    _events.remove(event)

def tick():
    for event in _events.copy():
        event.remaining_timer -= 1
        if event.remaining_timer <= 0:
            event.callback()
            if event.oneshot:
                clear_event(event)
            else:
                event.remaining_timer = event.original_timer

def init():
    set_timer(USEREVENT, 100)