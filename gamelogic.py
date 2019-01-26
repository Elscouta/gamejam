from pygame.rect import Rect

from config import PLAYER_WIDTH, PLAYER_HEIGHT

lightning_radius = 128

def get_player_light_area(player_x, player_y):
    return Rect(player_x - lightning_radius + PLAYER_WIDTH / 2,
                player_y - lightning_radius + PLAYER_HEIGHT / 2,
                2*lightning_radius,
                2*lightning_radius)

def tick():
    pass