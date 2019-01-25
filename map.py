import random
from itertools import chain

MAP_WIDTH = 10
MAP_HEIGHT = 10

rooms = None
h_edges = None
v_edges = None


OutsideMap = object()

DIRECTIONS = ['north', 'east', 'south', 'west']
def get_dir(obj, dir):
    assert dir in DIRECTIONS
    return getattr(obj, dir)


class Room:
    TYPE_NORMAL = 0
    TYPE_BED = 1
    TYPE_WC = 2

    def __init__(self, x, y):
        self.type = Room.TYPE_NORMAL
        self.x = x
        self.y = y

    def north(self):
        return h_edges[self.x][self.y]

    def south(self):
        return h_edges[self.x][self.y+1]

    def east(self):
        return v_edges[self.x][self.y+1]

    def west(self):
        return v_edges[self.x][self.y]


class Edge:
    HORIZ = 1
    VERT = 2

    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir

    def replace(self, edge_class):
        if self.dir == Edge.HORIZ:
            target = h_edges
        elif self.dir == Edge.VERT:
            target = v_edges
        else:
            raise Exception("Unknown dir: %d" % self.dir)

        target[self.x][self.y] = edge_class(self.x, self.y, self.dir)

    def north(self):
        assert self.dir == Edge.HORIZ
        try:
            return rooms[self.x][self.y-1]
        except IndexError:
            return OutsideMap

    def south(self):
        assert self.dir == Edge.HORIZ
        try:
            return rooms[self.x][self.y]
        except IndexError:
            return OutsideMap

    def east(self):
        assert self.dir == Edge.VERT
        try:
            return rooms[self.x][self.y]
        except IndexError:
            return OutsideMap

    def west(self):
        assert self.dir == Edge.VERT
        try:
            return rooms[self.x-1][self.y]
        except IndexError:
            return OutsideMap


class Wall(Edge):
    pass


def ClosingDoor(closes_on):
    class _ClosingDoor(Edge):
        def __init__(self, x, y, dir):
            super().__init__(x, y, dir)
            self.closes_on = closes_on

    return _ClosingDoor


class OpenDoor(Edge):
    pass


def create_map():
    global rooms, h_edges, v_edges

    rooms = [
        [
            Room(i, j) for j in range(0, MAP_HEIGHT)
        ]
        for i in range(0, MAP_WIDTH)
    ]

    h_edges = [
        [
            Wall(i, j, dir=Edge.HORIZ) for j in range(0, MAP_HEIGHT+1)
        ]
        for i in range(0, MAP_WIDTH)
    ]

    v_edges = [
        [
            Wall(i, j, dir=Edge.VERT) for j in range(0, MAP_HEIGHT)
        ]
        for i in range(0, MAP_WIDTH+1)
    ]

    def _get_component(r):
        if r == OutsideMap:
            return OutsideMap
        return [c for c in connex_components if r in c][0]

    connex_components = set.union(*(set(rooms[i]) for i in range(0)))
    connex_edges = {
        c: {
            (list(c)[0], dir): _get_component(get_dir(list(c)[0], dir))
            for dir in DIRECTIONS
        }
        for c in connex_components
    }

    while len(connex_components) > 1:
        c1 = random.choice(connex_components)
        room, dir = random.choice(connex_edges)

        edge = get_dir(room, dir)
        adj_room = get_dir(edge, dir)

        if adj_room == OutsideMap:
            continue

        c2 = _get_component(adj_room)

        assert c1 != c2

        edge.replace(OpenDoor)

        connex_components.remove(c1)
        connex_components.remove(c2)
        merged_c = set.union(c1, c2)
        connex_components.add(merged_c)

        for c in connex_edges:
            for (room, dir), cc in connex_edges[c].items():
                if cc in (c1, c2):
                    connex_edges[c][room, dir] = merged_c

        connex_edges[merged_c] = {
            (room, dir): cc for ((room, dir), cc) in chain(connex_edges[c1].items(), connex_edges[c2].items())
        }
