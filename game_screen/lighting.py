from pygame import Surface, SRCALPHA, Color, BLEND_RGBA_MIN
from pygame.rect import Rect

from config import PLAYER_WIDTH, PLAYER_HEIGHT, TILE_WIDTH, ROOM_WIDTH, TILE_HEIGHT, ROOM_HEIGHT
from game_screen.asset import get_light_halo
from utils import distance

lightning_radius = 128


def get_light_area(source_x, source_y, source_radius):
    return Rect(source_x - source_radius, source_y - source_radius,
                2*source_radius, 2*source_radius)

def get_player_light_area(player_x, player_y):
    return get_light_area(player_x + PLAYER_WIDTH / 2, player_y + PLAYER_HEIGHT / 2, lightning_radius)

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

def draw_light_source(light_mask, source_x, source_y, source_radius):
    from game_screen import map

    halo = get_light_halo(source_radius)
    room = map.get_room(source_x, source_y)
    clipped_halo = clip_light_halo_by_room(halo, room, source_x, source_y, source_radius)
    light_mask.blit(clipped_halo, map.to_screen_coords(get_light_area(source_x, source_y, source_radius)),
                    special_flags=BLEND_RGBA_MIN)

    for d in map.DIRECTIONS:
        edge = map.get_dir(room, d)
        if not edge.passable:
            continue

        edge_x, edge_y = edge.get_pixel_coords()
        edge_dist = distance((edge_x, edge_y), (source_x, source_y))

        if edge_dist > source_radius:
            continue

        secondary_radius = source_radius - edge_dist
        secondary_halo = get_light_halo(int(secondary_radius))
        clipped_halo = clip_light_halo_by_room(secondary_halo, map.get_dir(edge, d),
                                               edge_x, edge_y, secondary_radius)
        light_mask.blit(clipped_halo, map.to_screen_coords(get_light_area(edge_x, edge_y, secondary_radius)),
                         special_flags=BLEND_RGBA_MIN)
