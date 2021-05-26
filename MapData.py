from enum import Enum, unique

all_quadrants = {0, 1, 2, 3}
left_side = {0, 2}
right_side = {1, 3}
top_side = {0, 1}
bottom_side = {2, 3}

grid_size = 10


class GridMap(object):

    def __init__(self):
        self.nodeMap = {}
        self.maxHeight, self.minHeight = None, None
        self.maxWidth, self.minWidth = None, None
        self.door_map = {}
        self.tileIndices = {}

    def add_node(self, position, node):
        self.nodeMap[position] = node
        self.maxWidth = max(position[0]+1, self.maxWidth) if self.maxWidth is not None else position[0]+1
        self.minWidth = min(position[0], self.minWidth) if self.minWidth is not None else position[0]
        self.maxHeight = max(position[1]+1, self.maxHeight) if self.maxHeight is not None else position[1]+1
        self.minHeight = min(position[1], self.minHeight) if self.minHeight is not None else position[1]
        if node.door:
            self.door_map[node.door] = position
        return self

    @staticmethod
    def match_items(room_piece, match_point, match_door):
        match_pos, match_node = next(((p, n) for (p, n) in room_piece.nodeMap.items() if n.door == match_door))
        shift = match_point[0]-match_pos[0], match_point[1]-match_pos[1]
        return shift, match_node

    def check_for_collisions(self, room_piece, shift, match_node, current_pos):
        for pos, node in room_piece.nodeMap.items():
            if node == match_node:
                continue
            check_point = pos[0] + shift[0], pos[1] + shift[1]
            if check_point == current_pos:
                continue
            if check_point in self.nodeMap:
                return True  # todo: partial reserved check could go here.
        # check if box would be too large
        max_h = max(self.maxHeight, room_piece.maxHeight + shift[1])
        min_h = min(self.minHeight, room_piece.minHeight + shift[1])
        if max_h - min_h > grid_size:
            return True
        max_w = max(self.maxWidth, room_piece.maxWidth + shift[0])
        min_w = min(self.minWidth, room_piece.minWidth + shift[0])
        if max_w - min_w > grid_size:
            return True
        return False  # no collisions

    def merge_map(self, room_piece, shift, match_node):
        for pos, node in room_piece.nodeMap.items():
            if node == match_node:
                continue
            check_point = pos[0] + shift[0], pos[1] + shift[1]
            self.add_node(check_point, node)
        for index, quad_set in room_piece.tileIndices.items():
            if index in self.tileIndices:
                self.tileIndices[index].update(quad_set)
            else:
                self.tileIndices[index] = quad_set

    def can_add(self, other_floor):
        t_width = other_floor.width() + 1
        t_height = other_floor.height() + 1
        if self.width() + t_width <= grid_size:
            return self.maxWidth + 1 - other_floor.minWidth, self.minHeight - other_floor.minHeight
        if self.height() + t_height <= grid_size:
            return self.minWidth - other_floor.minWidth, self.maxHeight + 1 - other_floor.minHeight
        # naive brute force algorithm
        # python solution @ https://stackoverflow.com/questions/2478447
        # /find-largest-rectangle-containing-only-zeros-in-an-n%c3%97n-binary-matrix/4671342#4671342
        search_width = self.minWidth + grid_size
        search_height = self.minHeight + grid_size
        area_max = (0, ())
        h = {}
        w = {}
        for x in range(self.minWidth, search_width):
            for y in range(self.minHeight, search_height):
                if (x, y) in self.nodeMap:
                    h[(x, y)] = 0
                    w[(x, y)] = 0
                    continue
                if x == self.minWidth:
                    h[(x, y)] = 1
                else:
                    h[(x, y)] = h[(x-1, y)] + 1
                if y == self.minHeight:
                    w[(x, y)] = 1
                else:
                    w[(x, y)] = w[(x, y-1)] + 1
                min_w = w[(x, y)]
                for dh in range(h[(x, y)]):
                    min_w = min(min_w, w[(x-dh, y)])
                    area = (dh + 1) * min_w
                    if area > area_max[0]:
                        area_max = (area, (x-dh, y-min_w+1, x, y))
        x, y, z, w = area_max[1]
        if z - x + 1 >= t_width and w - y + 1 >= t_height:
            return x - other_floor.minWidth + 1, y - other_floor.minHeight + 1
        return None

    def height(self):
        return self.maxHeight - self.minHeight

    def width(self):
        return self.maxWidth - self.minWidth


@unique
class NodeType(Enum):
    Quad = 0
    Entrance = 1
    Reserved = 2
    PartialReserved = 3
    Connector = 4
    Empty = 5


class GridNode(object):
    def __init__(self, image, node_type, door=None):
        self.image = image
        self.type = node_type
        self.door = door


def empty_sector():
    return GridMap()


def sector(indices):
    gm = GridMap()
    for index, l in indices.items():
        gm.tileIndices[index] = set(l)
    return gm


region_to_rooms = {}


def init_map_data():
    init_hc()
    init_eastern()  # todo
    init_desert()  # todo
    init_hera()  # todo
    init_aga_tower()
    init_pod()  # todo


def init_hc():
    region_to_rooms['Hyrule Castle Lobby'] = (
        sector({0x61: all_quadrants})
        .add_node((0, 1),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle Lobby WN'))
        .add_node((0, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle Lobby W'))
        .add_node((1, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle Lobby North Stairs'))
        .add_node((1, 1), GridNode('97-0.png', NodeType.Quad))
        .add_node((1, 2), GridNode('97-2.png', NodeType.Quad))
        .add_node((1, 3),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle Lobby S'))
        .add_node((2, 1), GridNode('97-1.png', NodeType.Quad))
        .add_node((2, 2), GridNode('97-3.png', NodeType.Quad))
        .add_node((3, 1),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle Lobby E')))
    region_to_rooms['Hyrule Castle East Lobby'] = (
        sector({0x62: all_quadrants})
        .add_node((0, 1),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle East Lobby W'))
        .add_node((1, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle East Lobby NW'))
        .add_node((1, 1), GridNode('98-0.png', NodeType.Quad))
        .add_node((1, 2), GridNode('98-2.png', NodeType.Quad))
        .add_node((1, 3),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle East Lobby S'))
        .add_node((2, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle East Lobby N'))
        .add_node((2, 1), GridNode('98-1.png', NodeType.Quad))
        .add_node((2, 2), GridNode('98-3.png', NodeType.Quad)))
    region_to_rooms['Hyrule Castle West Lobby'] = (
        sector({0x60: right_side})
        .add_node((0, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle West Lobby N'))
        .add_node((0, 1), GridNode('96-1.png', NodeType.Quad))
        .add_node((0, 2), GridNode('96-3.png', NodeType.Quad))
        .add_node((0, 3),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle West Lobby S'))
        .add_node((1, 1),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle West Lobby EN'))
        .add_node((1, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle West Lobby E')))
    region_to_rooms['Hyrule Castle East Hall'] = (
        sector({0x52: {0, 2, 3}})
        .add_node((0, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle East Hall W'))
        .add_node((1, 0), GridNode('82-0.png', NodeType.Quad))
        .add_node((1, 1), GridNode('82-2.png', NodeType.Quad))
        .add_node((1, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle East Hall SW'))
        .add_node((2, 1), GridNode('82-3.png', NodeType.Quad))
        .add_node((2, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle East Hall S')))
    region_to_rooms['Hyrule Castle West Hall'] = (
        sector({0x50: right_side})
        .add_node((0, 0), GridNode('80-1.png', NodeType.Quad))
        .add_node((0, 1), GridNode('80-3.png', NodeType.Quad))
        .add_node((0, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle West Hall S'))
        .add_node((1, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle West Hall E')))
    region_to_rooms['Hyrule Castle Back Hall'] = (
        sector({0x01: top_side})
        .add_node((0, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle Back Hall W'))
        .add_node((1, 0), GridNode('1-0.png', NodeType.Quad))
        .add_node((2, 0), GridNode('1-1.png', NodeType.Quad))
        .add_node((3, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle Back Hall E')))
    hc_72_tile = (
        sector({0x72: all_quadrants})
        .add_node((0, 0), GridNode('114-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('114-2.png', NodeType.Quad))
        .add_node((0, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Dungeon North Abyss South Edge'))
        .add_node((1, 0), GridNode('114-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('114-3.png', NodeType.Quad)))
    region_to_rooms['Hyrule Dungeon Map Room'] = hc_72_tile
    region_to_rooms['Hyrule Dungeon North Abyss'] = hc_72_tile
    region_to_rooms['Hyrule Dungeon North Abyss Catwalk'] = hc_72_tile
    region_to_rooms['Hyrule Dungeon South Abyss'] = (
        sector({0x82: all_quadrants})
        .add_node((0, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Dungeon South Abyss West Edge'))
        .add_node((1, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Dungeon South Abyss North Edge'))
        .add_node((1, 1), GridNode('130-0.png', NodeType.Quad))
        .add_node((1, 2), GridNode('130-2.png', NodeType.Quad))
        .add_node((2, 1), GridNode('130-1.png', NodeType.Quad))
        .add_node((2, 2), GridNode('130-3.png', NodeType.Quad)))
    region_to_rooms['Hyrule Dungeon South Abyss Catwalk'] = (
        sector({0x82: {0}})
        .add_node((0, 1),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Dungeon South Abyss Catwalk West Edge'))
        .add_node((1, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Dungeon South Abyss Catwalk North Edge'))
        .add_node((1, 1), GridNode('130-0.png', NodeType.Quad)))
    region_to_rooms['Hyrule Dungeon Guardroom'] = (
        sector({0x81: all_quadrants})
        .add_node((0, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Dungeon Guardroom N'))
        .add_node((0, 1), GridNode('129-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('129-2.png', NodeType.Quad))
        .add_node((1, 1), GridNode('129-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('129-3.png', NodeType.Quad))
        .add_node((2, 1),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Dungeon Guardroom Catwalk Edge'))
        .add_node((2, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Dungeon Guardroom Abyss Edge')))
    hc_71_tile = (
        sector({0x71: {0, 2, 3}})
        .add_node((0, 0), GridNode('113-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('113-2.png', NodeType.Quad))
        .add_node((0, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Dungeon Guardroom Catwalk Edge'))
        .add_node((1, 1), GridNode('113-3.png', NodeType.Quad)))
    region_to_rooms['Hyrule Dungeon Armory Main'] = hc_71_tile
    region_to_rooms['Hyrule Dungeon Armory North Branch'] = hc_71_tile
    region_to_rooms['Hyrule Dungeon Staircase'] = (
        sector({0x70: {0}}).add_node((0, 0), GridNode('112-0.png', NodeType.Quad)))
    region_to_rooms['Hyrule Dungeon Cellblock'] = (
        sector({0x80: top_side}).add_node((0, 0), GridNode('128-0.png', NodeType.Quad))
        .add_node((1, 0), GridNode('128-1.png', NodeType.Quad)))
    hc_51_tile = (
        sector({0x51: all_quadrants})
        .add_node((0, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle Throne Room N'))
        .add_node((0, 1), GridNode('81-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('81-2.png', NodeType.Quad))
        .add_node((0, 3),  GridNode('empty-tile.png', NodeType.Reserved, 'Hyrule Castle Throne Room South Stairs'))
        .add_node((1, 1), GridNode('81-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('81-3.png', NodeType.Quad)))
    region_to_rooms['Hyrule Castle Throne Room'] = hc_51_tile
    region_to_rooms['Hyrule Castle Behind Tapestry'] = hc_51_tile
    region_to_rooms['Sewers Behind Tapestry'] = (
        sector({0x41: all_quadrants})
        .add_node((0, 0), GridNode('65-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('65-2.png', NodeType.Quad))
        .add_node((0, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Sewers Behind Tapestry S'))
        .add_node((1, 0), GridNode('65-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('65-3.png', NodeType.Quad)))
    region_to_rooms['Sewers Rope Room'] = (
        sector({0x42: top_side})
        .add_node((0, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Sewers Rope Room North Stairs'))
        .add_node((0, 1), GridNode('66-0.png', NodeType.Quad))
        .add_node((1, 1), GridNode('66-1.png', NodeType.Quad)))
    region_to_rooms['Sewers Dark Cross'] = (
        sector({0x32: all_quadrants})
        .add_node((0, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Sewers Dark Cross Key Door N'))
        .add_node((0, 1), GridNode('50-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('50-2.png', NodeType.Quad))
        .add_node((0, 3),  GridNode('empty-tile.png', NodeType.Reserved, 'Sewers Dark Cross South Stairs'))
        .add_node((1, 1), GridNode('50-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('50-3.png', NodeType.Quad)))
    region_to_rooms['Sewers Water'] = (
        sector({0x22: bottom_side})
        .add_node((0, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Sewers Water W'))
        .add_node((1, 0), GridNode('34-2.png', NodeType.Quad))
        .add_node((1, 1),  GridNode('empty-tile.png', NodeType.Reserved, 'Sewers Water S'))
        .add_node((2, 0), GridNode('34-3.png', NodeType.Quad)))
    region_to_rooms['Sewers Key Rat'] = (
        sector({0x21: all_quadrants})
        .add_node((0, 1), GridNode('33-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('33-2.png', NodeType.Quad))
        .add_node((1, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Sewers Key Rat Key Door N'))
        .add_node((1, 1), GridNode('33-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('33-3.png', NodeType.Quad))
        .add_node((2, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Sewers Key Rat E')))
    hc_11_tile = (
        sector({0x11: all_quadrants})
        .add_node((0, 0), GridNode('17-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('17-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('17-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('17-3.png', NodeType.Quad))
        .add_node((1, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Sewers Secret Room Key Door S')))
    region_to_rooms['Sewers Rat Path'] = hc_11_tile
    region_to_rooms['Sewers Secret Room Blocked Path'] = hc_11_tile
    hc_02_tile = (
        sector({0x02: all_quadrants})
        .add_node((0, 0), GridNode('2-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('2-2.png', NodeType.Quad))
        .add_node((0, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Sewers Pull Switch S'))
        .add_node((1, 0), GridNode('2-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('2-3.png', NodeType.Quad)))
    region_to_rooms['Sewers Yet More Rats'] = hc_02_tile
    region_to_rooms['Sewers Pull Switch'] = hc_02_tile
    region_to_rooms['Sanctuary'] = (
        sector({0x12: all_quadrants})
        .add_node((0, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Sanctuary N'))
        .add_node((0, 1), GridNode('18-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('18-2.png', NodeType.Quad))
        .add_node((0, 3),  GridNode('empty-tile.png', NodeType.Reserved, 'Sanctuary S'))
        .add_node((1, 1), GridNode('18-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('18-3.png', NodeType.Quad)))


def init_eastern():
    east_tile_c9 = (
        sector({0xc9: all_quadrants})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Eastern Lobby Bridge N'))
        .add_node((0, 1), GridNode('201-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('201-2.png', NodeType.Quad))
        .add_node((0, 3), GridNode('empty-tile.png', NodeType.Reserved, 'Eastern Lobby S'))
        .add_node((1, 1), GridNode('201-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('201-3.png', NodeType.Quad)))
    region_to_rooms['Eastern Lobby'] = east_tile_c9
    region_to_rooms['Eastern Lobby Bridge'] = east_tile_c9
    region_to_rooms['Eastern Cannonball'] = (
        sector({0xb9: all_quadrants})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Eastern Cannonball N'))
        .add_node((0, 1), GridNode('185-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('185-2.png', NodeType.Quad))
        .add_node((0, 3), GridNode('empty-tile.png', NodeType.Reserved, 'Eastern Cannonball S'))
        .add_node((1, 1), GridNode('185-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('185-3.png', NodeType.Quad)))
    region_to_rooms['Eastern Cannonball Ledge'] = (
        sector({0xb9: top_side.union({4})})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Eastern Cannonball Ledge WN'))
        .add_node((1, 0), GridNode('185-0.png', NodeType.Quad))
        .add_node((2, 0), GridNode('185-1.png', NodeType.Quad))
        .add_node((3, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Eastern Cannonball Ledge Key Door EN')))
    region_to_rooms['Eastern Courtyard Ledge'] = (
        sector({0xb9: bottom_side})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Eastern Courtyard Ledge W'))
        .add_node((1, 0), GridNode('169-0.png', NodeType.Quad))
        .add_node((1, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Eastern Courtyard Ledge S'))
        .add_node((2, 0), GridNode('169-1.png', NodeType.Quad))
        .add_node((3, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Eastern Courtyard Ledge E')))
    region_to_rooms['Eastern Courtyard'] = (
        sector({0xa9: top_side})
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Eastern Courtyard WN'))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Eastern Courtyard N'))
        .add_node((1, 1), GridNode('169-0.png', NodeType.Quad))
        .add_node((2, 1), GridNode('169-1.png', NodeType.Quad))
        .add_node((3, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Eastern Courtyard EN')))
    region_to_rooms['Eastern Big Key'] = (
        sector({0xb8: right_side})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Eastern Big Key NE'))
        .add_node((0, 1), GridNode('184-1.png', NodeType.Quad))
        .add_node((0, 2), GridNode('184-3.png', NodeType.Quad))
        .add_node((1, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Eastern Big Key EN')))

    east_d9_tile = (
        sector({0xd9: bottom_side})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Eastern Cannonball Hell WS'))
        .add_node((1, 0), GridNode('217-2.png', NodeType.Quad))
        .add_node((2, 0), GridNode('217-3.png', NodeType.Quad))
        .add_node((3, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Eastern False Switches ES')))
    region_to_rooms['Eastern False Switches'] = east_d9_tile
    region_to_rooms['Eastern Cannonball Hell'] = east_d9_tile
    region_to_rooms['Eastern Boss'] = (
        sector({0xc8: all_quadrants})
        .add_node((0, 0), GridNode('200-3.png', NodeType.Quad))
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Eastern Boss SE')))


def init_desert():
    dp_84_tile = (
        sector({0x85: all_quadrants})
            .add_node((0, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert Main Lobby NW Edge'))
            .add_node((0, 1), GridNode('132-0.png', NodeType.Quad))
            .add_node((0, 2), GridNode('132-2.png', NodeType.Quad))
            .add_node((0, 3),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert Main Lobby S'))
            .add_node((1, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert Main Lobby NE Edge'))
            .add_node((1, 1), GridNode('132-1.png', NodeType.Quad))
            .add_node((1, 2), GridNode('132-3.png', NodeType.Quad))
            .add_node((2, 1),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert Main Lobby E Edge')))
    region_to_rooms['Desert Main Lobby'] = dp_84_tile
    region_to_rooms['Desert Left Alcove'] = dp_84_tile
    region_to_rooms['Desert Right Alcove'] = dp_84_tile
    dp_85_tile = (
        sector({0x85: all_quadrants})
        .add_node((0, 1),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert East Wing W Edge'))
        .add_node((1, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert East Wing N Edge'))
        .add_node((1, 1), GridNode('133-0.png', NodeType.Quad))
        .add_node((1, 2), GridNode('133-2.png', NodeType.Quad))
        .add_node((2, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert Compass NW'))
        .add_node((2, 1), GridNode('133-1.png', NodeType.Quad))
        .add_node((2, 2), GridNode('133-3.png', NodeType.Quad))
        .add_node((2, 3),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert East Lobby S')))
    region_to_rooms['Desert East Lobby'] = dp_85_tile
    region_to_rooms['Desert East Wing'] = dp_85_tile
    region_to_rooms['Desert Compass Room'] = dp_85_tile
    region_to_rooms['Desert Cannonball'] = (
        sector({0x75: right_side})
        .add_node((0, 0), GridNode('117-1.png', NodeType.Quad))
        .add_node((0, 1), GridNode('117-3.png', NodeType.Quad))
        .add_node((0, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert Cannonball S')))
    region_to_rooms['Desert Arrow Pot Corner'] = (
        sector({0x75: left_side})
        .add_node((0, 1),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert Arrow Pot Corner W Edge'))
        .add_node((1, 0), GridNode('117-0.png', NodeType.Quad))
        .add_node((1, 1), GridNode('117-2.png', NodeType.Quad))
        .add_node((1, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert Arrow Pot Corner S Edge')))
    region_to_rooms['Desert Dead End'] = (
        sector({0x74: bottom_side})
        .add_node((0, 0), GridNode('116-2.png', NodeType.Quad))
        .add_node((0, 1),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert Dead End Edge'))
        .add_node((1, 0), GridNode('116-3.png', NodeType.Quad)))
    region_to_rooms['Desert North Hall'] = (
        sector({0x74: all_quadrants})
        .add_node((0, 1),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert North Hall W Edge'))
        .add_node((1, 0), GridNode('116-0.png', NodeType.Quad))
        .add_node((1, 1), GridNode('116-2.png', NodeType.Quad))
        .add_node((1, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert North Hall SW Edge'))
        .add_node((2, 0), GridNode('116-1.png', NodeType.Quad))
        .add_node((2, 1), GridNode('116-3.png', NodeType.Quad))
        .add_node((2, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert North Hall SE Edge'))
        .add_node((3, 1),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert North Hall E Edge')))
    region_to_rooms['Desert Sandworm Corner'] = (
        sector({0x73: all_quadrants})
        .add_node((0, 0), GridNode('115-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('115-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('115-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('115-3.png', NodeType.Quad))
        .add_node((1, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert Sandworm Corner S Edge'))
        .add_node((2, 1),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert Sandworm Corner E Edge')))
    dp_83_tile = (
        sector({0x83: all_quadrants})
        .add_node((0, 1), GridNode('131-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('131-2.png', NodeType.Quad))
        .add_node((0, 3),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert West S'))
        .add_node((1, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Desert West Wing N Edge'))
        .add_node((1, 1), GridNode('131-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('131-3.png', NodeType.Quad)))
    region_to_rooms['Desert West Wing'] = dp_83_tile
    region_to_rooms['Desert West Lobby'] = dp_83_tile


def init_hera():
    hera_77_tile = (
        sector({0x77: all_quadrants})
        .add_node((0, 0), GridNode('119-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('119-2.png', NodeType.Quad))
        .add_node((0, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Hera Lobby S'))
        .add_node((1, 0), GridNode('119-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('119-3.png', NodeType.Quad)))
    region_to_rooms['Hera Lobby'] = hera_77_tile
    region_to_rooms['Hera Down Stairs Landing'] = hera_77_tile
    region_to_rooms['Hera Up Stairs Landing'] = hera_77_tile
    region_to_rooms['Hera Back'] = hera_77_tile
    hera_27_tile = (
        sector({0x27: all_quadrants})
        .add_node((0, 0), GridNode('39-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('39-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('39-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('39-3.png', NodeType.Quad)))
    region_to_rooms['Hera 4F'] = hera_27_tile
    region_to_rooms['Hera Big Chest Landing'] = hera_27_tile
    region_to_rooms['Hera 5F'] = (
        sector({0x17: all_quadrants})
        .add_node((0, 0), GridNode('23-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('23-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('23-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('23-3.png', NodeType.Quad)))
    region_to_rooms['Hera Boss'] = (
        sector({0x07: all_quadrants})
        .add_node((0, 0), GridNode('7-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('7-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('7-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('7-3.png', NodeType.Quad)))


def init_pod():
    pod_4a_tile = (
        sector({0x4a: all_quadrants})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Middle Cage N'))
        .add_node((0, 1), GridNode('74-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('74-2.png', NodeType.Quad))
        .add_node((0, 3), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Lobby S'))
        .add_node((1, 1), GridNode('74-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('74-3.png', NodeType.Quad)))
    region_to_rooms['PoD Lobby'] = pod_4a_tile
    region_to_rooms['PoD Left Cage'] = pod_4a_tile
    region_to_rooms['PoD Middle Cage'] = pod_4a_tile
    region_to_rooms['PoD Shooter Room'] = (
        sector(({0x09: {0}}))
        .add_node((0, 0), GridNode('9-0.png', NodeType.Quad)))
    region_to_rooms['PoD Warp Room'] = (
        sector(({0x09: {1}}))
        .add_node((0, 0), GridNode('9-1.png', NodeType.Quad)))
    pod_3a_tile = (
        sector({0x3a: all_quadrants})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Pit Room NW'))
        .add_node((0, 1), GridNode('58-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('58-2.png', NodeType.Quad))
        .add_node((0, 3), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Pit Room S'))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Pit Room NE'))
        .add_node((1, 1), GridNode('58-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('58-3.png', NodeType.Quad)))
    region_to_rooms['PoD Pit Room'] = pod_3a_tile
    region_to_rooms['PoD Pit Room Blocked'] = pod_3a_tile
    region_to_rooms['PoD Big Key Landing'] = pod_3a_tile
    pod_0a_tile = (
        sector({0x0a: all_quadrants})
        .add_node((0, 0), GridNode('10-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('10-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('10-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('10-3.png', NodeType.Quad)))
    region_to_rooms['PoD Stalfos Basement'] = pod_0a_tile
    region_to_rooms['PoD Basement Ledge'] = pod_0a_tile
    pod_2a_tile = (
        sector({0x2a: all_quadrants})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Arena Main NW'))
        .add_node((0, 1), GridNode('42-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('42-2.png', NodeType.Quad))
        .add_node((0, 3), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Arena Main SW'))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Arena Main NE'))
        .add_node((1, 1), GridNode('42-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('42-3.png', NodeType.Quad))
        .add_node((1, 3), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Arena Bridge SE'))
        .add_node((2, 2), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Arena Crystals E')))
    region_to_rooms['PoD Arena Main'] = pod_2a_tile
    region_to_rooms['PoD Arena North'] = pod_2a_tile
    region_to_rooms['PoD Arena Bridge'] = pod_2a_tile
    region_to_rooms['PoD Arena Right'] = pod_2a_tile
    region_to_rooms['PoD Arena Ledge'] = (
        sector({0x2a: {4}})
        .add_node((0, 0), GridNode('42-3.png', NodeType.Quad))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Arena Ledge ES')))
    pod_1a_tile = (
        sector({0x1a: all_quadrants})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Falling Bridge WN'))
        .add_node((1, 0), GridNode('26-0.png', NodeType.Quad))
        .add_node((1, 1), GridNode('26-2.png', NodeType.Quad))
        .add_node((1, 2), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Falling Bridge SW'))
        .add_node((2, 0), GridNode('26-1.png', NodeType.Quad))
        .add_node((2, 1), GridNode('26-3.png', NodeType.Quad))
        .add_node((2, 2), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Harmless Hellway SE')))
    region_to_rooms['PoD Falling Bridge Ledge'] = pod_1a_tile
    region_to_rooms['PoD Falling Bridge'] = pod_1a_tile
    region_to_rooms['PoD Compass Room'] = pod_1a_tile
    region_to_rooms['PoD Harmless Hellway'] = pod_1a_tile
    region_to_rooms['PoD Dark Basement'] = (
        sector({0x6a: all_quadrants})
        .add_node((0, 0), GridNode('106-1.png', NodeType.Quad))
        .add_node((0, 1), GridNode('106-3.png', NodeType.Quad)))
    region_to_rooms['PoD Dark Maze'] = (
        sector({0x19: right_side})
        .add_node((0, 0), GridNode('25-1.png', NodeType.Quad))
        .add_node((0, 1), GridNode('25-3.png', NodeType.Quad))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Dark Maze EN'))
        .add_node((1, 1), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Dark Maze E')))
    region_to_rooms['PoD Big Chest Balcony'] = (
        sector({0x1a: {0}})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Big Chest Balcony W'))
        .add_node((1, 0), GridNode('26-0.png', NodeType.Quad)))
    pod_2b_tile = (
        sector({0x2b: all_quadrants})
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Sexy Statue W'))
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Map Balcony WS'))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Sexy Statue NW'))
        .add_node((1, 1), GridNode('43-0.png', NodeType.Quad))
        .add_node((1, 2), GridNode('43-2.png', NodeType.Quad))
        .add_node((1, 3), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Map Balcony South Stairs'))
        .add_node((2, 2), GridNode('43-3.png', NodeType.Quad)))
    region_to_rooms['PoD Map Balcony'] = pod_2b_tile
    region_to_rooms['PoD Sexy Statue'] = pod_2b_tile
    pod_1b_tile = (
        sector({0x1b: {0, 1, 2}})
        .add_node((0, 0), GridNode('27-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('27-2.png', NodeType.Quad))
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Mimics 2 SW'))
        .add_node((1, 0), GridNode('27-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Bow Statue Down Ladder')))
    region_to_rooms['PoD Mimics 2'] = pod_1b_tile
    region_to_rooms['PoD Bow Statue Right'] = pod_1b_tile
    region_to_rooms['PoD Dark Pegs Landing'] = (
        sector({0x0b: all_quadrants})
        .add_node((0, 1), GridNode('11-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('11-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Dark Pegs Up Ladder'))
        .add_node((1, 1), GridNode('11-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('11-1.png', NodeType.Quad)))
    region_to_rooms['PoD Dark Alley'] = (
        sector({0x6a: right_side.union({4})})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Dark Alley NE'))
        .add_node((0, 1), GridNode('106-1.png', NodeType.Quad))
        .add_node((0, 2), GridNode('106-3.png', NodeType.Quad)))
    region_to_rooms['PoD Boss'] = (
        sector({0x5a: {3}})
        .add_node((0, 1), GridNode('90-3.png', NodeType.Quad))
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'PoD Boss SE')))

    # swamp
    swamp_28_tile = (
        sector({0x28: all_quadrants})
        .add_node((0, 0), GridNode('40-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('40-2.png', NodeType.Quad))
        .add_node((0, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Lobby S'))
        .add_node((1, 0), GridNode('40-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('40-3.png', NodeType.Quad)))
    region_to_rooms['Swamp Lobby'] = swamp_28_tile
    region_to_rooms['Swamp Entrance'] = swamp_28_tile
    region_to_rooms['Swamp Pot Row'] = (
        sector({0x38: all_quadrants})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Pot Row WN'))
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Pot Row WS'))
        .add_node((1, 0), GridNode('56-0.png', NodeType.Quad))
        .add_node((1, 1), GridNode('56-2.png', NodeType.Quad)))
    region_to_rooms['Swamp Map Ledge'] = (
        sector({0x37: {1}})
        .add_node((0, 0), GridNode('55-1.png', NodeType.Quad))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Map Ledge EN')))
    swamp_37_tile = (
        sector({0x37: all_quadrants})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Hammer Switch WN'))
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Trench 1 Departure WS'))
        .add_node((1, 0), GridNode('55-0.png', NodeType.Quad))
        .add_node((1, 1), GridNode('55-2.png', NodeType.Quad))
        .add_node((2, 0), GridNode('55-1.png', NodeType.Quad))
        .add_node((2, 1), GridNode('55-3.png', NodeType.Quad))
        .add_node((3, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Trench 1 Approach ES')))
    region_to_rooms['Swamp Trench 1 Approach'] = swamp_37_tile
    region_to_rooms['Swamp Trench 1 Departure'] = swamp_37_tile
    region_to_rooms['Swamp Hammer Switch'] = swamp_37_tile
    swamp_36_tile = (
        sector({0x36: all_quadrants})
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Hub WN'))
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Hub WS'))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Trench 1 Departure WS'))
        .add_node((1, 1), GridNode('54-0.png', NodeType.Quad))
        .add_node((1, 2), GridNode('54-2.png', NodeType.Quad))
        .add_node((1, 3), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Hub S'))
        .add_node((2, 1), GridNode('54-1.png', NodeType.Quad))
        .add_node((2, 2), GridNode('54-3.png', NodeType.Quad))
        .add_node((3, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Hub ES')))
    region_to_rooms['Swamp Hub'] = swamp_36_tile
    region_to_rooms['Swamp Hub North Ledge'] = swamp_36_tile
    region_to_rooms['Swamp Donut Top'] = (
        sector({0x46: all_quadrants})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Donut Top N'))
        .add_node((0, 1), GridNode('70-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('70-2.png', NodeType.Quad))
        .add_node((1, 1), GridNode('70-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('70-3.png', NodeType.Quad)))
    swamp_35_tile = (
        sector({0x35: {1, 2, 3}})
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Trench 2 Departure WS'))
        .add_node((1, 0), GridNode('53-0.png', NodeType.Quad))
        .add_node((1, 1), GridNode('53-2.png', NodeType.Quad))
        .add_node((2, 0), GridNode('53-1.png', NodeType.Quad))
        .add_node((2, 1), GridNode('53-3.png', NodeType.Quad))
        .add_node((3, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Crystal Switch EN'))
        .add_node((3, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Trench 2 Pots ES')))
    region_to_rooms['Swamp Crystal Switch Outer'] = swamp_35_tile
    region_to_rooms['Swamp Trench 2 Pots'] = swamp_35_tile
    region_to_rooms['Swamp Trench 2 Departure'] = swamp_35_tile
    region_to_rooms['Swamp Big Key Ledge'] = (
        sector({0x35: {0}})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Big Key Ledge WN'))
        .add_node((1, 0), GridNode('53-0.png', NodeType.Quad)))
    swamp_34_tile = (
        sector({0x34: all_quadrants})
        .add_node((0, 0), GridNode('52-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('52-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('52-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('52-3.png', NodeType.Quad))
        .add_node((2, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Barrier EN'))
        .add_node((2, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Swamp West Shallows ES')))
    region_to_rooms['Swamp West Shallows'] = swamp_34_tile
    region_to_rooms['Swamp West Block Path'] = swamp_34_tile
    region_to_rooms['Swamp West Ledge'] = swamp_34_tile
    region_to_rooms['Swamp Barrier Ledge'] = swamp_34_tile
    region_to_rooms['Swamp Barrier'] = swamp_34_tile
    region_to_rooms['Swamp Attic'] = (
        sector({0x54: all_quadrants})
        .add_node((0, 0), GridNode('84-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('84-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('84-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('84-3.png', NodeType.Quad)))
    swamp_76_tile = (
        sector({0x76: all_quadrants})
        .add_node((0, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Basement Shallows NW'))
        .add_node((0, 1), GridNode('118-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('118-2.png', NodeType.Quad))
        .add_node((1, 1), GridNode('118-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('118-3.png', NodeType.Quad)))
    region_to_rooms['Swamp Drain Left'] = swamp_76_tile
    region_to_rooms['Swamp Drain Right'] = swamp_76_tile
    region_to_rooms['Swamp Flooded Room'] = swamp_76_tile
    region_to_rooms['Swamp Basement Shallows'] = swamp_76_tile
    swamp_66_tile = (
        sector({0x66: all_quadrants})
        .add_node((0, 0), GridNode('102-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('102-2.png', NodeType.Quad))
        .add_node((0, 2),  GridNode('empty-tile.png', NodeType.Reserved, 'Swamp Waterfall Room SW'))
        .add_node((1, 0), GridNode('102-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('102-3.png', NodeType.Quad)))
    region_to_rooms['Swamp Waterfall Room'] = swamp_66_tile
    region_to_rooms['Swamp Behind Waterfall'] = swamp_66_tile

    # skull
    region_to_rooms['Skull 3 Lobby'] = (
        sector({0x59: all_quadrants})
        .add_node((0, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Skull 3 Lobby NW'))
        .add_node((0, 1), GridNode('89-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('89-2.png', NodeType.Quad))
        .add_node((0, 3),  GridNode('empty-tile.png', NodeType.Reserved, 'Skull 3 Lobby SW'))
        .add_node((1, 1), GridNode('89-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('89-3.png', NodeType.Quad)))
    sk_49_tile = (
        sector({0x49: all_quadrants})
        .add_node((0, 0),  GridNode('empty-tile.png', NodeType.Reserved, 'Skull Vines NW'))
        .add_node((0, 1), GridNode('73-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('73-2.png', NodeType.Quad))
        .add_node((0, 3),  GridNode('empty-tile.png', NodeType.Reserved, 'Skull Star Pits SW'))
        .add_node((1, 1), GridNode('73-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('73-3.png', NodeType.Quad)))
    region_to_rooms['Skull Star Pits'] = sk_49_tile
    region_to_rooms['Skull Vines'] = sk_49_tile

    # tt
    region_to_rooms['Thieves Lobby'] = (
        sector({0xdb: {0, 1, 2}})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves Lobby N Edge'))
        .add_node((0, 1), GridNode('219-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('219-2.png', NodeType.Quad))
        .add_node((0, 3), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves Lobby S'))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves Lobby NE Edge'))
        .add_node((1, 1), GridNode('219-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('219-3.png', NodeType.Quad))
        .add_node((2, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves Lobby E')))
    region_to_rooms['Thieves Ambush'] = (
        sector({0xcb: all_quadrants})
        .add_node((0, 0), GridNode('203-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('203-2.png', NodeType.Quad))
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves Ambush S Edge'))
        .add_node((1, 0), GridNode('203-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('203-3.png', NodeType.Quad))
        .add_node((1, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves Ambush SE Edge'))
        .add_node((2, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves Ambush EN Edge'))
        .add_node((2, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves Ambush ES Edge')))
    tt_tile_cc = (
        sector({0xcc: all_quadrants})
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves BK Corner WN Edge'))
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves BK Corner WS Edge'))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves Rail Ledge NW'))
        .add_node((1, 1), GridNode('204-0.png', NodeType.Quad))
        .add_node((1, 2), GridNode('204-2.png', NodeType.Quad))
        .add_node((1, 3), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves BK Corner SW Edge'))
        .add_node((2, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves BK Corner NE'))
        .add_node((2, 1), GridNode('204-1.png', NodeType.Quad))
        .add_node((2, 2), GridNode('204-3.png', NodeType.Quad))
        .add_node((2, 3), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves BK Corner S Edge')))
    region_to_rooms['Thieves BK Corner'] = tt_tile_cc
    region_to_rooms['Thieves Rail Ledge'] = tt_tile_cc
    region_to_rooms['Thieves Compass Room'] = (
        sector({0xdc: all_quadrants})
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves Compass Room W'))
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves Compass Room WS Edge'))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves Compass Room NW Edge'))
        .add_node((1, 1), GridNode('220-0.png', NodeType.Quad))
        .add_node((1, 2), GridNode('220-2.png', NodeType.Quad))
        .add_node((2, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves Compass Room N Edge'))
        .add_node((2, 1), GridNode('220-1.png', NodeType.Quad))
        .add_node((2, 2), GridNode('220-3.png', NodeType.Quad)))
    region_to_rooms['Thieves Big Chest Nook'] = (
        sector({0xdb: {3}})
        .add_node((0, 0), GridNode('219-3.png', NodeType.Quad))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves Big Chest Nook ES Edge')))
    region_to_rooms['Thieves Spike Switch'] = (
        sector({0xab: {2}})
        .add_node((0, 0), GridNode('171-2.png', NodeType.Quad))
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Thieves Spike Switch SW')))

    # ice
    ice_0e_tile = (
        sector({0x0e: bottom_side})
        .add_node((0, 0), GridNode('14-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('14-3.png', NodeType.Quad))
        .add_node((1, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Ice Lobby SE')))
    region_to_rooms['Ice Lobby'] = ice_0e_tile
    region_to_rooms['Ice Jelly Key'] = ice_0e_tile
    ice_1e_tile = (
        sector({0x1e: {1, 2, 3}})
        .add_node((0, 1), GridNode('30-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('30-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('30-3.png', NodeType.Quad))
        .add_node((1, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Ice Cross Bottom SE'))
        .add_node((2, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Ice Cross Right ES')))
    region_to_rooms['Ice Floor Switch'] = ice_1e_tile
    region_to_rooms['Ice Cross Bottom'] = ice_1e_tile
    region_to_rooms['Ice Cross Right'] = ice_1e_tile
    ice_1f_tile = (
        sector({0x1f: bottom_side})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Ice Pengator Switch WS'))
        .add_node((1, 0), GridNode('31-2.png', NodeType.Quad))
        .add_node((2, 0), GridNode('31-3.png', NodeType.Quad))
        .add_node((2, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Ice Big Key Down Ladder')))
    region_to_rooms['Ice Pengator Switch'] = ice_1f_tile
    region_to_rooms['Ice Big Key'] = ice_1f_tile
    region_to_rooms['Ice Compass Room'] = (
        sector({0x1e: {1}})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Ice Compass Room NE'))
        .add_node((0, 1), GridNode('46-1.png', NodeType.Quad)))
    ice_4e_tile = (
        sector({0x4e: top_side})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Ice Bomb Jump NW'))
        .add_node((0, 1), GridNode('78-0.png', NodeType.Quad))
        .add_node((1, 1), GridNode('78-1.png', NodeType.Quad)))
    region_to_rooms['Ice Bomb Jump Ledge'] = ice_4e_tile
    region_to_rooms['Ice Narrow Corridor'] = ice_4e_tile
    region_to_rooms['Ice Pengator Trap'] = (
        sector({0x6e: {1}})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Ice Pengator Trap NE'))
        .add_node((0, 1), GridNode('110-1.png', NodeType.Quad)))
    ice_5e_tile = (
        sector({0x5e: {1, 2, 3}})
        .add_node((0, 1), GridNode('94-2.png', NodeType.Quad))
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Ice Firebar Down Ladder'))
        .add_node((1, 0), GridNode('94-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('94-3.png', NodeType.Quad))
        .add_node((1, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Ice Spike Cross SE'))
        .add_node((2, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Ice Spike Cross ES')))
    region_to_rooms['Ice Spike Cross'] = ice_5e_tile
    region_to_rooms['Ice Firebar'] = ice_5e_tile
    region_to_rooms['Ice Spike Room'] = (
        sector({0x5f: {2}})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Ice Pengator Trap NE'))
        .add_node((1, 0), GridNode('95-2.png', NodeType.Quad)))
    region_to_rooms['Ice Lonely Freezor'] = (
        sector({0x8e: {1}})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Ice Lonely Freezor NE'))
        .add_node((0, 1), GridNode('142-1.png', NodeType.Quad)))

    # mire
    mm_tile_c2 = (
        sector({0xc2: all_quadrants})
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Hub WN'))
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Hub WS'))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Hub Top NW'))
        .add_node((1, 1), GridNode('194-0.png', NodeType.Quad))
        .add_node((1, 2), GridNode('194-2.png', NodeType.Quad))
        .add_node((2, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Hub NE'))
        .add_node((2, 1), GridNode('194-1.png', NodeType.Quad))
        .add_node((2, 2), GridNode('194-3.png', NodeType.Quad))
        .add_node((2, 3), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Hub SE'))
        .add_node((3, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Hub Right EN'))
        .add_node((3, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Hub ES')))
    region_to_rooms['Mire Hub'] = mm_tile_c2
    region_to_rooms['Mire Hub Top'] = mm_tile_c2
    region_to_rooms['Mire Hub Right'] = mm_tile_c2
    mm_b3_tile = (
        sector({0xb3: left_side})
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Ledgehop WN'))
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Spikes WS'))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Ledgehop NW'))
        .add_node((1, 1), GridNode('179-0.png', NodeType.Quad))
        .add_node((1, 2), GridNode('179-2.png', NodeType.Quad))
        .add_node((1, 3), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Spikes SW')))
    region_to_rooms['Mire Spikes'] = mm_b3_tile
    region_to_rooms['Mire Ledgehop'] = mm_b3_tile
    mm_tile_c1 = (
        sector({0xc1: all_quadrants})
        .add_node((0, 1), GridNode('193-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('193-2.png', NodeType.Quad))
        .add_node((0, 3), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Tile Room SW'))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Wizzrobe Bypass NE'))
        .add_node((1, 1), GridNode('193-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('193-3.png', NodeType.Quad))
        .add_node((1, 3), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Conveyor Crystal SE'))
        .add_node((2, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Wizzrobe Bypass EN'))
        .add_node((2, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Conveyor Crystal ES')))
    region_to_rooms['Mire Conveyor Crystal'] = mm_tile_c1
    region_to_rooms['Mire Tile Room'] = mm_tile_c1
    region_to_rooms['Mire Wizzrobe Bypass'] = mm_tile_c1
    region_to_rooms['Mire Conveyor Barrier'] = (
        sector({0xd1: {0}})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Conveyor Barrier NW'))
        .add_node((0, 1), GridNode('209-0.png', NodeType.Quad)))
    region_to_rooms['Mire Neglected Room'] = (
        sector({0xd1: right_side})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Neglected Room NE'))
        .add_node((0, 1), GridNode('209-1.png', NodeType.Quad))
        .add_node((0, 2), GridNode('209-3.png', NodeType.Quad)))
    region_to_rooms['Mire BK Chest Ledge'] = (
        sector({0xd1: bottom_side})
        .add_node((0, 0), GridNode('209-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('209-3.png', NodeType.Quad)))
    mm_tile_b1 = (
        sector({0xb1: all_quadrants})
        .add_node((0, 1), GridNode('177-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('177-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Spike Barrier NE'))
        .add_node((1, 1), GridNode('177-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('177-3.png', NodeType.Quad))
        .add_node((1, 3), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Spike Barrier SE')))
    region_to_rooms['Mire Spike Barrier'] = mm_tile_b1
    region_to_rooms['Mire Square Rail'] = mm_tile_b1
    mm_tile_a1 = (
        sector({0xa1: {0, 1, 3}})
        .add_node((0, 0), GridNode('161-0.png', NodeType.Quad))
        .add_node((1, 0), GridNode('161-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('161-3.png', NodeType.Quad))
        .add_node((1, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Fishbone SE'))
        .add_node((2, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Fishbone E')))
    region_to_rooms['Mire Fishbone'] = mm_tile_a1
    region_to_rooms['Mire South Fish'] = mm_tile_a1
    region_to_rooms['Mire Over Bridge'] = (
        sector({0xa2: top_side.union({4})})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Over Bridge W'))
        .add_node((1, 0), GridNode('162-0.png', NodeType.Quad))
        .add_node((2, 0), GridNode('162-1.png', NodeType.Quad))
        .add_node((3, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Over Bridge E')))
    mm_tile_a2 = (
        sector({0xa2: all_quadrants})
        .add_node((0, 0), GridNode('162-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('162-2.png', NodeType.Quad))
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Left Bridge S'))
        .add_node((1, 0), GridNode('162-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('162-3.png', NodeType.Quad))
        .add_node((1, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Right Bridge SE')))
    region_to_rooms['Mire Right Bridge'] = mm_tile_a2
    region_to_rooms['Mire Left Bridge'] = mm_tile_a2
    region_to_rooms['Mire Bent Bridge'] = (
        sector({0xa3: left_side})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Bent Bridge W'))
        .add_node((1, 0), GridNode('163-0.png', NodeType.Quad))
        .add_node((1, 1), GridNode('166-2.png', NodeType.Quad))
        .add_node((1, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Mire Bent Bridge SW')))

    # tr
    tr_d6_tile_r = (
        sector({0xd6: right_side})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Lobby Ledge NE'))
        .add_node((0, 1), GridNode('214-1.png', NodeType.Quad))
        .add_node((0, 2), GridNode('214-3.png', NodeType.Quad))
        .add_node((0, 3), GridNode('empty-tile.png', NodeType.Reserved, 'TR Main Lobby SE')))
    region_to_rooms['TR Main Lobby'] = tr_d6_tile_r
    region_to_rooms['TR Lobby Ledge'] = tr_d6_tile_r
    region_to_rooms['TR Hub'] = (
        sector({0xc6: all_quadrants})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Hub NW'))
        .add_node((0, 1), GridNode('198-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('198-2.png', NodeType.Quad))
        .add_node((0, 3), GridNode('empty-tile.png', NodeType.Reserved, 'TR Hub SW'))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Hub NE'))
        .add_node((1, 1), GridNode('198-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('198-3.png', NodeType.Quad))
        .add_node((1, 3), GridNode('empty-tile.png', NodeType.Reserved, 'TR Hub SE'))
        .add_node((2, 1), GridNode('empty-tile.png', NodeType.Reserved, 'TR Hub EN'))
        .add_node((2, 2), GridNode('empty-tile.png', NodeType.Reserved, 'TR Hub ES')))
    region_to_rooms['TR Compass Room'] = (
        sector({0xd6: left_side})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Compass Room NW'))
        .add_node((0, 1), GridNode('214-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('214-2.png', NodeType.Quad)))
    region_to_rooms['TR Torches Ledge'] = (
        sector({0xc7: {2}})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Torches Ledge WS'))
        .add_node((1, 0), GridNode('199-2.png', NodeType.Quad)))
    region_to_rooms['TR Torches'] = (
        sector({0xc7: {0, 1, 3}})
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'TR Torches WN'))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Torches NW'))
        .add_node((1, 1), GridNode('199-0.png', NodeType.Quad))
        .add_node((1, 2), GridNode('199-2.png', NodeType.Quad))
        .add_node((2, 1), GridNode('199-1.png', NodeType.Quad))
        .add_node((2, 2), GridNode('199-3.png', NodeType.Quad)))
    region_to_rooms['TR Roller Room'] = (
        sector({0xb7: left_side})
        .add_node((0, 0), GridNode('183-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('183-2.png', NodeType.Quad))
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'TR Roller Room SW')))
    region_to_rooms['TR Tile Room'] = (
        sector({0xb6: right_side})
        .add_node((0, 0), GridNode('182-1.png', NodeType.Quad))
        .add_node((0, 1), GridNode('182-3.png', NodeType.Quad))
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'TR Tile Room SE')))
    tr_b6_tile_l = (
        sector({0xb6: left_side})
        .add_node((0, 0), GridNode('182-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('182-2.png', NodeType.Quad))
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'TR Pokey 1 SW')))
    region_to_rooms['TR Pokey 1'] = tr_b6_tile_l
    region_to_rooms['TR Chain Chomps Top'] = tr_b6_tile_l
    tr_15_tile = (
        sector({0x15: all_quadrants})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Pipe Pit WN'))
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'TR Pipe Ledge WS'))
        .add_node((1, 0), GridNode('21-0.png', NodeType.Quad))
        .add_node((1, 1), GridNode('21-2.png', NodeType.Quad))
        .add_node((2, 0), GridNode('21-1.png', NodeType.Quad))
        .add_node((2, 1), GridNode('21-3.png', NodeType.Quad)))
    region_to_rooms['TR Pipe Pit'] = tr_15_tile
    region_to_rooms['TR Pipe Ledge'] = tr_15_tile
    region_to_rooms['TR Lava Dual Pipes'] = (
        sector({0x14: all_quadrants.union({4})})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Lava Dual Pipes WN'))
        .add_node((1, 0), GridNode('20-0.png', NodeType.Quad))
        .add_node((1, 1), GridNode('20-2.png', NodeType.Quad))
        .add_node((1, 2), GridNode('empty-tile.png', NodeType.Reserved, 'TR Lava Dual Pipes SW'))
        .add_node((2, 0), GridNode('20-1.png', NodeType.Quad))
        .add_node((2, 1), GridNode('20-3.png', NodeType.Quad))
        .add_node((3, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Lava Dual Pipes EN')))
    region_to_rooms['TR Lava Island'] = (
        sector({0x14: all_quadrants.union({5})})
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'TR Lava Island WS'))
        .add_node((1, 0), GridNode('20-0.png', NodeType.Quad))
        .add_node((1, 1), GridNode('20-2.png', NodeType.Quad))
        .add_node((2, 0), GridNode('20-1.png', NodeType.Quad))
        .add_node((2, 1), GridNode('20-3.png', NodeType.Quad))
        .add_node((3, 1), GridNode('empty-tile.png', NodeType.Reserved, 'TR Lava Island ES')))
    region_to_rooms['TR Lava Escape'] = (
        sector({0x14: all_quadrants.union({6})})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Lava Escape NW'))
        .add_node((0, 1), GridNode('20-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('20-2.png', NodeType.Quad))
        .add_node((1, 1), GridNode('20-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('20-3.png', NodeType.Quad))
        .add_node((1, 3), GridNode('empty-tile.png', NodeType.Reserved, 'TR Lava Escape SE')))
    tr_13_tile = (
        sector({0x13: right_side})
        .add_node((0, 0), GridNode('19-1.png', NodeType.Quad))
        .add_node((0, 1), GridNode('19-3.png', NodeType.Quad))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Pokey 2 EN'))
        .add_node((1, 1), GridNode('empty-tile.png', NodeType.Reserved, 'TR Pokey 2 ES')))
    region_to_rooms['TR Pokey 2 Top'] = tr_13_tile
    region_to_rooms['TR Pokey 2 Bottom'] = tr_13_tile
    tr_24_tile = (
        sector({0x24: all_quadrants})
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'TR Hallway WS'))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Twin Pokeys NW'))
        .add_node((0, 0), GridNode('36-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('36-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Dodgers NE'))
        .add_node((0, 0), GridNode('36-1.png', NodeType.Quad))
        .add_node((0, 1), GridNode('36-3.png', NodeType.Quad))
        .add_node((1, 1), GridNode('empty-tile.png', NodeType.Reserved, 'TR Big Chest Entrance SE')))
    region_to_rooms['TR Twin Pokeys'] = tr_24_tile
    region_to_rooms['TR Dodgers'] = tr_24_tile
    region_to_rooms['TR Hallway'] = tr_24_tile
    region_to_rooms['TR Big Chest Entrance'] = tr_24_tile
    region_to_rooms['TR Lazy Eyes'] = (
        sector({0x23: {3}})
        .add_node((0, 0), GridNode('35-3.png', NodeType.Quad))
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'TR Lazy Eyes SE'))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Lazy Eyes ES')))
    tr_04_tile = (
        sector({0x04: all_quadrants})
        .add_node((0, 0), GridNode('4-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('4-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Dash Room SW'))
        .add_node((0, 0), GridNode('4-1.png', NodeType.Quad))
        .add_node((0, 1), GridNode('4-3.png', NodeType.Quad)))
    region_to_rooms['TR Dash Room'] = tr_04_tile
    region_to_rooms['TR Crystaroller Top'] = tr_04_tile
    region_to_rooms['TR Dark Ride'] = (
        sector({0xb5: all_quadrants})
        .add_node((0, 1), GridNode('181-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('181-2.png', NodeType.Quad))
        .add_node((0, 3), GridNode('empty-tile.png', NodeType.Reserved, 'TR Dark Ride SW'))
        .add_node((1, 1), GridNode('181-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('181-3.png', NodeType.Quad)))
    region_to_rooms['TR Dash Bridge'] = (
        sector({0xc5: left_side})
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'TR Dash Bridge WS'))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Dash Bridge NW'))
        .add_node((1, 1), GridNode('197-0.png', NodeType.Quad))
        .add_node((1, 2), GridNode('197-2.png', NodeType.Quad))
        .add_node((1, 3), GridNode('empty-tile.png', NodeType.Reserved, 'TR Dash Bridge SW')))
    region_to_rooms['TR Eye Bridge'] = (
        sector({0xd5: left_side})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Eye Bridge NW'))
        .add_node((0, 1), GridNode('213-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('213-2.png', NodeType.Quad))
        .add_node((0, 3), GridNode('empty-tile.png', NodeType.Reserved, 'TR Eye Bridge SW')))
    tr_c4_tile = (
        sector({0xc4: all_quadrants})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Crystal Maze North Stairs'))
        .add_node((0, 1), GridNode('196-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('196-2.png', NodeType.Quad))
        .add_node((1, 1), GridNode('196-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('196-3.png', NodeType.Quad))
        .add_node((2, 2), GridNode('empty-tile.png', NodeType.Reserved, 'TR Crystal Maze ES')))
    region_to_rooms['TR Crystal Maze Start'] = tr_c4_tile
    region_to_rooms['TR Crystal Maze End'] = tr_c4_tile
    region_to_rooms['TR Final Abyss'] = (
        sector({0xb4: all_quadrants})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'TR Final Abyss NW'))
        .add_node((0, 1), GridNode('180-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('180-2.png', NodeType.Quad))
        .add_node((0, 3), GridNode('empty-tile.png', NodeType.Reserved, 'TR Final Abyss South Stairs'))
        .add_node((1, 1), GridNode('180-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('180-3.png', NodeType.Quad)))
    region_to_rooms['TR Boss'] = (
        sector({0xa4: {2}})
        .add_node((0, 0), GridNode('164-2.png', NodeType.Quad))
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'TR Boss SW')))

    # gt
    # right side
    region_to_rooms['GT Crystal Conveyor'] = (
        sector({0x9d: top_side})
        .add_node((0, 1), GridNode('157-0.png', NodeType.Quad))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'GT Crystal Conveyor NE'))
        .add_node((1, 1), GridNode('157-1.png', NodeType.Quad)))
    region_to_rooms['GT Conveyor Star Pits'] = (
        sector({0x7b: top_side})
        .add_node((0, 0), GridNode('123-0.png', NodeType.Quad))
        .add_node((1, 0), GridNode('123-1.png', NodeType.Quad))
        .add_node((2, 0), GridNode('empty-tile.png', NodeType.Reserved, 'GT Conveyor Star Pits EN')))
    region_to_rooms['GT Falling Bridge'] = (
        sector({0x7c: left_side})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'GT Falling Bridge WN'))
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'GT Falling Bridge WS'))
        .add_node((1, 0), GridNode('124-0.png', NodeType.Quad))
        .add_node((1, 1), GridNode('124-2.png', NodeType.Quad)))
    region_to_rooms['GT Hidden Star'] = (
        sector({0x7b: {3}})
        .add_node((0, 0), GridNode('123-3.png', NodeType.Quad))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'GT Hidden Star ES')))
    region_to_rooms['GT Invisible Bridges'] = (
        sector({0x9d: bottom_side})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'GT Invisible Bridges WS'))
        .add_node((1, 0), GridNode('157-2.png', NodeType.Quad))
        .add_node((2, 0), GridNode('157-3.png', NodeType.Quad)))
    # left side
    region_to_rooms['GT DMs Room'] = (
        sector({0x7b: {2}})
        .add_node((0, 0), GridNode('123-2.png', NodeType.Quad))
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'GT DMs Room SW')))
    gt_8b_tile = (
        sector({0x8b: all_quadrants})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'GT Hookshot NW'))
        .add_node((0, 1), GridNode('139-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('139-2.png', NodeType.Quad))
        .add_node((0, 3), GridNode('empty-tile.png', NodeType.Reserved, 'GT Hookshot SW'))
        .add_node((1, 1), GridNode('139-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('139-3.png', NodeType.Quad))
        .add_node((2, 1), GridNode('empty-tile.png', NodeType.Reserved, 'GT Conveyor Cross WN')))
    region_to_rooms['GT Conveyor Cross'] = gt_8b_tile
    region_to_rooms['GT Hookshot North Platform'] = gt_8b_tile
    region_to_rooms['GT Hookshot South Entry'] = gt_8b_tile
    region_to_rooms['GT Double Switch Entry'] = (
        sector({0x9b: top_side})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'GT Double Switch NW'))
        .add_node((0, 1), GridNode('155-0.png', NodeType.Quad))
        .add_node((1, 1), GridNode('155-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('empty-tile.png', NodeType.Reserved, 'GT Spike Crystals Warp')))
    region_to_rooms['GT Firesnake Room'] = (
        sector({0x9d: {0, 1, 2}})
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'GT Warp Maze (Rails) WS'))
        .add_node((1, 1), GridNode('125-0.png', NodeType.Quad))
        .add_node((1, 2), GridNode('125-2.png', NodeType.Quad))
        .add_node((1, 3), GridNode('empty-tile.png', NodeType.Reserved, 'GT Warp Maze - Rail Choice Left Warp'))
        .add_node((2, 0), GridNode('empty-tile.png', NodeType.Reserved, 'GT Firesnake Room'))
        .add_node((2, 1), GridNode('125-1.png', NodeType.Quad)))
    region_to_rooms['GT Warp Maze - Pot Rail'] = (
        sector({0x9d: {4}})
        .add_node((0, 0), GridNode('pot-rail.png', NodeType.Quad))
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'GT Warp Maze - Pot Rail')))
    gt_9b_lower = (
        sector({0x9b: bottom_side})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'GT Warp Maze - Left Section'))
        .add_node((0, 1), GridNode('155-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'GT Warp Maze - Pit Exit Warp'))
        .add_node((1, 1), GridNode('155-3.png', NodeType.Quad))
        .add_node((2, 1), GridNode('empty-tile.png', NodeType.Reserved, 'GT Warp Maze (Pits) ES')))
    region_to_rooms['GT Warp Maze Exit Section'] = gt_9b_lower
    region_to_rooms['GT Warp Maze - Left Section'] = gt_9b_lower
    region_to_rooms['GT Warp Maze - Right Section'] = gt_9b_lower
    region_to_rooms['GT Warp Maze - Mid Section'] = gt_9b_lower
    region_to_rooms['GT Randomizer Room'] = (
        sector({0x7c: right_side})
        .add_node((0, 0), GridNode('124-1.png', NodeType.Quad))
        .add_node((0, 1), GridNode('124-3.png', NodeType.Quad))
        .add_node((1, 1), GridNode('empty-tile.png', NodeType.Reserved, 'GT Randomizer Room ES'))
    )
    gt_8c_tile = (
        sector({0x8c: {0, 1, 2}})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'GT Torch WN'))
        .add_node((1, 0), GridNode('140-0.png', NodeType.Quad))
        .add_node((1, 1), GridNode('140-2.png', NodeType.Quad))
        .add_node((1, 2), GridNode('empty-tile.png', NodeType.Reserved, 'GT Big Chest SW'))
        .add_node((2, 0), GridNode('140-1.png', NodeType.Quad))
        .add_node((3, 0), GridNode('empty-tile.png', NodeType.Reserved, 'GT Hope Room EN')))
    region_to_rooms["GT Bob's Torch"] = gt_8c_tile
    region_to_rooms['GT Hope Room'] = gt_8c_tile
    region_to_rooms['GT Big Chest'] = gt_8c_tile
    region_to_rooms['GT Blocked Stairs'] = gt_8c_tile
    region_to_rooms["GT Bob's Room"] = (
        sector({0x8c: {3}})
        .add_node((0, 0), GridNode('140-3.png', NodeType.Quad))
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'GT Bob\'s Room SE')))
    # upstairs
    gt_6b_tile = (
        sector({0x6b: all_quadrants})
        .add_node((0, 1), GridNode('107-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('107-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'GT Dash Hall NE'))
        .add_node((1, 1), GridNode('107-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('107-3.png', NodeType.Quad)))
    region_to_rooms['GT Dash Hall'] = gt_6b_tile
    region_to_rooms['GT Crystal Paths'] = gt_6b_tile
    region_to_rooms['GT Hidden Spikes'] = (
        sector({0x5b: all_quadrants})
        .add_node((0, 0), GridNode('91-1.png', NodeType.Quad))
        .add_node((0, 1), GridNode('91-3.png', NodeType.Quad))
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'GT Hidden Spikes SE'))
        .add_node((1, 0), GridNode('empty-tile.png', NodeType.Reserved, 'GT Hidden Spikes EN')))


def init_aga_tower():
    # at
    at_e0_tile = (
        sector({0xe0: all_quadrants})
        .add_node((0, 0), GridNode('224-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('224-2.png', NodeType.Quad))
        .add_node((0, 2), GridNode('empty-tile.png', NodeType.Reserved, 'Tower Lobby S'))
        .add_node((1, 0), GridNode('224-1.png', NodeType.Quad)))
    region_to_rooms['Tower Lobby'] = at_e0_tile
    region_to_rooms['Tower Room 03'] = at_e0_tile
    at_d0_tile = (
        sector({0xd0: all_quadrants})
        .add_node((0, 0), GridNode('208-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('208-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('208-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('208-3.png', NodeType.Quad)))
    region_to_rooms['Tower Lone Statue'] = at_d0_tile
    region_to_rooms['Tower Dark Chargers'] = at_d0_tile
    at_c0_tile = (
        sector({0xc0: all_quadrants})
        .add_node((0, 0), GridNode('192-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('192-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('192-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('192-3.png', NodeType.Quad)))
    region_to_rooms['Tower Dual Statues'] = at_c0_tile
    region_to_rooms['Tower Dark Archers'] = at_c0_tile
    at_b0_tile = (
        sector({0xb0: all_quadrants})
        .add_node((0, 0), GridNode('176-0.png', NodeType.Quad))
        .add_node((0, 1), GridNode('176-2.png', NodeType.Quad))
        .add_node((1, 0), GridNode('176-1.png', NodeType.Quad))
        .add_node((1, 1), GridNode('176-3.png', NodeType.Quad)))
    region_to_rooms['Tower Red Spears'] = at_b0_tile
    region_to_rooms['Tower Pacifist Run'] = at_b0_tile
    at_40_tile = (
        sector({0x40: {0, 2, 3}})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Tower Catwalk North Stairs'))
        .add_node((0, 1), GridNode('64-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('64-2.png', NodeType.Quad))
        .add_node((1, 1), GridNode('64-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('64-3.png', NodeType.Quad)))
    region_to_rooms['Tower Push Statue'] = at_40_tile
    region_to_rooms['Tower Catwalk'] = at_40_tile
    at_30_tile = (
        sector({0x30: left_side})
        .add_node((0, 0), GridNode('empty-tile.png', NodeType.Reserved, 'Tower Altar NW'))
        .add_node((0, 1), GridNode('48-0.png', NodeType.Quad))
        .add_node((0, 2), GridNode('48-2.png', NodeType.Quad))
        .add_node((0, 3), GridNode('empty-tile.png', NodeType.Reserved, 'Tower Antechamber South Stairs'))
        .add_node((1, 1), GridNode('48-1.png', NodeType.Quad))
        .add_node((1, 2), GridNode('48-3.png', NodeType.Quad)))
    region_to_rooms['Tower Antechamber'] = at_30_tile
    region_to_rooms['Tower Altar'] = at_30_tile
    region_to_rooms['Tower Agahnim 1'] = (
        sector({0x30: {2}})
        .add_node((0, 0), GridNode('32-2.png', NodeType.Quad))
        .add_node((0, 1), GridNode('empty-tile.png', NodeType.Reserved, 'Tower Antechamber South Stairs')))

# old_region_to_rooms = {


# 'Eastern Courtyard Ledge':make_room(169, bottom_side),
# 'Eastern East Wing':make_room(170, left_side),
# 'Eastern Pot Switch':make_room(170, [1]),
# 'Eastern Map Balcony':make_room(170, [3]),
# 'Eastern Map Room':make_room(170, [3]),
# 'Eastern West Wing':make_room(168, right_side),
# 'Eastern Stalfos Spawn':make_room(168, [0]),
# 'Eastern Compass Room':make_room(168, [2]),
# 'Eastern Hint Tile':make_room(168, right_side),
# 'Eastern Hint Tile Blocked Path':make_room(168, right_side),
# 'Eastern Fairies':make_room(137, top_side),
# 'Eastern Map Valley':make_room(170, left_side),
# 'Eastern Dark Square':make_room(186, [0]),
# 'Eastern Dark Pots':make_room(186, [1]),
# 'Eastern Big Key':make_room(184, right_side),
# 'Eastern Darkness':make_room(153, bottom_side),
# 'Eastern Rupees':make_room(153, [1]),
# 'Eastern Attic Start':make_room(218, [2]),
# 'Eastern Single Eyegore':make_room(216, [3]),
# 'Eastern Duo Eyegores':make_room(216, [1]),
#
#
#         # Desert Palace
# 'Desert Back Lobby':make_room(99, [2]),
# 'Desert Tiles 1':make_room(99, [0]),
# 'Desert Bridge':make_room(83, [0]),
# 'Desert Four Statues':make_room(83, [2]),
# 'Desert Beamos Hall':make_room(83, right_side),
# 'Desert Tiles 2':make_room(67, [3]),
# 'Desert Wall Slide':make_room(67, top_side),
# 'Desert Boss':make_room(51, [2]),
#
#         # Hera
# 'Hera Basement Cage':make_room(135, [2]),
# 'Hera Tile Room':make_room(135, [0]),
# 'Hera Tridorm':make_room(135, [1]),
# 'Hera Torches':make_room(135, [3]),
# 'Hera Beetles':make_room(49, [3]),
# 'Hera Startile Corner':make_room(49, [2]),
# 'Hera Startile Wide':make_room(49, top_side),
# 'Hera Fairies':make_room(167, [0]),
#
#         # pod

# 'PoD Conveyor':make_room(59, left_side),
# 'PoD Mimics 1':make_room(75, [0]),
# 'PoD Jelly Hall':make_room(75, bottom_side),
# 'PoD Warp Hint':make_room(75, [1]),
#
#         # swamp
# 'Swamp Push Statue':make_room(38, bottom_side),
# 'Swamp Shooters':make_room(38, [0]),
# 'Swamp Left Elbow':make_room(38, [1]),
# 'Swamp Right Elbow':make_room(38, [1]),

# 'Swamp C':make_room(22, [1]),
# 'Swamp Waterway':make_room(22, bottom_side),
# 'Swamp I':make_room(22, top_side),
# 'Swamp T':make_room(22, [0]),
# 'Swamp Boss':make_room(6, [2]),
#
#         # sw
# 'Skull 1 Lobby':make_room(88, [2]),
# 'Skull Map Room':make_room(88, [3]),
# 'Skull Pot Circle':make_room(88, [1]),
# 'Skull Pull Switch':make_room(88, [0]),
# 'Skull Big Chest':make_room(88, [2]),
# 'Skull Pinball':make_room(104, all_quadrants),
# 'Skull Compass Room':make_room(103, right_side), #????
# 'Skull Left Drop':make_room(103, left_side), #???
# 'Skull Pot Prison':make_room(87, [3]),
# 'Skull 2 East Lobby':make_room(87, [2]),
# 'Skull Big Key':make_room(87, [0]),
# 'Skull Lone Pot':make_room(87, [1]),
# 'Skull Small Hall':make_room(86, [3]), #???
# 'Skull Back Drop':make_room(86, right_side),
# 'Skull 2 West Lobby':make_room(86, [2]),
# 'Skull X Room':make_room(86, [0]),
# 'Skull 3 Lobby':make_room(89, left_side),
# 'Skull East Bridge':make_room(89, right_side),
# 'Skull West Bridge Nook':make_room(89, [2]),

# 'Skull Spike Corner':make_room(57, [2]),
# 'Skull Final Drop':make_room(57, [3]),
# 'Skull Boss':make_room(41, [3]),
#
#         # tt
# 'Thieves Hallway':make_room(188, right_side),
# 'Thieves Boss':make_room(172, [3]),
# 'Thieves Pot Alcove Mid':make_room(188, [2]),
# 'Thieves Pot Alcove Bottom':make_room(188, [2]),
# 'Thieves Pot Alcove Top':make_room(188, [2]),
# 'Thieves Conveyor Maze':make_room(188, [0]),
# 'Thieves Spike Track':make_room(187, [3]),
# 'Thieves Hellway':make_room(187, left_side),
# 'Thieves Hellway N Crystal':make_room(187, [0]),
# 'Thieves Hellway S Crystal':make_room(187, [2]),
# 'Thieves Triple Bypass':make_room(187, [1]),

# 'Thieves Attic':make_room(100, [2]),
# 'Thieves Cricket Hall Left':make_room(100, [3]),
# 'Thieves Cricket Hall Right':make_room(101, [2]),
# 'Thieves Attic Window':make_room(101, [3]),
# 'Thieves Basement Block':make_room(69, [0]),
# 'Thieves Blocked Entry':make_room(69, [0]),
# 'Thieves Lonely Zazak':make_room(69, [2]),
# 'Thieves Blind\'s Cell':make_room(69, right_side),
# 'Thieves Conveyor Bridge':make_room(68, right_side),
# 'Thieves Conveyor Block':make_room(68, [1]),
# 'Thieves Big Chest Room':make_room(68, [2]),
# 'Thieves Trap':make_room(68, [0]),
#
#         # ice
# 'Ice Floor Switch':make_room(30, [2]),
# 'Ice Cross Left':make_room(30, [3]),
# 'Ice Cross Bottom':make_room(30, [3]),
# 'Ice Cross Right':make_room(30, [3]),
# 'Ice Cross Top':make_room(30, [3]),
# 'Ice Pengator Switch':make_room(31, [2]),
# 'Ice Dead End':make_room(31, [3]),
# 'Ice Big Key':make_room(31, [3]),
# 'Ice Bomb Drop':make_room(30, [1]),
# 'Ice Stalfos Hint':make_room(62, [1]),
# 'Ice Conveyor':make_room(62, bottom_side),
# 'Ice Hammer Block':make_room(63, [2]),
# 'Ice Tongue Pull':make_room(63, [3]),
# 'Ice Freezors':make_room(126, [2]),
# 'Ice Freezors Ledge':make_room(126, [2]),
# 'Ice Tall Hint':make_room(126, right_side),
# 'Ice Hookshot Ledge':make_room(127, [0]),
# 'Ice Hookshot Balcony':make_room(127, [0]),
# 'Ice Spikeball':make_room(127, [2]),
# 'Iced T':make_room(174, [1]),
# 'Ice Catwalk':make_room(175, [0]),
# 'Ice Many Pots':make_room(159, [2]),
# 'Ice Crystal Right':make_room(158, [3]),
# 'Ice Crystal Left':make_room(158, [3]),
# 'Ice Crystal Block':make_room(158, [3]),
# 'Ice Big Chest View':make_room(158, [2]),
# 'Ice Big Chest Landing':make_room(158, [2]),
# 'Ice Backwards Room':make_room(158, [1]), #???
# 'Ice Anti-Fairy':make_room(190, [1]),#???
# 'Ice Switch Room':make_room(190, [3]),
# 'Ice Refill':make_room(191, [2]),
# 'Ice Fairy':make_room(191, [1]),
# 'Ice Antechamber':make_room(206, [1]),
# 'Ice Boss':make_room(222, [1]),
#
#         # mire
# 'Mire Lobby':make_room(152, bottom_side),
# 'Mire Post-Gap':make_room(152, [3]),
# 'Mire 2':make_room(210, right_side),
# 'Mire Lone Shooter':make_room(195, [2]),
# 'Mire Failure Bridge':make_room(195, left_side),
# 'Mire Falling Bridge':make_room(195, right_side),
# 'Mire Map Spike Side':make_room(195, [0]),
# 'Mire Map Spot':make_room(195, [0]),
# 'Mire Crystal Dead End':make_room(195, [0]),
# 'Mire Hidden Shooters':make_room(178, [3]),
# 'Mire Hidden Shooters Blocked':make_room(178, [3]),
# 'Mire Cross':make_room(178, [2]),
# 'Mire Minibridge':make_room(178, [1]),
# 'Mire BK Door Room':make_room(178, top_side),

# 'Mire Torches Top':make_room(151, [0]),
# 'Mire Torches Bottom':make_room(151, [2]),
# 'Mire Attic Hint':make_room(151, right_side),
# 'Mire Dark Shooters':make_room(147, top_side),
# 'Mire Key Rupees':make_room(147, [3]),
# 'Mire Block X':make_room(147, [2]),
# 'Mire Tall Dark and Roomy':make_room(146, right_side),
# 'Mire Crystal Right':make_room(146, [2]),
# 'Mire Crystal Mid':make_room(146, [2]),
# 'Mire Crystal Left':make_room(146, [2]),
# 'Mire Crystal Top':make_room(146, [0]),
# 'Mire Shooter Rupees':make_room(146, [0]),
# 'Mire Falling Foes':make_room(145, right_side),
# 'Mire Firesnake Skip':make_room(160, [1]),
# 'Mire Antechamber':make_room(160, [0]),
# 'Mire Boss':make_room(144, [2]),
#
#         # tr
# 'TR Final Abyss':make_room(180, all_quadrants),
# 'TR Boss':make_room(164, [2]),
#
#         # gt
# 'GT Lobby':make_room(12, all_quadrants),
# 'GT Blocked Stairs':make_room(140, [2]),
# 'GT Tile Room':make_room(141, [0]),
# 'GT Speed Torch':make_room(141, right_side),
# 'GT Speed Torch Upper':make_room(141, [1]),
# 'GT Pots n Blocks':make_room(141, [2]),
# 'GT Crystal Conveyor':make_room(157,[1]),
# 'GT Compass Room':make_room(157, [0]),
#
# 'GT Invisible Catwalk':make_room(156, all_quadrants), #???
#
#
# 'GT Double Switch Switches':make_room(155, [0]),
# 'GT Double Switch Transition':make_room(155, [0]),
# 'GT Double Switch Key Spot':make_room(155, [0]),
# 'GT Double Switch Exit':make_room(155, [0]),
# 'GT Spike Crystals':make_room(155, [1]),
# 'GT Warp Maze - Left Section':make_room(155, bottom_side),
# 'GT Warp Maze - Mid Section':make_room(155, bottom_side),
# 'GT Warp Maze - Right Section':make_room(155, bottom_side),
# 'GT Warp Maze - Pit Section':make_room(155, bottom_side),
# 'GT Warp Maze - Pit Exit Warp Spot':make_room(155, bottom_side),
#
# 'GT Firesnake Room':make_room(125, top_side),
# 'GT Firesnake Room Ledge':make_room(125, top_side),
# 'GT Warp Maze - Rail Choice':make_room(125, [2]), #ugh. Need to attach this together
# 'GT Warp Maze - Rando Rail':make_room(125, [2]),
# 'GT Warp Maze - Main Rails':make_room(125, [2]),
# 'GT Warp Maze - Pot Rail':make_room(125, [2]),
# 'GT Petting Zoo':make_room(125, [3]),

# 'GT Ice Armos':make_room(28, [3]),
# 'GT Big Key Room':make_room(28, [1]),
# 'GT Four Torches':make_room(28, [2]),
# 'GT Fairy Abyss':make_room(28, [0]),
# 'GT Cannonball Bridge':make_room(92, top_side),
# 'GT Refill':make_room(92, [3]),
# 'GT Gauntlet 1':make_room(93, [1]),
# 'GT Gauntlet 2':make_room(93, [0]),
# 'GT Gauntlet 3':make_room(93, [2]),
# 'GT Gauntlet 4':make_room(109, [0]),
# 'GT Gauntlet 5':make_room(109, [2]),
# 'GT Beam Dash':make_room(108, [3]),
# 'GT Lanmolas 2':make_room(108, [2]),
# 'GT Quad Pot':make_room(108, [1]),
# 'GT Wizzrobes 1':make_room(165, all_quadrants),
# 'GT Dashing Bridge':make_room(165, all_quadrants),
# 'GT Wizzrobes 2':make_room(165, all_quadrants),
# 'GT Conveyor Bridge':make_room(149, right_side),
# 'GT Torch Cross':make_room(150, left_side),
# 'GT Staredown':make_room(150, [3]),
# 'GT Falling Torches':make_room(61, [3]),
# 'GT Mini Helmasaur Room':make_room(61, [1]),
# 'GT Bomb Conveyor':make_room(61, [0]),
# 'GT Crystal Circles':make_room(61, [2]),
# 'GT Left Moldorm Ledge':make_room(77, [0]),
# 'GT Right Moldorm Ledge':make_room(77, [1]),
# 'GT Moldorm':make_room(77, all_quadrants),
# 'GT Moldorm Pit':make_room(166, all_quadrants),
# 'GT Validation':make_room(77, bottom_side),
# 'GT Validation Door':make_room(77, [2]),
# 'GT Frozen Over':make_room(76, right_side),
# 'GT Brightly Lit Hall':make_room(29, top_side),
# 'GT Agahnim 2':make_room(13, [2]),
# }
#
