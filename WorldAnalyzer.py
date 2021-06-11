import logging
from collections import Counter, deque, defaultdict
from itertools import groupby, combinations
from queue import PriorityQueue

from BaseClasses import CrystalBarrier, RegionType, dungeon_keys, ReqType, ReqSet
from EntranceShuffle import indirect_connections
from Items import ItemFactory
from Utils import merge_requirements, reduce_requirements


class WorldAnalyzer(object):

    def __init__(self, parent):
        self.world = parent
        parent.analyzer = self
        self.reachable_regions = {player: dict() for player in range(1, parent.players + 1)}
        self.blocked_connections = {player: dict() for player in range(1, parent.players + 1)}

        self.location_logic = {player: dict() for player in range(1, parent.players + 1)}

        self.logic_lookup = dict()
        self.reverse_lookup = dict()

    def analyze(self, player):
        rrp = self.reachable_regions[player]
        bc = self.blocked_connections[player]

        # init on first call - this can't be done on construction since the regions don't exist yet
        start = self.world.get_region('Menu', player)
        rrp_key = (start, CrystalBarrier.Orange)
        if not rrp_key in rrp:
            rrp[rrp_key] = ([ReqSet()], [[]])
            for conn in start.exits:
                requirements = conn.access_rule.get_requirements(self.world.progressive[player])
                bc[(conn, CrystalBarrier.Orange)] = (requirements, [])

        queue = PriorityQueue()
        for key, record in self.blocked_connections[player].items():
            queue.put(Visitor(key[0], key[1], record[0], record[1]))

        self.traverse_world(queue, rrp, bc, player)

    def build_location_logic(self):
        items = Counter()
        # init - logic lookup
        for player in range(1, self.world.players + 1):
            for location in self.world.get_filled_locations(player):
                if self.is_interesting_item(location.item):
                    item_name = 'Bottle' if location.item.name.startswith('Bottle') else location.item.name
                    items[(item_name, location.item.player)] += 1
            for prize in ItemFactory(['Red Pendant', 'Blue Pendant', 'Green Pendant', 'Crystal 1', 'Crystal 2',
                                      'Crystal 3', 'Crystal 4', 'Crystal 7', 'Crystal 5', 'Crystal 6'], player):
                items[(prize.name, prize.player)] += 1
        for dungeon in self.world.dungeons:
            for item in dungeon.all_items:
                if self.is_interesting_item(item):
                    item_name = 'Bottle' if item.name.startswith('Bottle') else item.name
                    items[(item_name, item.player)] += 1
        for item in self.world.itempool:
            if self.is_interesting_item(item):
                item_name = 'Bottle' if item.name.startswith('Bottle') else item.name
                items[(item_name, item.player)] += 1
        for key, amount in items.items():
            name, player = key
            self.logic_lookup[key] = ItemLogic(name, player, amount)

        for location in self.world.get_locations():
            loc_logic = location.access_rule.get_requirements(self)
            rrp = self.reachable_regions[location.player]
            if location.parent_region.type == RegionType.Dungeon:
                region_logic, paths = None, None
                for cs in [CrystalBarrier.Orange, CrystalBarrier.Blue, CrystalBarrier.Either]:
                    if (location.parent_region, cs) in rrp:
                        if region_logic is None:  # todo: or more simple
                            region_logic, paths = rrp[(location.parent_region, cs)]
            else:
                region_logic, paths = rrp[(location.parent_region, CrystalBarrier.Orange)]
            new_logic = merge_requirements(region_logic, loc_logic)
            paths = [k for k, v in groupby(paths)]
            self.location_logic[location.player][location] = (new_logic, paths)
            self.track_locks(location)

    @staticmethod
    def is_interesting_item(item):
        # deferred: heart containers and poh? - are we going for health requirements some day?
        return item.advancement or (item.type is not None and item.type in ['BigKey', 'SmallKey']) or (item.type is None and item.priority)

    # todo: multiworld
    def track_locks(self, location):
        (new_logic, paths) = self.location_logic[location.player][location]
        if location.item and self.is_interesting_item(location.item):
            if len(new_logic) == 0:
                item_name = 'Bottle' if location.item.name.startswith('Bottle') else location.item.name
                item_logic = self.logic_lookup[(item_name, location.item.player)]
                item_logic.locations.append(location)
                item_logic.logic_options.append(Counter())  # no requirements
                return

            key, complete_logic, valid_logic = self.calculate_complete_and_valid_logic(
                new_logic, location.player, location.item.name, location.item.player)
            if len(valid_logic) < len(complete_logic):
                self.location_logic[location.player][location] = (valid_logic, paths)
                # deferred: back track and clean up invalid logic - seems to be unnecessary

            item_logic = self.logic_lookup[key]
            # add this item to the item logic
            item_logic.logic_options.append(valid_logic)
            item_logic.locations.append(location)
            # clean up lookup table if this is now complete
            if item_logic.complete() and key in self.reverse_lookup:
                repeat, done, repeat_flagged = False, False, False
                while not done:
                    done = True
                    if repeat:
                        self.clean_up_complete(key, location.player)  # clean up the item logic first
                    for ref in self.reverse_lookup[key]:
                        if ref == key:
                            if not repeat:
                                done, repeat = False, True
                            continue
                        old_logic = self.logic_lookup[ref]
                        new_reqs = []
                        for logic in old_logic.logic_options:
                            if isinstance(logic, list):
                                sub_options = []
                                for sub_logic in logic:
                                    if key[0] in sub_logic:
                                        complete_valid, sub_merged = item_logic.get_option_subset(sub_logic[key[0]]), []
                                        for cv in complete_valid:
                                            sub_merge = merge_requirements(sub_logic, cv)
                                            (sub_merged.extend if isinstance(sub_merge, list) else sub_merged.append)(sub_merge)
                                        sub_options.extend(sub_merged)
                                        # self.record_reverse_refs(sub_merged, old_logic.player, ref)
                                    else:
                                        sub_options.append(sub_logic)
                                requirements = reduce_requirements(self.check_validity(sub_options, old_logic))
                                self.record_reverse_refs(requirements, old_logic.player, ref)
                                new_reqs.append(requirements)
                            elif key[0] in logic:
                                complete_valid, all_merged = item_logic.get_option_subset(logic[key[0]]), []
                                for cv in complete_valid:
                                    merged = merge_requirements(logic, cv)
                                    (all_merged.extend if isinstance(merged, list) else all_merged.append)(merged)
                                # self.record_reverse_refs(all_merged, old_logic.player, ref)
                                requirements = reduce_requirements(self.check_validity(all_merged, old_logic))
                                self.record_reverse_refs(requirements, old_logic.player, ref)
                                new_reqs.append(requirements)
                            else:
                                new_reqs.append(logic)
                        old_logic.logic_options = new_reqs

            # set up reverse lookup
            for lgc in valid_logic:
                self.record_reverse_refs(lgc, location.player, key)

    def calculate_complete_and_valid_logic(self, new_logic, location_player, name, player):
        if not isinstance(new_logic, list):
            new_logic = [new_logic]
        complete_logic = []
        for i, lgc in enumerate(new_logic):
            # update logic from the lookup - (makes a copy?)
            new_lgc = [Counter(x) for x in lgc] if isinstance(lgc, list) else Counter(lgc)
            for item, cnt in lgc.items():
                if (item, location_player) in self.logic_lookup:
                    item_logic = self.logic_lookup[(item, location_player)]
                    if item_logic.complete():
                        combined, subsets = [], item_logic.get_option_subset(cnt)
                        for subset in subsets:
                            merged = merge_requirements(new_lgc, subset)
                            (combined.extend if isinstance(merged, list) else combined.append)(merged)
                        new_lgc = combined
            (complete_logic.extend if isinstance(new_lgc, list) else complete_logic.append)(new_lgc)

        complete_logic = reduce_requirements(complete_logic)
        if not isinstance(complete_logic, list):
            complete_logic = [complete_logic]
        item_name = 'Bottle' if name.startswith('Bottle') else name
        item_player = player
        key = (item_name, item_player)

        valid_logic = self.check_validity(complete_logic, self.logic_lookup[key])
        return key, complete_logic, valid_logic

    def record_reverse_refs(self, logic, logic_player, key):
        if isinstance(logic, list):
            for lgc in logic:
                self.record_single_reverse_refs(key, lgc, logic_player)
        else:
            self.record_single_reverse_refs(key, logic, logic_player)

    def record_single_reverse_refs(self, key, lgc, logic_player):
        for item, cnt in lgc.items():
            if (item, logic_player) not in self.reverse_lookup:
                self.reverse_lookup[(item, logic_player)] = set()
            refs = self.reverse_lookup[(item, logic_player)]
            refs.add(key)

    def check_validity(self, complete_logic, item_logic):
        valid_logic = []
        for potential_logic in complete_logic:
            if item_logic.name not in potential_logic:
                valid_logic.append(potential_logic)
            else:
                needed = potential_logic[item_logic.name]
                total = self.logic_lookup[(item_logic.name, item_logic.player)].total_in_pool
                if total - needed > 0:
                    valid_logic.append(potential_logic)
        return valid_logic

    def traverse_world(self, queue, rrp, bc, player):
        p_flag = self.world.progressive[player]
        # run BFS on all connections, and keep track of those blocked by missing items
        while not queue.empty():

            visitor = queue.get()
            connection, crystal_state = connection_key = visitor.conn, visitor.cs
            logic, path = visitor.logic, visitor.path
            new_region = connection.connected_region
            if not self.should_visit(new_region, rrp, visitor):
                bc.pop(connection_key, None)
            # check for reachability?
            # elif self.should_defer(logic):
            #     requirements = connection.access_rule.get_requirements(p_flag)
            #     queue.append((connection, (crystal_state, requirements, path)))
            else:
                if new_region.type == RegionType.Dungeon:
                    new_crystal_state = crystal_state
                    for conn in new_region.exits:
                        door = conn.door
                        if door is not None and door.crystal == CrystalBarrier.Either:
                            new_crystal_state = CrystalBarrier.Either
                            break
                    self.assign_rrp(rrp, new_region, new_crystal_state, logic, path)
                    combined_logic = rrp[(new_region, new_crystal_state)][0]
                    bc.pop(connection_key, None)
                    for conn in new_region.exits:
                        new_logic = merge_requirements(combined_logic, conn.access_rule.get_requirements(p_flag))
                        new_path = list(path) + [conn]
                        door = conn.door
                        if door is not None and not door.blocked:
                            if not door.crystal or new_crystal_state == CrystalBarrier.Either or new_crystal_state == door.crystal:
                                door_crystal_state = door.crystal if door.crystal else new_crystal_state
                                packet = (new_logic, new_path)
                                bc_key = (conn, door_crystal_state)
                                bc[bc_key] = packet
                                queue.put(Visitor(conn, door_crystal_state, new_logic, new_path))
                        elif door is None:
                            # note: no door in dungeon indicates what exactly? (always traversable)?
                            bc_key = (conn, new_crystal_state)
                            packet = (new_logic, new_path)
                            bc[bc_key] = packet
                            queue.put(Visitor(conn, new_crystal_state, new_logic, new_path))
                else:
                    self.assign_rrp(rrp, new_region, CrystalBarrier.Orange, logic, path)
                    combined_logic = rrp[(new_region, CrystalBarrier.Orange)][0]
                    bc.pop(connection_key, None)
                    for conn in new_region.exits:
                        new_logic = merge_requirements(combined_logic, conn.access_rule.get_requirements(p_flag))
                        new_path = list(path) + [conn]
                        packet = (new_logic, new_path)
                        bc_key = (conn, CrystalBarrier.Orange)
                        bc[bc_key] = packet
                        queue.put(Visitor(conn, CrystalBarrier.Orange, new_logic, new_path))

                # Retry connections if the new region can unblock them
                # if new_region.name in indirect_connections:
                #     new_entrance = self.world.get_entrance(indirect_connections[new_region.name], player)
                #     bc_key = (new_entrance, CrystalBarrier.Orange)
                #     rrp_key = (new_entrance.parent_region, CrystalBarrier.Orange)
                #     if bc_key in bc and bc_key not in queue and rrp_key in rrp:
                #         for i in range(0, len(rrp[rrp_key][0])):
                #             trace = rrp[rrp_key]
                #             new_logic = merge_requirements(trace[0][i],
                #                                            new_entrance.access_rule.get_requirements(p_flag))
                #             packet = (new_logic, trace[1][i])
                #             queue.append((self.calc_priority(packet), (bc_key, packet)))

    def should_visit(self, new_region, rrp, visitor):
        if not new_region or visitor.impossible:
            return False
        if visitor.crystal_check and visitor.cs != CrystalBarrier.Either:
            any_valid = False
            for req_set in visitor.logic:
                may_pass = True
                for req in req_set.get_values():
                    if req.req_type == ReqType.Reachable and req.crystal != CrystalBarrier.Null:
                        if visitor.conn.parent_region.name == req.item and visitor.cs != req.crystal:
                            may_pass = False
                            break
                if may_pass:
                    any_valid = True
                    break
            if not any_valid:
                return False
        rrp_key = (new_region, visitor.cs)
        if rrp_key not in rrp:
            return True
        record = rrp[rrp_key]
        visited_logic = record[0]
        return self.is_logic_different(visitor.logic, visited_logic)

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
                        if not oldie.different(current):
                            current_state[i] = False
                            break
                    if current_state[i]:
                        return True
                return False
            else:
                for oldie in old_logic:
                    if not oldie.different(current_logic):
                        return False
                return True
        elif isinstance(current_logic, list):
            for current in current_logic:
                if old_logic.different(current):
                    return True
            return False
        else:
            return old_logic.different(current_logic)

    @staticmethod
    def assign_rrp(rrp, new_region, barrier, logic, path):
        key = (new_region, barrier)
        record = rrp[key] if key in rrp else ([], [])
        rrp[key] = WorldAnalyzer.combine_logic(record, logic, path)

    @staticmethod
    def combine_logic(record, logic, path):
        logic_to_delete, logic_to_append = [], []
        for visited_logic in record[0]:
            equal = visited_logic in logic if isinstance(logic, list) else visited_logic == logic
            if not equal and not WorldAnalyzer.is_logic_different(visited_logic, logic):
                logic_to_delete.append(visited_logic)
        if isinstance(logic, list):
            for logic_item in logic:
                if WorldAnalyzer.is_logic_different(logic_item, record[0]):
                    logic_to_append.append(logic_item)
        elif WorldAnalyzer.is_logic_different(logic, record[0]):
            logic_to_append.append(logic)
        for deletion in logic_to_delete:
            idx = record[0].index(deletion)
            record[0].pop(idx)
            record[1].pop(idx)
        for logic_item in logic_to_append:
            record[0].append(logic_item)
            record[1].append(path)
        return record[0], record[1]

    @staticmethod
    def print_rrp(rrp):
        logger = logging.getLogger('')
        logger.debug('RRP Checking')
        for key, packet in rrp.items():
            region, new_crystal_state = key
            logic, path = packet
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

    def print_item_logic(self):
        logger = logging.getLogger('')
        logger.debug('Item Checking')
        for key, item_logic in self.logic_lookup.items():
            logger.debug(f'\n{item_logic.name} (Player {item_logic.player})  Total: {item_logic.total_in_pool}')
            for i, logic_option in enumerate(item_logic.logic_options):
                multi = '' if item_logic.player == item_logic.locations[i].player else f' (Player {item_logic.locations[i].player})'
                logger.debug(f'Instance {i+1} @ {item_logic.locations[i].name}' + multi)
                if isinstance(logic_option, list):
                    for j in range(0, len(logic_option)):
                        logger.debug(f'{logic_option[j]}')
                else:
                    logger.debug(f'{logic_option}')

    def clean_up_complete(self, key, player):
        item_logic = self.logic_lookup[key]
        clean_options = []
        for logic in item_logic.logic_options:
            if not isinstance(logic, list):
                logic = [logic]
            clean_logic = []
            for lgc in logic:
                new_lgc = Counter(lgc)
                for item, cnt in lgc.items():
                    if (item, player) in self.logic_lookup:
                        other_logic = self.logic_lookup[(item, player)]
                        if other_logic.complete():
                            combined, subsets = [], other_logic.get_option_subset(cnt)
                            for subset in subsets:
                                merged = merge_requirements(new_lgc, subset)
                                (combined.extend if isinstance(merged, list) else combined.append)(merged)
                            new_lgc = combined
                (clean_logic.extend if isinstance(new_lgc, list) else clean_logic.append)(new_lgc)
            clean_logic = reduce_requirements(clean_logic)
            if not isinstance(clean_logic, list):
                clean_logic = [clean_logic]
            valid_logic = self.check_validity(clean_logic, item_logic)
            clean_options.append(valid_logic if len(valid_logic) > 1 else valid_logic[0])
        item_logic.logic_options = clean_options


class Visitor(object):
    def __init__(self, conn, cs, logic, path):
        self.conn = conn
        self.cs = cs
        self.logic = logic
        self.path = path
        self.crystal_check = False
        self.impossible = False
        self.priority = self.calc_priority()

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    def calc_priority(self):
        value = 0
        bump_value = False
        for req_set in self.logic:
            for req in req_set.get_values():
                if req.req_type == ReqType.Reachable:
                    bump_value = True
                    if req.crystal != CrystalBarrier.Null:
                        self.crystal_check = True
                if req.item == 'Impossible':
                    self.impossible = True
        if bump_value:
            value += 1000
        value += max([len(x.get_values()) for x in self.logic])
        return value

    def __str__(self):
        return self.conn.name


class ItemLogic(object):

    def __init__(self, name, player, total_in_pool):
        self.name = name
        self.player = player
        self.total_in_pool = total_in_pool
        # each entry is a list or Counter
        self.logic_options = []  # same length as total
        self.locations = []

    def complete(self):
        return len(self.logic_options) == self.total_in_pool

    def get_option_subset(self, cnt, exclude=None):
        options = self.logic_options
        if exclude:
            options = [n for i, n in enumerate(options) if i != exclude]
        combos = combinations(options, cnt)
        ret = []
        for combo in combos:
            val = None
            for logic_item in combo:
                if not val:
                    val = logic_item
                else:
                    val = merge_requirements(val, logic_item)
            ret.append(val)
        return ret

    def get_locking_items(self):
        locks = Counter()
        for logic_option in self.logic_options:
            if isinstance(logic_option, list):
                for lgc in logic_option:
                    locks &= lgc
            else:
                locks &= logic_option
        return locks

    def copy(self):
        ret = ItemLogic(self.name, self.player, self.total_in_pool)
        ret.logic_options.extend(self.logic_options)
        ret.locations.extend(self.locations)
        return ret

    def __eq__(self, other):
        return other and self.name == other.name and self.player == other.player

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.name, self.player))


# todo: use this to preserve the path, possibly
class LogicOption(object):

    def __init__(self):
        self.logic = Counter()
        self.path = []
