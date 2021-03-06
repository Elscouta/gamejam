import os
import random
from itertools import chain, product
from sys import stdout
from typing import List

import pygame as pg
from pygame import Surface
from pygame.rect import Rect

from asset import get_sprite
from config import MAP_WIDTH, MAP_HEIGHT, ROOM_WIDTH, ROOM_HEIGHT, TILE_WIDTH, TILE_HEIGHT, DOOR_POSITION, SCREEN_WIDTH, \
    SCREEN_HEIGHT, MIN_DISTANCE_WC_BED, MAX_DISTANCE_WC_BED, CLOSING_DOORS_SWAPS, \
    MAX_CLOSING_DOORS
from game_screen.furniture import BPaint, Furniture, GPaint, OPaint
from game_screen.lighting import draw_light_source, get_light_source_dampening
from game_screen.tile import WestWall, SouthWestCorner, WestOpenDoor, NorthOpenDoor, SouthOpenDoor, Floor, \
    NorthEastCorner, \
    EastOpenDoor, \
    SouthEastCorner, EastWall, NorthWall, SouthWall, NorthWestCorner, NorthClosedDoor, SouthClosedDoor, WestClosedDoor, \
    EastClosedDoor, BedsideLamp, BedTop, BedBottom, Tile, PorcelainFloor, PorcelainSouthWall, PorcelainNorthWall, \
    PorcelainEastWall, PorcelainSouthEastCorner, PorcelainNorthEastCorner, PorcelainWestWall, PorcelainSouthWestCorner, \
    PorcelainNorthWestCorner, PorcelainNorthClosedDoor, PorcelainSouthClosedDoor, PorcelainWestClosedDoor, \
    PorcelainEastClosedDoor, PorcelainWestOpenDoor, PorcelainEastOpenDoor, PorcelainSouthOpenDoor, \
    PorcelainNorthOpenDoor

rooms = None
h_edges = None
v_edges = None
initial_room = None
final_room = None
map_surface = None
closing_door_sound = None
closing_door_sequence = None
closed_door_count = 10
light_sources = None

OutsideMap = object()

DIRECTIONS = ['north', 'east', 'south', 'west']


def get_dir(obj, dir):
    assert dir in DIRECTIONS
    return getattr(obj, dir)()


def _outside_map(x, y):
    return x < 0 or x >= MAP_WIDTH or y < 0 or y >= MAP_HEIGHT


class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.distance_to_bed = None
        self.furnitures: List[Furniture] = []

    def replace(self, class_name):
        dtb = self.distance_to_bed
        rooms[self.x][self.y] = class_name(self.x, self.y)
        if dtb is not None:
            rooms[self.x][self.y].distance_to_bed = dtb

    @property
    def rect(self):
        return Rect(self.x * ROOM_WIDTH * TILE_WIDTH, self.y * ROOM_HEIGHT * TILE_HEIGHT,
                    ROOM_WIDTH * TILE_WIDTH, ROOM_HEIGHT * TILE_HEIGHT)

    def north(self):
        return h_edges[self.x][self.y]

    def south(self):
        return h_edges[self.x][self.y + 1]

    def east(self):
        return v_edges[self.x + 1][self.y]

    def west(self):
        return v_edges[self.x][self.y]

    def add_furniture(self, furniture):
        self.furnitures.append(furniture)

    def get_tile(self, tile_x, tile_y) -> List[Tile]:
        furniture_tiles = []
        for f in self.furnitures:
            if f.in_furniture(tile_x, tile_y):
                furniture_tiles.append(f.get_tile(*f.room_coords_to_furniture_coords(tile_x, tile_y)))
                break

        if tile_x == 0:
            if tile_y == 0:
                base_tile = NorthWestCorner
            elif tile_y == DOOR_POSITION:
                base_tile = v_edges[self.x][self.y].get_tile(right=True)
            elif tile_y == ROOM_HEIGHT - 1:
                base_tile = SouthWestCorner
            else:
                base_tile = WestWall
        elif tile_x == DOOR_POSITION:
            if tile_y == 0:
                base_tile = h_edges[self.x][self.y].get_tile(bottom=True)
            elif tile_y == ROOM_HEIGHT - 1:
                base_tile = h_edges[self.x][self.y + 1].get_tile(bottom=False)
            else:
                base_tile = Floor
        elif tile_x == ROOM_WIDTH - 1:
            if tile_y == 0:
                base_tile = NorthEastCorner
            elif tile_y == DOOR_POSITION:
                base_tile = v_edges[self.x + 1][self.y].get_tile(right=False)
            elif tile_y == ROOM_HEIGHT - 1:
                base_tile = SouthEastCorner
            else:
                base_tile = EastWall
        else:
            if tile_y == 0:
                base_tile = NorthWall
            elif tile_y == ROOM_HEIGHT - 1:
                base_tile = SouthWall
            else:
                base_tile = Floor

        return [base_tile] + furniture_tiles

    def __str__(self):
        return '.'

    def __repr__(self):
        return "Room(%s, %s)" % (self.x, self.y)


class Bedroom(Room):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.distance_to_bed = 0

    def get_tile(self, tile_x, tile_y):
        if (tile_x, tile_y) == (1, 0):
            return [BedsideLamp]
        elif (tile_x, tile_y) == (2, 0):
            return [BedTop]
        elif (tile_x, tile_y) == (2, 1):
            return [BedBottom]
        else:
            return super().get_tile(tile_x, tile_y)

    def get_initial_position(self):
        return (self.x * ROOM_WIDTH * TILE_WIDTH + int(2.2 * TILE_WIDTH),
                self.y * ROOM_HEIGHT * TILE_HEIGHT + int(1.8 * TILE_HEIGHT))

    def __str__(self):
        return 'B'

    def __repr__(self):
        return "Bedroom(%s, %s)" % (self.x, self.y)


class WC(Room):
    def __str__(self):
        return 'W'

    def __repr__(self):
        return "WC(%s, %s)" % (self.x, self.y)

    def get_tile(self, tile_x, tile_y) -> List[Tile]:
        furniture_tiles = []
        for f in self.furnitures:
            if f.in_furniture(tile_x, tile_y):
                furniture_tiles.append(f.get_tile(*f.room_coords_to_furniture_coords(tile_x, tile_y)))
                break

        if tile_x == 0:
            if tile_y == 0:
                base_tile = PorcelainNorthWestCorner
            elif tile_y == DOOR_POSITION:
                base_tile = v_edges[self.x][self.y].get_tile(right=True, porcelain=True)
            elif tile_y == ROOM_HEIGHT - 1:
                base_tile = PorcelainSouthWestCorner
            else:
                base_tile = PorcelainWestWall
        elif tile_x == DOOR_POSITION:
            if tile_y == 0:
                base_tile = h_edges[self.x][self.y].get_tile(bottom=True, porcelain=True)
            elif tile_y == ROOM_HEIGHT - 1:
                base_tile = h_edges[self.x][self.y+1].get_tile(bottom=False, porcelain=True)
            else:
                base_tile = PorcelainFloor
        elif tile_x == ROOM_WIDTH - 1:
            if tile_y == 0:
                base_tile = PorcelainNorthEastCorner
            elif tile_y == DOOR_POSITION:
                base_tile = v_edges[self.x+1][self.y].get_tile(right=False, porcelain=True)
            elif tile_y == ROOM_HEIGHT - 1:
                base_tile = PorcelainSouthEastCorner
            else:
                base_tile = PorcelainEastWall
        else:
            if tile_y == 0:
                base_tile = PorcelainNorthWall
            elif tile_y == ROOM_HEIGHT - 1:
                base_tile = PorcelainSouthWall
            else:
                base_tile = PorcelainFloor

        return [base_tile] + furniture_tiles

class Edge:
    HORIZ = 1
    VERT = 2

    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir

    def replace(self, edge_class):
        assert self.dir == Edge.HORIZ or 0 < self.x < MAP_WIDTH
        assert self.dir == Edge.VERT or 0 < self.y < MAP_HEIGHT

        if self.dir == Edge.HORIZ:
            target = h_edges
        elif self.dir == Edge.VERT:
            target = v_edges
        else:
            raise Exception("Unknown dir: %d" % self.dir)

        target[self.x][self.y] = edge_class(self.x, self.y, self.dir)

    def get_pixel_coords(self):
        if self.dir == Edge.HORIZ:
            return int((self.x + 0.5) * ROOM_WIDTH * TILE_WIDTH), self.y * ROOM_HEIGHT * TILE_HEIGHT
        else:
            return self.x * ROOM_WIDTH * TILE_WIDTH, int((self.y + 0.5) * ROOM_HEIGHT * TILE_HEIGHT)

    def north(self):
        assert self.dir == Edge.HORIZ
        if _outside_map(self.x, self.y - 1):
            return OutsideMap
        return rooms[self.x][self.y - 1]

    def south(self):
        assert self.dir == Edge.HORIZ
        if _outside_map(self.x, self.y):
            return OutsideMap
        return rooms[self.x][self.y]

    def east(self):
        assert self.dir == Edge.VERT
        if _outside_map(self.x, self.y):
            return OutsideMap
        return rooms[self.x][self.y]

    def west(self):
        assert self.dir == Edge.VERT
        if _outside_map(self.x - 1, self.y):
            return OutsideMap
        return rooms[self.x - 1][self.y]


class Wall(Edge):
    passable = False

    def __str__(self):
        return '+'

    def get_tile(self, bottom=None, right=None, porcelain=False):
        if self.dir == Edge.HORIZ:
            assert bottom is not None

            if bottom:
                return PorcelainNorthWall if porcelain else NorthWall
            else:
                return PorcelainSouthWall if porcelain else SouthWall

        else:
            assert right is not None

            if right:
                return PorcelainWestWall if porcelain else WestWall
            else:
                return PorcelainEastWall if porcelain else EastWall


class ClosedDoor(Edge):
    passable = False

    def get_tile(self, bottom=None, right=None, porcelain=False):
        if self.dir == Edge.HORIZ:
            assert bottom is not None

            if bottom:
                return PorcelainNorthClosedDoor if porcelain else NorthClosedDoor
            else:
                return PorcelainSouthClosedDoor if porcelain else SouthClosedDoor

        else:
            assert right is not None

            if right:
                return PorcelainWestClosedDoor if porcelain else WestClosedDoor
            else:
                return PorcelainEastClosedDoor if porcelain else EastClosedDoor

    def __str__(self):
        if self.dir == Edge.HORIZ:
            return '-'
        elif self.dir == Edge.VERT:
            return '|'
        else:
            raise Exception("Unknown dir: %d" % self.dir)


def ClosingDoor(closing_priority):
    class _ClosingDoor(Edge):
        @property
        def passable(self):
            return self.visible_state.passable

        @property
        def visible_state(self):
            if self.closing_priority >= closed_door_count:
                return OpenDoor(self.x, self.y, self.dir)
            else:
                return ClosedDoor(self.x, self.y, self.dir)

        def get_tile(self, *args, **kwargs):
            return self.visible_state.get_tile(*args, **kwargs)

        def __init__(self, x, y, dir):
            super().__init__(x, y, dir)
            self.closing_priority = closing_priority

        def __str__(self):
            return str(self.visible_state)

    return _ClosingDoor


class OpenDoor(Edge):
    passable = True

    def __str__(self):
        return ' '

    def get_tile(self, bottom=None, right=None, porcelain=False):
        if self.dir == Edge.HORIZ:
            assert bottom is not None

            if bottom:
                return PorcelainNorthOpenDoor if porcelain else NorthOpenDoor
            else:
                return PorcelainSouthOpenDoor if porcelain else SouthOpenDoor

        else:
            assert right is not None

            if right:
                return PorcelainWestOpenDoor if porcelain else WestOpenDoor
            else:
                return PorcelainEastOpenDoor if porcelain else EastOpenDoor


class MapCreationFailed(Exception):
    pass


def _fill_initial_surface():
    global map_surface

    map_surface = Surface((MAP_WIDTH * ROOM_WIDTH * TILE_WIDTH, MAP_HEIGHT * ROOM_HEIGHT * TILE_HEIGHT))
    room_x = 0

    for room_i in range(0, MAP_WIDTH):
        room_y = 0

        for room_j in range(0, MAP_HEIGHT):
            for tile_i in range(0, ROOM_WIDTH):
                for tile_j in range(0, ROOM_HEIGHT):
                    x_coord = room_x + tile_i * TILE_WIDTH
                    y_coord = room_y + tile_j * TILE_HEIGHT
                    for t in rooms[room_i][room_j].get_tile(tile_i, tile_j):
                        map_surface.blit(get_sprite(t.sprite_id), (x_coord, y_coord))

            room_y += ROOM_HEIGHT * TILE_HEIGHT
        room_x += ROOM_WIDTH * TILE_WIDTH


def _replace_door_bitmap():
    global map_surface
    global closed_door_count
    global closing_door_sequence

    newly_closed_door: Edge = closing_door_sequence[closed_door_count - 1]

    if newly_closed_door.dir == Edge.VERT:
        for i in range(-1, 1):
            room: Room = rooms[newly_closed_door.x + i][newly_closed_door.y]
            tile_i = 6 if i == -1 else 0
            tile_j = DOOR_POSITION
            for tile in room.get_tile(tile_i, tile_j):
                sprite_id = tile.sprite_id
                x_coord = (room.x * ROOM_WIDTH * TILE_WIDTH) + tile_i * TILE_WIDTH
                y_coord = (room.y * ROOM_HEIGHT * TILE_HEIGHT) + tile_j * TILE_HEIGHT
                map_surface.blit(get_sprite(sprite_id), (x_coord, y_coord))

    if newly_closed_door.dir == Edge.HORIZ:
        for i in range(-1, 1):
            room: Room = rooms[newly_closed_door.x][newly_closed_door.y + i]
            tile_i = DOOR_POSITION
            tile_j = 6 if i == -1 else 0
            for tile in room.get_tile(tile_i, tile_j):
                sprite_id = tile.sprite_id
                x_coord = (room.x * ROOM_WIDTH * TILE_WIDTH) + tile_i * TILE_WIDTH
                y_coord = (room.y * ROOM_HEIGHT * TILE_HEIGHT) + tile_j * TILE_HEIGHT
                map_surface.blit(get_sprite(sprite_id), (x_coord, y_coord))


def _determine_initial_room():
    global initial_room

    x = random.choice(tuple(range(0, MAP_WIDTH)))
    y = random.choice(tuple(range(0, MAP_HEIGHT)))

    rooms[x][y].replace(Bedroom)
    initial_room = rooms[x][y]


def _bfs_scan_creation():
    global closing_door_sequence, final_room
    closing_door_sequence = []

    wc_candidates = []
    first_room_candidates = []

    # 1 -- Breadth First Search
    queue = []
    visited = set()
    queue.append(initial_room)

    while queue:
        room, queue = queue[0], queue[1:]
        visited.add(room)

        if MIN_DISTANCE_WC_BED <= room.distance_to_bed <= MAX_DISTANCE_WC_BED:
            wc_candidates.append(room)

        if room.distance_to_bed == 1:
            first_room_candidates.append(room)

        for d in DIRECTIONS:
            edge = get_dir(room, d)
            adj_room = get_dir(edge, d)

            if adj_room == OutsideMap:
                continue

            if not edge.passable:
                closing_door_sequence.append(edge)
            else:
                if adj_room not in visited:
                    queue.append(adj_room)
                    visited.add(adj_room)
                    adj_room.distance_to_bed = room.distance_to_bed + 1

    # 2 -- Determine final room (WC Room)
    if not wc_candidates:
        raise MapCreationFailed('No candidates for final room.')
    final_room = random.choice(wc_candidates)
    final_room.replace(WC)
    final_room = rooms[final_room.x][final_room.y]

    # Add paint to the an adjacent room
    adjacent_room = random.choice(first_room_candidates)
    adjacent_room.add_furniture(BPaint(1, 4))

    # 3 -- Determine the closing door sequence
    closing_doors_count = len(closing_door_sequence)
    for _ in range(0, CLOSING_DOORS_SWAPS):
        i = random.choice(tuple(range(0, closing_doors_count)))
        j = random.choice(tuple(range(0, closing_doors_count)))

        if i != j:
            closing_door_sequence[i], closing_door_sequence[j] = closing_door_sequence[j], closing_door_sequence[i]

    for i in range(0, min(closing_doors_count, MAX_CLOSING_DOORS)):
        closing_door_sequence[i].replace(ClosingDoor(i))
        if closing_door_sequence[i].dir == Edge.HORIZ:
            closing_door_sequence[i] = h_edges[closing_door_sequence[i].x][closing_door_sequence[i].y]
        if closing_door_sequence[i].dir == Edge.VERT:
            closing_door_sequence[i] = v_edges[closing_door_sequence[i].x][closing_door_sequence[i].y]


def _init_sound():
    global closing_door_sound
    closing_door_sound = pg.mixer.Sound(os.path.join('assets', 'sfx_footsteps.wav'))


def _create():
    global rooms, h_edges, v_edges

    rooms = [
        [
            Room(i, j) for j in range(0, MAP_HEIGHT)
        ]
        for i in range(0, MAP_WIDTH)
    ]

    h_edges = [
        [
            Wall(i, j, dir=Edge.HORIZ) for j in range(0, MAP_HEIGHT + 1)
        ]
        for i in range(0, MAP_WIDTH)
    ]

    v_edges = [
        [
            Wall(i, j, dir=Edge.VERT) for j in range(0, MAP_HEIGHT)
        ]
        for i in range(0, MAP_WIDTH + 1)
    ]

    def _get_component(r):
        if r == OutsideMap:
            return OutsideMap
        return [c for c in connex_components if r in c][0]

    connex_components = {frozenset((rooms[i][j],)) for (i, j) in product(range(0, MAP_WIDTH),
                                                                         range(0, MAP_HEIGHT))}
    connex_edges = {
        c: {
            (list(c)[0], dir): _get_component(get_dir(get_dir(list(c)[0], dir), dir))
            for dir in DIRECTIONS
        }
        for c in connex_components
    }

    while len(connex_components) > 1:
        c1 = random.choice(tuple(connex_components))
        room, dir = random.choice(tuple(connex_edges[c1].keys()))

        edge = get_dir(room, dir)
        adj_room = get_dir(edge, dir)

        if adj_room == OutsideMap:
            continue

        c2 = _get_component(adj_room)

        assert c1 != c2

        edge.replace(OpenDoor)

        connex_components.remove(c1)
        connex_components.remove(c2)
        merged_c = frozenset.union(c1, c2)
        connex_components.add(merged_c)

        for c in connex_edges:
            for (room, dir), cc in connex_edges[c].items():
                if cc in (c1, c2):
                    connex_edges[c][room, dir] = merged_c

        connex_edges[merged_c] = {
            (room, dir): cc
            for ((room, dir), cc) in chain(connex_edges[c1].items(), connex_edges[c2].items())
            if cc != merged_c
        }


def _position_light_sources():
    global light_sources

    light_sources = []
    light_sources.append((initial_room.x * ROOM_WIDTH * TILE_WIDTH + 96,
                          initial_room.y * ROOM_HEIGHT * TILE_HEIGHT + 36,
                          128))
    x = final_room.x * ROOM_WIDTH * TILE_WIDTH + 228
    y = final_room.y * ROOM_WIDTH * TILE_WIDTH + 228
    light_sources.append((x, y, 278))

    for d in DIRECTIONS:
        edge = get_dir(final_room, d)
        if edge.passable:
            x, y = edge.get_pixel_coords()
            light_sources.append((x, y, 96))


def _position_furniture():
    for f in [BPaint, OPaint, OPaint, GPaint, GPaint] * 4:
        x = random.randint(0, MAP_WIDTH-1)
        y = random.randint(0, MAP_HEIGHT-1)

        if rooms[x][y] in (initial_room, final_room):
            continue

        if rooms[x][y].furnitures:
            continue

        i = random.randint(1, 4)
        j = random.randint(1, 4)
        rooms[x][y].add_furniture(f(i, j))


def init():
    _create()
    _init_sound()
    _determine_initial_room()
    _bfs_scan_creation()
    _position_furniture()
    _fill_initial_surface()
    _position_light_sources()


def draw(screen, light_mask):
    screen.blit(map_surface, to_screen_coords(0, 0))
    for source_x, source_y, source_radius in light_sources:
        damp = get_light_source_dampening(source_x, source_y)
        if not damp:
            continue

        draw_light_source(light_mask, source_x, source_y, int(source_radius*damp))


def close_door():
    global closed_door_count
    global closing_door_sound
    closed_door_count += 1
    _replace_door_bitmap()
    pg.mixer.Channel(2).play(closing_door_sound)


def get_room(coord_x, coord_y):
    return rooms[int(coord_x) // (ROOM_WIDTH * TILE_WIDTH)][int(coord_y) // (ROOM_HEIGHT * TILE_HEIGHT)]


def get_tile(player_x, player_y) -> List[Tile]:
    room = get_room(player_x, player_y)

    tile_x = (player_x % (ROOM_WIDTH * TILE_WIDTH)) // TILE_WIDTH
    tile_y = (player_y % (ROOM_HEIGHT * TILE_HEIGHT)) // TILE_HEIGHT
    return room.get_tile(tile_x, tile_y)


def random_point():
    return random.randint(0, MAP_WIDTH * ROOM_WIDTH * TILE_WIDTH), random.randint(0,
                                                                                  MAP_HEIGHT * ROOM_HEIGHT * TILE_HEIGHT)


def to_screen_coords(*args):
    from game_screen import player

    if isinstance(args[0], Rect):
        return args[0].move(SCREEN_WIDTH / 2 - player.get_x(),
                            SCREEN_HEIGHT / 2 - player.get_y())

    assert len(args) == 2
    return args[0] + (SCREEN_WIDTH / 2 - player.get_x()), args[1] + SCREEN_HEIGHT / 2 - player.get_y()


def print_map():
    for j in range(0, MAP_HEIGHT):
        for i in range(0, MAP_WIDTH):
            stdout.write('+')
            stdout.write('%s' % h_edges[i][j])
        stdout.write('+\n')

        for i in range(0, MAP_WIDTH):
            stdout.write('%s' % v_edges[i][j])
            stdout.write('%s' % rooms[i][j])
        stdout.write('%s\n' % v_edges[MAP_WIDTH][j])

    for i in range(0, MAP_WIDTH):
        stdout.write('+')
        stdout.write('%s' % h_edges[i][MAP_HEIGHT])
    stdout.write('+\n')
