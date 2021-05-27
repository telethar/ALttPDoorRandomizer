from DungeonGenerator import dungeon_portals
from MapData import region_to_rooms, GridMap, GridNode, NodeType, init_map_data
from BaseClasses import Direction, DoorType, Door

from collections import deque
import cv2
import logging
import os


class MapPiece(object):

    def __init__(self):
        pass


increment = 64
quad_mappings = {
    Direction.South: {
        0: 2, 2: 3, 1: 3
    },
    Direction.North: {
        0: 0, 2: 1, 1: 1
    }
}


class DefermentQueue(object):

    def __init__(self):
        self.warp = {}
        self.collision = {}
        self.floor = {}

    def any_ready(self):
        return len(self.warp) > 0 or len(self.collision) > 0 or len(self.floor) > 0


class VisitedData(object):

    def __init__(self):
        self.regions = set()
        self.doors = set()
        self.unconnected = {}  # door to floor it is mapped on
        self.connected = set()

    def connect(self, door):
        if door in self.unconnected:
            del self.unconnected[door]
        self.connected.add(door)
        if door.dest in self.unconnected:
            del self.unconnected[door]
        if isinstance(door.dest, Door):
            self.connected.add(door.dest)


def init_cursor(current_pos, door):
    return slide_cursor(current_pos, door.direction), quad_mappings[door.direction][door.doorIndex]


def slide_cursor(pos, direction):
    if direction is None or pos is None:
        return pos
    if direction == Direction.South:
        return pos[0], pos[1]-1
    if direction == Direction.North:
        return pos[0], pos[1]+1
    if direction == Direction.West:
        return pos[0]+1, pos[1]
    if direction == Direction.East:
        return pos[0]-1, pos[1]

# todo: warp affinity - for placing certain warps near each other


def create_maps(world):
    for player in range(1, world.players+1):
        init_map_data()
        for dungeon in world.dungeon_layouts[player].keys():
            portal_list = dungeon_portals[dungeon]
            if len(portal_list) == 1:
                portal = world.get_portal(next(iter(portal_list)), player)
                create_dungeon_map(dungeon, portal, world, player)


def create_dungeon_map(dungeon, portal, world, player):
    dungeon_floors = []
    door = portal.door
    init_pos = (5, 7) if door.doorIndex == 2 else (4, 7)
    init_floor = GridMap()
    dungeon_floors.append(init_floor)
    visited = VisitedData()
    visited.doors.add(door)
    queue = deque([(door, init_pos, init_floor)])
    deferred = DefermentQueue()
    while len(queue) > 0:
        door, current_pos, cur_floor = queue.popleft()
        if door.entranceFlag:
            cur_floor.add_node(current_pos, GridNode('entrance-arrow.png', NodeType.Entrance))
            if current_pos == init_pos:  # todo: remember to reset init_pos on starting a new portal
                region, dest = door.entrance.parent_region, door.name
            else:
                # todo: remove from portal deferred?
                region, dest = None, None
        else:
            region, dest = door.entrance.connected_region, door.dest.name
        if region and region in visited.regions:
            continue
        if region and region.name in region_to_rooms:
            map_node = region_to_rooms[region.name]
            direction = special_warps[door.name] if door.name in special_warps else door.direction
            match_point = current_pos if door.entranceFlag else slide_cursor(current_pos, direction)
            shift, match_node = cur_floor.match_items(map_node, match_point, dest)
            if not cur_floor.check_for_collisions(map_node, shift, match_node, current_pos):
                cur_floor.merge_map(map_node, shift, match_node)
                visited.connect(door)
                visited.regions.add(region)
                if region in deferred.collision:
                    del deferred.collision[region]
                queue_doors_for_new_region(cur_floor, queue, region, deferred, visited)
            else:
                if region.name in deferred.collision:
                    collision_options = deferred.collision[region]
                else:
                    collision_options = []
                    deferred.collision[region] = collision_options
                collision_options.append((door, current_pos, cur_floor))
                # this is where we'd adjust things via connectors or create a new floor
        if region and region.name not in region_to_rooms:
            logging.getLogger('').warning(f'{region} does not have map data')
        while len(queue) == 0 and deferred.any_ready():
            if len(deferred.warp) > 0:
                d = next(iter(deferred.warp.values()))
                if d not in visited.doors:
                    region = d.entrance.connected_region
                    if region not in visited.regions:
                        floor = find_floor_for_warp(d, dungeon_floors)
                        visited.regions.add(region)
                        queue_doors_for_new_region(floor, queue, region, deferred, visited)
                del deferred.warp[d.name]
            elif len(deferred.collision) > 0:
                region, option_list = next(iter(deferred.collision.items()))
                if region not in visited.regions:
                    # todo: figure out if we can slide it in using connectors
                    # chosen = random.choice(option_list)
                    add_new_floor(dungeon_floors, deferred, queue, region, visited)
                del deferred.collision[region]
            elif len(deferred.floor) > 0:
                d = next(iter(deferred.floor.values()))
                if d not in visited.doors:
                    region = d.entrance.connected_region
                    if region not in visited.regions:
                        covering_floor = covered(region, dungeon_floors)
                        if not covering_floor:
                            add_new_floor(dungeon_floors, deferred, queue, region, visited)
                        elif isinstance(covering_floor, GridMap):
                            visited.regions.add(region)
                            queue_doors_for_new_region(covering_floor, queue, region, deferred, visited)
                del deferred.floor[d.name]
            # todo: check the portal deferred
    dungeon_floors = combine_floors(dungeon_floors, visited)
    for i, floor in enumerate(dungeon_floors):
        fill_out_floor(floor)
        create_floor_image(floor, dungeon, f'{i + 1}f', player, world.seed)


def combine_floors(dungeon_floors, visited):
    while len(visited.unconnected) > 0:
        door, floor = next(iter(visited.unconnected.items()))
        if door.dest in visited.unconnected:
            dest_floor = visited.unconnected[door.dest]
            if dest_floor == floor:
                pass  # todo: can replace the reserved spot with a symbol or ignore if they don't have reserved spots
            else:
                spot = floor.can_add(dest_floor)
                if spot:
                    floor.merge_map(dest_floor, spot, None)
                    dungeon_floors.remove(dest_floor)
                    # re-write references
                    visited.unconnected = {d: (f if f != dest_floor else floor) for d, f in visited.unconnected.items()}
            del visited.unconnected[door.dest]
        del visited.unconnected[door]
    return dungeon_floors


def add_new_floor(dungeon_floors, deferred, queue, region, visited):
    init_shift = (4, 4)
    new_floor = GridMap()
    new_floor.merge_map(region_to_rooms[region.name], init_shift, None)
    visited.regions.add(region)
    dungeon_floors.append(new_floor)
    queue_doors_for_new_region(new_floor, queue, region, deferred, visited)


def covered(region, dungeon_floors):
    if region.name not in region_to_rooms:
        logging.getLogger('').warning(f'{region} does not have map data')
        return True
    room_piece = region_to_rooms[region.name]
    wanted_tile, quad_set = next(iter(room_piece.tileIndices.items()))
    for floor in dungeon_floors:
        if wanted_tile in floor.tileIndices:
            if quad_set.issubset(floor.tileIndices[wanted_tile]):
                return floor
    return False


def find_floor_for_warp(door, dungeon_floors):
    if 'Rail' in door.name:
        target = 'GT Warp Maze (Pits) ES'
    else:
        target = 'GT Warp Maze (Rails) WS'
    for floor in dungeon_floors:
        if target in floor.door_map:
            return floor
    logging.getLogger('').error(f'Unable to find {target} for {door}. Warp deferment problem')
    assert False


special_warps = {'GT Spike Crystals Warp': Direction.South, 'GT Warp Maze - Rail Choice Left Warp': Direction.South,
                 'GT Warp Maze - Pit Exit Warp': Direction.North}

warp_follow = {
    'GT Warp Maze - Rail Choice Right Warp', 'GT Warp Maze - Rando Rail Warp', 'GT Warp Maze - Main Rails Best Warp',
    'GT Warp Maze - Main Rails Mid Left Warp', 'GT Warp Maze - Main Rails Mid Right Warp',
    'GT Warp Maze - Main Rails Right Top Warp', 'GT Warp Maze - Main Rails Right Mid Warp',
    'GT Warp Maze - Left Section Warp', 'GT Warp Maze - Mid Section Left Warp', 'GT Warp Maze - Mid Section Right Warp',
    'GT Warp Maze - Right Section Warp', 'GT Warp Maze - Pot Rail Warp'
}


def queue_doors_for_new_region(cur_floor, queue, region, deferred, visited):
    doors_to_visit = find_doors(region, visited, cur_floor)
    for d in doors_to_visit:
        if d.type in [DoorType.SpiralStairs, DoorType.Hole, DoorType.Warp] and d.name not in special_warps:
            if d.name in warp_follow:
                deferred.warp[d.name] = d
            else:
                deferred.floor[d.name] = d
                if d.type == DoorType.SpiralStairs:
                    visited.unconnected[d] = cur_floor
        else:
            d_position = cur_floor.door_map[d.name] if d.name in cur_floor.door_map else None
            if d_position is None:  # middle doors of 3
                deferred.floor[d.name] = d
            else:
                queue.append((d, d_position, cur_floor))
                visited.unconnected[d] = cur_floor
                visited.doors.add(d)
                visited.doors.add(d.dest)


def find_doors(region, visited, cur_floor):
    queue = deque(region.exits)
    doors_to_visit = set()
    while len(queue) > 0:
        an_exit = queue.popleft()
        if an_exit.door:
            if an_exit.door.type in [DoorType.Logical, DoorType.Interior]:
                visited.doors.add(an_exit.door)
                if an_exit.connected_region:
                    conn = an_exit.connected_region
                elif an_exit.door.type != DoorType.Logical:  # blocked doors?
                    conn = an_exit.door.dest.entrance.parent_region
                else:
                    conn = None
                if conn and conn not in visited.regions:
                    visited.regions.add(conn)
                    for e in conn.exits:
                        queue.append(e)
            elif an_exit.door not in visited.doors:
                doors_to_visit.add(an_exit.door)
            elif an_exit.door not in visited.connected:
                visited.unconnected[an_exit.door] = cur_floor

    return doors_to_visit


def fill_out_floor(cur_floor):
    height = cur_floor.height()
    v_margin = (10 - height) // 2
    v_min = cur_floor.minHeight - v_margin
    v_max = cur_floor.maxHeight + v_margin + (0 if height % 2 == 0 else 1)

    width = cur_floor.width()
    h_margin = (10 - width) // 2
    h_min = cur_floor.minWidth - h_margin
    h_max = cur_floor.maxWidth + h_margin + (0 if width % 2 == 0 else 1)

    for x in range(h_min, h_max):
        for y in range(v_min, v_max):
            if (x, y) not in cur_floor.nodeMap:
                cur_floor.add_node((x, y), GridNode('empty-tile.png', NodeType.Empty))


def create_floor_image(cur_floor, dungeon, fid, player, seed):
    im_cache = {}
    im_rows = []
    for y in range(cur_floor.minHeight, cur_floor.maxHeight):
        im_row = []
        for x in range(cur_floor.minWidth, cur_floor.maxWidth):
            node = cur_floor.nodeMap[(x, y)]
            if node.image not in im_cache:
                im = cv2.imread(f'data/room_images/{node.image}')
                im_cache[node.image] = im
            im_row.append(im_cache[node.image])
        im_rows.append((cv2.hconcat(im_row)))
    full_im = cv2.vconcat(im_rows)
    os.makedirs('map_spoiler', exist_ok=True)
    cv2.imwrite(f'map_spoiler/{dungeon}-{fid}-{player}-{seed}.png', full_im)

