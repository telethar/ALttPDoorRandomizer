import copy
import logging
from collections import Counter, deque

from BaseClasses import CrystalBarrier, RegionType, flooded_keys, merge_requirements
from EntranceShuffle import indirect_connections

class CollectionState(object):

    def __init__(self, parent):
        self.prog_items = Counter()
        self.world = parent
        self.reachable_regions = {player: dict() for player in range(1, parent.players + 1)}
        self.blocked_connections = {player: dict() for player in range(1, parent.players + 1)}
        self.events = []
        self.path = {}
        self.locations_checked = set()
        self.stale = {player: True for player in range(1, parent.players + 1)}
        for item in parent.precollected_items:
            self.collect(item, True)
        self.door_counter = {player: Counter() for player in range(1, parent.players + 1)}
        self.reached_doors = {player: set() for player in range(1, parent.players + 1)}
        self.opened_doors = {player: set() for player in range(1, parent.players + 1)}
        self.dungeons_to_check = {player: dict() for player in range(1, parent.players + 1)}

    def update_reachable_regions(self, player):
        self.stale[player] = False
        rrp = self.reachable_regions[player]
        bc = self.blocked_connections[player]

        # init on first call - this can't be done on construction since the regions don't exist yet
        start = self.world.get_region('Menu', player)
        if not start in rrp:
            rrp[start] = (CrystalBarrier.Orange, [Counter()], [[]])
            for conn in start.exits:
                bc[conn] = (CrystalBarrier.Orange, Counter(), [])

        queue = deque(self.blocked_connections[player].items())

        ctr = 0
        # run BFS on all connections, and keep track of those blocked by missing items
        while len(queue) > 0:
            ctr += 1
            # if ctr % 1000 == 0:

            connection, record = queue.popleft()
            crystal_state, logic, path = record
            new_region = connection.connected_region
            if not self.should_visit(new_region, rrp, crystal_state, logic):
                bc.pop(connection, None)
            elif connection.can_reach(self):
                # location logic can go here
                # complete_logic = logic if new_region not in rrp else merge_requirements(rrp[new_region][1], logic)
                if new_region.type == RegionType.Dungeon:
                    new_crystal_state = crystal_state
                    for conn in new_region.exits:
                        door = conn.door
                        if door is not None and door.crystal == CrystalBarrier.Either and door.entrance.can_reach(self):
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

                self.path[new_region] = (new_region.name, self.path.get(connection, None))

                # Retry connections if the new region can unblock them
                if new_region.name in indirect_connections:
                    new_entrance = self.world.get_entrance(indirect_connections[new_region.name], player)
                    if new_entrance in bc and new_entrance not in queue and new_entrance.parent_region in rrp:
                        for i in range(0, len(rrp[new_entrance.parent_region][1])):
                            trace = rrp[new_entrance.parent_region]
                            new_logic = merge_requirements(trace[1][i], new_entrance.access_rule.get_requirements(self))
                            packet = (trace[0], new_logic, trace[2][i])
                            queue.append((new_entrance, packet))
            # if CollectionState.is_small_door(connection):
            #     door = connection.door
            #     if door.name not in self.reached_doors[player]:
            #         dungeon_name = connection.parent_region.dungeon.name
            #         self.door_counter[player][dungeon_name] += 1
            #         self.reached_doors[player].add(door.name)
            #         if dungeon_name not in self.dungeons_to_check[player].keys():
            #             self.dungeons_to_check[player][dungeon_name] = []
            #         checklist = self.dungeons_to_check[player][dungeon_name]
            #         checklist.append((door.name, door, connection, crystal_state))
            #         if door.dest and door.dest.smallKey:
            #             self.reached_doors[player].add(door.dest.name)

        # new_doors = False
        # for dungeon_name, checklist in self.dungeons_to_check[player].items():
        #     small_key_name = dungeon_keys[dungeon_name]
        #     key_total = self.prog_items[(small_key_name, player)]
        #     door_total = self.door_counter[player][dungeon_name]
        #     if key_total >= door_total:
        #         opened_doors = self.opened_doors[player]
        #         for door_name, door, connection, crystal_state in checklist:
        #             if door_name not in opened_doors:
        #                 new_doors = True
        #                 opened_doors.add(door_name)
        #                 if door.dest and door.dest.smallKey:
        #                     self.opened_doors[player].add(door.dest.name)
        #                 queue.append((connection, crystal_state))
        # if not new_doors:
        # logging.getLogger('').debug(error)
            else:
                pass
                # should we come back to it?
        self.print_rrp(rrp)

    def should_visit(self, new_region, rrp, crystal_state, logic):
        if not new_region:
            return False
        if new_region not in rrp:
            return True
        record = rrp[new_region]
        visited_logic = record[1]
        logic_is_different = True
        for old_logic in visited_logic:
            logic_is_different &= self.is_logic_different(logic, old_logic)
            if not logic_is_different:
                break
        if new_region.type != RegionType.Dungeon and logic_is_different:
            return True
        return (record[0] & crystal_state) != record[0] or logic_is_different

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
        logic_to_delete = []
        for visited_logic in record[1]:
            if not CollectionState.is_logic_different(visited_logic, logic):
                logic_to_delete.append(visited_logic)
        for deletion in logic_to_delete:
            idx = record[1].index(deletion)
            record[1].pop(idx)
            record[2].pop(idx)
        record[1].append(logic)
        record[2].append(path)
        record = (barrier, record[1], record[2])
        rrp[new_region] = record

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


    def copy(self):
        ret = CollectionState(self.world)
        ret.prog_items = self.prog_items.copy()
        ret.reachable_regions = {player: copy.copy(self.reachable_regions[player]) for player in range(1, self.world.players + 1)}
        ret.blocked_connections = {player: copy.copy(self.blocked_connections[player]) for player in range(1, self.world.players + 1)}
        ret.events = copy.copy(self.events)
        ret.path = copy.copy(self.path)
        ret.locations_checked = copy.copy(self.locations_checked)
        return ret

    def can_reach(self, spot, resolution_hint=None, player=None):
        try:
            spot_type = spot.spot_type
        except AttributeError:
            # try to resolve a name
            if resolution_hint == 'Location':
                spot = self.world.get_location(spot, player)
            elif resolution_hint == 'Entrance':
                spot = self.world.get_entrance(spot, player)
            else:
                # default to Region
                spot = self.world.get_region(spot, player)

        return spot.can_reach(self)

    def sweep_for_events(self, key_only=False, locations=None):
        # this may need improvement
        if locations is None:
            locations = self.world.get_filled_locations()
        new_locations = True
        checked_locations = 0
        while new_locations:
            reachable_events = [location for location in locations if location.event and
                                (not key_only or (not self.world.keyshuffle[location.item.player] and location.item.smallkey) or (not self.world.bigkeyshuffle[location.item.player] and location.item.bigkey))
                                and location.can_reach(self)]
            reachable_events = self._do_not_flood_the_keys(reachable_events)
            for event in reachable_events:
                if (event.name, event.player) not in self.events:
                    self.events.append((event.name, event.player))
                    self.collect(event.item, True, event)
            new_locations = len(reachable_events) > checked_locations
            checked_locations = len(reachable_events)

    def can_reach_blue(self, region, player):
        return region in self.reachable_regions[player] and self.reachable_regions[player][region] in [CrystalBarrier.Blue, CrystalBarrier.Either]

    def can_reach_orange(self, region, player):
        return region in self.reachable_regions[player] and self.reachable_regions[player][region] in [CrystalBarrier.Orange, CrystalBarrier.Either]

    def _do_not_flood_the_keys(self, reachable_events):
        adjusted_checks = list(reachable_events)
        for event in reachable_events:
            if event.name in flooded_keys.keys():
                flood_location = self.world.get_location(flooded_keys[event.name], event.player)
                if flood_location.item and flood_location not in self.locations_checked:
                    adjusted_checks.remove(event)
        if len(adjusted_checks) < len(reachable_events):
            return adjusted_checks
        return reachable_events

    def not_flooding_a_key(self, world, location):
        if location.name in flooded_keys.keys():
            flood_location = world.get_location(flooded_keys[location.name], location.player)
            item = flood_location.item
            item_is_important = False if not item else item.advancement or item.bigkey or item.smallkey
            return flood_location in self.locations_checked or not item_is_important
        return True

    @staticmethod
    def is_small_door(connection):
        return connection and connection.door and connection.door.smallKey

    def is_door_open(self, door_name, player):
        return door_name in self.opened_doors[player]

    def has(self, item, player, count=1):
        if count == 1:
            return (item, player) in self.prog_items
        return self.prog_items[item, player] >= count

    def has_sm_key(self, item, player, count=1):
        if self.world.retro[player]:
            if self.world.mode[player] == 'standard' and self.world.doorShuffle[player] == 'vanilla' and item == 'Small Key (Escape)':
                return True  # Cannot access the shop until escape is finished.  This is safe because the key is manually placed in make_custom_item_pool
            return self.can_buy_unlimited('Small Key (Universal)', player)
        if count == 1:
            return (item, player) in self.prog_items
        return self.prog_items[item, player] >= count

    def can_buy_unlimited(self, item, player):
        for shop in self.world.shops:
            if shop.region.player == player and shop.has_unlimited(item) and shop.region.can_reach(self):
                return True
        return False

    def item_count(self, item, player):
        return self.prog_items[item, player]

    def has_crystals(self, count, player):
        crystals = ['Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 5', 'Crystal 6', 'Crystal 7']
        return len([crystal for crystal in crystals if self.has(crystal, player)]) >= count

    def has_bottle(self, player):
        return self.bottle_count(player) > 0

    def bottle_count(self, player):
        return len([item for (item, itemplayer) in self.prog_items if item.startswith('Bottle') and itemplayer == player])

    def has_hearts(self, player, count):
        # Warning: This only considers items that are marked as advancement items
        return self.heart_count(player) >= count

    def heart_count(self, player):
        # Warning: This only considers items that are marked as advancement items
        diff = self.world.difficulty_requirements[player]
        return (
             min(self.item_count('Boss Heart Container', player), diff.boss_heart_container_limit)
             + self.item_count('Sanctuary Heart Container', player)
             + min(self.item_count('Piece of Heart', player), diff.heart_piece_limit) // 4
             + 3 # starting hearts
        )

    def can_extend_magic(self, player, smallmagic=16, fullrefill=False):  # This reflects the total magic Link has, not the total extra he has.
        basemagic = 8
        if self.has('Magic Upgrade (1/4)', player):
            basemagic = 32
        elif self.has('Magic Upgrade (1/2)', player):
            basemagic = 16
        if self.can_buy_unlimited('Green Potion', player) or self.can_buy_unlimited('Blue Potion', player):
            if self.world.difficulty_adjustments[player] == 'hard' and not fullrefill:
                basemagic = basemagic + int(basemagic * 0.5 * self.bottle_count(player))
            elif self.world.difficulty_adjustments[player] == 'expert' and not fullrefill:
                basemagic = basemagic + int(basemagic * 0.25 * self.bottle_count(player))
            else:
                basemagic = basemagic + basemagic * self.bottle_count(player)
        return basemagic >= smallmagic

    def can_kill_most_things(self, player, enemies=5):
        return (self.has_blunt_weapon(player)
                or self.has('Cane of Somaria', player)
                or (self.has('Cane of Byrna', player) and (enemies < 6 or self.can_extend_magic(player)))
                or self.can_shoot_arrows(player)
                or self.has('Fire Rod', player)
                )

    def can_shoot_arrows(self, player):
        if self.world.retro[player]:
            #todo: Non-progressive silvers grant wooden arrows, but progressive bows do not.  Always require shop arrows to be safe
            return self.has('Bow', player) and self.can_buy_unlimited('Single Arrow', player)
        return self.has('Bow', player)

    def can_get_good_bee(self, player):
        cave = self.world.get_region('Good Bee Cave', player)
        return (
             self.has_bottle(player) and
             self.has('Bug Catching Net', player) and
             (self.has_Boots(player) or (self.has_sword(player) and self.has('Quake', player))) and
             cave.can_reach(self) and
             self.is_not_bunny(cave, player)
        )

    def has_blunt_weapon(self, player):
        return self.has_sword(player) or self.has('Hammer', player)

    def can_flute(self, player):
        lw = self.world.get_region('Light World', player)
        return self.has('Ocarina', player) and lw.can_reach(self) and self.is_not_bunny(lw, player)

    def can_melt_things(self, player):
        return self.has('Fire Rod', player) or (self.has('Bombos', player) and self.has_sword(player))

    def can_avoid_lasers(self, player):
        return self.has('Mirror Shield', player) or self.has('Cane of Byrna', player) or self.has('Cape', player)

    def is_not_bunny(self, region, player):
        if self.has_Pearl(player):
            return True

        return region.is_light_world if self.world.mode[player] != 'inverted' else region.is_dark_world

    def can_reach_light_world(self, player):
        if True in [i.is_light_world for i in self.reachable_regions[player]]:
            return True
        return False

    def can_reach_dark_world(self, player):
        if True in [i.is_dark_world for i in self.reachable_regions[player]]:
            return True
        return False

    def collect(self, item, event=False, location=None):
        if location:
            self.locations_checked.add(location)
        changed = False
        if item.name.startswith('Progressive '):
            if 'Sword' in item.name:
                if self.has('Golden Sword', item.player):
                    pass
                elif self.has('Tempered Sword', item.player) and self.world.difficulty_requirements[item.player].progressive_sword_limit >= 4:
                    self.prog_items['Golden Sword', item.player] += 1
                    changed = True
                elif self.has('Master Sword', item.player) and self.world.difficulty_requirements[item.player].progressive_sword_limit >= 3:
                    self.prog_items['Tempered Sword', item.player] += 1
                    changed = True
                elif self.has('Fighter Sword', item.player) and self.world.difficulty_requirements[item.player].progressive_sword_limit >= 2:
                    self.prog_items['Master Sword', item.player] += 1
                    changed = True
                elif self.world.difficulty_requirements[item.player].progressive_sword_limit >= 1:
                    self.prog_items['Fighter Sword', item.player] += 1
                    changed = True
            elif 'Glove' in item.name:
                if self.has('Titans Mitts', item.player):
                    pass
                elif self.has('Power Glove', item.player):
                    self.prog_items['Titans Mitts', item.player] += 1
                    changed = True
                else:
                    self.prog_items['Power Glove', item.player] += 1
                    changed = True
            elif 'Shield' in item.name:
                if self.has('Mirror Shield', item.player):
                    pass
                elif self.has('Red Shield', item.player) and self.world.difficulty_requirements[item.player].progressive_shield_limit >= 3:
                    self.prog_items['Mirror Shield', item.player] += 1
                    changed = True
                elif self.has('Blue Shield', item.player)  and self.world.difficulty_requirements[item.player].progressive_shield_limit >= 2:
                    self.prog_items['Red Shield', item.player] += 1
                    changed = True
                elif self.world.difficulty_requirements[item.player].progressive_shield_limit >= 1:
                    self.prog_items['Blue Shield', item.player] += 1
                    changed = True
            elif 'Bow' in item.name:
                if self.has('Silver Arrows', item.player):
                    pass
                elif self.has('Bow', item.player):
                    self.prog_items['Silver Arrows', item.player] += 1
                    changed = True
                else:
                    self.prog_items['Bow', item.player] += 1
                    changed = True
            elif 'Armor' in item.name:
                if self.has('Red Mail', item.player):
                    pass
                elif self.has('Blue Mail', item.player):
                    self.prog_items['Red Mail', item.player] += 1
                    changed = True
                else:
                    self.prog_items['Blue Mail', item.player] += 1
                    changed = True

        elif item.name.startswith('Bottle'):
            if self.bottle_count(item.player) < self.world.difficulty_requirements[item.player].progressive_bottle_limit:
                self.prog_items[item.name, item.player] += 1
                changed = True
        elif event or item.advancement:
            self.prog_items[item.name, item.player] += 1
            changed = True

        self.stale[item.player] = True

        if changed:
            if not event:
                self.sweep_for_events()

    def remove(self, item):
        if item.advancement:
            to_remove = item.name
            if to_remove.startswith('Progressive '):
                if 'Sword' in to_remove:
                    if self.has('Golden Sword', item.player):
                        to_remove = 'Golden Sword'
                    elif self.has('Tempered Sword', item.player):
                        to_remove = 'Tempered Sword'
                    elif self.has('Master Sword', item.player):
                        to_remove = 'Master Sword'
                    elif self.has('Fighter Sword', item.player):
                        to_remove = 'Fighter Sword'
                    else:
                        to_remove = None
                elif 'Glove' in item.name:
                    if self.has('Titans Mitts', item.player):
                        to_remove = 'Titans Mitts'
                    elif self.has('Power Glove', item.player):
                        to_remove = 'Power Glove'
                    else:
                        to_remove = None
                elif 'Shield' in item.name:
                    if self.has('Mirror Shield', item.player):
                        to_remove = 'Mirror Shield'
                    elif self.has('Red Shield', item.player):
                        to_remove = 'Red Shield'
                    elif self.has('Blue Shield', item.player):
                        to_remove = 'Blue Shield'
                    else:
                        to_remove = 'None'
                elif 'Bow' in item.name:
                    if self.has('Silver Arrows', item.player):
                        to_remove = 'Silver Arrows'
                    elif self.has('Bow', item.player):
                        to_remove = 'Bow'
                    else:
                        to_remove = None

            if to_remove is not None:

                self.prog_items[to_remove, item.player] -= 1
                if self.prog_items[to_remove, item.player] < 1:
                    del (self.prog_items[to_remove, item.player])
                # invalidate caches, nothing can be trusted anymore now
                self.reachable_regions[item.player] = dict()
                self.blocked_connections[item.player] = dict()
                self.stale[item.player] = True

    def __getattr__(self, item):
        if item.startswith('can_reach_'):
            return self.can_reach(item[10])
        #elif item.startswith('has_'):
        #    return self.has(item[4])
        if item == '__len__':
            return

        raise RuntimeError('Cannot parse %s.' % item)