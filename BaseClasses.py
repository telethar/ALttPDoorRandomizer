import copy


class World(object):

    def __init__(self):
        self.regions = []
        self.itempool = []
        self.state = CollectionState(self)
        self.required_medallions = ['Ether', 'Quake']
        self._cached_locations = None
        self._entrance_cache = {}
        self._region_cache = {}
        self._entrance_cache = {}
        self._location_cache = {}
        self._item_cache = {}

    def get_region(self, regionname):
        if isinstance(regionname, Region):
            return regionname
        try:
            return self._region_cache[regionname]
        except KeyError:
            for region in self.regions:
                if region.name == regionname:
                    self._region_cache[regionname] = region
                    return region
            raise RuntimeError('No such region %s' % regionname)

    def get_entrance(self, entrance):
        if isinstance(entrance, Entrance):
            return entrance
        try:
            return self._entrance_cache[entrance]
        except KeyError:
            for region in self.regions:
                for exit in region.exits:
                    if exit.name == entrance:
                        self._entrance_cache[entrance] = exit
                        return exit
            raise RuntimeError('No such entrance %s' % entrance)

    def get_location(self, location):
        if isinstance(location, Location):
            return location
        try:
            return self._location_cache[location]
        except KeyError:
            for region in self.regions:
                for r_location in region.locations:
                    if r_location.name == location:
                        self._location_cache[location] = r_location
                        return r_location
        raise RuntimeError('No such entrance %s' % location)

    def find_items(self, item):
        return [location for location in self.get_locations() if location.item is not None and location.item.name == item]

    def push_item(self, location, item, collect=True):
        if not isinstance(location, Location):
            location = self.get_location(location)

        if location.item_rule(item):
            location.item = item
            item.location = location
            if collect:
                self.state.collect(item)

            print('Placed %s at %s' % (item, location))
        else:
            raise RuntimeError('Cannot assign item %s to location %s.' % (item, location))

    def get_locations(self):
        if self._cached_locations is None:
            self._cached_locations = []
            for region in self.regions:
                self._cached_locations.extend(region.locations)
        return self._cached_locations

    def get_unfilled_locations(self):
        return [location for location in self.get_locations() if location.item is None]

    def get_reachable_locations(self, state=None):
        if state is None:
            state = self.state
        return [location for location in self.get_locations() if state.can_reach(location)]

    def get_placeable_locations(self, state=None):
        if state is None:
            state = self.state
        return [location for location in self.get_locations() if location.item is None and state.can_reach(location)]

    def unlocks_new_location(self, item):
        temp_state = self.state.copy()
        temp_state._clear_cache()
        temp_state.collect(item)
        return len(self.get_placeable_locations()) < len(self.get_placeable_locations(temp_state))


class CollectionState(object):

    def __init__(self, parent, has_everything=False):
        self.prog_items = set()
        self.world = parent
        self.has_everything = has_everything
        self.changed = False
        self.region_cache = {}
        self.location_cache = {}
        self.entrance_cache = {}
        # use to avoid cycle dependencies during resolution
        self.recursion_cache = []

    def _clear_cache(self):
        # we only need to invalidate results which were False, places we could reach before we can still reach after adding more items
        self.region_cache = {k: v for k, v in self.region_cache.items() if v}
        self.location_cache = {k: v for k, v in self.location_cache.items() if v}
        self.entrance_cache = {k: v for k, v in self.entrance_cache.items() if v}
        self.recursion_cache = []
        self.changed = False

    def copy(self):
        ret = CollectionState(self.world, self.has_everything)
        ret.prog_items = copy.copy(self.prog_items)
        ret.changed = self.changed
        ret.region_cache = copy.copy(self.region_cache)
        ret.location_cache = copy.copy(self.location_cache)
        ret.entrance_cache = copy.copy(self.entrance_cache)
        ret.recursion_cache = copy.copy(self.recursion_cache)
        return ret

    def can_reach(self, spot, resolution_hint=None):
        if self.changed:
            self._clear_cache()

        if spot in self.recursion_cache:
            return False

        if isinstance(spot, Region):
            correct_cache = self.region_cache
        elif isinstance(spot, Location):
            correct_cache = self.location_cache
        elif isinstance(spot, Entrance):
            correct_cache = self.entrance_cache
        else:
            # try to resolve a name
            if resolution_hint == 'Location':
                spot = self.world.get_location(spot)
                correct_cache = self.location_cache
            elif resolution_hint == 'Entrance':
                spot = self.world.get_entrance(spot)
                correct_cache = self.entrance_cache
            else:
                # default to Region
                spot = self.world.get_region(spot)
                correct_cache = self.region_cache

        if spot not in correct_cache:
            # for the purpose of evaluating results, recursion is resolved by always denying recursive access (as that ia what we are trying to figure out right now in the first place
            self.recursion_cache.append(spot)
            can_reach = spot.can_reach(self)
            self.recursion_cache.pop()

            # we only store qualified false results (i.e. ones not inside a hypothetical)
            if not can_reach:
                if not self.recursion_cache:
                    correct_cache[spot] = can_reach
            else:
                correct_cache[spot] = can_reach
            return can_reach
        return correct_cache[spot]

    def can_collect(self, item, count=None):
        if isinstance(item, Item):
            item = item.name
        if count is None:
            cached = self.world._item_cache.get(item, None)
            if cached is None:
                candidates = self.world.find_items(item)
                if not candidates:
                    return False
                elif len(candidates) == 1:
                    cached = candidates[0]
                    self.world._item_cache[item] = cached
                else:
                    # this should probably not happen, wonky item distribution?
                    len([location for location in candidates if self.can_reach(location)]) >= 1
            return self.can_reach(cached)

        return len([location for location in self.world.find_items(item) if self.can_reach(location)]) >= count

    def has(self, item):
        if self.has_everything:
            return True
        else:
            return item in self.prog_items

    def can_lift_rocks(self):
        return self.has('Power Glove') or self.has('Titans Mitts')

    def can_lift_heavy_rocks(self):
        return self.has('Titans Mitts')

    def has_sword(self):
        return self.has('Fighter Sword') or self.has('Master Sword') or self.has('Tempered Sword') or self.has('Golden Sword')

    def has_beam_sword(self):
        return self.has('Master Sword') or self.has('Tempered Sword') or self.has('Golden Sword')

    def has_blunt_weapon(self):
        return self.has_sword() or self.has('Hammer')

    def has_Mirror(self):
        return self.has('Magic Mirror')

    def has_Boots(self):
        return self.has('Pegasus Boots')

    def has_Pearl(self):
        return self.has('Moon Pearl')

    def has_fire_source(self):
        return self.has('Fire Rod') or self.has('Lamp')

    def has_misery_mire_medallion(self):
        return self.has(self.world.required_medallions[0])

    def has_turtle_rock_medallion(self):
        return self.has(self.world.required_medallions[1])

    def collect(self, item):
        if item.name.startswith('Progressive '):
            if 'Sword' in item.name:
                if self.has('Golden Sword'):
                    return
                elif self.has('Tempered Sword'):
                    self.prog_items.add('Golden Sword')
                    self.changed = True
                elif self.has('Master Sword'):
                    self.prog_items.add('Tempered Sword')
                    self.changed = True
                elif self.has('Fighter Sword'):
                    self.prog_items.add('Master Sword')
                    self.changed = True
                else:
                    self.prog_items.add('Fighter Sword')
                    self.changed = True
            elif 'Glove' in item.name:
                if self.has('Titans Mitts'):
                    return
                elif self.has('Power Glove'):
                    self.prog_items.add('Titans Mitts')
                    self.changed = True
                else:
                    self.prog_items.add('Power Glove')
                    self.changed = True
            return

        if item.advancement:
            self.prog_items.add(item.name)
            self.changed = True

    def __getattr__(self, item):
        if item.startswith('can_reach_'):
            return self.can_reach(item[10])
        elif item.startswith('has_'):
            return self.has(item[4])

        raise RuntimeError('Cannot parse %s.' % item)


class Region(object):

    def __init__(self, name):
        self.name = name
        self.entrances = []
        self.exits = []
        self.locations = []

    def can_reach(self, state):
        for entrance in self.entrances:
            if state.can_reach(entrance):
                return True
        return False

    def add_locations(self, *locations):
        for location in locations:
            self.locations.append(Location(location, self))

    def add_exits(self, *exits):
        for exit in exits:
            self.exits.append(Entrance(exit, self))

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name


class Entrance(object):

    def __init__(self, name='', parent=None):
        self.name = name
        self.parent_region = parent
        self.connected_region = None

    def access_rule(self, state):
        return True

    def can_reach(self, state):
        if self.parent_region:
            if not state.can_reach(self.parent_region):
                return False

        return self.access_rule(state)

    def connect(self, region):
        self.connected_region = region
        region.entrances.append(self)

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name


class Location(object):

    def __init__(self, name='', parent=None, access=None, item_rule=None):
        self.name = name
        self.parent_region = parent
        self.item = None
        if access is not None:
            self.access_rule = access
        if item_rule is not None:
            self.item_rule = item_rule

    def access_rule(self, state):
        return True

    def item_rule(self, item):
        if item.name != 'Triforce':
            return True
        else:
            return False

    def can_reach(self, state):
        if self.parent_region:
            if not state.can_reach(self.parent_region):
                return False

        return self.access_rule(state)

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name


class Item(object):

    def __init__(self, name='', advancement=False, key=False):
        self.name = name
        self.advancement = advancement
        self.key = key
        self.location = None

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name
