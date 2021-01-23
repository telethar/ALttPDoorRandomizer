import logging
from collections import Counter, deque, defaultdict
from itertools import groupby

from BaseClasses import CrystalBarrier, RegionType, dungeon_keys
from EntranceShuffle import indirect_connections


class WorldAnalyzer(object):

    def __init__(self, parent):
        self.world = parent
        parent.analyzer = self
        self.reachable_regions = {player: dict() for player in range(1, parent.players + 1)}
        self.blocked_connections = {player: dict() for player in range(1, parent.players + 1)}

        self.location_logic = {player: dict() for player in range(1, parent.players + 1)}

        self.logic_lookup = {player: dict() for player in range(1, parent.players + 1)}
        self.reverse_lookup = {player: dict() for player in range(1, parent.players + 1)}

        # self.item_locked_by = {player: dict() for player in range(1, parent.players + 1)}
        # self.item_locks = {player: dict() for player in range(1, parent.players + 1)}

    def analyze(self, player):
        rrp = self.reachable_regions[player]
        bc = self.blocked_connections[player]

        # init on first call - this can't be done on construction since the regions don't exist yet
        start = self.world.get_region('Menu', player)
        if not start in rrp:
            rrp[start] = (CrystalBarrier.Orange, [Counter()], [[]])
            for conn in start.exits:
                requirements = conn.access_rule.get_requirements(self)
                bc[conn] = (CrystalBarrier.Orange, requirements, [])

        queue = deque(self.blocked_connections[player].items())

        self.traverse_world(queue, rrp, bc, player)

    def build_location_logic(self):
        for location in self.world.get_locations():
            loc_logic = location.access_rule.get_requirements(self)
            record = self.reachable_regions[location.player][location.parent_region]
            cs, region_logic, paths = record
            new_logic = merge_requirements(region_logic, loc_logic)
            paths = [k for k, v in groupby(paths)]
            self.location_logic[location.player][location] = (new_logic, paths)
            self.track_locks(location)

    @staticmethod
    def is_interesting_item(item):
        return item.advancement or item.priority or item.type is not None  # todo: heart containers and poh?

    # todo: multiworld
    def track_locks(self, location):
        (new_logic, paths) = self.location_logic[location.player][location]
        if location.item and len(new_logic) > 0 and self.is_interesting_item(location.item):
            item_name = 'Bottle' if location.item.name.startswith('Bottle') else location.item.name
            valid_logic = []
            if not isinstance(new_logic, list):
                new_logic = [new_logic]
            for potential_logic in new_logic:
                if item_name not in potential_logic or (item_name in progress_max and progress_max[item_name] - potential_logic[item_name] > 0):
                    valid_logic.append(potential_logic)
            if len(valid_logic) < len(new_logic):
                self.location_logic[location.player][location] = (valid_logic, paths)
                # todo: back track and clean up invalid logics

            indices = []
            for i, lgc in enumerate(new_logic):
                replaces = []
                for item, cnt in lgc.items():
                    if item in self.logic_lookup[location.item.player]:
                        replaces.append((item, self.logic_lookup[location.item.player][item][0]))  # todo: multiple
                for remove, replace in replaces:
                    del lgc[remove]  # todo: progressives
                    indices.append((i, merge_requirements(lgc, replace)))
            for idx, replacement in indices:
                new_logic[idx] = replacement

            if item_name not in self.logic_lookup[location.item.player]:
                self.logic_lookup[location.item.player][item_name] = []
            lookup_list = self.logic_lookup[location.item.player][item_name]
            lookup_list.append(new_logic)

            for lgc in new_logic:
                for item, cnt in lgc.items():
                    if item not in self.reverse_lookup[location.item.player]:
                        self.reverse_lookup[location.item.player][item] = set()
                    refs = self.reverse_lookup[location.item.player][item]
                    refs.add(item_name)

            # clean up lookup table
            if item_name in self.reverse_lookup[location.item.player]:
                for ref in self.reverse_lookup[location.item.player][item_name]:
                    old_logic = self.logic_lookup[location.item.player][ref][0]  # todo: multiple
                    for lgc in old_logic:
                        lgc[item_name] = 0  # todo: progressives
                    new_reqs = merge_requirements(old_logic, new_logic)
                    new_reqs = new_reqs if isinstance(new_reqs, list) else [new_reqs]
                    self.logic_lookup[location.item.player][ref] = new_reqs




            # logic_intersection = None
            # for valid in valid_logic:
            #     if not logic_intersection:
            #         logic_intersection = Counter(valid)
            #     else:
            #         logic_intersection &= valid
            # if item_name in self.item_locked_by[location.item.player]:
            #     item = self.item_locked_by[location.item.player][item_name]
            #     if not isinstance(item, list):
            #         item = self.item_locked_by[location.item.player][item_name] = [item]
            #     item.append(logic_intersection)
            # else:
            #     self.item_locked_by[location.item.player][item_name] = logic_intersection
            # for item, count in logic_intersection.items():
            #     locks = self.item_locks[location.player]
            #     if (item, count) not in locks:
            #         self.item_locks[location.player][(item, count)] = Counter()
            #     self.item_locks[location.player][(item, count)][item_name] += 1

    def traverse_world(self, queue, rrp, bc, player):
        # run BFS on all connections, and keep track of those blocked by missing items
        while len(queue) > 0:

            connection, record = queue.popleft()
            crystal_state, logic, path = record
            new_region = connection.connected_region
            if not self.should_visit(new_region, rrp, crystal_state, logic):
                bc.pop(connection, None)
            elif self.should_defer(logic):
                requirements = connection.access_rule.get_requirements(self)
                queue.append((connection, (crystal_state, requirements, path)))
            else:
                if new_region.type == RegionType.Dungeon:
                    new_crystal_state = crystal_state
                    for conn in new_region.exits:
                        door = conn.door
                        if door is not None and door.crystal == CrystalBarrier.Either:
                            new_crystal_state = CrystalBarrier.Either
                            break
                    if new_region in rrp:
                        new_crystal_state |= rrp[new_region][0]

                    self.assign_rrp(rrp, new_region, new_crystal_state, logic, path)
                    for conn in new_region.exits:
                        new_logic = merge_requirements(logic, conn.access_rule.get_requirements(self))
                        new_path = list(path) + [conn]
                        door = conn.door
                        if new_crystal_state == CrystalBarrier.Either:
                            bc.pop(conn, None)
                        if door is not None and not door.blocked:
                            door_crystal_state = door.crystal if door.crystal else new_crystal_state
                            packet = (door_crystal_state, new_logic, new_path)
                            bc[conn] = packet
                            queue.append((conn, packet))
                        elif door is None:
                            # note: no door in dungeon indicates what exactly? (always traversable)?
                            packet = (new_crystal_state, new_logic, new_path)
                            queue.append((conn, packet))
                else:
                    self.assign_rrp(rrp, new_region, CrystalBarrier.Orange, logic, path)
                    bc.pop(connection, None)
                    for conn in new_region.exits:
                        new_logic = merge_requirements(logic, conn.access_rule.get_requirements(self))
                        packet = (CrystalBarrier.Orange, new_logic, list(path) + [conn])
                        bc[conn] = packet
                        queue.append((conn, packet))

                # Retry connections if the new region can unblock them
                if new_region.name in indirect_connections:
                    new_entrance = self.world.get_entrance(indirect_connections[new_region.name], player)
                    if new_entrance in bc and new_entrance not in queue and new_entrance.parent_region in rrp:
                        for i in range(0, len(rrp[new_entrance.parent_region][1])):
                            trace = rrp[new_entrance.parent_region]
                            new_logic = merge_requirements(trace[1][i], new_entrance.access_rule.get_requirements(self))
                            packet = (trace[0], new_logic, trace[2][i])
                            queue.append((new_entrance, packet))

    def should_visit(self, new_region, rrp, crystal_state, logic):
        if not new_region:
            return False
        if new_region not in rrp:
            return True
        record = rrp[new_region]
        visited_logic = record[1]
        logic_is_different = self.is_logic_different(logic, visited_logic)
        if new_region.type != RegionType.Dungeon and logic_is_different:
            return True
        return (record[0] & crystal_state) != crystal_state or logic_is_different

    @staticmethod
    def should_defer(logic):
        if not isinstance(logic, list):
            logic = [logic]
        for lgc in logic:
            if 'Unreachable' in lgc:
                return True
        return False

    @staticmethod
    def is_logic_different(current_logic, old_logic):
        if isinstance(old_logic, list):
            if isinstance(current_logic, list):
                current_state = [True] * len(current_logic)
                for i, current in enumerate(current_logic):
                    for oldie in old_logic:
                        logic_diff = oldie - current
                        if len(logic_diff) == 0:
                            current_state[i] = False
                            break
                    if current_state[i]:
                        return True
                return False
            else:
                for oldie in old_logic:
                    logic_diff = oldie - current_logic
                    if len(logic_diff) == 0:
                        return False
                return True
        elif isinstance(current_logic, list):
            for current in current_logic:
                logic_diff = old_logic - current
                if len(logic_diff) > 0:
                    return True
            return False
        else:
            logic_diff = old_logic - current_logic
            return len(logic_diff) > 0

    @staticmethod
    def assign_rrp(rrp, new_region, barrier, logic, path):
        record = rrp[new_region] if new_region in rrp else (barrier, [], [])
        rrp[new_region] = WorldAnalyzer.combine_logic(record, barrier, logic, path)

    @staticmethod
    def combine_logic(record, barrier, logic, path):
        logic_to_delete, logic_to_append = [], []
        for visited_logic in record[1]:
            if not WorldAnalyzer.is_logic_different(visited_logic, logic):
                logic_to_delete.append(visited_logic)
        if isinstance(logic, list):
            for logic_item in logic:
                if WorldAnalyzer.is_logic_different(logic_item, record[1]):
                    logic_to_append.append(logic_item)
        elif WorldAnalyzer.is_logic_different(logic, record[1]):
            logic_to_append.append(logic)
        for deletion in logic_to_delete:
            idx = record[1].index(deletion)
            record[1].pop(idx)
            record[2].pop(idx)
        for logic_item in logic_to_append:
            record[1].append(logic_item)
            record[2].append(path)
        return barrier, record[1], record[2]

    @staticmethod
    def print_rrp(rrp):
        logger = logging.getLogger('')
        logger.debug('RRP Checking')
        for region, packet in rrp.items():
            new_crystal_state, logic, path = packet
            logger.debug(f'\nRegion: {region.name} (CS: {str(new_crystal_state)})')
            for i in range(0, len(logic)):
                logger.debug(f'{logic[i]}')
                logger.debug(f'{",".join(str(x) for x in path[i])}')

    def print_location_logic(self):
        logger = logging.getLogger('')
        logger.debug('Location Checking')
        for player in range(1, self.world.players + 1):
            for location, packet in self.location_logic[player].items():
                logic, path = packet
                logger.debug(f'\nLocation: {location.name}')
                if isinstance(logic, list):
                    for i in range(0, len(logic)):
                        logger.debug(f'{logic[i]}')
                else:
                    logger.debug(f'{logic}')
                for i in range(0, len(path)):
                    logger.debug(f'{", ".join(str(x) for x in path[i])}')


def merge_requirements(starting_requirements, new_requirements):
    merge = []
    if isinstance(starting_requirements, list):
        for req in starting_requirements:
            if isinstance(new_requirements, list):
                for new_r in new_requirements:
                    merge.append(req | new_r)
            else:
                merge.append(req | new_requirements)
    elif isinstance(new_requirements, list):
        for new_r in new_requirements:
            merge.append(starting_requirements | new_r)
    else:
        return reduce_requirements(starting_requirements | new_requirements)
    return reduce_requirements(merge)


only_one = {'Moon Pearl', 'Hammer', 'Blue Boomerang', 'Red Boomerang', 'Hookshot', 'Mushroom', 'Powder',
            'Fire Rod', 'Ice Rod', 'Bombos', 'Ether', 'Quake', 'Lamp', 'Shovel', 'Ocarina', 'Bug Catching Net',
            'Book of Mudora', 'Magic Mirror', 'Cape', 'Cane of Somaria', 'Cane of Byrna', 'Flippers', 'Pegasus Boots'}


def reduce_requirements(requirements):
    if not isinstance(requirements, list):
        requirements = [requirements]
    for req in requirements:
        for item in [x for x in req.keys() if x in only_one and req[x] > 1]:
            req[item] = 1
        substitute_progressive(req)  # todo: work with non-progressives?
    removals = []
    requirements = list(requirements)
    dedup_requirements = []
    for req in requirements:
        if req not in dedup_requirements:
            dedup_requirements.append(req)
    # subset manip
    for i, req in enumerate(dedup_requirements):
        for j, other_req in enumerate(dedup_requirements):
            if i == j:
                continue
            if all(req[k] >= other_req[k] for k in (req | other_req)):
                removals.append(req)
    reduced = list(dedup_requirements)  # todo: optimize by doing it in place?
    for removal in removals:
        if removal in reduced:
            reduced.remove(removal)
    assert len(reduced) != 0
    return reduced[0] if len(reduced) == 1 else list(reduced)


progress_sub = {
    'Fighter Sword': ('Progressive Sword', 1),
    'Master Sword': ('Progressive Sword', 2),
    'Tempered Sword': ('Progressive Sword', 3),
    'Golden Sword': ('Progressive Sword', 4),
    'Power Glove': ('Progressive Glove', 1),
    'Titans Mitts': ('Progressive Glove', 2),
    'Bow': ('Progressive Bow', 1),
    'Silver Arrows': ('Progressive Bow', 2),
    'Blue Mail': ('Progressive Armor', 1),
    'Red Mail': ('Progressive Armor', 2),
    'Blue Shield': ('Progressive Shield', 1),
    'Red Shield': ('Progressive Shield', 2),
    'Mirror Shield': ('Progressive Shield', 3),
}


def substitute_progressive(req_counter):
    for item in [x for x in req_counter.keys() if x in progress_sub.keys()]:
        progressive_item, count = progress_sub[item]
        req_counter[progressive_item] = count
        del req_counter[item]


# todo: pools with more/less progressives
progress_max = {
    'Progressive Sword': 4,
    'Progressive Glove': 2,
    'Progressive Bow': 2,
    'Progressive Armor': 2,
    'Progressive Shield': 3,
    'Bottle': 4,
}