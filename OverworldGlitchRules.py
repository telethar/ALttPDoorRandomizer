"""
Helper functions to deliver entrance/exit/region sets to OWG rules.
"""

from BaseClasses import Entrance

# Cave regions that superbunny can get through - but only with a sword.
sword_required_superbunny_mirror_regions = ["Spiral Cave (Top)"]

# Cave regions that superbunny can get through - but only with boots.
boots_required_superbunny_mirror_regions = ["Two Brothers House"]

# Cave locations that superbunny can access - but only with boots.
boots_required_superbunny_mirror_locations = [
    "Sahasrahla's Hut - Left",
    "Sahasrahla's Hut - Middle",
    "Sahasrahla's Hut - Right",
]

# Entrances that can't be superbunny-mirrored into.
invalid_mirror_bunny_entrances = [
    "Hype Cave",
    "Bonk Fairy (Dark)",
    "Thieves Town",
    "Hammer Peg Cave",
    "Brewery",
    "Hookshot Cave",
    "Dark Lake Hylia Ledge Fairy",
    "Dark Lake Hylia Ledge Spike Cave",
    "Palace of Darkness",
    "Misery Mire",
    "Turtle Rock",
    "Bonk Rock Cave",
    "Bonk Fairy (Light)",
    "50 Rupee Cave",
    "20 Rupee Cave",
    "Checkerboard Cave",
    "Light Hype Fairy",
    "Waterfall of Wishing",
    "Light World Bomb Hut",
    "Mini Moldorm Cave",
    "Ice Rod Cave",
    "Sanctuary Grave",
    "Kings Grave",
    "Sanctuary Grave",
    "Hyrule Castle Secret Entrance Drop",
    "Skull Woods Second Section Hole",
    "Skull Woods First Section Hole (North)",
]

# Interior locations that can be accessed with superbunny state.
superbunny_accessible_locations = [
    "Waterfall of Wishing - Left",
    "Waterfall of Wishing - Right",
    "King's Tomb",
    "Floodgate",
    "Floodgate Chest",
    "Cave 45",
    "Bonk Rock Cave",
    "Brewery",
    "C-Shaped House",
    "Chest Game",
    "Mire Shed - Left",
    "Mire Shed - Right",
    "Secret Passage",
    "Ice Rod Cave",
    "Pyramid Fairy - Left",
    "Pyramid Fairy - Right",
    "Superbunny Cave - Top",
    "Superbunny Cave - Bottom",
    "Blind's Hideout - Left",
    "Blind's Hideout - Right",
    "Blind's Hideout - Far Left",
    "Blind's Hideout - Far Right",
    "Kakariko Well - Left",
    "Kakariko Well - Middle",
    "Kakariko Well - Right",
    "Kakariko Well - Bottom",
    "Kakariko Tavern",
    "Library",
    "Spiral Cave",
] + boots_required_superbunny_mirror_locations


# Entrances that can be reached with full equipment using overworld glitches and don't need to be an exit.
# The following are still be mandatory exits:
# Open:
# Turtle Rock Isolated Ledge Entrance
# Skull Woods Second Section Door (West) (or Skull Woods Final Section)
# Inverted:
# Two Brothers House (West)
# Desert Palace Entrance (East)


non_mandatory_exits = [
    "Bumper Cave (Top)",
    "Death Mountain Return Cave (West)",
    "Hookshot Cave Back Entrance",
]

inverted_non_mandatory_exits = [
    "Desert Palace Entrance (North)",
    "Desert Palace Entrance (West)",
    "Agahnims Tower",
    "Hyrule Castle Entrance (West)",
    "Hyrule Castle Entrance (East)",
] + non_mandatory_exits

open_non_mandatory_exits = [
    "Dark Death Mountain Ledge (West)",
    "Dark Death Mountain Ledge (East)",
    "Mimic Cave",
    "Desert Palace Entrance (East)",
] + non_mandatory_exits


# Special Light World region exits that require boots clips.

inverted_boots_clip_exits_lw = [
    ("Light World DMA Clip Spot", "Light World", "West Death Mountain (Bottom)"),
    ("Hera Ascent", "West Death Mountain (Bottom)", "West Death Mountain (Top)"),
    ("Death Mountain Return Ledge Clip Spot", "Light World", "Death Mountain Return Ledge"),
    ("Death Mountain Entrance Clip Spot", "Light World", "Death Mountain Entrance"),
    ("Death Mountain Glitched Bridge", "West Death Mountain (Bottom)", "East Death Mountain (Top)"),
    ("Zora Descent Clip Spot", "East Death Mountain (Top)", "Zoras Domain"),
    ("Desert Northern Cliffs", "Light World", "Desert Northern Cliffs"),
    ("Desert Ledge Dropdown", "Desert Northern Cliffs", "Desert Ledge"),
    ("Desert Palace Entrance Dropdown", "Desert Northern Cliffs", "Desert Palace Entrance (North) Spot"),
    ("Lake Hylia Island Clip Spot", "Light World", "Lake Hylia Island"),
    ("Death Mountain Descent", "West Death Mountain (Bottom)", "Light World"),
    ("Kings Grave Clip Spot", "West Death Mountain (Bottom)", "Kings Grave Area"),
]

open_boots_clip_exits_lw = [
    ("Graveyard Ledge Clip Spot", "West Death Mountain (Bottom)", "Graveyard Ledge"),
    ("Desert Ledge (Northeast) Dropdown", "Desert Northern Cliffs", "Desert Checkerboard Ledge"),
    ("Spectacle Rock Clip Spot", "West Death Mountain (Top)", "Spectacle Rock"),
    ("Bombos Tablet Clip Spot", "Light World", "Bombos Tablet Ledge"),
    ("Floating Island Clip Spot", "East Death Mountain (Top)", "Death Mountain Floating Island"),
    ("Cave 45 Clip Spot", "Light World", "Cave 45 Ledge"),
] + inverted_boots_clip_exits_lw

# Special Dark World region exits that require boots clips.
boots_clip_exits_dw = [
    ("Dark World DMA Clip Spot", "West Dark World", "West Dark Death Mountain (Bottom)"),
    ("Bumper Cave Ledge Clip Spot", "West Dark World", "Bumper Cave Ledge"),
    ("Bumper Cave Entrance Clip Spot", "West Dark World", "Bumper Cave Entrance"),
    ("Catfish Descent", "Dark Death Mountain (Top)", "Catfish Area"),
    ("Hammer Pegs River Clip Spot", "East Dark World", "Hammer Peg Area"),
    ("Dark Lake Hylia Ledge Clip Spot", "East Dark World", "Southeast Dark World"),
    ("Dark Desert Cliffs Clip Spot", "South Dark World", "Dark Desert"),
    ("DW Floating Island Clip Spot", "East Dark Death Mountain (Bottom)", "Dark Death Mountain Floating Island"),
]

open_boots_clip_exits_dw = [
    ("Dark Death Mountain Descent", "West Dark Death Mountain (Bottom)", "West Dark World"),
    ("Ganons Tower Ascent", "West Dark Death Mountain (Bottom)", "Dark Death Mountain (Top)"),
    ("Dark Death Mountain Glitched Bridge", "West Dark Death Mountain (Bottom)", "Dark Death Mountain (Top)"),
    ("Turtle Rock (Top) Clip Spot", "Dark Death Mountain (Top)", "Turtle Rock (Top)"),
] + boots_clip_exits_dw

inverted_boots_clip_exits_dw = [
    ("Dark Desert Teleporter Clip Spot", "Dark Desert", "Dark Desert Ledge")
] + boots_clip_exits_dw


# Dark World drop-down ledges that require glitched speed.
glitched_speed_drops_dw = [
    ("Dark Death Mountain Ledge Clip Spot", "Dark Death Mountain (Top)", "Dark Death Mountain Ledge")
]


# Out of bounds transitions using the mirror
mirror_clip_spots_dw = [
    ("Dark Death Mountain Bunny Descent Mirror Spot", "West Dark Death Mountain (Bottom)", "West Dark World"),
    (
        "Dark Death Mountain Bunny Mirror To East Jump",
        "West Dark Death Mountain (Bottom)",
        "East Dark Death Mountain (Bottom)",
    ),
    ("Desert East Mirror Clip", "Dark Desert", "Desert Palace Mouth"),
]

# Mirror shenanigans placing a mirror portal with a broken camera
mirror_offset_spots_dw = [("Dark Death Mountain Offset Mirror", "West Dark Death Mountain (Bottom)", "East Dark World")]

# Mirror shenanigans placing a mirror portal with a broken camera

mirror_offset_spots_lw = [
    ("Death Mountain Offset Mirror", "West Death Mountain (Bottom)", "Light World"),
    ("Death Mountain Uncle Offset Mirror", "West Death Mountain (Bottom)", "Hyrule Castle Secret Entrance Area"),
    ("Death Mountain Castle Ledge Offset Mirror", "West Death Mountain (Bottom)", "Hyrule Castle Ledge"),
]


def create_owg_connections(world, player):
    """
    Add OWG transitions to player's world without logic
    """
    if world.mode[player] == "inverted":
        connections = (
            inverted_boots_clip_exits_dw
            + inverted_boots_clip_exits_lw
            + glitched_speed_drops_dw
            + mirror_offset_spots_lw
        )
    else:
        connections = (
            open_boots_clip_exits_dw
            + open_boots_clip_exits_lw
            + glitched_speed_drops_dw
            + mirror_clip_spots_dw
            + mirror_offset_spots_dw
        )

    create_no_logic_connections(player, world, connections)


def overworld_glitches_rules(world, player):
    inverted = world.mode[player] == "inverted"

    # Boots-accessible locations.
    set_owg_rules(
        player,
        world,
        inverted_boots_clip_exits_lw if inverted else open_boots_clip_exits_lw,
        lambda state: state.can_boots_clip_lw(player),
    )
    set_owg_rules(
        player,
        world,
        inverted_boots_clip_exits_dw if inverted else open_boots_clip_exits_dw,
        lambda state: state.can_boots_clip_dw(player),
    )
    # Glitched speed drops.
    set_owg_rules(
        player,
        world,
        glitched_speed_drops_dw,
        lambda state: state.can_get_glitched_speed_dw(player),
    )
    # Dark Death Mountain Ledge Clip Spot also accessible with mirror.
    if not inverted:
        add_alternate_rule(
            world.get_entrance("Dark Death Mountain Ledge Clip Spot", player), lambda state: state.has_Mirror(player)
        )

    # Mirror clip spots.
    if inverted:
        set_owg_rules(
            player,
            world,
            mirror_offset_spots_lw,
            lambda state: state.has_Mirror(player) and state.can_boots_clip_dw(player),
        )
    else:
        set_owg_rules(player, world, mirror_clip_spots_dw, lambda state: state.has_Mirror(player))
        set_owg_rules(
            player,
            world,
            mirror_offset_spots_dw,
            lambda state: state.has_Mirror(player) and state.can_boots_clip_lw(player),
        )
        
    # Regions that require the boots and some other stuff.
    if not inverted:
        world.get_entrance("Turtle Rock Teleporter", player).access_rule = lambda state: (
            state.can_boots_clip_lw(player) or state.can_lift_heavy_rocks(player)
        ) and state.has("Hammer", player)

        add_alternate_rule(
            world.get_entrance("Waterfall Fairy Access", player),
            lambda state: state.has_Pearl(player) or state.has_Boots(player),
        )  # assumes access to Waterwalk ability (boots case)
    else:
        add_alternate_rule(world.get_entrance("Waterfall Fairy Access", player), lambda state: state.has_Pearl(player))

    world.get_entrance("Dark Desert Teleporter", player).access_rule = lambda state: (
        state.can_flute(player) or state.can_boots_clip_dw(player)
    ) and state.can_lift_heavy_rocks(player)

    add_alternate_rule(
        world.get_entrance("Dark Witch Rock (North)", player), lambda state: state.can_boots_clip_dw(player)
    )
    add_alternate_rule(
        world.get_entrance("Broken Bridge Pass (Top)", player), lambda state: state.can_boots_clip_dw(player)
    )
    add_alternate_rule(
        world.get_location("Zora's Ledge", player), lambda state: state.can_boots_clip_lw(player)
    )  # assumes access to Waterwalk ability

    add_alternate_rule(
        world.get_location('Maze Race', player), lambda state: state.can_boots_clip_lw(player)
    )

    # This is doable even with bad enemies
    add_alternate_rule(world.get_location("Hobo", player), lambda state: state.can_boots_clip_lw(player))

    # Bunny pocket
    if not inverted:
        add_alternate_rule(world.get_entrance("Skull Woods Final Section", player), lambda state: state.can_bunny_pocket(player) and state.has("Fire Rod", player))
        add_alternate_rule(world.get_entrance("Dark World Shop", player), lambda state: state.can_bunny_pocket(player) and state.has("Hammer", player))
    


def add_alternate_rule(entrance, rule):
    old_rule = entrance.access_rule
    entrance.access_rule = lambda state: old_rule(state) or rule(state)


def create_no_logic_connections(player, world, connections):
    for entrance, parent_region, target_region, *rule_override in connections:
        parent = world.get_region(parent_region, player)
        target = world.get_region(target_region, player)
        connection = Entrance(player, entrance, parent)
        parent.exits.append(connection)
        connection.connect(target)


def set_owg_rules(player, world, connections, default_rule):
    for entrance, parent_region, target_region, *rule_override in connections:
        connection = world.get_entrance(entrance, player)
        rule = rule_override[0] if len(rule_override) > 0 else default_rule
        connection.access_rule = rule
