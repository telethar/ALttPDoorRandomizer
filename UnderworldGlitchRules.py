from BaseClasses import Entrance
import Rules
from OverworldGlitchRules import create_no_logic_connections


def get_kikiskip_spots():
    """
    Spectacle Rock Cave (Bottom) -> Palace of Darkness Exit, a.k.a. Kiki Skip
    """
    yield ("Kiki Skip", "Spectacle Rock Cave (Bottom)", "Palace of Darkness Portal")


def get_mireheraswamp_spots():
    """
    "Mire Torches Top -> Tower of Hera Exit, a.k.a. Mire to Hera Clip
    "Mire Torches Top -> Swamp Palace Exit, a.k.a. Hera to Swamp Clip
    """

    yield ("Mire to Hera Clip", "Mire Torches Top", "Hera Portal")
    yield ("Hera to Swamp Clip", "Mire Torches Top", "Swamp Portal")


def get_icepalace_spots():
    """
    "Ice Palace Exit -> Ice Palace Exit, a.k.a. Ice Palace Clip
    """
    yield ("Ice Lobby Clip", "Ice Portal", "Ice Bomb Drop")


def get_thievesdesert_spots():
    """
    "Thieves' Town -> Desert Palace , a.k.a. Thieves to Desert Clip
    Accessing any of the exits will be in logic because of the ability to dungeon bunny revive
    """
    yield ("Thieves to Desert Clip", "Thieves Attic", "Desert West Portal")
    yield ("Thieves to Desert Clip", "Thieves Attic", "Desert South Portal")
    yield ("Thieves to Desert Clip", "Thieves Attic", "Desert East Portal")


def get_specrock_spots():
    """
    "Spectacle Rock Cave (Peak) -> Spectacle Rock Cave (Top), a.k.a. Spectacle Rock Cave Clip
    """
    yield ("Spec Rock Clip", "Spectacle Rock Cave (Peak)", "Spectacle Rock Cave (Top)")


def get_paradox_spots():
    """
    "Paradox Cave Front -> Paradox Cave Chest Area, a.k.a. Paradox Cave Teleport (dash citrus, 1f right, teleport up)
    """
    yield ("Paradox Front Teleport", "Paradox Cave Front", "Paradox Cave Chest Area")


# We need to make connectors at a separate time from the connections, because of how dungeons are linked to regions
def get_kikiskip_connectors(world, player):
        yield ("Kiki Skip", "Spectacle Rock Cave (Bottom)", world.get_entrance("Palace of Darkness Exit", player).connected_region)


def get_mireheraswamp_connectors(world, player):
        yield ("Mire to Hera Clip", "Mire Torches Top", world.get_entrance("Tower of Hera Exit", player).connected_region)
        yield ("Mire to Hera Clip", "Mire Torches Top", world.get_entrance("Swamp Palace Exit", player).connected_region)


def get_thievesdesert_connectors(world, player):
        yield ("Thieves to Desert Clip", "Thieves Attic", world.get_entrance("Desert Palace Exit (West)", player).connected_region)
        yield ("Thieves to Desert Clip", "Thieves Attic", world.get_entrance("Desert Palace Exit (South)", player).connected_region)
        yield ("Thieves to Desert Clip", "Thieves Attic", world.get_entrance("Desert Palace Exit (East)", player).connected_region)

def get_specrock_connectors(world, player):
        yield ("Spec Rock Clip", "Spectacle Rock Cave (Peak)", world.get_entrance("Spectacle Rock Cave Exit (Top)", player).connected_region)
        yield ("Spec Rock Clip", "Spectacle Rock Cave (Peak)", world.get_entrance("Spectacle Rock Cave Exit", player).connected_region)



# Create connections between dungeons/locations
def create_hybridmajor_connections(world, player):
    create_no_logic_connections(player, world, get_kikiskip_spots())
    create_no_logic_connections(player, world, get_mireheraswamp_spots())
    create_no_logic_connections(player, world, get_icepalace_spots())
    create_no_logic_connections(player, world, get_thievesdesert_spots())
    create_no_logic_connections(player, world, get_specrock_spots())
    create_no_logic_connections(player, world, get_paradox_spots())


# Turn dungeons into connectors
def create_hybridmajor_connectors(world, player):
    create_no_logic_connections(player, world, get_kikiskip_connectors(world, player))
    create_no_logic_connections(player, world, get_mireheraswamp_connectors(world, player))
    create_no_logic_connections(player, world, get_thievesdesert_connectors(world, player))
    create_no_logic_connections(player, world, get_specrock_connectors(world, player))


# For some entrances, we need to fake having pearl, because we're in fake DW/LW.
# This creates a copy of the input state that has Moon Pearl.
def fake_pearl_state(state, player):
    if state.has("Moon Pearl", player):
        return state
    fake_state = state.copy()
    fake_state.prog_items["Moon Pearl", player] += 1
    return fake_state


# Sets the rules on where we can actually go using this clip.
# Behavior differs based on what type of ER shuffle we're playing.
def dungeon_reentry_rules(world, player, clip: Entrance, dungeon_region: str, dungeon_exit: str):
    fix_dungeon_exits = world.fix_palaceofdarkness_exit[player]
    fix_fake_worlds = world.fix_fake_world[player]

    dungeon_entrance = [r for r in world.get_region(dungeon_region, player).entrances if r.name != clip.name][0]
    if not fix_dungeon_exits:  # vanilla, simple, restricted, dungeonssimple; should never have fake worlds fix
        # Dungeons are only shuffled among themselves. We need to check SW, MM, and AT because they can't be reentered trivially.

        # entrance doesn't exist until you fire rod it from the other side
        if dungeon_entrance.name == "Skull Woods Final Section":
            Rules.set_rule(clip, lambda state: False)

        elif dungeon_entrance.name == "Misery Mire":
            if world.swords[player] == "swordless":
                Rules.add_rule(clip, lambda state: state.has_misery_mire_medallion(player))
            else:
                Rules.add_rule(clip, lambda state: state.has_sword(player) and state.has_misery_mire_medallion(player))

        elif dungeon_entrance.name == "Agahnims Tower":
            Rules.add_rule(clip, lambda state: state.has("Cape", player) or state.has_beam_sword(player) or state.has("Beat Agahnim 1", player))

        # Then we set a restriction on exiting the dungeon, so you can't leave unless you got in normally.
        Rules.add_rule(world.get_entrance(dungeon_exit, player), lambda state: dungeon_entrance.can_reach(state))
    elif not fix_fake_worlds:  # full, dungeonsfull; fixed dungeon exits, but no fake worlds fix
        # Entry requires the entrance's requirements plus a fake pearl, but you don't gain logical access to the surrounding region.
        Rules.add_rule(clip, lambda state: dungeon_entrance.access_rule(fake_pearl_state(state, player)))
        # exiting restriction
        Rules.add_rule(world.get_entrance(dungeon_exit, player), lambda state: dungeon_entrance.can_reach(state))

    # Otherwise, the shuffle type is lean, lite, crossed, or insanity; all of these do not need additional rules on where we can go,
    # since the clip links directly to the exterior region.


def underworld_glitches_rules(world, player):
    # Ice Palace Entrance Clip, needs bombs or cane of somaria to exit bomb drop room
    Rules.add_rule(world.get_entrance("Ice Bomb Drop SE", player),
                   lambda state: state.can_dash_clip(world.get_region("Ice Lobby", player), player) and 
                   (state.can_use_bombs(player) or state.has('Cane of Somaria', player)),
                   combine="or")

    # Kiki Skip
    kks = world.get_entrance("Kiki Skip", player)
    Rules.set_rule(kks, lambda state: state.can_bomb_clip(kks.parent_region, player))
    dungeon_reentry_rules(world, player, kks, "Palace of Darkness Portal", "Palace of Darkness Exit")

    # Mire -> Hera -> Swamp
    def mire_clip(state):
        return state.can_reach("Mire Torches Top", "Region", player) and state.can_dash_clip(world.get_region("Mire Torches Top", player), player)

    def hera_clip(state):
        return state.can_reach("Hera 4F", "Region", player) and state.can_dash_clip(world.get_region("Hera 4F", player), player)
    

    Rules.add_rule(world.get_entrance("Hera Startile Corner NW", player), lambda state: mire_clip(state) and state.has("Big Key (Misery Mire)", player), combine="or")
    
    mire_to_hera = world.get_entrance("Mire to Hera Clip", player)
    mire_to_swamp = world.get_entrance("Hera to Swamp Clip", player)
    Rules.set_rule(mire_to_hera, mire_clip)
    Rules.set_rule(mire_to_swamp, lambda state: mire_clip(state) and state.has("Flippers", player))

    # Using the entrances for various ER types. Hera -> Swamp never matters because you can only logically traverse with the mire keys
    dungeon_reentry_rules(world, player, mire_to_hera, "Hera Lobby", "Tower of Hera Exit")
    dungeon_reentry_rules(world, player, mire_to_swamp, "Swamp Lobby", "Swamp Palace Exit")   
    # We need to set _all_ swamp doors to be openable with mire keys, otherwise the small key can't be behind them - 6 keys because of Pots
    # Flippers required for all of these doors to prevent locks when flooding
    for door in [
        "Swamp Trench 1 Approach ES",
        "Swamp Hammer Switch SW",
        "Swamp Entrance Down Stairs",
        "Swamp Pot Row WS",
        "Swamp Trench 1 Key Ledge NW",
        "Swamp Hub WN",
        "Swamp Hub North Ledge N",
        "Swamp Crystal Switch EN",
        "Swamp Push Statue S",
        "Swamp Waterway NW",
        "Swamp T SW",
    ]:
        Rules.add_rule(world.get_entrance(door, player), lambda state: mire_clip(state) and state.has("Small Key (Misery Mire)", player, count=6) and state.has('Flippers', player), combine="or")
        # Rules.add_rule(world.get_entrance(door, player), lambda state: mire_clip(state) and state.has('Flippers', player), combine="or")

    Rules.add_rule(world.get_location("Trench 1 Switch", player), lambda state: mire_clip(state) or hera_clip(state), combine="or")

    # Build the rule for SP moat.
    # We need to be able to s+q to old man, then go to either Mire or Hera at either Hera or GT.
    # First we require a certain type of entrance shuffle, then build the rule from its pieces.
    if not world.swamp_patch_required[player]:
        if world.shuffle[player] in [
            "vanilla",
            "dungeonssimple",
            "dungeonsfull",
            "dungeonscrossed",
        ]:
            rule_map = {
                "Mire Portal": (lambda state: state.can_reach("Mire Torches Top", "Entrance", player)),
                "Hera Portal": (lambda state: state.can_reach("Hera Startile Corner NW", "Entrance", player)),
            }
            inverted = world.mode[player] == "inverted"

            def hera_rule(state):
                return (state.has("Moon Pearl", player) or not inverted) and rule_map.get(world.get_entrance("Tower of Hera", player).connected_region.name, lambda state: False)(state)

            def gt_rule(state):
                return (state.has("Moon Pearl", player) or inverted) and rule_map.get(
                    world.get_entrance(("Ganons Tower" if not inverted else "Inverted Ganons Tower"), player).connected_region.name, lambda state: False)(state)

            def mirrorless_moat_rule(state):
                return state.can_reach("Old Man S&Q", "Entrance", player) and mire_clip(state) and (hera_rule(state) or gt_rule(state))

            Rules.add_rule(world.get_entrance("Swamp Lobby Moat", player), lambda state: mirrorless_moat_rule(state), combine="or")

    # Thieves -> Hera
    Rules.add_rule(world.get_entrance("Thieves to Desert Clip", player), lambda state: state.can_dash_clip(world.get_region("Thieves Attic", player), player))
    dungeon_reentry_rules(world, player, world.get_entrance("Thieves to Desert Clip", player), "Desert West Portal", "Desert Palace Exit (West)")
    dungeon_reentry_rules(world, player, world.get_entrance("Thieves to Desert Clip", player), "Desert South Portal", "Desert Palace Exit (South)")
    dungeon_reentry_rules(world, player, world.get_entrance("Thieves to Desert Clip", player), "Desert East Portal", "Desert Palace Exit (East)")

    # Collecting left chests in Paradox Cave using a dash clip -> dash citrus, 1f right, teleport up
    paradox_left_chests = ['Paradox Cave Lower - Far Left', 'Paradox Cave Lower - Left', 'Paradox Cave Lower - Middle']
    for location in paradox_left_chests:
        Rules.add_rule(world.get_location(location, player), lambda state: state.can_dash_clip(world.get_location(location, player).parent_region, player), 'or')
     
    # Collecting right chests in Paradox Cave using a dash clip on left side -> dash citrus, 1f right, teleport up, then hitting the switch
    paradox_right_chests = ['Paradox Cave Lower - Right', 'Paradox Cave Lower - Far Right']
    for location in paradox_right_chests:
        Rules.add_rule(world.get_location(location, player), lambda state: (state.can_dash_clip(world.get_location(location, player).parent_region, player) and state.can_hit_crystal(player)), 'or')
    
