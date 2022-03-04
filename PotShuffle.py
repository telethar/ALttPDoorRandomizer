from collections import defaultdict

from BaseClasses import PotItem, Pot, PotFlags, CrystalBarrier, LocationType
from Utils import int16_as_bytes, pc_to_snes

movable_switch_rooms = defaultdict(lambda: [],
                                   {'PoD Stalfos Basement': ['PoD Basement Ledge'],
                                    'Thieves Attic Switch': ['Thieves Attic Hint'],
                                    'Mire Hub Switch': ['Mire Hub', 'Mire Hub Right']})

invalid_key_rooms = {
    'Swamp Big Key Ledge',
    'Swamp Trench 2 Departure',
    'Desert Wall Slide',
    'Skull X Room',  # only required for 100% locations
    'GT Map Room',
    'GT Warp Maze - Mid Section'
}

vanilla_pots = {
    2: [Pot(80, 6, PotItem.Nothing, 'Sewers Yet More Rats', PotFlags.LowerRegion),
        Pot(80, 8, PotItem.Nothing, 'Sewers Yet More Rats', PotFlags.LowerRegion),
        Pot(44, 8, PotItem.Nothing, 'Sewers Yet More Rats', PotFlags.LowerRegion),
        Pot(44, 10, PotItem.Nothing, 'Sewers Yet More Rats', PotFlags.LowerRegion)],
    4: [Pot(162, 25, PotItem.Nothing, 'TR Dash Room'), Pot(152, 25, PotItem.Nothing, 'TR Dash Room'), Pot(152, 22, PotItem.Nothing, 'TR Dash Room'), Pot(162, 22, PotItem.Nothing, 'TR Dash Room'), Pot(204, 19, PotItem.Bomb, 'TR Tongue Pull'),
        Pot(240, 19, PotItem.Bomb, 'TR Tongue Pull')],
    9: [Pot(12, 4, PotItem.OneRupee, 'PoD Shooter Room'), Pot(48, 4, PotItem.Heart, 'PoD Shooter Room'), Pot(12, 12, PotItem.Switch, 'PoD Shooter Room')],
    0xa: [Pot(96, 8, PotItem.Heart, 'PoD Stalfos Basement'), Pot(104, 8, PotItem.Heart, 'PoD Stalfos Basement'),
          Pot(204, 11, PotItem.Switch, 'PoD Stalfos Basement'), Pot(100, 9, PotItem.Nothing, 'PoD Stalfos Basement'),
          Pot(100, 7, PotItem.Nothing, 'PoD Stalfos Basement'),
          Pot(156, 17, PotItem.Bomb, 'PoD Basement Ledge', PotFlags.SwitchLogicChange),
          Pot(160, 17, PotItem.FiveArrows, 'PoD Basement Ledge', PotFlags.SwitchLogicChange)],
    0xb: [Pot(202, 3, PotItem.Bomb, 'PoD Dark Pegs Left'), Pot(202, 12, PotItem.Bomb, 'PoD Dark Pegs Left')],
    0x11: [Pot(152, 19, PotItem.Nothing, 'Sewers Secret Room'), Pot(152, 15, PotItem.Nothing, 'Sewers Secret Room'), Pot(144, 15, PotItem.Heart, 'Sewers Secret Room'), Pot(160, 15, PotItem.Heart, 'Sewers Secret Room'),
          Pot(144, 19, PotItem.Heart, 'Sewers Secret Room'), Pot(160, 19, PotItem.Heart, 'Sewers Secret Room')],
    0x15: [Pot(96, 4, PotItem.Bomb, 'TR Pipe Pit'), Pot(100, 4, PotItem.SmallMagic, 'TR Pipe Pit'), Pot(104, 4, PotItem.Heart, 'TR Pipe Pit'), Pot(108, 4, PotItem.SmallMagic, 'TR Pipe Pit'), Pot(112, 4, PotItem.FiveArrows, 'TR Pipe Pit'),
          Pot(12, 6, PotItem.OneRupee, 'TR Pipe Pit'), Pot(16, 6, PotItem.FiveArrows, 'TR Pipe Pit'), Pot(20, 6, PotItem.FiveRupees, 'TR Pipe Pit'), Pot(70, 11, PotItem.BigMagic, 'TR Pipe Ledge')],
    0x16: [Pot(188, 3, PotItem.Heart, 'Swamp I'), Pot(192, 3, PotItem.Heart, 'Swamp I'), Pot(188, 4, PotItem.SmallMagic, 'Swamp I'), Pot(192, 4, PotItem.SmallMagic, 'Swamp I'), Pot(188, 5, PotItem.FiveArrows, 'Swamp I'),
          Pot(192, 5, PotItem.FiveArrows, 'Swamp I'), Pot(188, 6, PotItem.Bomb, 'Swamp I'), Pot(192, 6, PotItem.Bomb, 'Swamp I'), Pot(240, 19, PotItem.Key, 'Swamp Waterway')],
    0x17: [Pot(100, 13, PotItem.Heart, 'Hera 5F Pot Block'), Pot(100, 14, PotItem.Heart, 'Hera 5F Pot Block'), Pot(100, 15, PotItem.Heart, 'Hera 5F Pot Block'), Pot(100, 16, PotItem.Heart, 'Hera 5F Pot Block'), Pot(100, 17, PotItem.Heart, 'Hera 5F Pot Block'), Pot(100, 18, PotItem.Heart, 'Hera 5F Pot Block'),
          Pot(104, 13, PotItem.Heart, 'Hera 5F Pot Block'), Pot(104, 14, PotItem.Heart, 'Hera 5F Pot Block'), Pot(104, 15, PotItem.Heart, 'Hera 5F Pot Block'), Pot(104, 16, PotItem.Heart, 'Hera 5F Pot Block'), Pot(104, 17, PotItem.Heart, 'Hera 5F Pot Block'), Pot(104, 18, PotItem.Heart, 'Hera 5F Pot Block')],
    26: [Pot(28, 5, PotItem.Bomb, 'PoD Falling Bridge Ledge'), Pot(32, 5, PotItem.Bomb, 'PoD Falling Bridge Ledge'), Pot(28, 27, PotItem.Bomb, 'PoD Falling Bridge'), Pot(32, 27, PotItem.Bomb, 'PoD Falling Bridge'),
         Pot(232, 19, PotItem.Nothing, 'PoD Harmless Hellway'), Pot(212, 19, PotItem.Nothing, 'PoD Harmless Hellway')],
    27: [Pot(20, 23, PotItem.FiveArrows, 'PoD Mimics 2'), Pot(40, 23, PotItem.FiveArrows, 'PoD Mimics 2')],
    30: [Pot(84, 9, PotItem.Bomb, 'Ice Bomb Drop')],
    31: [Pot(28, 25, PotItem.Switch, 'Ice Pengator Switch'), Pot(28, 23, PotItem.Nothing, 'Ice Pengator Switch'), Pot(86, 26, PotItem.Nothing, 'Ice Big Key'), Pot(86, 27, PotItem.Nothing, 'Ice Big Key')],
    33: [Pot(160, 20, PotItem.Nothing, 'Sewers Key Rat'), Pot(168, 24, PotItem.SmallMagic, 'Sewers Key Rat'), Pot(48, 28, PotItem.Heart, 'Sewers Key Rat'), Pot(82, 28, PotItem.SmallMagic, 'Sewers Key Rat'),
         Pot(100, 28, PotItem.Nothing, 'Sewers Key Rat'), Pot(104, 28, PotItem.Nothing, 'Sewers Key Rat')],
    35: [Pot(86, 26, PotItem.OneRupee, 'TR Lazy Eyes'), Pot(90, 26, PotItem.Heart, 'TR Lazy Eyes'), Pot(94, 26, PotItem.OneRupee, 'TR Lazy Eyes'), Pot(98, 26, PotItem.Bomb, 'TR Lazy Eyes'), Pot(102, 26, PotItem.OneRupee, 'TR Lazy Eyes')],
    36: [Pot(12, 4, PotItem.FiveRupees, 'TR Twin Pokeys'), Pot(48, 4, PotItem.Heart, 'TR Twin Pokeys'), Pot(12, 12, PotItem.SmallMagic, 'TR Twin Pokeys'), Pot(48, 12, PotItem.OneRupee, 'TR Twin Pokeys')],
    38: [Pot(28, 4, PotItem.Bomb, 'Swamp Shooters'), Pot(12, 8, PotItem.SmallMagic, 'Swamp Shooters'), Pot(150, 19, PotItem.Switch, 'Swamp Push Statue'), Pot(22, 26, PotItem.FiveRupees, 'Swamp Push Statue'),
         Pot(220, 26, PotItem.FiveArrows, 'Swamp Push Statue', PotFlags.SwitchLogicChange)],
    39: [Pot(214, 19, PotItem.Nothing, 'Hera 4F'), Pot(214, 20, PotItem.Nothing, 'Hera 4F'), Pot(166, 20, PotItem.Bomb, 'Hera 4F'), Pot(214, 21, PotItem.Heart, 'Hera 4F'), Pot(40, 28, PotItem.OneRupee, 'Hera 4F'),
         Pot(44, 28, PotItem.OneRupee, 'Hera 4F'), Pot(80, 28, PotItem.FiveRupees, 'Hera 4F'), Pot(84, 28, PotItem.FiveRupees, 'Hera 4F'), Pot(102, 17, PotItem.Nothing, 'Hera 4F'), Pot(98, 17, PotItem.Nothing, 'Hera 4F'),
         Pot(106, 17, PotItem.Nothing, 'Hera 4F'), Pot(166, 21, PotItem.Nothing, 'Hera 4F'), Pot(166, 19, PotItem.Nothing, 'Hera 4F'), Pot(92, 12, PotItem.Nothing, 'Hera 4F'), Pot(160, 12, PotItem.Nothing, 'Hera 4F')],
    42: [Pot(80, 12, PotItem.OneRupee, 'PoD Arena Main'), Pot(80, 19, PotItem.Heart, 'PoD Arena Main')],
    43: [Pot(16, 5, PotItem.Heart, 'PoD Sexy Statue'), Pot(44, 5, PotItem.Switch, 'PoD Sexy Statue'), Pot(16, 6, PotItem.Heart, 'PoD Sexy Statue'), Pot(44, 6, PotItem.Bomb, 'PoD Sexy Statue'), Pot(16, 7, PotItem.Heart, 'PoD Sexy Statue'),
         Pot(44, 7, PotItem.Bomb, 'PoD Sexy Statue'), Pot(146, 21, PotItem.Bomb, 'PoD Map Balcony'), Pot(170, 21, PotItem.FiveArrows, 'PoD Map Balcony'), Pot(146, 22, PotItem.Bomb, 'PoD Map Balcony'),
         Pot(170, 22, PotItem.FiveArrows, 'PoD Map Balcony')],
    44: [Pot(108, 24, PotItem.Heart, 'Hookshot Cave (Middle)'), Pot(112, 24, PotItem.Heart, 'Hookshot Cave (Middle)')],
    0x2F: [Pot(28, 7, PotItem.Heart, 'Kakariko Well (back)'), Pot(32, 7, PotItem.Heart, 'Kakariko Well (back)'),
           Pot(28, 9, PotItem.FiveRupees, 'Kakariko Well (back)'), Pot(32, 9, PotItem.FiveRupees, 'Kakariko Well (back)'),
           Pot(172, 19, PotItem.FiveRupees, 'Kakariko Well (top)'), Pot(180, 19, PotItem.FiveRupees, 'Kakariko Well (top)'),
           Pot(104, 27, PotItem.Heart, 'Kakariko Well (bottom)'), Pot(104, 28, PotItem.Heart, 'Kakariko Well (bottom)')],
    49: [Pot(92, 28, PotItem.Bomb, 'Hera Beetles'), Pot(96, 28, PotItem.Nothing, 'Hera Beetles')],
    50: [Pot(28, 13, PotItem.SmallMagic, 'Sewers Dark Cross')],
    52: [Pot(78, 8, PotItem.FiveRupees, 'Swamp Barrier Ledge'), Pot(92, 8, PotItem.FiveRupees, 'Swamp Barrier Ledge')],
    0x35: [Pot(60, 6, PotItem.Key, 'Swamp Trench 2 Alcove'), Pot(20, 8, PotItem.FiveRupees, 'Swamp Big Key Ledge'), Pot(24, 8, PotItem.FiveRupees, 'Swamp Big Key Ledge'), Pot(28, 8, PotItem.FiveRupees, 'Swamp Big Key Ledge'),
           Pot(32, 8, PotItem.FiveRupees, 'Swamp Big Key Ledge'), Pot(36, 8, PotItem.FiveRupees, 'Swamp Big Key Ledge'), Pot(48, 20, PotItem.Heart, 'Swamp Trench 2 Departure'), Pot(76, 23, PotItem.Nothing, 'Swamp Trench 2 Pots'),
           Pot(88, 23, PotItem.Nothing, 'Swamp Trench 2 Pots'), Pot(100, 27, PotItem.Nothing, 'Swamp Trench 2 Pots'), Pot(242, 28, PotItem.Nothing, 'Swamp Trench 2 Pots'), Pot(240, 22, PotItem.Heart, 'Swamp Trench 2 Pots'),
           Pot(76, 28, PotItem.Heart, 'Swamp Trench 2 Pots')],
    0x36: [Pot(108, 4, PotItem.Bomb, 'Swamp Hub Dead Ledge'), Pot(112, 4, PotItem.FiveRupees, 'Swamp Hub Dead Ledge'),
           Pot(10, 16, PotItem.Heart, 'Swamp Hub Side Ledges'), Pot(154, 15, PotItem.Nothing, 'Swamp Hub Side Ledges'),
           Pot(114, 16, PotItem.Key, 'Swamp Hub Side Ledges'), Pot(222, 15, PotItem.Nothing, 'Swamp Hub Side Ledges'),
           Pot(188, 5, PotItem.Nothing, 'Swamp Hub North Ledge'),
           Pot(192, 5, PotItem.Nothing, 'Swamp Hub North Ledge')],
    0x37: [Pot(60, 6, PotItem.Key, 'Swamp Trench 1 Alcove'), Pot(48, 20, PotItem.Nothing, 'Swamp Trench 1 Key Ledge')],
    0x38: [Pot(164, 12, PotItem.Bomb, 'Swamp Pot Row'), Pot(164, 13, PotItem.FiveRupees, 'Swamp Pot Row'), Pot(164, 18, PotItem.Bomb, 'Swamp Pot Row'), Pot(164, 19, PotItem.Key, 'Swamp Pot Row')],
    0x39: [Pot(12, 20, PotItem.Heart, 'Skull Spike Corner'), Pot(48, 28, PotItem.FiveArrows, 'Skull Spike Corner'), Pot(100, 22, PotItem.SmallMagic, 'Skull Final Drop'), Pot(100, 26, PotItem.FiveArrows, 'Skull Final Drop')],
    0x3C: [Pot(24, 8, PotItem.SmallMagic, 'Hookshot Cave (Hook Islands)'),
           Pot(64, 12, PotItem.FiveRupees, 'Hookshot Cave (Hook Islands)'),
           Pot(20, 14, PotItem.OneRupee, 'Hookshot Cave (Hook Islands)'),
           Pot(20, 19, PotItem.Nothing, 'Hookshot Cave (Hook Islands)'),
           Pot(68, 18, PotItem.FiveRupees, 'Hookshot Cave (Bonk Islands)'),
           Pot(96, 19, PotItem.Heart, 'Hookshot Cave (Front)'),
           Pot(64, 20, PotItem.FiveRupees, 'Hookshot Cave (Bonk Islands)'),
           Pot(64, 26, PotItem.FiveRupees, 'Hookshot Cave (Bonk Islands)')],
    0x3D: [Pot(76, 12, PotItem.Bomb, 'GT Mini Helmasaur Room'), Pot(112, 12, PotItem.Bomb, 'GT Mini Helmasaur Room'), Pot(24, 22, PotItem.Heart, 'GT Crystal Inner Circle'), Pot(40, 22, PotItem.FiveArrows, 'GT Crystal Inner Circle'),
           Pot(32, 24, PotItem.Heart, 'GT Crystal Inner Circle'), Pot(20, 26, PotItem.FiveRupees, 'GT Crystal Inner Circle'), Pot(36, 26, PotItem.BigMagic, 'GT Crystal Inner Circle')],
    0x3E: [Pot(96, 6, PotItem.Bomb, 'Ice Stalfos Hint'), Pot(100, 6, PotItem.SmallMagic, 'Ice Stalfos Hint'), Pot(88, 10, PotItem.Heart, 'Ice Stalfos Hint'), Pot(92, 10, PotItem.SmallMagic, 'Ice Stalfos Hint')],
    0x3F: [Pot(12, 25, PotItem.OneRupee, 'Ice Hammer Block'), Pot(20, 25, PotItem.OneRupee, 'Ice Hammer Block'),
           Pot(12, 26, PotItem.Bomb, 'Ice Hammer Block'), Pot(20, 26, PotItem.Bomb, 'Ice Hammer Block'),
           Pot(12, 27, PotItem.Switch, 'Ice Hammer Block'), Pot(20, 27, PotItem.Heart, 'Ice Hammer Block'),
           Pot(28, 23, PotItem.Key, 'Ice Hammer Block', PotFlags.Block)],
    0x41: [Pot(100, 10, PotItem.Heart, 'Sewers Behind Tapestry'), Pot(52, 15, PotItem.OneRupee, 'Sewers Behind Tapestry'), Pot(52, 16, PotItem.SmallMagic, 'Sewers Behind Tapestry'), Pot(148, 22, PotItem.SmallMagic, 'Sewers Behind Tapestry')],
    0x43: [Pot(66, 4, PotItem.FiveArrows, 'Desert Wall Slide'), Pot(78, 4, PotItem.SmallMagic, 'Desert Wall Slide'), Pot(66, 9, PotItem.Heart, 'Desert Wall Slide'), Pot(78, 9, PotItem.Heart, 'Desert Wall Slide'),
           Pot(112, 28, PotItem.Nothing, 'Desert Tiles 2'), Pot(76, 28, PotItem.Nothing, 'Desert Tiles 2'), Pot(76, 20, PotItem.Nothing, 'Desert Tiles 2'), Pot(112, 20, PotItem.Key, 'Desert Tiles 2')],
    0x44: [Pot(204, 7, PotItem.Nothing, 'Thieves Conveyor Bridge', PotFlags.Block)],
    0x45: [Pot(12, 4, PotItem.FiveArrows, 'Thieves Basement Block'),
           Pot(48, 12, PotItem.FiveArrows, 'Thieves Basement Block'),
           Pot(92, 11, PotItem.Nothing, "Thieves Blind's Cell Interior"), Pot(108, 11, PotItem.Heart, "Thieves Blind's Cell Interior"),
           Pot(220, 16, PotItem.SmallMagic, "Thieves Blind's Cell Interior"),
           Pot(236, 16, PotItem.Heart, "Thieves Blind's Cell Interior"),
           Pot(0x9C, 7, PotItem.Nothing, 'Thieves Basement Block', PotFlags.Block)],
    70: [Pot(96, 5, PotItem.Heart, 'Swamp Donut Top'), Pot(28, 27, PotItem.Heart, 'Swamp Donut Bottom')],
    73: [Pot(104, 15, PotItem.SmallMagic, 'Skull Torch Room'), Pot(104, 16, PotItem.SmallMagic, 'Skull Torch Room'), Pot(156, 27, PotItem.Nothing, 'Skull Star Pits'), Pot(172, 24, PotItem.Nothing, 'Skull Star Pits'),
         Pot(172, 23, PotItem.Nothing, 'Skull Star Pits'), Pot(144, 20, PotItem.Nothing, 'Skull Star Pits'), Pot(144, 19, PotItem.SmallMagic, 'Skull Star Pits'), Pot(172, 20, PotItem.Heart, 'Skull Star Pits'),
         Pot(144, 27, PotItem.Heart, 'Skull Star Pits'), Pot(172, 28, PotItem.SmallMagic, 'Skull Star Pits'), Pot(160, 27, PotItem.Nothing, 'Skull Star Pits')],
    74: [Pot(14, 5, PotItem.Switch, 'PoD Left Cage'), Pot(32, 5, PotItem.Bomb, 'PoD Left Cage'), Pot(14, 11, PotItem.Heart, 'PoD Left Cage'), Pot(32, 11, PotItem.OneRupee, 'PoD Left Cage'), Pot(56, 8, PotItem.Bomb, 'PoD Middle Cage'),
         Pot(68, 8, PotItem.Bomb, 'PoD Middle Cage'), Pot(92, 5, PotItem.Bomb, 'PoD Middle Cage'), Pot(110, 5, PotItem.Switch, 'PoD Middle Cage'), Pot(92, 11, PotItem.OneRupee, 'PoD Middle Cage'), Pot(110, 11, PotItem.Heart, 'PoD Middle Cage')],
    75: [Pot(20, 6, PotItem.FiveArrows, 'PoD Mimics 1'), Pot(40, 6, PotItem.Heart, 'PoD Mimics 1')],
    78: [Pot(140, 7, PotItem.Nothing, 'Ice Bomb Jump Catwalk'), Pot(48, 10, PotItem.Nothing, 'Ice Bomb Jump Catwalk'), Pot(140, 11, PotItem.Switch, 'Ice Bomb Jump Catwalk'), Pot(28, 12, PotItem.Heart, 'Ice Bomb Jump Catwalk'),
         Pot(112, 12, PotItem.SmallMagic, 'Ice Narrow Corridor')],
    0x50: [Pot(96, 0x6, PotItem.Heart, 'Hyrule Castle West Hall', PotFlags.LowerRegion),
           Pot(100, 0x6, PotItem.Heart, 'Hyrule Castle West Hall', PotFlags.LowerRegion)],
    82: [Pot(138, 3, PotItem.Heart, 'Hyrule Castle East Hall'), Pot(194, 26, PotItem.Heart, 'Hyrule Castle East Hall')],
    0x53: [Pot(92, 11, PotItem.Heart, 'Desert Beamos Hall'), Pot(96, 11, PotItem.SmallMagic, 'Desert Beamos Hall'), Pot(100, 11, PotItem.Key, 'Desert Beamos Hall'), Pot(104, 11, PotItem.Heart, 'Desert Beamos Hall')],
    84: [Pot(186, 25, PotItem.FiveRupees, 'Swamp Attic'), Pot(186, 26, PotItem.Heart, 'Swamp Attic'), Pot(186, 27, PotItem.Heart, 'Swamp Attic'), Pot(186, 28, PotItem.Heart, 'Swamp Attic')],
    85: [Pot(230, 24, PotItem.SmallMagic, 'Hyrule Castle Secret Entrance'), Pot(230, 25, PotItem.SmallMagic, 'Hyrule Castle Secret Entrance')],
    0x56: [Pot(100, 6, PotItem.Nothing, 'Skull Back Drop'), Pot(96, 10, PotItem.Nothing, 'Skull Back Drop'), Pot(92, 10, PotItem.Nothing, 'Skull Back Drop'), Pot(20, 6, PotItem.SmallMagic, 'Skull X Room'),
           Pot(40, 6, PotItem.SmallMagic, 'Skull X Room'), Pot(24, 7, PotItem.SmallMagic, 'Skull X Room'), Pot(36, 7, PotItem.SmallMagic, 'Skull X Room'), Pot(12, 8, PotItem.Heart, 'Skull X Room'), Pot(48, 8, PotItem.Heart, 'Skull X Room'),
           Pot(24, 9, PotItem.SmallMagic, 'Skull X Room'), Pot(36, 9, PotItem.SmallMagic, 'Skull X Room'), Pot(20, 10, PotItem.FiveRupees, 'Skull X Room'), Pot(40, 10, PotItem.FiveRupees, 'Skull X Room'), Pot(12, 20, PotItem.Key, 'Skull 2 West Lobby'),
           Pot(48, 20, PotItem.Nothing, 'Skull 2 West Lobby')],
    87: [Pot(92, 7, PotItem.BigMagic, 'Skull Lone Pot'), Pot(32, 4, PotItem.Nothing, 'Skull Big Key'), Pot(92, 23, PotItem.Bomb, 'Skull Pot Prison'), Pot(100, 23, PotItem.SmallMagic, 'Skull Pot Prison'),
         Pot(84, 25, PotItem.FiveRupees, 'Skull Pot Prison'), Pot(76, 27, PotItem.Heart, 'Skull Pot Prison'), Pot(12, 20, PotItem.SmallMagic, 'Skull 2 East Lobby'), Pot(48, 20, PotItem.SmallMagic, 'Skull 2 East Lobby'),
         Pot(30, 22, PotItem.Switch, 'Skull 2 East Lobby')],
    88: [Pot(12, 7, PotItem.SmallMagic, 'Skull Pull Switch'), Pot(16, 7, PotItem.Nothing, 'Skull Pull Switch'), Pot(16, 8, PotItem.SmallMagic, 'Skull Pull Switch'), Pot(12, 12, PotItem.Nothing, 'Skull Pull Switch'),
         Pot(96, 9, PotItem.Nothing, 'Skull Pot Circle'), Pot(92, 8, PotItem.Nothing, 'Skull Pot Circle'), Pot(108, 8, PotItem.Nothing, 'Skull Pot Circle'), Pot(108, 6, PotItem.Nothing, 'Skull Pot Circle'),
         Pot(104, 5, PotItem.Nothing, 'Skull Pot Circle'), Pot(92, 6, PotItem.Nothing, 'Skull Pot Circle'), Pot(96, 5, PotItem.Bomb, 'Skull Pot Circle'), Pot(100, 5, PotItem.SmallMagic, 'Skull Pot Circle'),
         Pot(92, 7, PotItem.Heart, 'Skull Pot Circle'), Pot(108, 7, PotItem.Heart, 'Skull Pot Circle'), Pot(100, 9, PotItem.SmallMagic, 'Skull Pot Circle'), Pot(104, 9, PotItem.Bomb, 'Skull Pot Circle')],
    0x59: [Pot(26, 0xb, PotItem.Heart, 'Skull 3 Lobby', PotFlags.LowerRegion),
           Pot(32, 8, PotItem.Nothing, 'Skull 3 Lobby', PotFlags.LowerRegion),
           Pot(76, 28, PotItem.Nothing, 'Skull East Bridge'),
           Pot(112, 28, PotItem.Nothing, 'Skull East Bridge')],
    0x5B: [Pot(218, 0x5, PotItem.Nothing, 'GT Hidden Spikes', PotFlags.LowerRegion),
           Pot(222, 0x5, PotItem.Switch, 'GT Hidden Spikes', PotFlags.LowerRegion),
           Pot(226, 0x5, PotItem.Nothing, 'GT Hidden Spikes', PotFlags.LowerRegion)],
    92: [Pot(228, 25, PotItem.Nothing, 'GT Refill'), Pot(104, 24, PotItem.Nothing, 'GT Refill'), Pot(228, 22, PotItem.Nothing, 'GT Refill'), Pot(216, 25, PotItem.Nothing, 'GT Refill'), Pot(84, 24, PotItem.Nothing, 'GT Refill'),
         Pot(216, 22, PotItem.Nothing, 'GT Refill'), Pot(94, 22, PotItem.Bomb, 'GT Refill'), Pot(94, 26, PotItem.BigMagic, 'GT Refill')],
    93: [Pot(16, 5, PotItem.Bomb, 'GT Gauntlet 2'), Pot(44, 5, PotItem.FiveRupees, 'GT Gauntlet 2'), Pot(16, 11, PotItem.OneRupee, 'GT Gauntlet 2'), Pot(44, 11, PotItem.FiveArrows, 'GT Gauntlet 2'), Pot(12, 20, PotItem.FiveArrows, 'GT Gauntlet 3'),
         Pot(48, 20, PotItem.Bomb, 'GT Gauntlet 3'), Pot(12, 28, PotItem.SmallMagic, 'GT Gauntlet 3'), Pot(48, 28, PotItem.Bomb, 'GT Gauntlet 3')],
    94: [Pot(92, 4, PotItem.SmallMagic, 'Ice Falling Square'), Pot(96, 4, PotItem.SmallMagic, 'Ice Falling Square'), Pot(76, 8, PotItem.Heart, 'Ice Falling Square'), Pot(112, 8, PotItem.Heart, 'Ice Falling Square')],
    95: [Pot(44, 27, PotItem.Switch, 'Ice Spike Room')],
    96: [Pot(76, 4, PotItem.Heart, 'Hyrule Castle West Lobby'), Pot(112, 4, PotItem.Heart, 'Hyrule Castle West Lobby')],
    98: [Pot(208, 21, PotItem.Heart, 'Hyrule Castle East Lobby')],
    0x63: [Pot(48, 4, PotItem.Nothing, 'Desert Tiles 1'), Pot(12, 4, PotItem.Nothing, 'Desert Tiles 1'), Pot(12, 8, PotItem.Nothing, 'Desert Tiles 1'), Pot(48, 12, PotItem.Nothing, 'Desert Tiles 1'), Pot(48, 8, PotItem.Heart, 'Desert Tiles 1'),
          Pot(12, 12, PotItem.Key, 'Desert Tiles 1')],
    0x64: [Pot(12, 22, PotItem.Bomb, 'Thieves Attic Hint', PotFlags.SwitchLogicChange),
           Pot(16, 22, PotItem.Bomb, 'Thieves Attic Hint', PotFlags.SwitchLogicChange),
           Pot(20, 22, PotItem.Bomb, 'Thieves Attic Hint', PotFlags.SwitchLogicChange),
           Pot(36, 28, PotItem.Bomb, 'Thieves Attic Switch'), Pot(40, 28, PotItem.SmallMagic, 'Thieves Attic Switch'),
           Pot(44, 28, PotItem.SmallMagic, 'Thieves Attic Switch'), Pot(48, 28, PotItem.Switch, 'Thieves Attic Switch')],
    0x65: [Pot(100, 28, PotItem.Bomb, 'Thieves Attic Window'), Pot(104, 28, PotItem.Bomb, 'Thieves Attic Window')],
    0x66: [Pot(48, 0x5, PotItem.FiveArrows, 'Swamp Refill', PotFlags.LowerRegion),
           Pot(52, 0x5, PotItem.Bomb, 'Swamp Refill', PotFlags.LowerRegion),
           Pot(56, 0x5, PotItem.FiveRupees, 'Swamp Refill', PotFlags.LowerRegion),
           Pot(48, 0x6, PotItem.FiveArrows, 'Swamp Refill', PotFlags.LowerRegion),
           Pot(52, 0x6, PotItem.Bomb, 'Swamp Refill', PotFlags.LowerRegion),
           Pot(56, 0x6, PotItem.FiveRupees, 'Swamp Refill', PotFlags.LowerRegion),
           Pot(84, 5, PotItem.Heart, 'Swamp Behind Waterfall'),
           Pot(104, 5, PotItem.FiveArrows, 'Swamp Behind Waterfall'),
           Pot(84, 6, PotItem.Heart, 'Swamp Behind Waterfall'),
           Pot(104, 6, PotItem.Bomb, 'Swamp Behind Waterfall')],
    103: [Pot(22, 26, PotItem.Nothing, 'Skull Left Drop'), Pot(18, 22, PotItem.Nothing, 'Skull Left Drop'), Pot(12, 7, PotItem.FiveArrows, 'Skull Left Drop'), Pot(48, 7, PotItem.SmallMagic, 'Skull Left Drop'),
          Pot(18, 23, PotItem.SmallMagic, 'Skull Left Drop'), Pot(18, 26, PotItem.Heart, 'Skull Left Drop'), Pot(96, 19, PotItem.Heart, 'Skull Compass Room'), Pot(74, 20, PotItem.SmallMagic, 'Skull Compass Room'),
          Pot(92, 9, PotItem.Nothing, 'Skull Compass Room'), Pot(84, 28, PotItem.Nothing, 'Skull Compass Room'), Pot(104, 28, PotItem.Heart, 'Skull Compass Room')],
    104: [Pot(84, 14, PotItem.Nothing, 'Skull Pinball'), Pot(84, 13, PotItem.Nothing, 'Skull Pinball'), Pot(88, 12, PotItem.Nothing, 'Skull Pinball'), Pot(88, 6, PotItem.Nothing, 'Skull Pinball'), Pot(88, 5, PotItem.Nothing, 'Skull Pinball'),
          Pot(88, 4, PotItem.Nothing, 'Skull Pinball'), Pot(64, 17, PotItem.Nothing, 'Skull Pinball'), Pot(64, 15, PotItem.Nothing, 'Skull Pinball'), Pot(64, 7, PotItem.Heart, 'Skull Pinball'), Pot(88, 7, PotItem.SmallMagic, 'Skull Pinball'),
          Pot(64, 16, PotItem.Heart, 'Skull Pinball'), Pot(64, 24, PotItem.SmallMagic, 'Skull Pinball'), Pot(64, 25, PotItem.Heart, 'Skull Pinball')],
    0x6B: [Pot(28, 5, PotItem.Heart, 'GT Crystal Paths'), Pot(44, 5, PotItem.Nothing, 'GT Crystal Paths'), Pot(28, 8, PotItem.Nothing, 'GT Crystal Paths'), Pot(44, 8, PotItem.SmallMagic, 'GT Crystal Paths'),
           Pot(28, 11, PotItem.SmallMagic, 'GT Crystal Paths'), Pot(44, 11, PotItem.Nothing, 'GT Crystal Paths'), Pot(90, 25, PotItem.Nothing, 'GT Mimics 2'), Pot(98, 25, PotItem.FiveArrows, 'GT Mimics 2')],
    0x6C: [Pot(20, 6, PotItem.Heart, 'GT Quad Pot'), Pot(40, 6, PotItem.FiveArrows, 'GT Quad Pot'), Pot(20, 10, PotItem.Bomb, 'GT Quad Pot'), Pot(40, 10, PotItem.SmallMagic, 'GT Quad Pot')],
    0x6D: [Pot(28, 26, PotItem.Heart, 'GT Gauntlet 5'), Pot(32, 26, PotItem.Heart, 'GT Gauntlet 5'), Pot(28, 27, PotItem.SmallMagic, 'GT Gauntlet 5'), Pot(32, 27, PotItem.SmallMagic, 'GT Gauntlet 5')],
    115: [Pot(154, 21, PotItem.FiveArrows, 'Desert Circle of Pots'), Pot(158, 21, PotItem.OneRupee, 'Desert Circle of Pots'), Pot(20, 23, PotItem.Switch, 'Desert Circle of Pots'), Pot(36, 23, PotItem.FiveRupees, 'Desert Circle of Pots'),
          Pot(144, 24, PotItem.Heart, 'Desert Circle of Pots'), Pot(168, 24, PotItem.FiveArrows, 'Desert Circle of Pots'), Pot(20, 26, PotItem.SmallMagic, 'Desert Circle of Pots'), Pot(36, 26, PotItem.Heart, 'Desert Circle of Pots'),
          Pot(154, 27, PotItem.OneRupee, 'Desert Circle of Pots'), Pot(158, 27, PotItem.FiveRupees, 'Desert Circle of Pots')],
    116: [Pot(30, 5, PotItem.SmallMagic, 'Desert Map Room'), Pot(62, 5, PotItem.Switch, 'Desert Map Room'), Pot(94, 5, PotItem.SmallMagic, 'Desert Map Room'), Pot(14, 11, PotItem.Heart, 'Desert Map Room'),
          Pot(46, 11, PotItem.FiveArrows, 'Desert Map Room'), Pot(78, 11, PotItem.FiveArrows, 'Desert Map Room'), Pot(110, 11, PotItem.Heart, 'Desert Map Room')],
    117: [Pot(148, 22, PotItem.SmallMagic, 'Desert Arrow Pot Corner'), Pot(160, 22, PotItem.FiveArrows, 'Desert Arrow Pot Corner'), Pot(172, 22, PotItem.Heart, 'Desert Arrow Pot Corner')],
    118: [Pot(112, 12, PotItem.Heart, 'Swamp Drain Right'), Pot(84, 23, PotItem.Heart, 'Swamp Flooded Spot'), Pot(96, 23, PotItem.Heart, 'Swamp Flooded Spot')],
    0x7B: [Pot(48, 10, PotItem.Nothing, 'GT Conveyor Star Pits'), Pot(88, 10, PotItem.Nothing, 'GT Conveyor Star Pits'), Pot(76, 7, PotItem.Nothing, 'GT Conveyor Star Pits'), Pot(60, 4, PotItem.Heart, 'GT Conveyor Star Pits'),
          Pot(64, 4, PotItem.Key, 'GT Conveyor Star Pits')],
    124: [Pot(36, 21, PotItem.Nothing, 'GT Falling Bridge'), Pot(24, 11, PotItem.Nothing, 'GT Falling Bridge'), Pot(28, 4, PotItem.Heart, 'GT Falling Bridge'), Pot(32, 4, PotItem.Heart, 'GT Falling Bridge')],
    125: [Pot(44, 12, PotItem.Nothing, 'GT Firesnake Room'), Pot(44, 6, PotItem.Nothing, 'GT Firesnake Room'), Pot(112, 6, PotItem.Heart, 'GT Firesnake Room'), Pot(108, 20, PotItem.FiveArrows, 'GT Warp Maze - Pot Rail'),
          Pot(114, 20, PotItem.Bomb, 'GT Petting Zoo'), Pot(76, 28, PotItem.Bomb, 'GT Petting Zoo')],
    126: [Pot(86, 15, PotItem.Heart, 'Ice Tall Hint'), Pot(82, 26, PotItem.SmallMagic, 'Ice Tall Hint'), Pot(100, 26, PotItem.Switch, 'Ice Tall Hint'), Pot(104, 26, PotItem.Nothing, 'Ice Tall Hint')],
    128: [Pot(48, 4, PotItem.Heart, 'Hyrule Dungeon Cellblock'), Pot(52, 4, PotItem.Heart, 'Hyrule Dungeon Cellblock'), Pot(56, 4, PotItem.Heart, 'Hyrule Dungeon Cellblock')],
    0x82: [Pot(50, 0x5, PotItem.Nothing, 'Hyrule Dungeon South Abyss', PotFlags.LowerRegion),
           Pot(50, 0xA, PotItem.Nothing, 'Hyrule Dungeon South Abyss', PotFlags.LowerRegion),
           Pot(76, 0x12, PotItem.Heart, 'Hyrule Dungeon South Abyss', PotFlags.LowerRegion)],
    131: [Pot(76, 4, PotItem.FiveArrows, 'Desert West Wing'), Pot(80, 4, PotItem.OneRupee, 'Desert West Wing'), Pot(76, 28, PotItem.FiveRupees, 'Desert West Wing'), Pot(80, 28, PotItem.FiveArrows, 'Desert West Wing')],
    132: [Pot(64, 17, PotItem.Nothing, 'Desert Main Lobby'), Pot(60, 17, PotItem.Nothing, 'Desert Main Lobby'), Pot(80, 14, PotItem.Nothing, 'Desert Main Lobby'), Pot(44, 14, PotItem.Nothing, 'Desert Main Lobby'),
          Pot(100, 6, PotItem.Nothing, 'Desert Main Lobby'), Pot(24, 6, PotItem.Nothing, 'Desert Main Lobby'), Pot(24, 7, PotItem.FiveArrows, 'Desert Main Lobby'), Pot(100, 7, PotItem.FiveArrows, 'Desert Main Lobby')],
    133: [Pot(44, 28, PotItem.Heart, 'Desert East Wing'), Pot(48, 28, PotItem.FiveArrows, 'Desert East Wing')],
    135: [Pot(12, 11, PotItem.Nothing, 'Hera Tile Room'), Pot(16, 12, PotItem.Nothing, 'Hera Tile Room'), Pot(40, 12, PotItem.Nothing, 'Hera Tile Room'), Pot(32, 12, PotItem.Nothing, 'Hera Tile Room'), Pot(24, 12, PotItem.Nothing, 'Hera Tile Room'),
          Pot(16, 11, PotItem.Nothing, 'Hera Tile Room'), Pot(76, 20, PotItem.SmallMagic, 'Hera Torches'), Pot(112, 20, PotItem.BigMagic, 'Hera Torches')],
    0x8B: [Pot(76, 12, PotItem.Nothing, 'GT Conveyor Cross'), Pot(112, 12, PotItem.Key, 'GT Conveyor Cross'), Pot(32, 23, PotItem.Nothing, 'GT Hookshot South Platform'), Pot(28, 23, PotItem.Nothing, 'GT Hookshot South Platform'),
           Pot(32, 9, PotItem.SmallMagic, 'GT Hookshot Mid Platform'), Pot(76, 20, PotItem.Nothing, 'GT Map Room'), Pot(76, 28, PotItem.Heart, 'GT Map Room')],
    140: [Pot(76, 12, PotItem.Switch, 'GT Hope Room'), Pot(112, 12, PotItem.SmallMagic, 'GT Hope Room'), Pot(76, 20, PotItem.Bomb, "GT Bob's Room"), Pot(92, 20, PotItem.Bomb, "GT Bob's Room"), Pot(100, 21, PotItem.FiveArrows, "GT Bob's Room"),
          Pot(104, 26, PotItem.Bomb, "GT Bob's Room"), Pot(88, 27, PotItem.Bomb, "GT Bob's Room")],
    141: [Pot(204, 11, PotItem.Nothing, 'GT Speed Torch Upper'), Pot(204, 14, PotItem.BigMagic, 'GT Speed Torch Upper'), Pot(28, 23, PotItem.Heart, 'GT Pots n Blocks'), Pot(36, 23, PotItem.Heart, 'GT Pots n Blocks'),
          Pot(32, 24, PotItem.BigMagic, 'GT Pots n Blocks')],
    142: [Pot(80, 5, PotItem.FiveArrows, 'Ice Lonely Freezor'), Pot(80, 6, PotItem.Nothing, 'Ice Lonely Freezor')],
    145: [Pot(84, 4, PotItem.Heart, 'Mire Falling Foes'), Pot(104, 4, PotItem.SmallMagic, 'Mire Falling Foes')],
    146: [Pot(86, 23, PotItem.Nothing, 'Mire Tall Dark and Roomy'), Pot(92, 23, PotItem.Nothing, 'Mire Tall Dark and Roomy'), Pot(98, 23, PotItem.Nothing, 'Mire Tall Dark and Roomy'), Pot(104, 23, PotItem.Nothing, 'Mire Tall Dark and Roomy')],
    0x93: [Pot(28, 7, PotItem.Switch, 'Mire Dark Shooters'),
           Pot(0x9C, 0x17, PotItem.Nothing, 'Mire Block X', PotFlags.Block),
           Pot(96, 7, PotItem.Heart, 'Mire Dark Shooters', PotFlags.NoSwitch)],
    0x96: [Pot(14, 18, PotItem.Nothing, 'GT Torch Cross'),
           Pot(32, 5, PotItem.Nothing, 'GT Torch Cross'),
           Pot(0x2e, 0xb, PotItem.Nothing, 'GT Torch Cross'),
           Pot(32, 17, PotItem.SmallMagic, 'GT Torch Cross'),
           Pot(32, 24, PotItem.SmallMagic, 'GT Torch Cross'),
           Pot(14, 24, PotItem.Nothing, 'GT Torch Cross'),
           Pot(76, 21, PotItem.Heart, 'GT Staredown'),
           Pot(112, 21, PotItem.BigMagic, 'GT Staredown')],
    153: [Pot(40, 20, PotItem.SmallMagic, 'Eastern Darkness'), Pot(84, 20, PotItem.Heart, 'Eastern Darkness')],
    0x9B: [Pot(48, 4, PotItem.SmallMagic, 'GT Double Switch Pot Corners'), Pot(48, 12, PotItem.Key, 'GT Double Switch Pot Corners'), Pot(28, 24, PotItem.Nothing, 'GT Warp Maze - Mid Section'), Pot(32, 24, PotItem.Nothing, 'GT Warp Maze - Mid Section')],
    156: [Pot(56, 8, PotItem.SmallMagic, 'GT Invisible Catwalk'), Pot(56, 9, PotItem.FiveArrows, 'GT Invisible Catwalk')],
    157: [Pot(76, 4, PotItem.Bomb, 'GT Crystal Conveyor Left'), Pot(84, 4, PotItem.SmallMagic, 'GT Crystal Conveyor Left'), Pot(32, 7, PotItem.Nothing, 'GT Compass Room'), Pot(40, 9, PotItem.Nothing, 'GT Compass Room')],
    0x9F: [Pot(138, 20, PotItem.Nothing, 'Ice Many Pots'), Pot(138, 19, PotItem.Heart, 'Ice Many Pots'), Pot(178, 19, PotItem.Heart, 'Ice Many Pots'), Pot(40, 21, PotItem.Switch, 'Ice Many Pots'), Pot(138, 21, PotItem.Key, 'Ice Many Pots'),
           Pot(20, 27, PotItem.Heart, 'Ice Many Pots'), Pot(138, 27, PotItem.Heart, 'Ice Many Pots'), Pot(178, 28, PotItem.Heart, 'Ice Many Pots'), Pot(178, 21, PotItem.Nothing, 'Ice Many Pots'), Pot(178, 20, PotItem.Nothing, 'Ice Many Pots'),
           Pot(40, 27, PotItem.Nothing, 'Ice Many Pots'), Pot(178, 27, PotItem.Nothing, 'Ice Many Pots'), Pot(178, 26, PotItem.Nothing, 'Ice Many Pots'), Pot(138, 28, PotItem.Nothing, 'Ice Many Pots'), Pot(138, 26, PotItem.Nothing, 'Ice Many Pots'),
           Pot(20, 21, PotItem.Nothing, 'Ice Many Pots')],
    0xA1: [Pot(150, 6, PotItem.Key, 'Mire Fishbone'), Pot(100, 11, PotItem.SmallMagic, 'Mire Fishbone'), Pot(104, 12, PotItem.Heart, 'Mire Fishbone'), Pot(108, 13, PotItem.SmallMagic, 'Mire Fishbone'), Pot(112, 14, PotItem.Heart, 'Mire Fishbone'),
           Pot(96, 27, PotItem.Nothing, 'Mire South Fish'), Pot(92, 21, PotItem.Nothing, 'Mire South Fish'), Pot(96, 23, PotItem.Heart, 'Mire South Fish'), Pot(92, 25, PotItem.Nothing, 'Mire South Fish'),
           Pot(76, 28, PotItem.Nothing, 'Mire South Fish'), Pot(112, 28, PotItem.Nothing, 'Mire South Fish')],
    0xA2: [Pot(12, 28, PotItem.BigMagic, 'Mire Left Bridge')],
    168: [Pot(138, 28, PotItem.Nothing, 'Eastern Stalfos Spawn'), Pot(178, 28, PotItem.Nothing, 'Eastern Stalfos Spawn'), Pot(178, 19, PotItem.Nothing, 'Eastern Stalfos Spawn'), Pot(138, 19, PotItem.Heart, 'Eastern Stalfos Spawn'),
          Pot(30, 24, PotItem.OneRupee, 'Eastern Stalfos Spawn')],
    0xA9: [Pot(144, 0xB, PotItem.FiveArrows, 'Eastern Courtyard', PotFlags.LowerRegion),
           Pot(236, 0xB, PotItem.FiveArrows, 'Eastern Courtyard', PotFlags.LowerRegion),
           Pot(144, 0xC, PotItem.FiveArrows, 'Eastern Courtyard', PotFlags.LowerRegion),
           Pot(236, 0xC, PotItem.Heart, 'Eastern Courtyard', PotFlags.LowerRegion),
           Pot(12, 19, PotItem.Nothing, 'Eastern Courtyard Ledge'),
           Pot(112, 19, PotItem.Nothing, 'Eastern Courtyard Ledge'),
           Pot(16, 20, PotItem.Heart, 'Eastern Courtyard Ledge'),
           Pot(108, 20, PotItem.Heart, 'Eastern Courtyard Ledge')],
    0xAA: [Pot(212, 10, PotItem.Nothing, 'Eastern Pot Switch'), Pot(232, 10, PotItem.Nothing, 'Eastern Pot Switch'),
           Pot(232, 5, PotItem.Nothing, 'Eastern Pot Switch'), Pot(212, 5, PotItem.Heart, 'Eastern Pot Switch'),
           Pot(94, 8, PotItem.Switch, 'Eastern Pot Switch'),
           Pot(108, 0x17, PotItem.Heart, 'Eastern Map Balcony', PotFlags.LowerRegion),
           Pot(108, 0x18, PotItem.Heart, 'Eastern Map Balcony', PotFlags.LowerRegion),
           Pot(108, 0x19, PotItem.Heart, 'Eastern Map Balcony', PotFlags.LowerRegion)],
    0xAB: [Pot(20, 24, PotItem.Key, 'Thieves Spike Switch')],
    174: [Pot(76, 12, PotItem.Switch, 'Iced T')],
    176: [Pot(20, 27, PotItem.Nothing, 'Tower Circle of Pots'), Pot(24, 24, PotItem.Nothing, 'Tower Circle of Pots'), Pot(44, 25, PotItem.Nothing, 'Tower Circle of Pots'), Pot(20, 21, PotItem.Bomb, 'Tower Circle of Pots'),
          Pot(28, 21, PotItem.OneRupee, 'Tower Circle of Pots'), Pot(32, 21, PotItem.FiveRupees, 'Tower Circle of Pots'), Pot(40, 21, PotItem.FiveArrows, 'Tower Circle of Pots'), Pot(16, 23, PotItem.FiveRupees, 'Tower Circle of Pots'),
          Pot(44, 23, PotItem.OneRupee, 'Tower Circle of Pots'), Pot(36, 24, PotItem.Heart, 'Tower Circle of Pots'), Pot(16, 25, PotItem.Heart, 'Tower Circle of Pots'), Pot(28, 27, PotItem.FiveArrows, 'Tower Circle of Pots'),
          Pot(40, 27, PotItem.Bomb, 'Tower Circle of Pots'), Pot(32, 27, PotItem.Nothing, 'Tower Circle of Pots')],
    177: [Pot(76, 4, PotItem.Heart, 'Mire Spike Barrier'), Pot(112, 4, PotItem.OneRupee, 'Mire Spike Barrier')],
    0xB2: [Pot(48, 0x8, PotItem.OneRupee, 'Mire BK Door Room', PotFlags.LowerRegion),
           Pot(76, 0x8, PotItem.OneRupee, 'Mire BK Door Room', PotFlags.LowerRegion),
           Pot(48, 0x9, PotItem.Nothing, 'Mire BK Door Room', PotFlags.LowerRegion),
           Pot(76, 0x9, PotItem.Heart, 'Mire BK Door Room', PotFlags.LowerRegion),
           Pot(48, 0xA, PotItem.Nothing, 'Mire BK Door Room', PotFlags.LowerRegion),
           Pot(76, 0xA, PotItem.Nothing, 'Mire BK Door Room', PotFlags.LowerRegion)],
    0xB3: [Pot(12, 20, PotItem.Key, 'Mire Spikes'), Pot(48, 20, PotItem.SmallMagic, 'Mire Spikes'), Pot(48, 28, PotItem.Switch, 'Mire Spikes')],
    0xB4: [Pot(44, 28, PotItem.BigMagic, 'TR Final Abyss Balcony'), Pot(48, 28, PotItem.Heart, 'TR Final Abyss Balcony')],
    0xB5: [Pot(112, 4, PotItem.FiveRupees, 'TR Dark Ride Ledges'), Pot(112, 15, PotItem.Heart, 'TR Dark Ride Ledges'),
           Pot(76, 16, PotItem.Switch, 'TR Dark Ride Ledges'), Pot(112, 16, PotItem.BigMagic, 'TR Dark Ride Ledges'),
           Pot(112, 17, PotItem.Heart, 'TR Dark Ride Ledges'), Pot(112, 28, PotItem.Bomb, 'TR Dark Ride Ledges')],
    0xB6: [Pot(94, 9, PotItem.BigMagic, 'TR Refill')],
    0xB7: [Pot(30, 5, PotItem.SmallMagic, 'TR Roller Room')],
    0xB8: [Pot(96, 13, PotItem.Switch, 'Eastern Big Key'), Pot(88, 16, PotItem.Heart, 'Eastern Big Key'), Pot(104, 16, PotItem.Heart, 'Eastern Big Key')],
    0xB9: [Pot(92, 18, PotItem.OneRupee, 'Eastern Cannonball'), Pot(96, 18, PotItem.FiveRupees, 'Eastern Cannonball'), Pot(104, 18, PotItem.FiveRupees, 'Eastern Cannonball'), Pot(108, 18, PotItem.OneRupee, 'Eastern Cannonball')],
    0xBA: [Pot(100, 8, PotItem.Nothing, 'Eastern Dark Pots'), Pot(88, 8, PotItem.Nothing, 'Eastern Dark Pots'), Pot(94, 4, PotItem.OneRupee, 'Eastern Dark Pots'), Pot(76, 6, PotItem.Heart, 'Eastern Dark Pots'),
          Pot(112, 6, PotItem.Key, 'Eastern Dark Pots'), Pot(76, 10, PotItem.Heart, 'Eastern Dark Pots'), Pot(112, 10, PotItem.SmallMagic, 'Eastern Dark Pots'), Pot(94, 12, PotItem.OneRupee, 'Eastern Dark Pots')],
    0xBC: [Pot(86, 4, PotItem.Heart, 'Thieves Hallway'), Pot(102, 4, PotItem.Key, 'Thieves Hallway'), Pot(138, 3, PotItem.Bomb, 'Thieves Conveyor Maze'), Pot(178, 3, PotItem.Switch, 'Thieves Conveyor Maze'),
          Pot(138, 12, PotItem.Heart, 'Thieves Conveyor Maze'), Pot(178, 12, PotItem.Bomb, 'Thieves Conveyor Maze'), Pot(12, 20, PotItem.Nothing, 'Thieves Pot Alcove Mid'), Pot(48, 20, PotItem.Bomb, 'Thieves Pot Alcove Mid'),
          Pot(12, 28, PotItem.Bomb, 'Thieves Pot Alcove Mid'), Pot(48, 28, PotItem.Bomb, 'Thieves Pot Alcove Mid'), Pot(28, 21, PotItem.FiveRupees, 'Thieves Pot Alcove Top'), Pot(32, 21, PotItem.FiveRupees, 'Thieves Pot Alcove Top'),
          Pot(28, 27, PotItem.FiveRupees, 'Thieves Pot Alcove Bottom'), Pot(32, 27, PotItem.FiveRupees, 'Thieves Pot Alcove Bottom')],
    190: [Pot(92, 25, PotItem.Switch, 'Ice Switch Room')],
    191: [Pot(40, 20, PotItem.FiveArrows, 'Ice Refill'), Pot(44, 20, PotItem.Heart, 'Ice Refill'), Pot(48, 20, PotItem.Bomb, 'Ice Refill'), Pot(40, 28, PotItem.SmallMagic, 'Ice Refill'), Pot(44, 28, PotItem.SmallMagic, 'Ice Refill'),
          Pot(48, 28, PotItem.SmallMagic, 'Ice Refill')],
    192: [Pot(48, 10, PotItem.Bomb, 'Tower Dark Pits'), Pot(12, 14, PotItem.FiveRupees, 'Tower Dark Pits'), Pot(12, 26, PotItem.Heart, 'Tower Dark Pits'), Pot(28, 27, PotItem.OneRupee, 'Tower Dark Pits')],
    0xC2: [Pot(180, 7, PotItem.Switch, 'Mire Hub Switch'),
          Pot(100, 0xE, PotItem.SmallMagic, 'Mire Hub Right', PotFlags.LowerRegion),
          Pot(68, 0x10, PotItem.OneRupee, 'Mire Hub', PotFlags.LowerRegion),
          Pot(64, 0x14, PotItem.FiveArrows, 'Mire Hub', PotFlags.LowerRegion)],
    0xC4: [Pot(84, 9, PotItem.Bomb, 'TR Crystal Maze Interior'), Pot(24, 14, PotItem.Heart, 'TR Crystal Maze Interior'), Pot(56, 17, PotItem.FiveRupees, 'TR Crystal Maze Interior'), Pot(84, 17, PotItem.Bomb, 'TR Crystal Maze Interior'),
          Pot(12, 21, PotItem.FiveArrows, 'TR Crystal Maze Interior'), Pot(76, 23, PotItem.OneRupee, 'TR Crystal Maze Interior'), Pot(48, 25, PotItem.SmallMagic, 'TR Crystal Maze Interior'), Pot(12, 26, PotItem.Heart, 'TR Crystal Maze Interior')],
    0xC6: [Pot(12, 7, PotItem.BigMagic, 'TR Hub Ledges'), Pot(12, 25, PotItem.Heart, 'TR Hub Ledges')],
    0xC7: [Pot(12, 10, PotItem.Heart, 'TR Torches'), Pot(12, 11, PotItem.BigMagic, 'TR Torches'), Pot(12, 22, PotItem.SmallMagic, 'TR Torches Ledge'), Pot(12, 28, PotItem.FiveArrows, 'TR Torches Ledge')],
    0xC9: [Pot(30, 22, PotItem.OneRupee, 'Eastern Lobby'), Pot(94, 22, PotItem.OneRupee, 'Eastern Lobby'), Pot(60, 22, PotItem.Switch, 'Eastern Lobby')],
    0xCB: [Pot(80, 4, PotItem.Nothing, 'Thieves Ambush'), Pot(80, 28, PotItem.Nothing, 'Thieves Ambush'), Pot(88, 16, PotItem.Heart, 'Thieves Ambush'), Pot(88, 28, PotItem.FiveRupees, 'Thieves Ambush')],
    0xCC: [Pot(36, 4, PotItem.FiveRupees, 'Thieves Rail Ledge'), Pot(36, 28, PotItem.FiveRupees, 'Thieves Rail Ledge'), Pot(112, 4, PotItem.Heart, 'Thieves BK Corner'), Pot(112, 28, PotItem.Bomb, 'Thieves BK Corner')],
    0xCE: [Pot(76, 8, PotItem.SmallMagic, 'Ice Antechamber'), Pot(80, 8, PotItem.SmallMagic, 'Ice Antechamber'),
           Pot(108, 12, PotItem.Bomb, 'Ice Antechamber'), Pot(112, 12, PotItem.FiveArrows, 'Ice Antechamber'),
           Pot(204, 11, PotItem.Hole, 'Ice Antechamber'),
           Pot(0x6c, 8, PotItem.Nothing, 'Ice Antechamber', PotFlags.Block)],
    208: [Pot(158, 5, PotItem.SmallMagic, 'Tower Dark Maze'), Pot(140, 11, PotItem.OneRupee, 'Tower Dark Maze'), Pot(42, 13, PotItem.SmallMagic, 'Tower Dark Maze'), Pot(48, 16, PotItem.Heart, 'Tower Dark Maze'),
          Pot(176, 20, PotItem.OneRupee, 'Tower Dark Maze'), Pot(146, 23, PotItem.FiveRupees, 'Tower Dark Maze'), Pot(12, 28, PotItem.Heart, 'Tower Dark Maze')],
    209: [Pot(48, 4, PotItem.BigMagic, 'Mire Conveyor Barrier'), Pot(168, 7, PotItem.OneRupee, 'Mire Conveyor Barrier'), Pot(76, 4, PotItem.OneRupee, 'Mire Neglected Room'), Pot(112, 4, PotItem.FiveArrows, 'Mire Neglected Room'),
          Pot(76, 12, PotItem.Nothing, 'Mire Neglected Room'), Pot(112, 12, PotItem.OneRupee, 'Mire Neglected Room')],
    214: [Pot(92, 22, PotItem.BigMagic, 'TR Main Lobby'), Pot(96, 22, PotItem.Bomb, 'TR Main Lobby')],
    216: [Pot(202, 8, PotItem.Heart, 'Eastern Duo Eyegores'), Pot(242, 8, PotItem.FiveArrows, 'Eastern Duo Eyegores'), Pot(202, 10, PotItem.FiveArrows, 'Eastern Duo Eyegores'), Pot(242, 10, PotItem.FiveArrows, 'Eastern Duo Eyegores'),
          Pot(202, 12, PotItem.FiveArrows, 'Eastern Duo Eyegores'), Pot(242, 12, PotItem.Heart, 'Eastern Duo Eyegores'), Pot(92, 24, PotItem.Heart, 'Eastern Single Eyegore'), Pot(96, 24, PotItem.FiveArrows, 'Eastern Single Eyegore')],
    217: [Pot(92, 20, PotItem.FiveArrows, 'Eastern False Switches'), Pot(92, 28, PotItem.Heart, 'Eastern False Switches')],
    218: [Pot(24, 23, PotItem.FiveArrows, 'Eastern Attic Start'), Pot(36, 23, PotItem.FiveArrows, 'Eastern Attic Start'), Pot(24, 25, PotItem.Switch, 'Eastern Attic Start'), Pot(36, 25, PotItem.Heart, 'Eastern Attic Start')],
    0xDB: [Pot(12, 4, PotItem.Nothing, 'Thieves Lobby'),
           Pot(62, 19, PotItem.Nothing, 'Thieves Lobby', PotFlags.LowerRegion),
           Pot(112, 4, PotItem.FiveRupees, 'Thieves Lobby'), Pot(88, 16, PotItem.Heart, 'Thieves Lobby')],
    0xDC: [Pot(56, 4, PotItem.FiveRupees, 'Thieves Compass Room'), Pot(112, 4, PotItem.Bomb, 'Thieves Compass Room'), Pot(68, 16, PotItem.Heart, 'Thieves Compass Room'), Pot(12, 28, PotItem.FiveArrows, 'Thieves Compass Room')],
    0xE3: [Pot(88, 0x17, PotItem.Nothing, 'Bat Cave (right)', PotFlags.LowerRegion),
           Pot(100, 0x19, PotItem.OneRupee, 'Bat Cave (right)', PotFlags.LowerRegion)],
    0xE4: [Pot(32, 9, PotItem.FiveRupees, 'Old Man House'), Pot(112, 10, PotItem.OneRupee, 'Old Man House')],
    0xE5: [Pot(48, 4, PotItem.OneRupee, 'Old Man House Back'), Pot(76, 4, PotItem.OneRupee, 'Old Man House Back'), Pot(112, 16, PotItem.OneRupee, 'Old Man House Back'), Pot(64, 18, PotItem.FiveRupees, 'Old Man House Back')],
    0xE6: [Pot(108, 12, PotItem.FiveArrows, 'Death Mountain Return Cave (left)'), Pot(88, 16, PotItem.Heart, 'Death Mountain Return Cave (left)'), Pot(72, 20, PotItem.Nothing, 'Death Mountain Return Cave (left)'),
           Pot(56, 24, PotItem.OneRupee, 'Death Mountain Return Cave (left)')],
    0xE7: [Pot(68, 5, PotItem.OneRupee, 'Death Mountain Return Cave (right)'), Pot(72, 5, PotItem.OneRupee, 'Death Mountain Return Cave (right)')],
    232: [Pot(96, 4, PotItem.Heart, 'Superbunny Cave (Bottom)')],
    235: [Pot(206, 8, PotItem.FiveRupees, 'Bumper Cave'), Pot(210, 8, PotItem.FiveRupees, 'Bumper Cave'), Pot(88, 14, PotItem.SmallMagic, 'Bumper Cave'), Pot(92, 14, PotItem.Heart, 'Bumper Cave'), Pot(96, 14, PotItem.SmallMagic, 'Bumper Cave')],
    241: [Pot(64, 5, PotItem.Heart, 'Old Man Cave')],
    0xF3: [Pot(0x28, 0x14, PotItem.Nothing, 'Elder House'),
           Pot(0x2C, 0x14, PotItem.Nothing, 'Elder House'),
           Pot(0x30, 0x14, PotItem.Nothing, 'Elder House')],
    248: [Pot(242, 13, PotItem.BigMagic, 'Superbunny Cave (Top)')],
    253: [Pot(88, 6, PotItem.FiveRupees, 'Fairy Ascension Cave (Top)'), Pot(100, 6, PotItem.FiveRupees, 'Fairy Ascension Cave (Top)'), Pot(84, 23, PotItem.FiveRupees, 'Fairy Ascension Cave (Bottom)'),
          Pot(84, 24, PotItem.FiveRupees, 'Fairy Ascension Cave (Bottom)')],
    255: [Pot(92, 8, PotItem.Heart, 'Paradox Cave Bomb Area'), Pot(96, 8, PotItem.Heart, 'Paradox Cave Bomb Area'), Pot(112, 28, PotItem.OneRupee, 'Paradox Cave Front')],
    257: [Pot(12, 20, PotItem.Heart, 'Snitch Lady (East)'), Pot(224, 19, PotItem.Chicken, 'Snitch Lady (West)'), Pot(228, 19, PotItem.Heart, 'Snitch Lady (West)')],
    258: [Pot(146, 19, PotItem.Heart, 'Sick Kids House'), Pot(150, 19, PotItem.Heart, 'Sick Kids House')],
    259: [Pot(140, 7, PotItem.Chicken, 'Tavern'), Pot(140, 9, PotItem.Nothing, 'Tavern'), Pot(12, 12, PotItem.Heart, 'Tavern (Front)')],
    260: [Pot(202, 21, PotItem.Heart, 'Links House'), Pot(202, 22, PotItem.Heart, 'Links House'), Pot(202, 23, PotItem.Heart, 'Links House')],
    261: [Pot(30, 20, PotItem.Heart, 'Sahasrahlas Hut'), Pot(28, 21, PotItem.Heart, 'Sahasrahlas Hut'), Pot(32, 21, PotItem.Heart, 'Sahasrahlas Hut')],
    0x106: [Pot(0x6c, 0x1b, PotItem.Nothing, 'Brewery')],
    263: [Pot(214, 23, PotItem.Bomb, 'Light World Bomb Hut'), Pot(222, 23, PotItem.FiveArrows, 'Light World Bomb Hut'), Pot(230, 23, PotItem.Bomb, 'Light World Bomb Hut'), Pot(214, 25, PotItem.OneRupee, 'Light World Bomb Hut'),
          Pot(222, 25, PotItem.Nothing, 'Light World Bomb Hut'), Pot(230, 25, PotItem.OneRupee, 'Light World Bomb Hut'), Pot(214, 27, PotItem.Bomb, 'Light World Bomb Hut'), Pot(230, 27, PotItem.Bomb, 'Light World Bomb Hut')],
    264: [Pot(166, 19, PotItem.Chicken, 'Chicken House')],
    268: [Pot(88, 14, PotItem.Heart, 'Hookshot Fairy')],
    276: [Pot(92, 4, PotItem.Heart, 'Dark Desert Hint'), Pot(96, 4, PotItem.Heart, 'Dark Desert Hint'), Pot(92, 5, PotItem.Bomb, 'Dark Desert Hint'), Pot(96, 5, PotItem.Bomb, 'Dark Desert Hint'), Pot(92, 10, PotItem.FiveArrows, 'Dark Desert Hint'),
          Pot(96, 10, PotItem.Heart, 'Dark Desert Hint')],
    0x117: [Pot(138, 3, PotItem.Heart, 'Spike Cave'), Pot(142, 3, PotItem.Heart, 'Spike Cave'),
            Pot(166, 3, PotItem.Heart, 'Spike Cave'), Pot(170, 3, PotItem.Heart, 'Spike Cave'),
            Pot(138, 4, PotItem.Heart, 'Spike Cave'), Pot(142, 4, PotItem.Heart, 'Spike Cave'),
            Pot(166, 4, PotItem.Heart, 'Spike Cave'), Pot(170, 4, PotItem.Heart, 'Spike Cave'),
            Pot(0x18, 0x8, PotItem.Nothing, 'Spike Cave', PotFlags.Block)],
    281: [Pot(44, 28, PotItem.Heart, 'Blinds Hideout'), Pot(48, 28, PotItem.OneRupee, 'Blinds Hideout'), Pot(76, 28, PotItem.Heart, 'Blinds Hideout'), Pot(80, 28, PotItem.Heart, 'Blinds Hideout')],
    282: [Pot(214, 10, PotItem.Heart, 'Palace of Darkness Hint'), Pot(218, 10, PotItem.Heart, 'Palace of Darkness Hint'), Pot(226, 10, PotItem.Heart, 'Palace of Darkness Hint'), Pot(230, 10, PotItem.Heart, 'Palace of Darkness Hint')],
    0x11B: [Pot(24, 0x15, PotItem.Nothing, 'Cave 45', PotFlags.LowerRegion),
            Pot(24, 0x16, PotItem.Heart, 'Cave 45', PotFlags.LowerRegion),
            Pot(32, 0x16, PotItem.Heart, 'Cave 45', PotFlags.LowerRegion),
            Pot(40, 0x16, PotItem.Heart, 'Cave 45', PotFlags.LowerRegion),
            Pot(24, 0x17, PotItem.Heart, 'Cave 45', PotFlags.LowerRegion),
            Pot(28, 0x18, PotItem.Heart, 'Cave 45', PotFlags.LowerRegion),
            Pot(92, 22, PotItem.Bomb, 'Graveyard Cave'), Pot(96, 22, PotItem.Heart, 'Graveyard Cave'),
            Pot(92, 23, PotItem.Bomb, 'Graveyard Cave'), Pot(96, 23, PotItem.Heart, 'Graveyard Cave'),
            Pot(92, 24, PotItem.Bomb, 'Graveyard Cave'), Pot(96, 24, PotItem.Heart, 'Graveyard Cave'),
            Pot(92, 25, PotItem.Bomb, 'Graveyard Cave'), Pot(96, 25, PotItem.Heart, 'Graveyard Cave')],
    0x11D: [Pot(60, 6, PotItem.FiveRupees, 'Blinds Hideout (Top)'), Pot(64, 6, PotItem.FiveRupees, 'Blinds Hideout (Top)'),
            Pot(60, 7, PotItem.FiveRupees, 'Blinds Hideout (Top)'), Pot(64, 7, PotItem.FiveRupees, 'Blinds Hideout (Top)'),
            Pot(60, 8, PotItem.FiveRupees, 'Blinds Hideout (Top)'), Pot(64, 8, PotItem.FiveRupees, 'Blinds Hideout (Top)')],
    0x11F: [Pot(174, 28, PotItem.Heart, 'Lumberjack House'), Pot(178, 28, PotItem.Heart, 'Lumberjack House')],
    292: [Pot(20, 20, PotItem.FiveRupees, '50 Rupee Cave'), Pot(40, 20, PotItem.FiveRupees, '50 Rupee Cave'), Pot(20, 21, PotItem.FiveRupees, '50 Rupee Cave'), Pot(40, 21, PotItem.FiveRupees, '50 Rupee Cave'),
          Pot(20, 22, PotItem.FiveRupees, '50 Rupee Cave'), Pot(40, 22, PotItem.FiveRupees, '50 Rupee Cave'), Pot(24, 24, PotItem.FiveRupees, '50 Rupee Cave'), Pot(28, 24, PotItem.FiveRupees, '50 Rupee Cave'),
          Pot(32, 24, PotItem.FiveRupees, '50 Rupee Cave'), Pot(36, 24, PotItem.FiveRupees, '50 Rupee Cave')],
    293: [Pot(24, 25, PotItem.FiveRupees, '20 Rupee Cave'), Pot(28, 25, PotItem.FiveRupees, '20 Rupee Cave'), Pot(32, 25, PotItem.FiveRupees, '20 Rupee Cave'), Pot(36, 25, PotItem.FiveRupees, '20 Rupee Cave'),
          Pot(88, 22, PotItem.Heart, 'Dark Lake Hylia Ledge Spike Cave'), Pot(100, 22, PotItem.Heart, 'Dark Lake Hylia Ledge Spike Cave'), Pot(88, 28, PotItem.Heart, 'Dark Lake Hylia Ledge Spike Cave'), Pot(100, 28, PotItem.Heart, 'Dark Lake Hylia Ledge Spike Cave')],
    0x127: [Pot(24, 25, PotItem.Nothing, 'Dark World Hammer Peg Cave'), Pot(28, 25, PotItem.Nothing, 'Dark World Hammer Peg Cave'), Pot(32, 25, PotItem.Nothing, 'Dark World Hammer Peg Cave'), Pot(36, 25, PotItem.Nothing, 'Dark World Hammer Peg Cave')],
}


def shuffle_pots(world, player):
    import RaceRandom as random

    new_pot_contents = PotSecretTable()

    for super_tile in vanilla_pots:
        old_pots = vanilla_pots[super_tile]
        new_pots = [Pot(pot.x, pot.y, PotItem.Nothing, pot.room, pot.flags) for pot in old_pots]
        # sort in the order Hole, Switch, Key, Other, Nothing
        sort_order = {PotItem.Hole: 4, PotItem.Switch: 3, PotItem.Key: 2, PotItem.Nothing: 0}
        old_pots = sorted(old_pots, key=lambda pot: sort_order.get(pot.item, 1), reverse=True)

        for old_pot in old_pots:
            if old_pot.item == PotItem.Nothing:
                break
            elif old_pot.item == PotItem.Hole:
                # Can only go in vanilla position (or the other big rock)
                available_pots = (pot for pot in new_pots if pot.x == old_pot.x and pot.y == old_pot.y)
            elif old_pot.item == PotItem.Switch:
                available_pots = (pot for pot in new_pots if (pot.room == old_pot.room or pot.room in movable_switch_rooms[old_pot.room]) and not (pot.flags & PotFlags.NoSwitch))
            elif old_pot.item == PotItem.Key:
                if world.doorShuffle[player] == 'vanilla' and not world.retro[player] and world.pottery[player] == 'none' and world.logic[player] != 'nologic':
                    available_pots = (pot for pot in new_pots if pot.room not in invalid_key_rooms)
                else:
                    available_pots = new_pots
            else:
                available_pots = new_pots

            available_pots = [pot for pot in available_pots if pot.item == PotItem.Nothing]

            new_pot = random.choice(available_pots)
            new_pot.item = old_pot.item
            if world.retro[player] and new_pot.item == PotItem.FiveArrows:
                new_pot.item = PotItem.FiveRupees

            if new_pot.item == PotItem.Key:
                key = next(location for location in world.get_region(old_pot.room, player).locations if location.name in key_drop_data)
                key.pot = new_pot
                if new_pot.room != old_pot.room:
                    # Move pot key to new room
                    world.get_region(old_pot.room, player).locations.remove(key)
                    world.get_region(new_pot.room, player).locations.append(key)
                    key.parent_region = world.get_region(new_pot.room, player)
            elif new_pot.item == PotItem.Switch and (new_pot.flags & PotFlags.SwitchLogicChange):
                if new_pot.room == 'PoD Basement Ledge':
                    basement = world.get_region(old_pot.room, player)
                    ledge = world.get_region(new_pot.room, player)
                    ledge.locations.append(basement.locations.pop())
                elif new_pot.room == 'Swamp Push Statue':
                    from Rules import set_rule
                    set_rule(world.get_entrance('Swamp Push Statue NE', player), lambda state: state.has('Cane of Somaria', player))
                    world.get_door('Swamp Push Statue NW', player).blocked = True
                elif new_pot.room == 'Thieves Attic Hint':
                    # Rule is created based on barrier
                    world.get_door('Thieves Attic ES', player).barrier(CrystalBarrier.Orange)
                else:
                    raise Exception("Switch location in room %s requires logic change" % new_pot.room)

        new_pot_contents.room_map[super_tile] = new_pots

    world.pot_contents[player] = new_pot_contents


def shuffle_pot_switches(world, player):
    import RaceRandom as random

    for super_tile in vanilla_pots:
        new_pots = world.pot_contents[player].room_map[super_tile]
        # sort in the order Hole, Switch, Key, Other, Nothing
        sort_order = {PotItem.Hole: 4, PotItem.Switch: 3, PotItem.Key: 2, PotItem.Nothing: 0}
        old_pots = sorted(new_pots, key=lambda pot: sort_order.get(pot.item, 1), reverse=True)

        for old_pot in old_pots:
            if old_pot.item != PotItem.Switch:
                break
            else:
                available_pots = [pot for pot in new_pots if (pot.room == old_pot.room or pot.room in movable_switch_rooms[old_pot.room]) and not (pot.flags & PotFlags.NoSwitch)]

            new_pot = random.choice(available_pots)
            new_pot.item, old_pot.item = old_pot.item, new_pot.item
            if world.retro[player] and new_pot.item == PotItem.FiveArrows:
                new_pot.item = PotItem.FiveRupees

            if new_pot.item == PotItem.Switch and (new_pot.flags & PotFlags.SwitchLogicChange):
                if new_pot.room == 'PoD Basement Ledge':
                    basement = world.get_region(old_pot.room, player)
                    ledge = world.get_region(new_pot.room, player)
                    ledge.locations.append(basement.locations.pop())
                elif new_pot.room == 'Swamp Push Statue':
                    from Rules import set_rule
                    set_rule(world.get_entrance('Swamp Push Statue NE', player), lambda state: state.has('Cane of Somaria', player))
                    world.get_door('Swamp Push Statue NW', player).blocked = True
                elif new_pot.room == 'Thieves Attic Hint':
                    # Rule is created based on barrier
                    world.get_door('Thieves Attic ES', player).barrier(CrystalBarrier.Orange)
                else:
                    raise Exception("Switch location in room %s requires logic change" % new_pot.room)
    for location in world.get_locations():
        if location.player == player and location.type == LocationType.Pot and location.pot.item == PotItem.Switch:
            location.real = False
            if location in world.dynamic_locations:
                world.dynamic_locations.remove(location)
            location.parent_region.locations.remove(location)
    world.clear_location_cache()


key_drop_data = {
    'Hyrule Castle - Map Guard Key Drop': ['Drop', (0x09E20C, 0x72, 0), 'dropped in Hyrule Castle', 'Small Key (Escape)'],
    'Hyrule Castle - Boomerang Guard Key Drop': ['Drop', (0x09E204, 0x71, 1), 'dropped in Hyrule Castle', 'Small Key (Escape)'],
    'Hyrule Castle - Key Rat Key Drop': ['Drop', (0x09DB80, 0x21, 0), 'dropped in Hyrule Castle', 'Small Key (Escape)'],
    'Hyrule Castle - Big Key Drop': ['Drop', (0x09E327, 0x80, 2), 'dropped in Hyrule Castle', 'Big Key (Escape)'],
    'Eastern Palace - Dark Square Pot Key': ['Pot', 0xBA, 'in a pot in Eastern Palace', 'Small Key (Eastern Palace)'],
    'Eastern Palace - Dark Eyegore Key Drop': ['Drop', (0x09E4F8, 0x99, 3), 'dropped in Eastern Palace', 'Small Key (Eastern Palace)'],
    'Desert Palace - Desert Tiles 1 Pot Key': ['Pot', 0x63, 'in a pot in Desert Palace', 'Small Key (Desert Palace)'],
    'Desert Palace - Beamos Hall Pot Key': ['Pot', 0x53, 'in a pot in Desert Palace', 'Small Key (Desert Palace)'],
    'Desert Palace - Desert Tiles 2 Pot Key': ['Pot', 0x43, 'in a pot in Desert Palace', 'Small Key (Desert Palace)'],
    'Castle Tower - Dark Archer Key Drop': ['Drop', (0x09E7C9, 0xC0, 3), 'dropped in Castle Tower', 'Small Key (Agahnims Tower)'],
    'Castle Tower - Circle of Pots Key Drop': ['Drop', (0x09E688, 0xB0, 10), 'dropped in Castle Tower', 'Small Key (Agahnims Tower)'],
    'Swamp Palace - Pot Row Pot Key': ['Pot', 0x38, 'in a pot in Swamp Palace', 'Small Key (Swamp Palace)'],
    'Swamp Palace - Trench 1 Pot Key': ['Pot', 0x37, 'in a pot in Swamp Palace', 'Small Key (Swamp Palace)'],
    'Swamp Palace - Hookshot Pot Key': ['Pot', 0x36, 'in a pot in Swamp Palace', 'Small Key (Swamp Palace)'],
    'Swamp Palace - Trench 2 Pot Key': ['Pot', 0x35, 'in a pot in Swamp Palace', 'Small Key (Swamp Palace)'],
    'Swamp Palace - Waterway Pot Key': ['Pot', 0x16, 'in a pot in Swamp Palace', 'Small Key (Swamp Palace)'],
    'Skull Woods - West Lobby Pot Key': ['Pot', 0x56, 'in a pot in Skull Woods', 'Small Key (Skull Woods)'],
    'Skull Woods - Spike Corner Key Drop': ['Drop', (0x09DD74, 0x39, 1), 'dropped near Mothula', 'Small Key (Skull Woods)'],
    "Thieves' Town - Hallway Pot Key": ['Pot', 0xBC, "in a pot in Thieves' Town", 'Small Key (Thieves Town)'],
    "Thieves' Town - Spike Switch Pot Key": ['Pot', 0xAB, "in a pot in Thieves' Town", 'Small Key (Thieves Town)'],
    'Ice Palace - Jelly Key Drop': ['Drop', (0x09DA21, 0xE, 3), 'dropped in Ice Palace', 'Small Key (Ice Palace)'],
    'Ice Palace - Conveyor Key Drop': ['Drop', (0x09DE08, 0x3E, 8), 'dropped in Ice Palace', 'Small Key (Ice Palace)'],
    'Ice Palace - Hammer Block Key Drop': ['Pot', 0x3F, 'under a block in Ice Palace', 'Small Key (Ice Palace)'],
    'Ice Palace - Many Pots Pot Key': ['Pot', 0x9F, 'int a pot in Ice Palace', 'Small Key (Ice Palace)'],
    'Misery Mire - Spikes Pot Key': ['Pot', 0xB3, 'in a pot in Misery Mire', 'Small Key (Misery Mire)'],
    'Misery Mire - Fishbone Pot Key': ['Pot', 0xA1, 'in a pot in forgotten Mire', 'Small Key (Misery Mire)'],
    'Misery Mire - Conveyor Crystal Key Drop': ['Drop', (0x09E7FB, 0xC1, 9), 'dropped in Misery Mire', 'Small Key (Misery Mire)'],
    'Turtle Rock - Pokey 1 Key Drop': ['Drop', (0x09E70D, 0xB6, 5), 'dropped in Turtle Rock', 'Small Key (Turtle Rock)'],
    'Turtle Rock - Pokey 2 Key Drop': ['Drop', (0x09DA5D, 0x13, 6), 'dropped in Turtle Rock', 'Small Key (Turtle Rock)'],
    'Ganons Tower - Conveyor Cross Pot Key': ['Pot', 0x8B, "in a pot in Ganon's Tower", 'Small Key (Ganons Tower)'],
    'Ganons Tower - Double Switch Pot Key': ['Pot', 0x9B, "in a pot in Ganon's Tower", 'Small Key (Ganons Tower)'],
    'Ganons Tower - Conveyor Star Pits Pot Key': ['Pot', 0x7B, "in a pot in Ganon's Tower", 'Small Key (Ganons Tower)'],
    'Ganons Tower - Mini Helmasaur Key Drop': ['Drop', (0x09DDC4, 0x3D, 2), "dropped atop Ganon's Tower", 'Small Key (Ganons Tower)']
}


class PotSecretTable(object):
    def __init__(self):
        self.room_map = defaultdict(list)
        self.multiworld_count = 0

    def write_pot_data_to_rom(self, rom):
        pointer_address = 0x140000  # pots currently in bank 28
        pointer_offset = 0x128 * 2
        empty_address = (pointer_address + pointer_offset)
        empty_pointer = pc_to_snes(empty_address) & 0xFFFF
        data_pointer = pointer_address + pointer_offset + 2
        for room in range(0, 0x128):
            if room in self.room_map:
                list_idx = 0
                data_address = pc_to_snes(data_pointer) & 0xFFFF
                rom.write_bytes(pointer_address + room * 2, int16_as_bytes(data_address))
                for pot in self.room_map[room]:
                    rom.write_bytes(data_pointer + list_idx * 3, pot.pot_data())
                    list_idx += 1
                rom.write_bytes(data_pointer + list_idx * 3, [0xFF, 0xFF])
                data_pointer += 3 * list_idx + 2
            else:
                rom.write_bytes(pointer_address + room * 2, int16_as_bytes(empty_pointer))
        rom.write_bytes(empty_address, [0xFF, 0xFF])

    def size(self):
        size = 0x128 * 2
        for room in range(0, 0x128):
            if room in self.room_map:
                pot_list = [p for p in self.room_map[room]]
                if pot_list:
                    size += len(pot_list) * 3 + 2
        return size
