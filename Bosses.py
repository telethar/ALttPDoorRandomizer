import logging
import random

from BaseClasses import Boss
from Fill import FillError
from Rules import has_blunt_weapon, can_shoot_arrows, can_extend_magic, has, or_rule, and_rule, has_sword, can_get_good_bee, flag


def BossFactory(boss, world, player):
    if boss is None:
        return None
    if boss in boss_table:
        enemizer_name, defeat_rule = boss_table[boss]
        return Boss(boss, enemizer_name, defeat_rule(world, player), player)

    logging.getLogger('').error('Unknown Boss: %s', boss)
    return None


def ArmosKnightsDefeatRule(world, player):
    # Magic amounts are probably a bit overkill
    return or_rule(
        has_blunt_weapon(player),
        can_shoot_arrows(world, player),
        and_rule(has('Cane of Somaria', player) and can_extend_magic(player, 10)),
        and_rule(has('Cane of Byrna', player) and can_extend_magic(player, 16)),
        and_rule(has('Ice Rod', player) and can_extend_magic(player, 32)),
        and_rule(has('Fire Rod', player) and can_extend_magic(player, 32)),
        has('Blue Boomerang', player),
        has('Red Boomerang', player))


def LanmolasDefeatRule(world, player):
    return or_rule(
        has_blunt_weapon(player),
        has('Fire Rod', player),
        has('Ice Rod', player),
        has('Cane of Somaria', player),
        has('Cane of Byrna', player),
        can_shoot_arrows(world, player))


def MoldormDefeatRule(world, player):
    return has_blunt_weapon(player)


def HelmasaurKingDefeatRule(world, player):
    return or_rule(has_sword(player), can_shoot_arrows(world, player))


def ArrghusDefeatRule(world, player):
    return and_rule(
        has('Hookshot', player),
        or_rule(
            has_blunt_weapon(player),
            or_rule(
                and_rule(has('Fire Rod', player), or_rule(can_extend_magic(player, 12), can_shoot_arrows(world, player))),  # assuming mostly getting two puff with one shot
                and_rule(has('Ice Rod', player), or_rule(can_extend_magic(player, 16), can_shoot_arrows(world, player)))
            )
            # TODO: ideally we would have a check for bow and silvers, which combined with the
            # hookshot is enough. This is not coded yet because the silvers that only work in pyramid feature
            # makes this complicated
        )
    )


def MothulaDefeatRule(world, player):
    return or_rule(
        has_blunt_weapon(player),
        and_rule(has('Fire Rod', player), can_extend_magic(player, 10)),
        # TODO: Not sure how much (if any) extend magic is needed for these two, since they only apply
        # to non-vanilla locations, so are harder to test, so sticking with what VT has for now:
        and_rule(has('Cane of Somaria', player), can_extend_magic(player, 16)),
        and_rule(has('Cane of Byrna', player), can_extend_magic(player, 16)),
        can_get_good_bee(world, player)
    )


def BlindDefeatRule(world, player):
    return or_rule(has_blunt_weapon(player), has('Cane of Somaria', player), has('Cane of Byrna', player))


def KholdstareDefeatRule(world, player):
    return and_rule(
        or_rule(
            has('Fire Rod', player),
            and_rule(
                has('Bombos', player),
                # FIXME: the following only actually works for the vanilla location for swordless
                or_rule(has_sword(player), flag(world.swords[player] == 'swordless'))
            )
        ),
        or_rule(
            has_blunt_weapon(player),
            and_rule(has('Fire Rod', player) and can_extend_magic(player, 20)),
            # FIXME: this actually only works for the vanilla location for swordless
            and_rule(
                has('Fire Rod', player),
                has('Bombos', player),
                flag(world.swords[player] == 'swordless'),
                can_extend_magic(player, 16)
            )
        )
    )


def VitreousDefeatRule(world, player):
    return or_rule(can_shoot_arrows(world, player), has_blunt_weapon(player))


def TrinexxDefeatRule(world, player):
    return and_rule(
        has('Fire Rod', player),
        has('Ice Rod', player),
        or_rule(
            has('Hammer', player),
            has('Golden Sword', player),
            has('Tempered Sword', player),
            and_rule(has('Master Sword', player) and can_extend_magic(player, 16)),
            and_rule(has_sword(player) and can_extend_magic(player, 32))
        )
    )


def AgahnimDefeatRule(world, player):
    return or_rule(has_sword(player), has('Hammer', player), has('Bug Catching Net', player))


boss_table = {
    'Armos Knights': ('Armos', ArmosKnightsDefeatRule),
    'Lanmolas': ('Lanmola', LanmolasDefeatRule),
    'Moldorm': ('Moldorm', MoldormDefeatRule),
    'Helmasaur King': ('Helmasaur', HelmasaurKingDefeatRule),
    'Arrghus': ('Arrghus', ArrghusDefeatRule),
    'Mothula': ('Mothula', MothulaDefeatRule),
    'Blind': ('Blind', BlindDefeatRule),
    'Kholdstare': ('Kholdstare', KholdstareDefeatRule),
    'Vitreous': ('Vitreous', VitreousDefeatRule),
    'Trinexx': ('Trinexx', TrinexxDefeatRule),
    'Agahnim': ('Agahnim', AgahnimDefeatRule),
    'Agahnim2': ('Agahnim2', AgahnimDefeatRule)
}


def can_place_boss(world, player, boss, dungeon_name, level=None):
    if world.swords[player] in ['swordless'] and boss == 'Kholdstare' and dungeon_name != 'Ice Palace':
        return False

    if dungeon_name == 'Ganons Tower' and level == 'top':
        if boss in ["Armos Knights", "Arrghus",	"Blind", "Trinexx", "Lanmolas"]:
            return False

    if dungeon_name == 'Ganons Tower' and level == 'middle':
        if boss in ["Blind"]:
            return False

    if dungeon_name == 'Tower of Hera' and boss in ["Armos Knights", "Arrghus",	"Blind", "Trinexx", "Lanmolas"]:
        return False

    if dungeon_name == 'Skull Woods' and boss in ["Trinexx"]:
        return False

    if boss in ["Agahnim",	"Agahnim2",	"Ganon"]:
        return False
    return True


def place_bosses(world, player):
    if world.boss_shuffle[player] == 'none':
        return
    # Most to least restrictive order
    boss_locations = [
        ['Ganons Tower', 'top'],
        ['Tower of Hera', None],
        ['Skull Woods', None],
        ['Ganons Tower', 'middle'],
        ['Eastern Palace', None],
        ['Desert Palace', None],
        ['Palace of Darkness', None],
        ['Swamp Palace', None],
        ['Thieves Town', None],
        ['Ice Palace', None],
        ['Misery Mire', None],
        ['Turtle Rock', None],
        ['Ganons Tower', 'bottom'],
    ]

    all_bosses = sorted(boss_table.keys()) #s orted to be deterministic on older pythons
    placeable_bosses = [boss for boss in all_bosses if boss not in ['Agahnim', 'Agahnim2', 'Ganon']]

    if world.boss_shuffle[player] in ["simple", "full"]:
        # temporary hack for swordless kholdstare:
        if world.swords[player] == 'swordless':
            world.get_dungeon('Ice Palace', player).boss = BossFactory('Kholdstare', player)
            logging.getLogger('').debug('Placing boss Kholdstare at Ice Palace')
            boss_locations.remove(['Ice Palace', None])
            placeable_bosses.remove('Kholdstare')

        if world.boss_shuffle[player] == "basic": # vanilla bosses shuffled
            bosses = placeable_bosses + ['Armos Knights', 'Lanmolas', 'Moldorm']
        else: # all bosses present, the three duplicates chosen at random
            bosses = all_bosses + [random.choice(placeable_bosses) for _ in range(3)]

        logging.getLogger('').debug('Bosses chosen %s', bosses)

        random.shuffle(bosses)
        for [loc, level] in boss_locations:
            loc_text = loc + (' ('+level+')' if level else '')
            boss = next((b for b in bosses if can_place_boss(world, player, b, loc, level)), None)
            if not boss:
                raise FillError('Could not place boss for location %s' % loc_text)
            bosses.remove(boss)

            # GT Bosses can move dungeon - find the real dungeon to place them in
            if level:
                loc = [x.name for x in world.dungeons if x.player == player and level in x.bosses.keys()][0]
                loc_text = loc + ' (' + level + ')'
            logging.getLogger('').debug('Placing boss %s at %s', boss, loc_text)
            world.get_dungeon(loc, player).bosses[level] = BossFactory(boss, player)
    elif world.boss_shuffle[player] == "random": #all bosses chosen at random
        for [loc, level] in boss_locations:
            loc_text = loc + (' ('+level+')' if level else '')
            try:
                boss = random.choice([b for b in placeable_bosses if can_place_boss(world, player, b, loc, level)])
            except IndexError:
                raise FillError('Could not place boss for location %s' % loc_text)

            # GT Bosses can move dungeon - find the real dungeon to place them in
            if level:
                loc = [x.name for x in world.dungeons if x.player == player and level in x.bosses.keys()][0]
                loc_text = loc + ' (' + level + ')'
            logging.getLogger('').debug('Placing boss %s at %s', boss, loc_text)
            world.get_dungeon(loc, player).bosses[level] = BossFactory(boss, player)
