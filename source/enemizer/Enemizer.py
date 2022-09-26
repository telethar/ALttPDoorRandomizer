import RaceRandom as random

from source.dungeon.EnemyList import SpriteType
from source.enemizer.SpriteSheets import uw_sub_group_choices, setup_required_dungeon_groups

water_rooms = {
    0x16, 0x28, 0x34, 0x36, 0x38, 0x46, 0x66
}  # these room need to be locked on the gfx ID : 17

# todo: task list
# anti-fairy shutter logic
# check cucco, implement flag for certain immune enemies that are okay in shutter rooms
# Room 0x16 (sprites 4,5,6 need to be water but 0-3 don't)
#

shutter_sprites = {
    0xb8: {0, 1, 2, 3, 4, 5}, 0xb: {4, 5, 6, 7, 8, 9}, 0x1b: {3, 4, 5}, 0x4b: {0, 3, 4}, 0x4: {9, 13, 14},
    0x24: {3, 5, 6}, # not sure about 6 - bunny beam under pot
    0x28: {0, 1, 2, 3, 4}, 0xe: {0, 1, 2, 3}, 0x2e: {0, 1, 2, 3, 4, 5}, 0x3e: {1, 2}, 0x6e: {0, 1, 2, 3, 4},
    0x31: {7, 8, 10}, 0x44: {2, 3, 5}, 0x45: {1, 2, 3},  0x53: {5, 6, 8, 9, 10}, 0x75: {0, 2, 3, 4, 5},
    0x85: {2, 3, 4, 5}, 0x5d: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}, 0x6b: {5, 6, 7, 8, 9, 10, 11, 12, 13},
    0x6d: {0, 1, 2, 3, 4, 5, 6, 7, 8}, 0x7b: {3, 4, 8}, 0x7d: {4, 5, 6, 7, 8}, 0x8d: {0, 1, 2, 3, 4},
    0xa5: {0, 1, 2, 3, 4, 5, 6, 7}, 0x71: {0, 1}, 0xd8: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
    0xb0: {0, 1, 2, 3, 4, 5, 7, 8, 9, 10}, 0xc0: {0, 1, 2}, 0xe0: {0, 1, 2, 3}, 0xb2: {5, 6, 7, 10, 11},
    0xd2: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}, 0xef: {0, 1, 2}, 0x10c: {4, 5, 6, 7}, 0x123: {0, 1, 2, 3}
}

water_sprites = {
    0x16: {4, 5, 6}, 0x28: {0, 1, 2, 3}, 0x34: {0, 1, 2}, 0x36: {1, 2, 5, 7, 8}, 0x38: {0, 1, 2, 4, 5, 6},
}

# not really shutters: only tiles:
# 0xb6 TR Tile, TR Pokey 1, Chain chomp?
# 0x87 hera tile room?
# 0x3d gt minihelma?
# 0x8d gt tile room?
# 0x96 gt torch cross?


def setup_specific_requirements(data_tables):
    requirements = data_tables.sprite_requirements
    water_groups = set()
    water_sub_groups = {0: set(), 1: set(), 2: set(), 3: set()}
    killable_groups = set()
    killable_sub_groups = {0: set(), 1: set(), 2: set(), 3: set()}
    key_groups = set()
    key_sub_groups = {0: set(), 1: set(), 2: set(), 3: set()}

    for sid, requirement in requirements.items():
        if isinstance(requirement, dict):
            continue
        if requirement.good_for_uw_water():
            water_groups.update(requirement.groups)
            for i in range(0, 4):
                limited = [x for x in requirement.sub_groups[i] if x in uw_sub_group_choices[i]]
                water_sub_groups[i].update(limited)
        if requirement.good_for_shutter():
            killable_groups.update(requirement.groups)
            for i in range(0, 4):
                killable_sub_groups[i].update(requirement.sub_groups[i])
            if requirement.can_drop:
                key_groups.update(requirement.groups)
                for i in range(0, 4):
                    key_sub_groups[i].update(requirement.sub_groups[i])
    return water_groups, water_sub_groups, killable_groups, killable_sub_groups, key_groups, key_sub_groups


def get_possible_sheets(room_id, data_tables, specific, uw_sheets):
    # forced sprites for room
    requirements = data_tables.sprite_requirements

    water_groups, water_sub_groups, killable_groups, killable_sub_groups, key_groups, key_sub_groups = specific

    # forced_req = set()
    key_needed = False
    killable_needed = room_id in shutter_sprites
    water_needed = room_id in water_rooms

    for sheet in data_tables.sprite_sheets.values():
        if room_id in sheet.room_set:
            return [sheet]

    match_all_room_groups = set()
    match_all_sub_groups = {0: set(), 1: set(), 2: set(), 3: set()}
    # match_all_sub_groups = {0: set(uw_sub_group_choices[0] + [70, 72]), 1: set(uw_sub_group_choices[1] + [13, 73]),
    #                          2: set(uw_sub_group_choices[2] + [19]), 3: set(uw_sub_group_choices[3] + [25, 68])}
    
    for sprite in data_tables.uw_enemy_table.room_map[room_id]:
        sprite_secondary = 0 if sprite.sub_type != SpriteType.Overlord else sprite.sub_type
        key = (sprite.kind, sprite_secondary)
        if key not in requirements:
            continue
        req = requirements[key]
        if isinstance(req, dict):
            req = req[room_id]
        if req.static or not req.can_randomize:
            if req.groups:
                match_all_room_groups.intersection_update(req.groups)
                if not match_all_room_groups:
                    match_all_room_groups = set(req.groups)
            for i in range(0, 4):
                if req.sub_groups[i]:
                    match_all_sub_groups[i].intersection_update(req.sub_groups[i])
                    if not match_all_sub_groups[i]:
                        match_all_sub_groups[i] = set(req.sub_groups[i])
            # forced_req.add(req)
            if sprite.drops_item:
                key_needed = True

    match_any_room_groups = set()
    match_any_sub_groups = {0: set(), 1: set(), 2: set(), 3: set()}
    exclude_all_groups = set()
    exclude_all_sub_groups = {0: set(), 1: set(), 2: set(), 3: set()}

    if water_needed:
        if water_groups:
            match_any_room_groups.update(water_groups)
        for i in range(0, 4):
            if water_sub_groups[i]:
                match_any_sub_groups[i].update(water_sub_groups[i])
    else:  # exclude water stuff
        exclude_all_groups.update(water_groups)
        for i in range(0, 4):
            exclude_all_sub_groups[i].update(water_sub_groups[i])

    if key_needed:
        if key_groups:
            match_any_room_groups.update(key_groups)
            for i in range(0, 4):
                if key_sub_groups[i]:
                    match_any_sub_groups[i].update(key_sub_groups[i])
    elif killable_needed:
        if killable_groups:
            match_any_room_groups.update(killable_groups)
            for i in range(0, 4):
                if killable_sub_groups[i]:
                    match_any_sub_groups[i].update(killable_sub_groups[i])

    possible_sheets = []
    for sheet in uw_sheets:
        str(sheet)
        if match_all_room_groups and sheet not in match_all_room_groups:
            continue
        if any(match_all_sub_groups[i] and sheet.sub_groups[i] not in match_all_sub_groups[i] for i in range(0, 4)):
            continue
        if exclude_all_groups and sheet in exclude_all_groups:
            continue
        if any(exclude_all_sub_groups[i] and sheet.sub_groups[i] in exclude_all_sub_groups[i] for i in range(0, 4)):
            continue
        if match_any_room_groups and sheet not in match_any_sub_groups:
            continue
        test_subs = [i for i in range(0, 4) if match_any_sub_groups[i]]
        if test_subs and all(sheet.sub_groups[i] not in match_any_sub_groups[i] for i in test_subs):
            continue
        possible_sheets.append(sheet)
    return possible_sheets


def uw_candidate_sprites(data_tables):
    requirements = data_tables.sprite_requirements
    uw_sprite_candidates = []
    uw_sheet_candidates = []

    candidate_groups = set()
    candidate_sub_groups = {0: set(), 1: set(), 2: set(), 3: set()}

    for k, r in requirements.items():
        if isinstance(r, dict):
            continue
        if not r.static and r.uw_valid and not r.dont_use:
            candidate_groups.update(r.groups)
            for i in range(0, 4):
                candidate_sub_groups[i].update(r.sub_groups[i])
            uw_sprite_candidates.append(k)

    for num in range(65, 124):
        sheet = data_tables.sprite_sheets[num]
        if candidate_groups and sheet not in candidate_groups:
            continue
        test_subs = [i for i in range(0, 4) if candidate_sub_groups[i]]
        if test_subs and all(sheet.sub_groups[i] not in candidate_sub_groups[i] for i in test_subs):
            continue
        uw_sheet_candidates.append(sheet)

    return uw_sprite_candidates, uw_sheet_candidates


def get_possible_enemy_sprites(room_id, sheet, uw_sprites, data_tables):
    ret = []
    for sprite in uw_sprites:
        requirement = data_tables.sprite_requirements[sprite]
        if isinstance(requirement, dict):
            requirement = requirement[room_id]
        if sheet.valid_sprite(requirement) and requirement.can_spawn_in_room(room_id):
            ret.append(requirement)
    return ret


def get_randomize_able_sprites(room_id, data_tables):
    sprite_table = {}
    for idx, sprite in enumerate(data_tables.uw_enemy_table.room_map[room_id]):
        sprite_secondary = 0 if sprite.sub_type != SpriteType.Overlord else sprite.sub_type
        key = (sprite.kind, sprite_secondary)
        if key not in data_tables.sprite_requirements:
            continue
        req = data_tables.sprite_requirements[key]
        if isinstance(req, dict):
            continue
        if not req.static and req.can_randomize:
            sprite_table[idx] = sprite
    return sprite_table


# RandomizeRooms(optionFlags);
def randomize_underworld_rooms(data_tables):
    # RoomCollection.RandomizeRoomSpriteGroups
    # randomize room sprite sheets

    specific = setup_specific_requirements(data_tables)
    uw_candidates, uw_sheets = uw_candidate_sprites(data_tables)
    for room_id in range(0, 0x128):
        if room_id in {0, 1, 3, 6, 7, 0xd, 0x14, 0x1c, 0x20, 0x29, 0x30, 0x33,
                       0x4d, 0x5a, 0x7F, 0x90, 0xa4, 0xac, 0xc8, 0xde}:
            continue
        if room_id not in data_tables.uw_enemy_table.room_map:
            continue
        # sprite_reqs = data_tables.sprite_requirements
        randomizeable_sprites = get_randomize_able_sprites(room_id, data_tables)
        if randomizeable_sprites:
            candidate_sheets = get_possible_sheets(room_id, data_tables, specific, uw_sheets)
            chosen_sheet = random.choice(candidate_sheets)
            data_tables.room_headers[room_id].sprite_sheet = chosen_sheet.id - 0x40
            candidate_sprites = get_possible_enemy_sprites(room_id, chosen_sheet, uw_candidates, data_tables)
            if room_id in water_rooms:
                water_sprites = [x for x in candidate_sprites if x.water_only]
                for i, sprite in randomizeable_sprites.items():
                    chosen = random.choice(water_sprites)
                    sprite.kind = chosen.sprite
            else:
                # todo: stal sprites
                for i, sprite in randomizeable_sprites.items():
                    if sprite.drops_item:
                        key_sprites = [x for x in candidate_sprites if x.good_for_key_drop() and not x.water_only]
                        chosen = random.choice(key_sprites)
                    elif room_id in shutter_sprites and i in shutter_sprites[room_id]:
                        killable_sprite = [x for x in candidate_sprites if x.good_for_shutter() and not x.water_only]
                        chosen = random.choice(killable_sprite)
                    else:
                        non_water = [x for x in candidate_sprites if not x.water_only]
                        chosen = random.choice(non_water)
                    sprite.kind = chosen.sprite
        # done with sprites
    # done with rooms