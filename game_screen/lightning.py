from pygame import Surface, SRCALPHA, Color
from pygame.rect import Rect

from config import PLAYER_WIDTH, PLAYER_HEIGHT, TILE_WIDTH, ROOM_WIDTH, TILE_HEIGHT, ROOM_HEIGHT

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
