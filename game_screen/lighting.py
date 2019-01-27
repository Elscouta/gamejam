from pygame import Surface, SRCALPHA, Color, BLEND_RGBA_MIN
from pygame.rect import Rect

from config import PLAYER_WIDTH, PLAYER_HEIGHT, TILE_WIDTH, ROOM_WIDTH, TILE_HEIGHT, ROOM_HEIGHT
from events import schedule_event
from asset import get_light_halo
from utils import distance

player_lightning_radius = 192


def get_light_area(source_x, source_y, source_radius):
    return Rect(source_x - source_radius, source_y - source_radius,
                2*source_radius, 2*source_radius)


def get_player_light_area(player_x, player_y):
    return get_light_area(player_x + PLAYER_WIDTH / 2, player_y + PLAYER_HEIGHT / 2, player_lightning_radius)


def clip_light_halo_by_room(halo, room, source_x, source_y, source_radius):
    room_mask = Surface((halo.get_width(), halo.get_height()), flags=SRCALPHA)
    room_mask.fill(Color(0, 0, 0))

    left = max(room.x * ROOM_WIDTH * TILE_WIDTH - (source_x - source_radius), 0)
    top = max(room.y * ROOM_HEIGHT * TILE_HEIGHT - (source_y - source_radius), 0)
    right = (room.x+1) * ROOM_WIDTH * TILE_WIDTH - (source_x - source_radius)
    bottom = (room.y+1) * ROOM_HEIGHT * TILE_HEIGHT - (source_y - source_radius)

    room_relative_to_halo = Rect(left, top, right-left, bottom-top)
    room_mask.fill(Color(0, 0, 0, 0), rect=room_relative_to_halo)
    clipped_halo = halo.copy()
    clipped_halo.blit(room_mask, dest=(0, 0))

    return clipped_halo

def get_light_source_dampening(source_x, source_y):
    from game_screen import map, player

    sroom = map.get_room(source_x, source_y)
    proom = map.get_room(*player.get_pos())

    if sroom == proom:
        return 1
    elif sroom.x == proom.x and sroom.y > proom.y:
        dir = 'north'
        length = sroom.y - proom.y
        c1 = source_x
        c2 = player.get_x()
        c = sroom.x * TILE_WIDTH * ROOM_WIDTH + 228
    elif sroom.x == proom.x and sroom.y < proom.y:
        dir = 'south'
        length = proom.y - sroom.y
        c1 = source_x
        c2 = player.get_x()
        c = sroom.x * TILE_WIDTH * ROOM_WIDTH + 228
    elif sroom.y == proom.y and sroom.x > proom.x:
        dir = 'east'
        length = sroom.x - proom.x
        c1 = source_y
        c2 = player.get_y()
        c = sroom.y * TILE_WIDTH * ROOM_WIDTH + 228
    elif sroom.y == proom.y and sroom.x < proom.x:
        dir = 'west'
        length = proom.x - sroom.x
        c1 = source_y
        c2 = player.get_y()
        c = sroom.y * TILE_WIDTH * ROOM_WIDTH + 228
    else:
        return 0

    if length >= 3:
        return 0

    croom = proom
    while croom != sroom:
        if not map.get_dir(croom, dir).passable:
            return 0
        croom = map.get_dir(map.get_dir(croom, dir), dir)

    damp = 0.75
    if length >= 1:
        damp *= 1 - 0.5 * abs(2*c - c1 - c2) / (ROOM_WIDTH * TILE_WIDTH)

    if length >= 2:
        damp *= 0.75
        damp *= 1 - 0.30 * abs(3*c - 2 * c1 - c2) / (ROOM_WIDTH * TILE_WIDTH)
        damp *= 1 - 0.30 * abs(3*c - c1 - 2 * c2) / (ROOM_WIDTH * TILE_WIDTH)

    return damp

def draw_light_source(light_mask, source_x, source_y, source_radius):
    from game_screen import map

    halo = get_light_halo(source_radius)
    room = map.get_room(source_x, source_y)
    light_mask.set_clip(map.to_screen_coords(room.rect))
    light_mask.blit(halo, map.to_screen_coords(get_light_area(source_x, source_y, source_radius)),
                    special_flags=BLEND_RGBA_MIN)
    light_mask.set_clip(None)

    for d in map.DIRECTIONS:
        edge = map.get_dir(room, d)
        if not edge.passable:
            continue

        edge_x, edge_y = edge.get_pixel_coords()
        edge_dist = distance((edge_x, edge_y), (source_x, source_y))

        if edge_dist > source_radius:
            continue

        adj_room = map.get_dir(edge, d)
        secondary_radius = source_radius - edge_dist
        secondary_halo = get_light_halo(int(secondary_radius))
        light_mask.set_clip(map.to_screen_coords(adj_room.rect))
        light_mask.blit(secondary_halo, map.to_screen_coords(get_light_area(edge_x, edge_y, secondary_radius)),
                         special_flags=BLEND_RGBA_MIN)
        light_mask.set_clip(None)


def reduce_player_light(impact=1):
    global player_lightning_radius
    player_lightning_radius -= impact
    if player_lightning_radius < 1:
        player_lightning_radius = 1


def decay_player_extra_light():
    global player_lightning_radius
    from game_screen import logic

    if not logic.is_player_safe() and player_lightning_radius > 128:
        player_lightning_radius = int(0.9 * player_lightning_radius)


def rotate_lights():
    pass


def init():
    schedule_event(rotate_lights, 1, oneshot=False)
    schedule_event(reduce_player_light, 30, oneshot=False)
    schedule_event(decay_player_extra_light, 1, oneshot=False)
