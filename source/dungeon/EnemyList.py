import math
import typing

try:
    from fast_enum import FastEnum
except ImportError:
    from enum import IntFlag as FastEnum

from source.logic.Rule import RuleFactory


class EnemyStats:
    def __init__(self, sprite, static, drop_flag=False, prize_pack=0, sub_type=0):
        self.sprite = sprite
        self.sub_type = sub_type
        self.static = static
        # self.health = health
        # self.damage = damage
        self.drop_flag = drop_flag
        self.prize_pack = prize_pack


class EnemySprite(FastEnum):
    CorrectPullSwitch = 0x04,
    WrongPullSwitch = 0x06
    Octorok = 0x08
    Moldorm = 0x09
    Cucco = 0x0b

    Octoballoon = 0x0f
    OctoballoonBaby = 0x10
    Hinox = 0x11
    Moblin = 0x12
    MiniHelmasaur = 0x13
    ThievesTownGrate = 0x14
    AntiFairy = 0x15
    Wiseman = 0x16
    Hoarder = 0x17
    MiniMoldorm = 0x18
    Poe = 0x19
    Smithy = 0x1a
    Arrow = 0x1b
    Statue = 0x1c
    FluteQuest = 0x1d    
    CrystalSwitch = 0x1e
    SickKid = 0x1f
    Sluggula = 0x20
    WaterSwitch = 0x21
    Ropa = 0x22
    RedBari = 0x23
    BlueBari = 0x24
    TalkingTree = 0x25
    HardhatBeetle = 0x26
    Deadrock = 0x27
    DarkWorldHintNpc = 0x28
    AdultNpc = 0x29
    SweepingLady = 0x2a
    Hobo = 0x2b
    Lumberjacks = 0x2c
    TelepathicTile = 0x2d
    FluteKid = 0x2e
    RaceGameLady = 0x2f

    FortuneTeller = 0x31
    ArgueBros = 0x32
    RupeePull = 0x33
    YoungSnitch = 0x34
    Innkeeper = 0x35
    Witch = 0x36
    Waterfall = 0x37
    EyeStatue = 0x38
    Locksmith = 0x39
    MagicBat = 0x3a
    BonkItem = 0x3b
    KidInKak = 0x3c
    OldSnitch = 0x3d
    Hoarder2 = 0x3e
    TutorialGuard = 0x3f
    
    LightningGate = 0x40
    BlueGuard = 0x41
    GreenGuard = 0x42
    RedSpearGuard = 0x43
    BluesainBolt = 0x44
    UsainBolt = 0x45
    BlueArcher = 0x46
    GreenBushGuard = 0x47
    RedJavelinGuard = 0x48
    RedBushGuard = 0x49    
    BombGuard = 0x4a
    GreenKnifeGuard = 0x4b
    Geldman = 0x4c
    Popo = 0x4e
    Popo2 = 0x4f
    
    ArmosKnight = 0x53
    Lanmolas = 0x54
    Zora = 0x56
    DesertStatue = 0x57
    Crab = 0x58
    LostWoodsBird = 0x59
    LostWoodsSquirrel =0x5a
    SparkCW = 0x5b
    SparkCCW = 0x5c
    RollerVerticalUp = 0x5d
    RollerVerticalDown = 0x5e
    RollerHorizontalLeft = 0x5f
    RollerHorizontalRight = 0x60
    Beamos = 0x61
    MasterSword = 0x62
    DebirandoPit = 0x63
    Debirando = 0x64
    ArcheryNpc = 0x65
    WallCannonVertLeft = 0x66
    WallCannonVertRight = 0x67
    WallCannonHorzTop = 0x68
    WallCannonHorzBottom = 0x69    
    BallNChain = 0x6a
    CannonTrooper = 0x6b
    CricketRat = 0x6d
    Snake = 0x6e
    Keese = 0x6f
    
    Leever = 0x71
    FairyPondTrigger = 0x72
    UnclePriest = 0x73
    RunningNpc = 0x74
    BottleMerchant = 0x75
    Zelda = 0x76
    Grandma = 0x78
    Agahnim = 0x7a
    FloatingSkull = 0x7c
    BigSpike = 0x7d
    FirebarCW = 0x7e
    FirebarCCW = 0x7f
    Firesnake = 0x80
    Hover = 0x81
    AntiFairyCircle = 0x82
    GreenEyegoreMimic = 0x83
    RedEyegoreMimic = 0x84
    YellowStalfos = 0x85  # falling stalfos that shoots head
    Kondongo = 0x86
    Mothula = 0x88
    SpikeBlock = 0x8a
    Gibdo = 0x8b
    Arrghus = 0x8c
    Arrghi = 0x8d
    Terrorpin = 0x8e 
    Blob = 0x8f    
    Wallmaster = 0x90
    StalfosKnight = 0x91
    HelmasaurKing = 0x92
    Bumper = 0x93
    Pirogusu = 0x94
    LaserEyeLeft = 0x95
    LaserEyeRight = 0x96
    LaserEyeTop = 0x97
    LaserEyeBottom = 0x98
    Pengator = 0x99
    Kyameron = 0x9a
    Wizzrobe = 0x9b
    Zoro = 0x9c
    Babasu = 0x9d
    GroveOstritch = 0x9e
    GroveRabbit = 0x9f
    GroveBird = 0xa0    
    Freezor = 0xa1
    Kholdstare = 0xa2
    KholdstareShell = 0xa3
    FallingIce = 0xa4
    BlueZazak = 0xa5
    RedZazak = 0xa6
    Stalfos = 0xa7
    # ... OW
    OldMan = 0xad
    PipeDown = 0xae
    PipeUp = 0xaf
    PipeRight = 0xb0
    PipeLeft = 0xb1
    GoodBee = 0xb2
    PedestalPlaque = 0xb3
    BombShopGuy = 0xb5
    BlindMaiden = 0xb7
    
    Whirlpool = 0xba
    Shopkeeper = 0xbb
    Drunkard = 0xbc
    Vitreous = 0xbd   
    # ... (spawnables)
    Catfish = 0xc0
    CutsceneAgahnim = 0xc1
    Boulder = 0xc2
    Gibo = 0xc3  # patrick!
    Thief = 0xc4
    Medusa = 0xc5
    FourWayShooter = 0xc6
    Pokey = 0xc7
    BigFairy = 0xc8
    Tektite = 0xc9  # firebat?
    Chainchomp = 0xca
    TrinexxRockHead = 0xcb
    TrinexxFireHead = 0xcc
    TrinexxIceHead = 0xcd
    Blind = 0xce
    Swamola = 0xcf    
    Lynel = 0xd0
    BunnyBeam = 0xd1
    FloppingFish = 0xd2
    Stal = 0xd3
    Ganon = 0xd6

    Faerie = 0xe3
    SmallKey = 0xe4
    MagicShopAssistant = 0xe9
    HeartPiece = 0xeb
    CastleMantle = 0xee
    
    
class SpriteType(FastEnum):
    Normal = 0x00
    Overlord = 0x07


def init_enemy_stats():
    enemy_stats = {
        EnemySprite.CorrectPullSwitch: EnemyStats(EnemySprite.CorrectPullSwitch, True),
        EnemySprite.WrongPullSwitch: EnemyStats(EnemySprite.WrongPullSwitch, True),
        EnemySprite.Octorok: EnemyStats(EnemySprite.Octorok, False, True, 2),
        EnemySprite.Moldorm: EnemyStats(EnemySprite.Moldorm, True, False),
        EnemySprite.Cucco: EnemyStats(EnemySprite.Cucco, False, False),

        EnemySprite.Octoballoon: EnemyStats(EnemySprite.Octoballoon, False, False, 0),
        EnemySprite.OctoballoonBaby: EnemyStats(EnemySprite.OctoballoonBaby, False),
        EnemySprite.Hinox: EnemyStats(EnemySprite.Hinox, False, True, 4),
        EnemySprite.Moblin: EnemyStats(EnemySprite.Moblin, False, True, 1),
        EnemySprite.MiniHelmasaur: EnemyStats(EnemySprite.MiniHelmasaur, False, True, 7),
        EnemySprite.ThievesTownGrate: EnemyStats(EnemySprite.ThievesTownGrate, True),
        EnemySprite.AntiFairy: EnemyStats(EnemySprite.AntiFairy, False, False),
        EnemySprite.Wiseman: EnemyStats(EnemySprite.Wiseman, True),
        EnemySprite.Hoarder: EnemyStats(EnemySprite.Hoarder, False, False),
        EnemySprite.MiniMoldorm: EnemyStats(EnemySprite.MiniMoldorm, False, True, 2),
        EnemySprite.Poe: EnemyStats(EnemySprite.Poe, False, True, 6),
        EnemySprite.Smithy: EnemyStats(EnemySprite.Smithy, True),
        EnemySprite.Arrow: EnemyStats(EnemySprite.Arrow, True),
        EnemySprite.Statue: EnemyStats(EnemySprite.Statue, True),
        EnemySprite.FluteQuest: EnemyStats(EnemySprite.FluteQuest, True),
        EnemySprite.CrystalSwitch: EnemyStats(EnemySprite.CrystalSwitch, True),
        EnemySprite.SickKid: EnemyStats(EnemySprite.SickKid, True),
        EnemySprite.Sluggula: EnemyStats(EnemySprite.Sluggula, False, True, 4),
        EnemySprite.WaterSwitch: EnemyStats(EnemySprite.WaterSwitch, True),
        EnemySprite.Ropa: EnemyStats(EnemySprite.Ropa, False, True, 2),
        EnemySprite.RedBari: EnemyStats(EnemySprite.RedBari, False, True, 6, 2),
        EnemySprite.BlueBari: EnemyStats(EnemySprite.BlueBari, False, True, 6, 2),
        EnemySprite.TalkingTree: EnemyStats(EnemySprite.TalkingTree, True),
        EnemySprite.HardhatBeetle: EnemyStats(EnemySprite.HardhatBeetle, False, True, (2, 6)),
        EnemySprite.Deadrock: EnemyStats(EnemySprite.Deadrock, False, False),
        EnemySprite.DarkWorldHintNpc: EnemyStats(EnemySprite.DarkWorldHintNpc, True),
        EnemySprite.AdultNpc: EnemyStats(EnemySprite.AdultNpc, True),
        EnemySprite.SweepingLady: EnemyStats(EnemySprite.SweepingLady, True),
        EnemySprite.Hobo: EnemyStats(EnemySprite.Hobo, True),
        EnemySprite.Lumberjacks: EnemyStats(EnemySprite.Lumberjacks, True),
        EnemySprite.TelepathicTile: EnemyStats(EnemySprite.TelepathicTile, True),
        EnemySprite.FluteKid: EnemyStats(EnemySprite.FluteKid, True),
        EnemySprite.RaceGameLady: EnemyStats(EnemySprite.RaceGameLady, True),

        EnemySprite.FortuneTeller: EnemyStats(EnemySprite.FortuneTeller, True),
        EnemySprite.ArgueBros: EnemyStats(EnemySprite.ArgueBros, True),
        EnemySprite.RupeePull: EnemyStats(EnemySprite.RupeePull, True),
        EnemySprite.YoungSnitch: EnemyStats(EnemySprite.YoungSnitch, True),
        EnemySprite.Innkeeper: EnemyStats(EnemySprite.Innkeeper, True),
        EnemySprite.Witch: EnemyStats(EnemySprite.Witch, True),
        EnemySprite.Waterfall: EnemyStats(EnemySprite.Waterfall, True),
        EnemySprite.EyeStatue: EnemyStats(EnemySprite.EyeStatue, True),
        EnemySprite.Locksmith: EnemyStats(EnemySprite.Locksmith, True),
        EnemySprite.MagicBat: EnemyStats(EnemySprite.MagicBat, True),
        EnemySprite.BonkItem: EnemyStats(EnemySprite.BonkItem, True),
        EnemySprite.KidInKak: EnemyStats(EnemySprite.KidInKak, True),
        EnemySprite.OldSnitch: EnemyStats(EnemySprite.OldSnitch, True),
        EnemySprite.Hoarder2: EnemyStats(EnemySprite.Hoarder2, False, False),
        EnemySprite.TutorialGuard: EnemyStats(EnemySprite.TutorialGuard, True),

        EnemySprite.LightningGate: EnemyStats(EnemySprite.LightningGate, True),
        EnemySprite.BlueGuard: EnemyStats(EnemySprite.BlueGuard, False, True, 1),
        EnemySprite.GreenGuard: EnemyStats(EnemySprite.GreenGuard, False, True, 1),
        EnemySprite.RedSpearGuard: EnemyStats(EnemySprite.RedSpearGuard, False, True, 1),
        EnemySprite.BluesainBolt: EnemyStats(EnemySprite.BluesainBolt, False, True, 7),
        EnemySprite.UsainBolt: EnemyStats(EnemySprite.UsainBolt, False, True, 1),
        EnemySprite.BlueArcher: EnemyStats(EnemySprite.BlueArcher, False, True, 5),
        EnemySprite.GreenBushGuard: EnemyStats(EnemySprite.GreenBushGuard, False, True, 5),
        EnemySprite.RedJavelinGuard: EnemyStats(EnemySprite.RedJavelinGuard, False, True, 3),
        EnemySprite.RedBushGuard: EnemyStats(EnemySprite.RedBushGuard, False, True, 7),
        EnemySprite.BombGuard: EnemyStats(EnemySprite.BombGuard, False, True, 4),
        EnemySprite.GreenKnifeGuard: EnemyStats(EnemySprite.GreenKnifeGuard, False, True, 1),
        EnemySprite.Geldman: EnemyStats(EnemySprite.Geldman, False, True, 2),
        EnemySprite.Popo: EnemyStats(EnemySprite.Popo, False, True, 2),
        EnemySprite.Popo2: EnemyStats(EnemySprite.Popo2, False, True, 2),

        EnemySprite.ArmosKnight: EnemyStats(EnemySprite.ArmosKnight, True, False),
        EnemySprite.Lanmolas: EnemyStats(EnemySprite.Lanmolas, True, False),
        EnemySprite.Zora: EnemyStats(EnemySprite.Zora, False, True, 4),
        EnemySprite.DesertStatue: EnemyStats(EnemySprite.DesertStatue, True),
        EnemySprite.Crab: EnemyStats(EnemySprite.Crab, False, True, 1),
        EnemySprite.LostWoodsBird: EnemyStats(EnemySprite.LostWoodsBird, True),
        EnemySprite.LostWoodsSquirrel: EnemyStats(EnemySprite.LostWoodsSquirrel, True),
        EnemySprite.SparkCW: EnemyStats(EnemySprite.SparkCW, False, False),
        EnemySprite.SparkCCW: EnemyStats(EnemySprite.SparkCCW, False, False),
        EnemySprite.RollerVerticalUp: EnemyStats(EnemySprite.RollerVerticalUp, False, False),
        EnemySprite.RollerVerticalDown: EnemyStats(EnemySprite.RollerVerticalDown, False, False),
        EnemySprite.RollerHorizontalLeft: EnemyStats(EnemySprite.RollerHorizontalLeft, False, False),
        EnemySprite.RollerHorizontalRight: EnemyStats(EnemySprite.RollerHorizontalRight, False, False),
        EnemySprite.Beamos: EnemyStats(EnemySprite.Beamos, False, False),
        EnemySprite.MasterSword: EnemyStats(EnemySprite.MasterSword, True),
        EnemySprite.DebirandoPit: EnemyStats(EnemySprite.DebirandoPit, False, True, 2),
        EnemySprite.Debirando: EnemyStats(EnemySprite.Debirando, False, True, 2),
        EnemySprite.ArcheryNpc: EnemyStats(EnemySprite.ArcheryNpc, True),
        EnemySprite.WallCannonVertLeft: EnemyStats(EnemySprite.WallCannonVertLeft, True),
        EnemySprite.WallCannonVertRight: EnemyStats(EnemySprite.WallCannonVertRight, True),
        EnemySprite.WallCannonHorzTop: EnemyStats(EnemySprite.WallCannonHorzTop, True),
        EnemySprite.WallCannonHorzBottom: EnemyStats(EnemySprite.WallCannonHorzBottom, True),
        EnemySprite.BallNChain: EnemyStats(EnemySprite.BallNChain, False, True, 2),
        EnemySprite.CannonTrooper: EnemyStats(EnemySprite.CannonTrooper, False, True, 1),
        EnemySprite.CricketRat: EnemyStats(EnemySprite.CricketRat, False, True, 2),
        EnemySprite.Snake: EnemyStats(EnemySprite.Snake, False, True, (1, 7)),
        EnemySprite.Keese: EnemyStats(EnemySprite.Keese, False, True, (0, 7)),

        EnemySprite.Leever: EnemyStats(EnemySprite.Leever, False, True, 1),
        EnemySprite.FairyPondTrigger: EnemyStats(EnemySprite.FairyPondTrigger, True),
        EnemySprite.UnclePriest: EnemyStats(EnemySprite.UnclePriest, True),
        EnemySprite.RunningNpc: EnemyStats(EnemySprite.RunningNpc, True),
        EnemySprite.BottleMerchant: EnemyStats(EnemySprite.BottleMerchant, True),
        EnemySprite.Zelda: EnemyStats(EnemySprite.Zelda, True),
        EnemySprite.Grandma: EnemyStats(EnemySprite.Grandma, True),
        EnemySprite.Agahnim: EnemyStats(EnemySprite.Agahnim, True),
        EnemySprite.FloatingSkull: EnemyStats(EnemySprite.FloatingSkull, False, True, 7),
        EnemySprite.BigSpike: EnemyStats(EnemySprite.BigSpike, False, False),
        EnemySprite.FirebarCW: EnemyStats(EnemySprite.FirebarCW, False, False),
        EnemySprite.FirebarCCW: EnemyStats(EnemySprite.FirebarCCW, False, False),
        EnemySprite.Firesnake: EnemyStats(EnemySprite.Firesnake, False, False),
        EnemySprite.Hover: EnemyStats(EnemySprite.Hover, False, True, 2),
        EnemySprite.AntiFairyCircle: EnemyStats(EnemySprite.AntiFairyCircle, False, False),
        EnemySprite.GreenEyegoreMimic: EnemyStats(EnemySprite.GreenEyegoreMimic, False, True, 5),
        EnemySprite.RedEyegoreMimic: EnemyStats(EnemySprite.RedEyegoreMimic, False, True, 5),
        EnemySprite.YellowStalfos: EnemyStats(EnemySprite.YellowStalfos, True),
        EnemySprite.Kondongo: EnemyStats(EnemySprite.Kondongo, False, True, 6),
        EnemySprite.Mothula: EnemyStats(EnemySprite.Mothula, True),
        EnemySprite.SpikeBlock: EnemyStats(EnemySprite.SpikeBlock, False, False),
        EnemySprite.Gibdo: EnemyStats(EnemySprite.Gibdo, False, True, 3),
        EnemySprite.Arrghus: EnemyStats(EnemySprite.Arrghus, True),
        EnemySprite.Arrghi: EnemyStats(EnemySprite.Arrghi, True),
        EnemySprite.Terrorpin: EnemyStats(EnemySprite.Terrorpin, False, True, 2),
        EnemySprite.Blob: EnemyStats(EnemySprite.Blob, False, True, 1),
        EnemySprite.Wallmaster: EnemyStats(EnemySprite.Wallmaster, True),
        EnemySprite.StalfosKnight: EnemyStats(EnemySprite.StalfosKnight, False, True, 4),
        EnemySprite.HelmasaurKing: EnemyStats(EnemySprite.HelmasaurKing, True),
        EnemySprite.Bumper: EnemyStats(EnemySprite.Bumper, True),
        EnemySprite.Pirogusu: EnemyStats(EnemySprite.Pirogusu, True),
        EnemySprite.LaserEyeLeft: EnemyStats(EnemySprite.LaserEyeLeft, True),
        EnemySprite.LaserEyeRight: EnemyStats(EnemySprite.LaserEyeRight, True),
        EnemySprite.LaserEyeTop: EnemyStats(EnemySprite.LaserEyeTop, True),
        EnemySprite.LaserEyeBottom: EnemyStats(EnemySprite.LaserEyeBottom, True),
        EnemySprite.Pengator: EnemyStats(EnemySprite.Pengator, False, True, 3),
        EnemySprite.Kyameron: EnemyStats(EnemySprite.Kyameron, False, False),
        EnemySprite.Wizzrobe: EnemyStats(EnemySprite.Wizzrobe, False, True, 1),
        EnemySprite.Zoro: EnemyStats(EnemySprite.Zoro, True),
        EnemySprite.Babasu: EnemyStats(EnemySprite.Babasu, False, True, 0),
        EnemySprite.GroveOstritch: EnemyStats(EnemySprite.GroveOstritch, True),
        EnemySprite.GroveRabbit: EnemyStats(EnemySprite.GroveRabbit, True),
        EnemySprite.GroveBird: EnemyStats(EnemySprite.GroveBird, True),
        EnemySprite.Freezor: EnemyStats(EnemySprite.Freezor, True, True, 0),
        EnemySprite.Kholdstare: EnemyStats(EnemySprite.Kholdstare, True),
        EnemySprite.KholdstareShell: EnemyStats(EnemySprite.KholdstareShell, True),
        EnemySprite.FallingIce: EnemyStats(EnemySprite.FallingIce, True),
        EnemySprite.BlueZazak: EnemyStats(EnemySprite.BlueZazak, False, True, 6),
        EnemySprite.RedZazak: EnemyStats(EnemySprite.RedZazak, False, True, 6),
        EnemySprite.Stalfos: EnemyStats(EnemySprite.Stalfos, False, True, 6),
    # ... OW
        EnemySprite.OldMan: EnemyStats(EnemySprite.OldMan, True),
        EnemySprite.PipeDown: EnemyStats(EnemySprite.PipeDown, True),
        EnemySprite.PipeUp: EnemyStats(EnemySprite.PipeUp, True),
        EnemySprite.PipeRight: EnemyStats(EnemySprite.PipeRight, True),
        EnemySprite.PipeLeft: EnemyStats(EnemySprite.PipeLeft, True),
        EnemySprite.GoodBee: EnemyStats(EnemySprite.GoodBee, True),
        EnemySprite.PedestalPlaque: EnemyStats(EnemySprite.PedestalPlaque, True),
        EnemySprite.BombShopGuy: EnemyStats(EnemySprite.BombShopGuy, True),
        EnemySprite.BlindMaiden: EnemyStats(EnemySprite.BlindMaiden, True),

        EnemySprite.Whirlpool: EnemyStats(EnemySprite.Whirlpool, True),
        EnemySprite.Shopkeeper: EnemyStats(EnemySprite.Shopkeeper, True),
        EnemySprite.Drunkard: EnemyStats(EnemySprite.Drunkard, True),
        EnemySprite.Vitreous: EnemyStats(EnemySprite.Vitreous, True),
        EnemySprite.Catfish: EnemyStats(EnemySprite.Catfish, True),
        EnemySprite.CutsceneAgahnim: EnemyStats(EnemySprite.CutsceneAgahnim, True),
        EnemySprite.Boulder: EnemyStats(EnemySprite.Boulder, True),
        EnemySprite.Gibo: EnemyStats(EnemySprite.Gibo, False, True, 0),  # patrick!
        EnemySprite.Thief: EnemyStats(EnemySprite.Thief, False, False),  # could drop if killable thieves is on
        EnemySprite.Medusa: EnemyStats(EnemySprite.Medusa, True),
        EnemySprite.FourWayShooter: EnemyStats(EnemySprite.FourWayShooter, True),
        EnemySprite.Pokey: EnemyStats(EnemySprite.Pokey, False, True, 7),
        EnemySprite.BigFairy: EnemyStats(EnemySprite.BigFairy, True),
        EnemySprite.Tektite: EnemyStats(EnemySprite.Tektite, False, True, 2),
        EnemySprite.Chainchomp: EnemyStats(EnemySprite.Chainchomp, False, False),
        EnemySprite.TrinexxRockHead: EnemyStats(EnemySprite.TrinexxRockHead, True),
        EnemySprite.TrinexxFireHead: EnemyStats(EnemySprite.TrinexxFireHead, True),
        EnemySprite.TrinexxIceHead: EnemyStats(EnemySprite.TrinexxIceHead, True),
        EnemySprite.Blind: EnemyStats(EnemySprite.Blind, True),
        EnemySprite.Swamola: EnemyStats(EnemySprite.Swamola, False, True, 0),
        EnemySprite.Lynel: EnemyStats(EnemySprite.Lynel, False, True, 7),
        EnemySprite.BunnyBeam: EnemyStats(EnemySprite.BunnyBeam, False, False),  # todo: medallions can kill bunny beams?
        EnemySprite.FloppingFish: EnemyStats(EnemySprite.FloppingFish, True),
        EnemySprite.Stal: EnemyStats(EnemySprite.Stal, False, True, 1),
        EnemySprite.Ganon: EnemyStats(EnemySprite.Ganon, True),

        EnemySprite.Faerie: EnemyStats(EnemySprite.Faerie, True),
        EnemySprite.SmallKey: EnemyStats(EnemySprite.SmallKey, True),
        EnemySprite.MagicShopAssistant: EnemyStats(EnemySprite.MagicShopAssistant, True),
        EnemySprite.HeartPiece: EnemyStats(EnemySprite.HeartPiece, True),
        EnemySprite.CastleMantle: EnemyStats(EnemySprite.CastleMantle, True),

    }


class Sprite(object):
    def __init__(self, super_tile, kind, sub_type, layer, tile_x, tile_y,
                 region=None, drops_item=False, drop_item_kind=None):
        self.super_tile = super_tile
        self.kind = kind
        self.sub_type = sub_type
        self.layer = layer
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.region = region
        self.drops_item = drops_item
        self.drop_item_kind = drop_item_kind


# map of super_tile to list of Sprite objects:
vanilla_sprites = {}


def create_sprite(super_tile, kind, sub_type, layer, tile_x, tile_y, region=None, drops_item=False, drop_item_kind=None):
    if super_tile not in vanilla_sprites:
        vanilla_sprites[super_tile] = []
    vanilla_sprites[super_tile].append(Sprite(kind, sub_type, layer, tile_x, tile_y,
                                              region, drops_item, drop_item_kind))


def init_vanilla_sprites():
    create_sprite(0x0000, EnemySprite.Ganon, 0x00, 0, 0x17, 0x05, 'Pyramid')
    create_sprite(0x0002, EnemySprite.CricketRat, 0x00, 1, 0x12, 0x05, 'Sewers Yet More Rats')
    create_sprite(0x0002, EnemySprite.CricketRat, 0x00, 1, 0x15, 0x06, 'Sewers Yet More Rats')
    create_sprite(0x0002, EnemySprite.CricketRat, 0x00, 1, 0x0f, 0x08, 'Sewers Yet More Rats')
    create_sprite(0x0002, EnemySprite.CricketRat, 0x00, 1, 0x10, 0x08, 'Sewers Yet More Rats')
    create_sprite(0x0002, EnemySprite.CricketRat, 0x00, 1, 0x18, 0x09, 'Sewers Yet More Rats')
    create_sprite(0x0002, 0x06, SpriteType.Overlord, 1, 0x0f, 0x17)
    create_sprite(0x0002, 0x06, SpriteType.Overlord, 1, 0x09, 0x18)
    create_sprite(0x0002, 0x06, SpriteType.Overlord, 1, 0x0b, 0x18)
    create_sprite(0x0002, 0x06, SpriteType.Overlord, 1, 0x0a, 0x19)
    create_sprite(0x0002, 0x06, SpriteType.Overlord, 1, 0x0c, 0x19)
    create_sprite(0x0002, 0x06, SpriteType.Overlord, 1, 0x09, 0x1a)
    create_sprite(0x0002, 0x06, SpriteType.Overlord, 1, 0x0b, 0x1b)
    create_sprite(0x0002, EnemySprite.WrongPullSwitch, 0x00, 1, 0x0a, 0x17)
    create_sprite(0x0002, EnemySprite.CorrectPullSwitch, 0x00, 1, 0x15, 0x17)
    create_sprite(0x0002, EnemySprite.CricketRat, 0x00, 1, 0x0d, 0x1a, 'Sewers Pull Switch')
    create_sprite(0x0002, EnemySprite.CricketRat, 0x00, 1, 0x12, 0x1a, 'Sewers Pull Switch')
    create_sprite(0x0004, EnemySprite.CrystalSwitch, 0x00, 0, 0x09, 0x04)
    create_sprite(0x0004, EnemySprite.RollerVerticalUp, 0x00, 0, 0x14, 0x04, 'TR Rupees')
    create_sprite(0x0004, EnemySprite.RollerHorizontalRight, 0x00, 0, 0x1b, 0x04, 'TR Rupees')
    create_sprite(0x0004, EnemySprite.RollerHorizontalLeft, 0x00, 0, 0x05, 0x07, 'TR Crystaroller Middle')
    create_sprite(0x0004, EnemySprite.RollerHorizontalLeft, 0x00, 0, 0x15, 0x09, 'TR Rupees')
    create_sprite(0x0004, 0x16, SpriteType.Overlord, 0, 0x07, 0x12)
    create_sprite(0x0004, EnemySprite.CorrectPullSwitch, 0x00, 0, 0x15, 0x15)
    create_sprite(0x0004, EnemySprite.WrongPullSwitch, 0x00, 0, 0x1a, 0x15)
    create_sprite(0x0004, 0x1a, SpriteType.Overlord, 0, 0x18, 0x15)
    create_sprite(0x0004, EnemySprite.Blob, 0x00, 0, 0x1c, 0x15, 'TR Tongue Pull')
    create_sprite(0x0004, 0x1a, SpriteType.Overlord, 0, 0x16, 0x17)
    create_sprite(0x0004, 0x1a, SpriteType.Overlord, 0, 0x1a, 0x17)
    create_sprite(0x0004, 0x1a, SpriteType.Overlord, 0, 0x18, 0x18)
    create_sprite(0x0004, EnemySprite.Blob, 0x00, 0, 0x1a, 0x1a, 'TR Tongue Pull')
    create_sprite(0x0004, EnemySprite.Blob, 0x00, 0, 0x15, 0x1b, 'TR Tongue Pull')
    create_sprite(0x0004, EnemySprite.Pokey, 0x00, 0, 0x07, 0x18, 'TR Dash Room')
    create_sprite(0x0006, EnemySprite.Arrghus, 0x00, 0, 0x07, 0x17)
    create_sprite(0x0006, EnemySprite.Arrghi, 0x00, 0, 0x07, 0x17)
    create_sprite(0x0006, EnemySprite.Arrghi, 0x00, 0, 0x07, 0x17)
    create_sprite(0x0006, EnemySprite.Arrghi, 0x00, 0, 0x07, 0x17)
    create_sprite(0x0006, EnemySprite.Arrghi, 0x00, 0, 0x07, 0x17)
    create_sprite(0x0006, EnemySprite.Arrghi, 0x00, 0, 0x07, 0x17)
    create_sprite(0x0006, EnemySprite.Arrghi, 0x00, 0, 0x07, 0x17)
    create_sprite(0x0006, EnemySprite.Arrghi, 0x00, 0, 0x07, 0x17)
    create_sprite(0x0006, EnemySprite.Arrghi, 0x00, 0, 0x07, 0x17)
    create_sprite(0x0006, EnemySprite.Arrghi, 0x00, 0, 0x07, 0x17)
    create_sprite(0x0006, EnemySprite.Arrghi, 0x00, 0, 0x07, 0x17)
    create_sprite(0x0006, EnemySprite.Arrghi, 0x00, 0, 0x07, 0x17)
    create_sprite(0x0006, EnemySprite.Arrghi, 0x00, 0, 0x07, 0x17)
    create_sprite(0x0006, EnemySprite.Arrghi, 0x00, 0, 0x07, 0x17)
    create_sprite(0x0007, EnemySprite.Moldorm, 0x00, 0, 0x12, 0x0e)
    create_sprite(0x0008, EnemySprite.BigFairy, 0x00, 0, 0x07, 0x16)
    create_sprite(0x0009, EnemySprite.Medusa, 0x00, 0, 0x07, 0x08)
    create_sprite(0x0009, EnemySprite.Medusa, 0x00, 0, 0x08, 0x08)
    create_sprite(0x0009, EnemySprite.AntiFairy, 0x00, 0, 0x17, 0x0b, 'PoD Warp Room')
    create_sprite(0x000a, EnemySprite.Terrorpin, 0x00, 0, 0x17, 0x08, 'PoD Stalfos Basement')
    create_sprite(0x000a, EnemySprite.Terrorpin, 0x00, 0, 0x17, 0x09, 'PoD Stalfos Basement')
    create_sprite(0x000a, 0x05, SpriteType.Overlord, 0, 0x0d, 0x09)
    create_sprite(0x000a, 0x05, SpriteType.Overlord, 0, 0x11, 0x09)
    create_sprite(0x000a, 0x17, SpriteType.Overlord, 0, 0x13, 0x0b)
    create_sprite(0x000a, 0x05, SpriteType.Overlord, 0, 0x0d, 0x0e)
    create_sprite(0x000a, 0x05, SpriteType.Overlord, 0, 0x11, 0x0e)
    create_sprite(0x000b, EnemySprite.CrystalSwitch, 0x00, 0, 0x1c, 0x04)
    create_sprite(0x000b, EnemySprite.Terrorpin, 0x00, 0, 0x07, 0x08, 'PoD Lonely Turtle')
    create_sprite(0x000b, EnemySprite.Terrorpin, 0x00, 0, 0x16, 0x0b, 'PoD Dark Pegs Middle')
    create_sprite(0x000b, EnemySprite.Terrorpin, 0x00, 0, 0x1b, 0x0b, 'PoD Dark Pegs Right')
    create_sprite(0x000b, EnemySprite.Terrorpin, 0x00, 0, 0x05, 0x16, 'PoD Turtle Party')
    create_sprite(0x000b, EnemySprite.Terrorpin, 0x00, 0, 0x0a, 0x16, 'PoD Turtle Party')
    create_sprite(0x000b, EnemySprite.Terrorpin, 0x00, 0, 0x07, 0x19, 'PoD Turtle Party')
    create_sprite(0x000b, EnemySprite.Terrorpin, 0x00, 0, 0x08, 0x19, 'PoD Turtle Party')
    create_sprite(0x000b, EnemySprite.Terrorpin, 0x00, 0, 0x06, 0x1b, 'PoD Turtle Party')
    create_sprite(0x000b, EnemySprite.Terrorpin, 0x00, 0, 0x09, 0x1b, 'PoD Turtle Party')
    create_sprite(0x000d, EnemySprite.Agahnim, 0x00, 0, 0x07, 0x15)
    create_sprite(0x000e, EnemySprite.Freezor, 0x00, 0, 0x16, 0x12, 'Ice Lobby')
    create_sprite(0x000e, EnemySprite.BlueBari, 0x00, 0, 0x05, 0x16, 'Ice Jelly Key')
    create_sprite(0x000e, EnemySprite.BlueBari, 0x00, 0, 0x05, 0x18, 'Ice Jelly Key')
    create_sprite(0x000e, EnemySprite.BlueBari, 0x00, 0, 0x05, 0x1a, 'Ice Jelly Key', True, 0xe4)
    create_sprite(0x0011, EnemySprite.CricketRat, 0x00, 0, 0x17, 0x0a, 'Sewers Rat Path')
    create_sprite(0x0011, EnemySprite.CricketRat, 0x00, 0, 0x18, 0x0a, 'Sewers Rat Path')
    create_sprite(0x0011, EnemySprite.Keese, 0x00, 0, 0x17, 0x0c, 'Sewers Rat Path')
    create_sprite(0x0011, EnemySprite.Keese, 0x00, 0, 0x18, 0x0c, 'Sewers Rat Path')
    create_sprite(0x0011, EnemySprite.CricketRat, 0x00, 0, 0x1c, 0x11, 'Sewers Rat Path')
    create_sprite(0x0011, EnemySprite.CricketRat, 0x00, 0, 0x1c, 0x12, 'Sewers Rat Path')
    create_sprite(0x0011, EnemySprite.CricketRat, 0x00, 0, 0x1a, 0x16, 'Sewers Rat Path')
    create_sprite(0x0011, EnemySprite.CricketRat, 0x00, 0, 0x1b, 0x16, 'Sewers Rat Path')
    create_sprite(0x0012, EnemySprite.UnclePriest, 0x00, 0, 0x0f, 0x07)
    create_sprite(0x0012, EnemySprite.Zelda, 0x00, 0, 0x10, 0x06)
    create_sprite(0x0013, EnemySprite.CrystalSwitch, 0x00, 0, 0x14, 0x11)
    create_sprite(0x0013, EnemySprite.AntiFairy, 0x00, 0, 0x18, 0x04, 'TR Pokey 2 Top')
    create_sprite(0x0013, EnemySprite.AntiFairy, 0x00, 0, 0x1a, 0x04, 'TR Pokey 2 Top')
    create_sprite(0x0013, EnemySprite.AntiFairy, 0x00, 0, 0x18, 0x05, 'TR Pokey 2 Top')
    create_sprite(0x0013, EnemySprite.AntiFairy, 0x00, 0, 0x1a, 0x05, 'TR Pokey 2 Top')
    create_sprite(0x0013, EnemySprite.FloatingSkull, 0x00, 0, 0x1b, 0x16, 'TR Pokey 2 Bottom')
    create_sprite(0x0013, EnemySprite.Pokey, 0x00, 0, 0x16, 0x18, 'TR Pokey 2 Bottom', True, 0xe4)
    create_sprite(0x0013, EnemySprite.LaserEyeRight, 0x00, 0, 0x1e, 0x18)
    create_sprite(0x0013, EnemySprite.FloatingSkull, 0x00, 0, 0x14, 0x1a, 'TR Pokey 2 Bottom')
    create_sprite(0x0013, EnemySprite.BunnyBeam, 0x00, 0, 0x1b, 0x1b)
    create_sprite(0x0014, EnemySprite.PipeRight, 0x00, 1, 0x0c, 0x04)
    create_sprite(0x0014, EnemySprite.PipeUp, 0x00, 1, 0x0f, 0x0a)
    create_sprite(0x0014, EnemySprite.PipeDown, 0x00, 1, 0x19, 0x0a)
    create_sprite(0x0014, EnemySprite.PipeDown, 0x00, 1, 0x03, 0x0d)
    create_sprite(0x0014, EnemySprite.PipeDown, 0x00, 1, 0x1b, 0x0d)
    create_sprite(0x0014, EnemySprite.PipeDown, 0x00, 1, 0x0f, 0x13)
    create_sprite(0x0014, EnemySprite.PipeRight, 0x00, 1, 0x08, 0x18)
    create_sprite(0x0014, EnemySprite.PipeLeft, 0x00, 1, 0x17, 0x18)
    create_sprite(0x0014, EnemySprite.PipeRight, 0x00, 1, 0x0c, 0x1b)
    create_sprite(0x0014, EnemySprite.PipeLeft, 0x00, 1, 0x13, 0x1b)
    create_sprite(0x0015, EnemySprite.PipeDown, 0x00, 1, 0x04, 0x0c)
    create_sprite(0x0015, EnemySprite.PipeDown, 0x00, 1, 0x11, 0x11)
    create_sprite(0x0015, EnemySprite.PipeUp, 0x00, 1, 0x04, 0x17)
    create_sprite(0x0015, EnemySprite.PipeLeft, 0x00, 1, 0x16, 0x1b)
    create_sprite(0x0015, EnemySprite.Blob, 0x00, 1, 0x0a, 0x09, 'TR Pipe Pit')
    create_sprite(0x0015, EnemySprite.Blob, 0x00, 1, 0x15, 0x09, 'TR Pipe Pit')
    create_sprite(0x0015, EnemySprite.AntiFairy, 0x00, 1, 0x09, 0x0a, 'TR Pipe Pit')
    create_sprite(0x0015, EnemySprite.Pokey, 0x00, 1, 0x18, 0x16, 'TR Pipe Pit')
    create_sprite(0x0015, EnemySprite.AntiFairy, 0x00, 1, 0x08, 0x17, 'TR Pipe Pit')
    create_sprite(0x0015, EnemySprite.AntiFairy, 0x00, 1, 0x17, 0x17, 'TR Pipe Pit')
    create_sprite(0x0016, EnemySprite.Blob, 0x00, 0, 0x15, 0x07, 'Swamp C')
    create_sprite(0x0016, EnemySprite.Blob, 0x00, 0, 0x15, 0x08, 'Swamp C')
    create_sprite(0x0016, EnemySprite.BlueBari, 0x00, 0, 0x15, 0x09, 'Swamp C')
    create_sprite(0x0016, EnemySprite.Blob, 0x00, 0, 0x10, 0x0a, 'Swamp I')
    create_sprite(0x0016, EnemySprite.Hover, 0x00, 1, 0x0c, 0x18, 'Swamp Waterway')  # todo: quake only
    create_sprite(0x0016, EnemySprite.Hover, 0x00, 1, 0x07, 0x1b, 'Swamp Waterway')
    create_sprite(0x0016, EnemySprite.Hover, 0x00, 1, 0x14, 0x1b, 'Swamp Waterway')
    create_sprite(0x0017, EnemySprite.Bumper, 0x00, 0, 0x07, 0x0b)
    create_sprite(0x0017, EnemySprite.Bumper, 0x00, 0, 0x10, 0x0e)
    create_sprite(0x0017, EnemySprite.Bumper, 0x00, 0, 0x07, 0x16)
    create_sprite(0x0017, EnemySprite.HardhatBeetle, 0x00, 0, 0x15, 0x07, 'Hera 5F')
    create_sprite(0x0017, EnemySprite.HardhatBeetle, 0x00, 0, 0x0b, 0x09, 'Hera 5F')
    create_sprite(0x0017, EnemySprite.FirebarCW, 0x00, 0, 0x06, 0x11, 'Hera 5F')
    create_sprite(0x0017, EnemySprite.HardhatBeetle, 0x00, 0, 0x12, 0x11, 'Hera 5F')
    create_sprite(0x0017, EnemySprite.HardhatBeetle, 0x00, 0, 0x0b, 0x17, 'Hera 5F')
    create_sprite(0x0017, EnemySprite.HardhatBeetle, 0x00, 0, 0x17, 0x17, 'Hera 5F')
    create_sprite(0x0019, EnemySprite.Kondongo, 0x00, 0, 0x16, 0x0a, 'PoD Dark Maze')
    create_sprite(0x0019, EnemySprite.Kondongo, 0x00, 0, 0x1a, 0x0e, 'PoD Dark Maze')
    create_sprite(0x0019, EnemySprite.Kondongo, 0x00, 0, 0x16, 0x10, 'PoD Dark Maze')
    create_sprite(0x0019, EnemySprite.Kondongo, 0x00, 0, 0x18, 0x16, 'PoD Dark Maze')
    create_sprite(0x001a, EnemySprite.MiniHelmasaur, 0x00, 0, 0x08, 0x06, 'PoD Falling Bridge Mid')
    create_sprite(0x001a, EnemySprite.Terrorpin, 0x00, 0, 0x16, 0x06, 'PoD Compass Room')
    create_sprite(0x001a, EnemySprite.Terrorpin, 0x00, 0, 0x19, 0x06, 'PoD Compass Room')
    create_sprite(0x001a, EnemySprite.Terrorpin, 0x00, 0, 0x16, 0x0a, 'PoD Compass Room')
    create_sprite(0x001a, EnemySprite.Terrorpin, 0x00, 0, 0x19, 0x0a, 'PoD Compass Room')
    create_sprite(0x001a, EnemySprite.MiniHelmasaur, 0x00, 0, 0x07, 0x10, 'PoD Falling Bridge Mid')
    create_sprite(0x001a, EnemySprite.SpikeBlock, 0x00, 0, 0x16, 0x15, 'PoD Harmless Hellway')
    create_sprite(0x001a, EnemySprite.SpikeBlock, 0x00, 0, 0x16, 0x17, 'PoD Harmless Hellway')
    create_sprite(0x001a, EnemySprite.Statue, 0x00, 0, 0x15, 0x19)
    create_sprite(0x001a, EnemySprite.SpikeBlock, 0x00, 0, 0x16, 0x19, 'PoD Harmless Hellway')
    create_sprite(0x001a, 0x0b, SpriteType.Overlord, 0, 0x07, 0x1a)
    create_sprite(0x001b, EnemySprite.CrystalSwitch, 0x00, 0, 0x07, 0x04)
    create_sprite(0x001b, EnemySprite.EyeStatue, 0x00, 0, 0x10, 0x04)
    create_sprite(0x001b, EnemySprite.SpikeBlock, 0x00, 0, 0x03, 0x0c, 'PoD Bow Statue Left')
    create_sprite(0x001b, EnemySprite.RedEyegoreMimic, 0x00, 0, 0x07, 0x14, 'PoD Mimics 2')
    create_sprite(0x001b, EnemySprite.GreenEyegoreMimic, 0x00, 0, 0x03, 0x1c, 'PoD Mimics 2')
    create_sprite(0x001b, EnemySprite.GreenEyegoreMimic, 0x00, 0, 0x0c, 0x1c, 'PoD Mimics 2')
    create_sprite(0x001c, EnemySprite.ArmosKnight, 0x00, 0, 0x14, 0x15)
    create_sprite(0x001c, EnemySprite.ArmosKnight, 0x00, 0, 0x17, 0x15)
    create_sprite(0x001c, EnemySprite.ArmosKnight, 0x00, 0, 0x1a, 0x15)
    create_sprite(0x001c, EnemySprite.ArmosKnight, 0x00, 0, 0x1a, 0x18)
    create_sprite(0x001c, EnemySprite.ArmosKnight, 0x00, 0, 0x17, 0x18)
    create_sprite(0x001c, EnemySprite.ArmosKnight, 0x00, 0, 0x14, 0x18)
    create_sprite(0x001c, 0x19, SpriteType.Overlord, 0, 0x17, 0x18)
    create_sprite(0x001c, EnemySprite.Faerie, 0x00, 0, 0x07, 0x07)
    create_sprite(0x001c, EnemySprite.Faerie, 0x00, 0, 0x08, 0x07)
    create_sprite(0x001c, EnemySprite.Faerie, 0x00, 0, 0x07, 0x08)
    create_sprite(0x001c, EnemySprite.Faerie, 0x00, 0, 0x08, 0x08)
    create_sprite(0x001e, EnemySprite.CrystalSwitch, 0x00, 0, 0x1a, 0x09)
    create_sprite(0x001e, EnemySprite.RedBari, 0x00, 0, 0x16, 0x05, 'Ice Bomb Drop - Top')
    create_sprite(0x001e, EnemySprite.RedBari, 0x00, 0, 0x19, 0x05, 'Ice Bomb Drop - Top')
    create_sprite(0x001e, EnemySprite.RedBari, 0x00, 0, 0x16, 0x0a, 'Ice Bomb Drop')
    create_sprite(0x001e, EnemySprite.RedBari, 0x00, 0, 0x19, 0x0a, 'Ice Bomb Drop')
    create_sprite(0x001e, EnemySprite.Blob, 0x00, 0, 0x08, 0x18, 'Ice Floor Switch')
    create_sprite(0x001e, EnemySprite.Blob, 0x00, 0, 0x05, 0x1c, 'Ice Floor Switch')
    create_sprite(0x001f, EnemySprite.Pengator, 0x00, 0, 0x04, 0x15, 'Ice Pengator Switch')
    create_sprite(0x001f, EnemySprite.Pengator, 0x00, 0, 0x09, 0x15, 'Ice Pengator Switch')
    create_sprite(0x001f, EnemySprite.AntiFairy, 0x00, 0, 0x06, 0x16, 'Ice Pengator Switch')
    create_sprite(0x001f, EnemySprite.BunnyBeam, 0x00, 0, 0x07, 0x17, 'Ice Pengator Switch')
    create_sprite(0x001f, EnemySprite.Pengator, 0x00, 0, 0x0a, 0x17, 'Ice Pengator Switch')
    create_sprite(0x001f, EnemySprite.Pengator, 0x00, 0, 0x0a, 0x19, 'Ice Pengator Switch')
    create_sprite(0x001f, EnemySprite.Pengator, 0x00, 0, 0x04, 0x1b, 'Ice Pengator Switch')
    create_sprite(0x001f, EnemySprite.Pengator, 0x00, 0, 0x09, 0x1b, 'Ice Pengator Switch')
    create_sprite(0x0020, EnemySprite.Agahnim, 0x00, 0, 0x07, 0x15)
    create_sprite(0x0021, EnemySprite.CricketRat, 0x00, 0, 0x05, 0x06, 'Sewers Key Rat', True, 0xe4)
    create_sprite(0x0021, EnemySprite.Keese, 0x00, 0, 0x17, 0x06, 'Sewers Key Rat')
    create_sprite(0x0021, EnemySprite.Keese, 0x00, 0, 0x18, 0x06, 'Sewers Key Rat')
    create_sprite(0x0021, EnemySprite.CricketRat, 0x00, 0, 0x11, 0x09, 'Sewers Key Rat')
    create_sprite(0x0021, EnemySprite.CricketRat, 0x00, 0, 0x0d, 0x0a, 'Sewers Key Rat')
    create_sprite(0x0021, EnemySprite.CricketRat, 0x00, 0, 0x07, 0x14, 'Sewers Dark Aquabats')
    create_sprite(0x0021, EnemySprite.Keese, 0x00, 0, 0x0d, 0x14, 'Sewers Dark Aquabats')
    create_sprite(0x0021, EnemySprite.Keese, 0x00, 0, 0x12, 0x14, 'Sewers Dark Aquabats')
    create_sprite(0x0021, EnemySprite.CricketRat, 0x00, 0, 0x0d, 0x18, 'Sewers Dark Aquabats')
    create_sprite(0x0021, EnemySprite.CricketRat, 0x00, 0, 0x0a, 0x1c, 'Sewers Dark Aquabats')
    create_sprite(0x0021, EnemySprite.CricketRat, 0x00, 0, 0x13, 0x1c, 'Sewers Dark Aquabats')
    create_sprite(0x0022, EnemySprite.CricketRat, 0x00, 0, 0x06, 0x14, 'Sewers Water')
    create_sprite(0x0022, EnemySprite.CricketRat, 0x00, 0, 0x08, 0x14, 'Sewers Water')
    create_sprite(0x0022, EnemySprite.CricketRat, 0x00, 0, 0x11, 0x14, 'Sewers Water')
    create_sprite(0x0022, EnemySprite.CricketRat, 0x00, 0, 0x12, 0x14, 'Sewers Water')
    create_sprite(0x0022, EnemySprite.CricketRat, 0x00, 0, 0x11, 0x15, 'Sewers Water')
    create_sprite(0x0022, EnemySprite.CricketRat, 0x00, 0, 0x12, 0x15, 'Sewers Water')
    create_sprite(0x0022, EnemySprite.CricketRat, 0x00, 0, 0x09, 0x18, 'Sewers Water')
    create_sprite(0x0023, EnemySprite.LaserEyeTop, 0x00, 0, 0x15, 0x14)
    create_sprite(0x0023, EnemySprite.LaserEyeTop, 0x00, 0, 0x16, 0x14)
    create_sprite(0x0023, EnemySprite.LaserEyeTop, 0x00, 0, 0x17, 0x14)
    create_sprite(0x0023, EnemySprite.LaserEyeTop, 0x00, 0, 0x18, 0x14)
    create_sprite(0x0023, EnemySprite.LaserEyeTop, 0x00, 0, 0x19, 0x14)
    create_sprite(0x0024, EnemySprite.Medusa, 0x00, 0, 0x13, 0x04)
    create_sprite(0x0024, EnemySprite.Medusa, 0x00, 0, 0x1c, 0x04)
    create_sprite(0x0024, EnemySprite.RollerHorizontalRight, 0x00, 0, 0x1b, 0x06, 'TR Dodgers')
    create_sprite(0x0024, EnemySprite.Pokey, 0x00, 0, 0x05, 0x08, 'TR Twin Pokeys')
    create_sprite(0x0024, EnemySprite.Medusa, 0x00, 0, 0x07, 0x08)
    create_sprite(0x0024, EnemySprite.Pokey, 0x00, 0, 0x0a, 0x08, 'TR Twin Pokeys')
    create_sprite(0x0024, EnemySprite.BunnyBeam, 0x00, 0, 0x0c, 0x0c, 'TR Twin Pokeys')
    create_sprite(0x0026, EnemySprite.Medusa, 0x00, 0, 0x03, 0x04)
    create_sprite(0x0026, EnemySprite.RedBari, 0x00, 0, 0x1a, 0x05, 'Swamp Right Elbow')
    create_sprite(0x0026, EnemySprite.RedBari, 0x00, 0, 0x05, 0x06, 'Swamp Shooters')
    create_sprite(0x0026, EnemySprite.Stalfos, 0x00, 0, 0x09, 0x06, 'Swamp Shooters')
    create_sprite(0x0026, EnemySprite.Stalfos, 0x00, 0, 0x04, 0x09, 'Swamp Shooters')
    create_sprite(0x0026, EnemySprite.Medusa, 0x00, 0, 0x0c, 0x0c)
    create_sprite(0x0026, EnemySprite.Statue, 0x00, 0, 0x06, 0x17)
    create_sprite(0x0026, EnemySprite.FourWayShooter, 0x00, 0, 0x19, 0x17)
    create_sprite(0x0026, EnemySprite.RedBari, 0x00, 0, 0x07, 0x18, 'Swamp Push Statue')
    create_sprite(0x0026, EnemySprite.Kyameron, 0x00, 0, 0x15, 0x18, 'Swamp Push Statue')
    create_sprite(0x0026, EnemySprite.BlueBari, 0x00, 0, 0x18, 0x19, 'Swamp Push Statue')
    create_sprite(0x0026, EnemySprite.Firesnake, 0x00, 0, 0x1c, 0x1a, 'Swamp Push Statue')
    create_sprite(0x0027, EnemySprite.MiniMoldorm, 0x00, 0, 0x17, 0x09, 'Hera 4F')
    create_sprite(0x0027, EnemySprite.MiniMoldorm, 0x00, 0, 0x18, 0x13, 'Hera 4F')
    create_sprite(0x0027, EnemySprite.MiniMoldorm, 0x00, 0, 0x1b, 0x13, 'Hera 4F')
    create_sprite(0x0027, EnemySprite.MiniMoldorm, 0x00, 0, 0x0c, 0x1a, 'Hera 4F')
    create_sprite(0x0027, EnemySprite.SparkCW, 0x00, 0, 0x0f, 0x06, 'Hera Big Chest Landing')
    create_sprite(0x0027, EnemySprite.Kondongo, 0x00, 0, 0x05, 0x0e, 'Hera 4F')
    create_sprite(0x0027, EnemySprite.Kondongo, 0x00, 0, 0x04, 0x16, 'Hera 4F')
    create_sprite(0x0028, EnemySprite.Kyameron, 0x00, 0, 0x0a, 0x06, 'Hera 4F')
    create_sprite(0x0028, EnemySprite.Hover, 0x00, 0, 0x08, 0x08, 'Swamp Entrance')
    create_sprite(0x0028, EnemySprite.Hover, 0x00, 0, 0x0b, 0x0a, 'Swamp Entrance')
    create_sprite(0x0028, EnemySprite.Hover, 0x00, 0, 0x07, 0x0d, 'Swamp Entrance')
    create_sprite(0x0028, EnemySprite.SpikeBlock, 0x00, 0, 0x08, 0x10, 'Swamp Entrance')
    create_sprite(0x0029, EnemySprite.Mothula, 0x00, 0, 0x18, 0x16)
    create_sprite(0x0029, 0x07, SpriteType.Overlord, 0, 0x07, 0x16)
    create_sprite(0x002a, EnemySprite.CrystalSwitch, 0x00, 0, 0x10, 0x17)
    create_sprite(0x002a, EnemySprite.Bumper, 0x00, 0, 0x0f, 0x0f)
    create_sprite(0x002a, EnemySprite.HardhatBeetle, 0x00, 0, 0x0d, 0x08, 'PoD Arena North')
    create_sprite(0x002a, EnemySprite.HardhatBeetle, 0x00, 0, 0x07, 0x0c, 'PoD Arena Main')
    create_sprite(0x002a, EnemySprite.HardhatBeetle, 0x00, 0, 0x10, 0x0c, 'PoD Arena Main')
    create_sprite(0x002a, EnemySprite.HardhatBeetle, 0x00, 0, 0x0d, 0x0f, 'PoD Arena Main')
    create_sprite(0x002a, EnemySprite.HardhatBeetle, 0x00, 0, 0x13, 0x11, 'PoD Arena Main')
    create_sprite(0x002a, EnemySprite.HardhatBeetle, 0x00, 0, 0x0f, 0x13, 'PoD Arena Main')
    create_sprite(0x002b, EnemySprite.CrystalSwitch, 0x00, 0, 0x0a, 0x11, 'PoD Arena Main')
    create_sprite(0x002b, EnemySprite.Statue, 0x00, 0, 0x0a, 0x0a)
    create_sprite(0x002b, EnemySprite.RedBari, 0x00, 0, 0x07, 0x17, 'PoD Map Balcony')
    create_sprite(0x002b, EnemySprite.Faerie, 0x00, 0, 0x16, 0x17)
    create_sprite(0x002b, EnemySprite.Faerie, 0x00, 0, 0x18, 0x18)
    create_sprite(0x002b, EnemySprite.RedBari, 0x00, 0, 0x05, 0x1a, 'PoD Map Balcony')
    create_sprite(0x002b, EnemySprite.RedBari, 0x00, 0, 0x0a, 0x1a, 'PoD Map Balcony')
    create_sprite(0x002b, EnemySprite.Faerie, 0x00, 0, 0x17, 0x1a)
    create_sprite(0x002c, EnemySprite.BigFairy, 0x00, 0, 0x17, 0x05)
    create_sprite(0x002c, EnemySprite.Faerie, 0x00, 0, 0x09, 0x04)
    create_sprite(0x002c, EnemySprite.Faerie, 0x00, 0, 0x06, 0x05)
    create_sprite(0x002c, EnemySprite.Faerie, 0x00, 0, 0x08, 0x07)
    create_sprite(0x002e, EnemySprite.Pengator, 0x00, 0, 0x14, 0x06, 'Ice Compass Room')
    create_sprite(0x002e, EnemySprite.Pengator, 0x00, 0, 0x1c, 0x06, 'Ice Compass Room')
    create_sprite(0x002e, EnemySprite.Pengator, 0x00, 0, 0x16, 0x08, 'Ice Compass Room')
    create_sprite(0x002e, EnemySprite.Pengator, 0x00, 0, 0x19, 0x08, 'Ice Compass Room')
    create_sprite(0x002e, EnemySprite.Pengator, 0x00, 0, 0x14, 0x0b, 'Ice Compass Room')
    create_sprite(0x002e, EnemySprite.Pengator, 0x00, 0, 0x1b, 0x0b, 'Ice Compass Room')
    create_sprite(0x0030, EnemySprite.CutsceneAgahnim, 0x00, 0, 0x07, 0x05)
    create_sprite(0x0031, EnemySprite.CrystalSwitch, 0x00, 0, 0x18, 0x1a)
    create_sprite(0x0031, EnemySprite.CrystalSwitch, 0x00, 0, 0x16, 0x0b)
    create_sprite(0x0031, EnemySprite.HardhatBeetle, 0x00, 0, 0x15, 0x05, 'Hera Startile Wide')
    create_sprite(0x0031, EnemySprite.HardhatBeetle, 0x00, 0, 0x05, 0x06, 'Hera Startile Wide')
    create_sprite(0x0031, EnemySprite.HardhatBeetle, 0x00, 0, 0x03, 0x09, 'Hera Startile Wide')
    create_sprite(0x0031, EnemySprite.HardhatBeetle, 0x00, 0, 0x0b, 0x0c, 'Hera Startile Wide')
    create_sprite(0x0031, EnemySprite.HardhatBeetle, 0x00, 0, 0x03, 0x15, 'Hera Startile Corner')
    create_sprite(0x0031, EnemySprite.HardhatBeetle, 0x00, 0, 0x1b, 0x15, 'Hera Beetles')
    create_sprite(0x0031, EnemySprite.HardhatBeetle, 0x00, 0, 0x13, 0x16, 'Hera Beetles')
    create_sprite(0x0031, EnemySprite.HardhatBeetle, 0x00, 0, 0x03, 0x18, 'Hera Startile Corner')
    create_sprite(0x0031, EnemySprite.HardhatBeetle, 0x00, 0, 0x17, 0x19, 'Hera Beetles')
    create_sprite(0x0031, EnemySprite.HardhatBeetle, 0x00, 0, 0x09, 0x1c, 'Hera Startile Corner')
    create_sprite(0x0032, EnemySprite.Keese, 0x00, 0, 0x0b, 0x0d, 'Sewers Dark Cross')
    create_sprite(0x0032, EnemySprite.Snake, 0x00, 0, 0x0f, 0x0d, 'Sewers Dark Cross')
    create_sprite(0x0032, EnemySprite.Keese, 0x00, 0, 0x13, 0x0d, 'Sewers Dark Cross')
    create_sprite(0x0032, EnemySprite.Snake, 0x00, 0, 0x10, 0x0e, 'Sewers Dark Cross')
    create_sprite(0x0032, EnemySprite.Snake, 0x00, 0, 0x12, 0x0f, 'Sewers Dark Cross')
    create_sprite(0x0033, EnemySprite.Lanmolas, 0x00, 0, 0x06, 0x17)
    create_sprite(0x0033, EnemySprite.Lanmolas, 0x00, 0, 0x09, 0x17)
    create_sprite(0x0033, EnemySprite.Lanmolas, 0x00, 0, 0x07, 0x19)
    create_sprite(0x0034, EnemySprite.Hover, 0x00, 0, 0x0f, 0x0b, 'Swamp West Shallows')
    create_sprite(0x0034, EnemySprite.Hover, 0x00, 0, 0x10, 0x12, 'Swamp West Shallows')
    create_sprite(0x0034, EnemySprite.Kyameron, 0x00, 0, 0x0f, 0x15, 'Swamp West Shallows')
    create_sprite(0x0034, EnemySprite.Firesnake, 0x00, 0, 0x19, 0x17, 'Swamp West Shallows')
    create_sprite(0x0034, EnemySprite.Blob, 0x00, 0, 0x03, 0x18, 'Swamp West Block Path')
    create_sprite(0x0034, EnemySprite.BlueBari, 0x00, 0, 0x14, 0x18, 'Swamp West Shallows')
    create_sprite(0x0034, EnemySprite.Stalfos, 0x00, 0, 0x16, 0x1a, 'Swamp West Shallows')
    create_sprite(0x0035, EnemySprite.CrystalSwitch, 0x00, 0, 0x16, 0x06)
    create_sprite(0x0035, EnemySprite.WaterSwitch, 0x00, 0, 0x14, 0x05)
    create_sprite(0x0035, EnemySprite.RedBari, 0x00, 0, 0x18, 0x05, 'Swamp Crystal Switch Outer')
    create_sprite(0x0035, EnemySprite.SpikeBlock, 0x00, 0, 0x13, 0x09, 'Swamp Crystal Switch Outer')
    create_sprite(0x0035, EnemySprite.Stalfos, 0x00, 0, 0x14, 0x0b, 'Swamp Crystal Switch Outer')
    create_sprite(0x0035, EnemySprite.Blob, 0x00, 0, 0x07, 0x14, 'Swamp Trench 2 Departure')
    create_sprite(0x0035, EnemySprite.Stalfos, 0x00, 0, 0x14, 0x18, 'Swamp Trench 2 Pots')
    create_sprite(0x0035, EnemySprite.Firesnake, 0x00, 0, 0x16, 0x19, 'Swamp Trench 2 Pots')
    create_sprite(0x0035, EnemySprite.FourWayShooter, 0x00, 0, 0x17, 0x1a)
    create_sprite(0x0035, EnemySprite.BlueBari, 0x00, 0, 0x14, 0x1b, 'Swamp Trench 2 Pots')
    create_sprite(0x0035, EnemySprite.Stalfos, 0x00, 0, 0x1b, 0x1c, 'Swamp Trench 2 Pots')
    create_sprite(0x0036, 0x12, SpriteType.Overlord, 0, 0x17, 0x02)
    create_sprite(0x0036, EnemySprite.Hover, 0x00, 0, 0x0b, 0x0a, 'Swamp Hub')
    create_sprite(0x0036, EnemySprite.Hover, 0x00, 0, 0x14, 0x0a, 'Swamp Hub')
    create_sprite(0x0036, EnemySprite.Medusa, 0x00, 0, 0x15, 0x0b)
    create_sprite(0x0036, 0x10, SpriteType.Overlord, 0, 0x01, 0x0d)
    create_sprite(0x0036, EnemySprite.Kyameron, 0x00, 0, 0x14, 0x13, 'Swamp Hub')
    create_sprite(0x0036, 0x11, SpriteType.Overlord, 0, 0x1e, 0x13)
    create_sprite(0x0036, EnemySprite.Hover, 0x00, 0, 0x09, 0x14, 'Swamp Hub')
    create_sprite(0x0036, EnemySprite.Hover, 0x00, 0, 0x12, 0x17, 'Swamp Hub')
    create_sprite(0x0036, 0x13, SpriteType.Overlord, 0, 0x0a, 0x1e)
    create_sprite(0x0036, 0x13, SpriteType.Overlord, 0, 0x14, 0x1e)
    create_sprite(0x0037, EnemySprite.WaterSwitch, 0x00, 0, 0x0b, 0x04)
    create_sprite(0x0037, EnemySprite.Stalfos, 0x00, 0, 0x05, 0x06, 'Swamp Hammer Switch')
    create_sprite(0x0037, EnemySprite.Blob, 0x00, 0, 0x17, 0x08, 'Swamp Map Ledge')
    create_sprite(0x0037, EnemySprite.Blob, 0x00, 0, 0x1a, 0x08, 'Swamp Map Ledge')
    create_sprite(0x0037, EnemySprite.Stalfos, 0x00, 0, 0x0c, 0x09, 'Swamp Hammer Switch')
    create_sprite(0x0037, EnemySprite.Firesnake, 0x00, 0, 0x15, 0x14, 'Swamp Trench 1 Approach')
    create_sprite(0x0037, EnemySprite.Stalfos, 0x00, 0, 0x17, 0x17, 'Swamp Trench 1 Approach')
    create_sprite(0x0037, EnemySprite.BlueBari, 0x00, 0, 0x13, 0x19, 'Swamp Trench 1 Approach')
    create_sprite(0x0037, EnemySprite.FourWayShooter, 0x00, 0, 0x17, 0x1a)
    create_sprite(0x0037, EnemySprite.RedBari, 0x00, 0, 0x15, 0x1c, 'Swamp Trench 1 Approach')
    create_sprite(0x0038, EnemySprite.Hover, 0x00, 0, 0x0c, 0x06, 'Swamp Pot Row')
    create_sprite(0x0038, EnemySprite.Hover, 0x00, 0, 0x07, 0x0a, 'Swamp Pot Row')
    create_sprite(0x0038, EnemySprite.Kyameron, 0x00, 0, 0x0c, 0x0c, 'Swamp Pot Row')
    create_sprite(0x0038, EnemySprite.Medusa, 0x00, 0, 0x0c, 0x10, 'Swamp Pot Row')
    create_sprite(0x0038, EnemySprite.Kyameron, 0x00, 0, 0x06, 0x14, 'Swamp Pot Row')
    create_sprite(0x0038, EnemySprite.Kyameron, 0x00, 0, 0x0c, 0x18, 'Swamp Pot Row')
    create_sprite(0x0038, EnemySprite.Hover, 0x00, 0, 0x07, 0x1a, 'Swamp Pot Row')
    create_sprite(0x0039, EnemySprite.MiniMoldorm, 0x00, 0, 0x04, 0x18, 'Skull Spike Corner')
    create_sprite(0x0039, 0x09, SpriteType.Overlord, 0, 0x0f, 0x0f)
    create_sprite(0x0039, EnemySprite.Gibdo, 0x00, 0, 0x05, 0x15, 'Skull Spike Corner', True, 0xe4)
    create_sprite(0x0039, EnemySprite.MiniHelmasaur, 0x00, 0, 0x09, 0x15, 'Skull Spike Corner')
    create_sprite(0x0039, EnemySprite.SpikeBlock, 0x00, 0, 0x17, 0x16, 'Skull Spike Corner')
    create_sprite(0x0039, EnemySprite.HardhatBeetle, 0x00, 0, 0x0b, 0x18, 'Skull Spike Corner')
    create_sprite(0x0039, EnemySprite.SpikeBlock, 0x00, 0, 0x17, 0x1a, 'Skull Spike Corner')
    create_sprite(0x003a, EnemySprite.Terrorpin, 0x00, 0, 0x0e, 0x11, 'PoD Pit Room',)
    create_sprite(0x003a, EnemySprite.Terrorpin, 0x00, 0, 0x11, 0x11, 'PoD Pit Room',)
    create_sprite(0x003a, EnemySprite.Medusa, 0x00, 0, 0x04, 0x14, 'PoD Pit Room',)
    create_sprite(0x003a, EnemySprite.BlueBari, 0x00, 0, 0x0a, 0x14, 'PoD Pit Room',)
    create_sprite(0x003a, EnemySprite.BlueBari, 0x00, 0, 0x15, 0x14, 'PoD Pit Room',)
    create_sprite(0x003a, EnemySprite.Medusa, 0x00, 0, 0x1b, 0x14, 'PoD Pit Room',)
    create_sprite(0x003b, EnemySprite.SpikeBlock, 0x00, 0, 0x03, 0x06, 'PoD Conveyor')
    create_sprite(0x003b, EnemySprite.RedBari, 0x00, 0, 0x07, 0x09, 'PoD Conveyor')
    create_sprite(0x003b, EnemySprite.SpikeBlock, 0x00, 0, 0x0c, 0x0d, 'PoD Conveyor')
    create_sprite(0x003b, EnemySprite.BlueBari, 0x00, 0, 0x08, 0x0f, 'PoD Conveyor')
    create_sprite(0x003b, EnemySprite.SpikeBlock, 0x00, 0, 0x03, 0x13, 'PoD Conveyor')
    create_sprite(0x003b, EnemySprite.BlueBari, 0x00, 0, 0x07, 0x16, 'PoD Conveyor')
    create_sprite(0x003b, EnemySprite.SpikeBlock, 0x00, 0, 0x0c, 0x1a, 'PoD Conveyor')
    create_sprite(0x003c, EnemySprite.HardhatBeetle, 0x00, 0, 0x09, 0x08, 'Hookshot Cave (Hook Islands)')
    create_sprite(0x003c, EnemySprite.BlueBari, 0x00, 0, 0x0a, 0x14, 'Hookshot Cave (Hook Islands)')
    create_sprite(0x003c, EnemySprite.BlueBari, 0x00, 0, 0x12, 0x14, 'Hookshot Cave (Bonk Islands)')
    create_sprite(0x003d, EnemySprite.CrystalSwitch, 0x00, 0, 0x05, 0x17)
    create_sprite(0x003d, EnemySprite.CrystalSwitch, 0x00, 0, 0x0a, 0x19)
    create_sprite(0x003d, EnemySprite.MiniHelmasaur, 0x00, 0, 0x17, 0x07, 'GT Mini Helmasaur Room', True, 0xe4)
    create_sprite(0x003d, EnemySprite.MiniHelmasaur, 0x00, 0, 0x18, 0x07, 'GT Mini Helmasaur Room')
    create_sprite(0x003d, EnemySprite.Medusa, 0x00, 0, 0x15, 0x08, 'GT Mini Helmasaur Room')
    create_sprite(0x003d, EnemySprite.Medusa, 0x00, 0, 0x1a, 0x08, 'GT Mini Helmasaur Room')
    create_sprite(0x003d, EnemySprite.SpikeBlock, 0x00, 0, 0x04, 0x0a, 'GT Bomb Conveyor')
    create_sprite(0x003d, EnemySprite.BigSpike, 0x00, 0, 0x03, 0x0b, 'GT Bomb Conveyor')
    create_sprite(0x003d, 0x0a, SpriteType.Overlord, 0, 0x1b, 0x15)
    create_sprite(0x003d, EnemySprite.SparkCCW, 0x00, 0, 0x13, 0x16, 'GT Falling Torches')
    create_sprite(0x003d, EnemySprite.SparkCW, 0x00, 0, 0x1c, 0x16, 'GT Falling Torches')
    create_sprite(0x003d, EnemySprite.SparkCW, 0x00, 0, 0x09, 0x16, 'GT Crystal Inner Circle')
    create_sprite(0x003d, EnemySprite.BunnyBeam, 0x00, 0, 0x07, 0x17, 'GT Crystal Inner Circle')
    create_sprite(0x003d, EnemySprite.AntiFairy, 0x00, 0, 0x08, 0x17, 'GT Crystal Inner Circle')
    create_sprite(0x003e, EnemySprite.CrystalSwitch, 0x00, 0, 0x06, 0x15)
    create_sprite(0x003e, EnemySprite.StalfosKnight, 0x00, 0, 0x19, 0x04, 'Ice Stalfos Hint')
    create_sprite(0x003e, EnemySprite.StalfosKnight, 0x00, 0, 0x16, 0x0b, 'Ice Stalfos Hint')
    create_sprite(0x003e, EnemySprite.Babasu, 0x00, 0, 0x05, 0x12, 'Ice Conveyor')
    create_sprite(0x003e, EnemySprite.Babasu, 0x00, 0, 0x0e, 0x12, 'Ice Conveyor')
    create_sprite(0x003e, 0x07, SpriteType.Overlord, 0, 0x10, 0x12)
    create_sprite(0x003e, EnemySprite.Babasu, 0x00, 0, 0x12, 0x12, 'Ice Conveyor')
    create_sprite(0x003e, EnemySprite.Babasu, 0x00, 0, 0x15, 0x12, 'Ice Conveyor')
    create_sprite(0x003e, EnemySprite.BlueBari, 0x00, 0, 0x07, 0x16, 'Ice Conveyor')
    create_sprite(0x003e, EnemySprite.BlueBari, 0x00, 0, 0x11, 0x18, 'Ice Conveyor', True, 0xe4)
    create_sprite(0x003e, EnemySprite.BlueBari, 0x00, 0, 0x15, 0x19, 'Ice Conveyor')
    create_sprite(0x003e, EnemySprite.BlueBari, 0x00, 0, 0x0b, 0x1a, 'Ice Conveyor')
    create_sprite(0x003f, EnemySprite.CorrectPullSwitch, 0x00, 0, 0x04, 0x15)
    create_sprite(0x003f, EnemySprite.StalfosKnight, 0x00, 0, 0x0c, 0x16, 'Ice Right H')
    create_sprite(0x003f, EnemySprite.CorrectPullSwitch, 0x00, 0, 0x13, 0x15)
    create_sprite(0x003f, EnemySprite.StalfosKnight, 0x00, 0, 0x04, 0x17, 'Ice Hammer Block')
    create_sprite(0x003f, EnemySprite.BunnyBeam, 0x00, 0, 0x08, 0x18, 'Ice Hammer Block')
    create_sprite(0x0040, EnemySprite.BlueGuard, 0x00, 1, 0x09, 0x08, 'Tower Catwalk')
    create_sprite(0x0040, EnemySprite.BlueGuard, 0x1b, 1, 0x09, 0x0f, 'Tower Catwalk')
    create_sprite(0x0040, EnemySprite.Statue, 0x00, 1, 0x18, 0x15, 'Tower Push Statue')
    create_sprite(0x0040, EnemySprite.RedSpearGuard, 0x00, 1, 0x1b, 0x18, 'Tower Push Statue')
    create_sprite(0x0040, EnemySprite.BlueArcher, 0x00, 1, 0x17, 0x1a, 'Tower Push Statue')
    create_sprite(0x0040, EnemySprite.BlueArcher, 0x00, 1, 0x19, 0x1a, 'Tower Push Statue')
    create_sprite(0x0041, EnemySprite.CricketRat, 0x00, 0, 0x11, 0x0a, 'Sewers Behind Tapestry')
    create_sprite(0x0041, EnemySprite.CricketRat, 0x00, 0, 0x1b, 0x0b, 'Sewers Behind Tapestry')
    create_sprite(0x0041, EnemySprite.CricketRat, 0x00, 0, 0x0f, 0x0d, 'Sewers Behind Tapestry')
    create_sprite(0x0041, EnemySprite.CricketRat, 0x00, 0, 0x06, 0x15, 'Sewers Behind Tapestry')
    create_sprite(0x0042, EnemySprite.Snake, 0x00, 0, 0x12, 0x06, 'Sewers Rope Room')
    create_sprite(0x0042, EnemySprite.Snake, 0x00, 0, 0x13, 0x06, 'Sewers Rope Room')
    create_sprite(0x0042, EnemySprite.Snake, 0x00, 0, 0x14, 0x06, 'Sewers Rope Room')
    create_sprite(0x0042, EnemySprite.Snake, 0x00, 0, 0x12, 0x07, 'Sewers Rope Room')
    create_sprite(0x0042, EnemySprite.Snake, 0x00, 0, 0x13, 0x07, 'Sewers Rope Room')
    create_sprite(0x0042, EnemySprite.Snake, 0x00, 0, 0x14, 0x07, 'Sewers Rope Room')
    create_sprite(0x0043, EnemySprite.RedEyegoreMimic, 0x00, 0, 0x0c, 0x06, 'Desert Wall Slide')
    create_sprite(0x0043, 0x14, SpriteType.Overlord, 0, 0x17, 0x18)
    create_sprite(0x0044, EnemySprite.Bumper, 0x00, 0, 0x09, 0x06, 'Thieves Trap')
    create_sprite(0x0044, EnemySprite.Bumper, 0x00, 0, 0x05, 0x08, 'Thieves Trap')
    create_sprite(0x0044, EnemySprite.BlueBari, 0x00, 0, 0x08, 0x04, 'Thieves Trap')
    create_sprite(0x0044, EnemySprite.BlueBari, 0x00, 0, 0x03, 0x08, 'Thieves Trap')
    create_sprite(0x0044, EnemySprite.Blob, 0x00, 0, 0x17, 0x08, 'Thieves Conveyor Bridge')
    create_sprite(0x0044, EnemySprite.BlueBari, 0x00, 0, 0x08, 0x0c, 'Thieves Trap')
    create_sprite(0x0044, EnemySprite.RedBari, 0x00, 0, 0x17, 0x0f, 'Thieves Conveyor Bridge')
    create_sprite(0x0044, 0x0a, SpriteType.Overlord, 0, 0x0b, 0x15)
    create_sprite(0x0044, EnemySprite.BlueBari, 0x00, 0, 0x18, 0x16, 'Thieves Conveyor Bridge')
    create_sprite(0x0045, EnemySprite.BlindMaiden, 0x00, 0, 0x19, 0x06)
    create_sprite(0x0045, EnemySprite.RedZazak, 0x00, 0, 0x06, 0x06, 'Thieves Basement Block')
    create_sprite(0x0045, EnemySprite.BlueZazak, 0x00, 0, 0x04, 0x0b, 'Thieves Basement Block')
    create_sprite(0x0045, EnemySprite.Stalfos, 0x00, 0, 0x0b, 0x0b, 'Thieves Basement Block')
    create_sprite(0x0045, EnemySprite.BunnyBeam, 0x00, 0, 0x17, 0x0b, "Thieves Blind's Cell Interior")
    create_sprite(0x0045, EnemySprite.BlueZazak, 0x00, 0, 0x18, 0x0c, "Thieves Blind's Cell Interior")
    create_sprite(0x0045, EnemySprite.BlueZazak, 0x00, 0, 0x1a, 0x0c, "Thieves Blind's Cell Interior")
    create_sprite(0x0045, EnemySprite.BlueZazak, 0x00, 0, 0x18, 0x11, "Thieves Blind's Cell Interior")
    create_sprite(0x0045, EnemySprite.Blob, 0x00, 0, 0x16, 0x18, "Thieves Blind's Cell")
    create_sprite(0x0045, EnemySprite.RedZazak, 0x00, 0, 0x19, 0x1b, "Thieves Blind's Cell")
    create_sprite(0x0045, EnemySprite.RedZazak, 0x00, 0, 0x07, 0x1c, 'Thieves Lonely Zazak')
    create_sprite(0x0046, EnemySprite.Hover, 0x00, 0, 0x16, 0x05, 'Swamp Donut Top')
    create_sprite(0x0046, 0x11, SpriteType.Overlord, 0, 0x1b, 0x06)
    create_sprite(0x0046, EnemySprite.Hover, 0x00, 0, 0x09, 0x1a, 'Swamp Donut Bottom')
    create_sprite(0x0046, 0x11, SpriteType.Overlord, 0, 0x1b, 0x1a)
    create_sprite(0x0046, EnemySprite.Hover, 0x00, 0, 0x11, 0x1b, 'Swamp Donut Bottom')
    create_sprite(0x0049, EnemySprite.MiniMoldorm, 0x00, 0, 0x0b, 0x05, 'Skull Vines')
    create_sprite(0x0049, EnemySprite.MiniMoldorm, 0x00, 0, 0x04, 0x0b, 'Skull Vines')
    create_sprite(0x0049, EnemySprite.MiniMoldorm, 0x00, 0, 0x09, 0x0c, 'Skull Vines')
    create_sprite(0x0049, EnemySprite.BunnyBeam, 0x00, 0, 0x08, 0x06, 'Skull Vines')
    create_sprite(0x0049, EnemySprite.Gibdo, 0x00, 0, 0x07, 0x08, 'Skull Vines')
    create_sprite(0x0049, EnemySprite.Gibdo, 0x00, 0, 0x17, 0x0b, 'Skull Torch Room')
    create_sprite(0x0049, 0x09, SpriteType.Overlord, 0, 0x0f, 0x0f, 'Skull Torch Room')
    create_sprite(0x0049, EnemySprite.Gibdo, 0x00, 0, 0x17, 0x10, 'Skull Torch Room')
    create_sprite(0x0049, EnemySprite.Gibdo, 0x00, 0, 0x16, 0x14, 'Skull Torch Room')
    create_sprite(0x0049, EnemySprite.BlueBari, 0x00, 0, 0x09, 0x16, 'Skull Star Pits')
    create_sprite(0x0049, EnemySprite.RedBari, 0x00, 0, 0x0a, 0x17, 'Skull Star Pits')
    create_sprite(0x0049, EnemySprite.BlueBari, 0x00, 0, 0x07, 0x18, 'Skull Star Pits')
    create_sprite(0x0049, EnemySprite.Gibdo, 0x00, 0, 0x1a, 0x18, 'Skull Torch Room')
    create_sprite(0x004a, EnemySprite.Statue, 0x00, 0, 0x14, 0x07, 'PoD Middle Cage')
    create_sprite(0x004a, EnemySprite.MiniHelmasaur, 0x00, 0, 0x08, 0x08, 'PoD Left Cage')
    create_sprite(0x004a, EnemySprite.MiniHelmasaur, 0x00, 0, 0x18, 0x08, 'PoD Middle Cage')
    create_sprite(0x004b, EnemySprite.RedEyegoreMimic, 0x00, 0, 0x07, 0x04, 'PoD Mimics 1')
    create_sprite(0x004b, EnemySprite.AntiFairy, 0x00, 0, 0x17, 0x05, 'PoD Warp Hint')
    create_sprite(0x004b, EnemySprite.AntiFairy, 0x00, 0, 0x18, 0x06, 'PoD Warp Hint')
    create_sprite(0x004b, EnemySprite.GreenEyegoreMimic, 0x00, 0, 0x04, 0x08, 'PoD Mimics 1')
    create_sprite(0x004b, EnemySprite.GreenEyegoreMimic, 0x00, 0, 0x0b, 0x08, 'PoD Mimics 1')
    create_sprite(0x004b, EnemySprite.BlueBari, 0x00, 0, 0x0f, 0x18, 'PoD Jelly Hall')
    create_sprite(0x004b, EnemySprite.BlueBari, 0x00, 0, 0x0b, 0x19, 'PoD Jelly Hall')
    create_sprite(0x004b, EnemySprite.BlueBari, 0x00, 0, 0x12, 0x19, 'PoD Jelly Hall')
    create_sprite(0x004c, EnemySprite.Bumper, 0x00, 0, 0x15, 0x11, 'GT Frozen Over')
    create_sprite(0x004c, EnemySprite.Bumper, 0x00, 0, 0x19, 0x12, 'GT Frozen Over')
    create_sprite(0x004c, EnemySprite.MiniHelmasaur, 0x00, 0, 0x15, 0x05, 'GT Frozen Over')
    create_sprite(0x004c, EnemySprite.MiniHelmasaur, 0x00, 0, 0x1a, 0x05, 'GT Frozen Over')
    create_sprite(0x004c, EnemySprite.MiniHelmasaur, 0x00, 0, 0x17, 0x06, 'GT Frozen Over')
    create_sprite(0x004c, EnemySprite.MiniHelmasaur, 0x00, 0, 0x18, 0x0a, 'GT Frozen Over')
    create_sprite(0x004c, EnemySprite.MiniHelmasaur, 0x00, 0, 0x14, 0x15, 'GT Frozen Over')
    create_sprite(0x004c, EnemySprite.SpikeBlock, 0x00, 0, 0x13, 0x18, 'GT Frozen Over')
    create_sprite(0x004d, EnemySprite.Moldorm, 0x00, 0, 0x0e, 0x0e)
    create_sprite(0x004e, EnemySprite.Blob, 0x00, 0, 0x14, 0x08, 'Ice Narrow Corridor')
    create_sprite(0x004e, EnemySprite.Blob, 0x00, 0, 0x16, 0x08, 'Ice Narrow Corridor')
    create_sprite(0x004e, EnemySprite.Blob, 0x00, 0, 0x18, 0x08, 'Ice Narrow Corridor')
    create_sprite(0x004e, EnemySprite.FirebarCW, 0x00, 0, 0x07, 0x09, 'Ice Bomb Jump Catwalk')
    create_sprite(0x004f, EnemySprite.Faerie, 0x00, 0, 0x17, 0x06)
    create_sprite(0x004f, EnemySprite.Faerie, 0x00, 0, 0x14, 0x08)
    create_sprite(0x004f, EnemySprite.Faerie, 0x00, 0, 0x1a, 0x08)
    create_sprite(0x0050, EnemySprite.GreenGuard, 0x00, 1, 0x17, 0x0e, 'Hyrule Castle West Hall')
    create_sprite(0x0050, EnemySprite.GreenKnifeGuard, 0x00, 1, 0x18, 0x10, 'Hyrule Castle West Hall')
    create_sprite(0x0050, EnemySprite.GreenKnifeGuard, 0x00, 1, 0x17, 0x12, 'Hyrule Castle West Hall')
    create_sprite(0x0051, EnemySprite.CastleMantle, 0x00, 0, 0x0e, 0x02, 'Hyrule Castle Throne Room')
    create_sprite(0x0051, EnemySprite.BlueGuard, 0x01, 1, 0x09, 0x17, 'Hyrule Castle Throne Room')
    create_sprite(0x0051, EnemySprite.BlueGuard, 0x02, 1, 0x16, 0x17, 'Hyrule Castle Throne Room')
    create_sprite(0x0052, EnemySprite.GreenGuard, 0x00, 1, 0x07, 0x0d, 'Hyrule Castle East Hall')
    create_sprite(0x0052, EnemySprite.GreenKnifeGuard, 0x00, 1, 0x08, 0x0f, 'Hyrule Castle East Hall')
    create_sprite(0x0052, EnemySprite.GreenKnifeGuard, 0x00, 1, 0x07, 0x12, 'Hyrule Castle East Hall')
    create_sprite(0x0053, EnemySprite.Popo, 0x00, 0, 0x17, 0x07, 'Desert Beamos Hall')
    create_sprite(0x0053, EnemySprite.Beamos, 0x00, 0, 0x1c, 0x09, 'Desert Beamos Hall')
    create_sprite(0x0053, EnemySprite.Popo2, 0x00, 0, 0x17, 0x0c, 'Desert Beamos Hall')
    create_sprite(0x0053, EnemySprite.Popo2, 0x00, 0, 0x1a, 0x0c, 'Desert Beamos Hall')
    create_sprite(0x0053, EnemySprite.Beamos, 0x00, 0, 0x13, 0x0e, 'Desert Beamos Hall')
    create_sprite(0x0053, EnemySprite.Popo, 0x00, 0, 0x05, 0x15, 'Desert Four Statues')
    create_sprite(0x0053, EnemySprite.Popo, 0x00, 0, 0x0b, 0x16, 'Desert Four Statues')
    create_sprite(0x0053, EnemySprite.Popo, 0x00, 0, 0x1a, 0x17, 'Desert Beamos Hall')
    create_sprite(0x0053, EnemySprite.Beamos, 0x00, 0, 0x07, 0x19, 'Desert Four Statues')
    create_sprite(0x0053, EnemySprite.Popo, 0x00, 0, 0x04, 0x1a, 'Desert Four Statues')
    create_sprite(0x0053, EnemySprite.Popo, 0x00, 0, 0x0b, 0x1a, 'Desert Four Statues')
    create_sprite(0x0053, EnemySprite.Beamos, 0x00, 0, 0x1b, 0x1a, 'Desert Beamos Hall')
    create_sprite(0x0053, EnemySprite.Popo, 0x00, 0, 0x1a, 0x1b, 'Desert Beamos Hall')
    create_sprite(0x0054, EnemySprite.Kyameron, 0x00, 0, 0x0e, 0x05, 'Swamp Attic')
    create_sprite(0x0054, EnemySprite.Hover, 0x00, 0, 0x0c, 0x0b, 'Swamp Attic')
    create_sprite(0x0054, EnemySprite.Medusa, 0x00, 0, 0x0b, 0x0e, 'Swamp Attic')
    create_sprite(0x0054, EnemySprite.FirebarCW, 0x00, 0, 0x0f, 0x0e, 'Swamp Attic')
    create_sprite(0x0054, EnemySprite.Hover, 0x00, 0, 0x10, 0x0f, 'Swamp Attic')
    create_sprite(0x0054, EnemySprite.Kyameron, 0x00, 0, 0x12, 0x14, 'Swamp Attic')
    create_sprite(0x0054, EnemySprite.Hover, 0x00, 0, 0x0f, 0x15, 'Swamp Attic')
    create_sprite(0x0054, EnemySprite.Kyameron, 0x00, 0, 0x0c, 0x17, 'Swamp Attic')
    create_sprite(0x0055, EnemySprite.UnclePriest, 0x00, 0, 0x0e, 0x08, 'Hyrule Castle Secret Entrance')
    create_sprite(0x0055, EnemySprite.GreenKnifeGuard, 0x00, 0, 0x14, 0x15, 'Hyrule Castle Secret Entrance')
    create_sprite(0x0055, EnemySprite.GreenKnifeGuard, 0x00, 0, 0x0d, 0x16, 'Hyrule Castle Secret Entrance')
    create_sprite(0x0056, 0x0a, SpriteType.Overlord, 0, 0x0b, 0x05, 'Skull X Room')
    create_sprite(0x0056, EnemySprite.Bumper, 0x00, 0, 0x07, 0x19)
    create_sprite(0x0056, EnemySprite.Bumper, 0x00, 0, 0x17, 0x19)
    create_sprite(0x0056, EnemySprite.MiniHelmasaur, 0x00, 0, 0x07, 0x04, 'Skull X Room')
    create_sprite(0x0056, EnemySprite.HardhatBeetle, 0x00, 0, 0x1b, 0x05, 'Skull Back Drop')
    create_sprite(0x0056, EnemySprite.MiniHelmasaur, 0x00, 0, 0x03, 0x06, 'Skull X Room')
    create_sprite(0x0056, EnemySprite.MiniHelmasaur, 0x00, 0, 0x0c, 0x06, 'Skull X Room')
    create_sprite(0x0056, 0x09, SpriteType.Overlord, 0, 0x0f, 0x0f)
    create_sprite(0x0056, EnemySprite.HardhatBeetle, 0x00, 0, 0x13, 0x11, 'Skull Back Drop')
    create_sprite(0x0056, EnemySprite.SpikeBlock, 0x00, 0, 0x18, 0x12, 'Skull Back Drop')
    create_sprite(0x0056, EnemySprite.HardhatBeetle, 0x00, 0, 0x03, 0x1b, 'Skull 2 West Lobby')
    create_sprite(0x0056, EnemySprite.Firesnake, 0x00, 0, 0x13, 0x1c, 'Skull Small Hall')
    create_sprite(0x0056, EnemySprite.HardhatBeetle, 0x00, 0, 0x19, 0x1c, 'Skull Small Hall')
    create_sprite(0x0057, EnemySprite.BunnyBeam, 0x00, 0, 0x08, 0x04, 'Skull Big Key')
    create_sprite(0x0057, EnemySprite.RedBari, 0x00, 0, 0x0c, 0x04, 'Skull Big Key')
    create_sprite(0x0057, EnemySprite.SpikeBlock, 0x00, 0, 0x08, 0x05, 'Skull Big Key')
    create_sprite(0x0057, EnemySprite.Stalfos, 0x00, 0, 0x04, 0x07, 'Skull Big Key')
    create_sprite(0x0057, EnemySprite.Stalfos, 0x00, 0, 0x03, 0x0c, 'Skull Big Key')
    create_sprite(0x0057, EnemySprite.Gibdo, 0x00, 0, 0x0c, 0x0c, 'Skull Big Key')
    create_sprite(0x0057, 0x09, SpriteType.Overlord, 0, 0x0f, 0x0f)
    create_sprite(0x0057, EnemySprite.Gibdo, 0x00, 0, 0x05, 0x14, 'Skull 2 East Lobby')
    create_sprite(0x0057, EnemySprite.Gibdo, 0x00, 0, 0x0a, 0x14, 'Skull 2 East Lobby')
    create_sprite(0x0057, EnemySprite.Gibdo, 0x00, 0, 0x17, 0x14, 'Skull Pot Prison')
    create_sprite(0x0057, EnemySprite.Gibdo, 0x00, 0, 0x19, 0x14, 'Skull Pot Prison')
    create_sprite(0x0057, EnemySprite.Stalfos, 0x00, 0, 0x15, 0x15, 'Skull Pot Prison')
    create_sprite(0x0057, EnemySprite.Gibdo, 0x00, 0, 0x13, 0x17, 'Skull Pot Prison')
    create_sprite(0x0057, EnemySprite.BlueBari, 0x00, 0, 0x07, 0x18, 'Skull 2 East Lobby')
    create_sprite(0x0057, EnemySprite.BlueBari, 0x00, 0, 0x08, 0x18, 'Skull 2 East Lobby')
    create_sprite(0x0057, EnemySprite.Statue, 0x00, 0, 0x0b, 0x18, 'Skull 2 East Lobby')
    create_sprite(0x0058, EnemySprite.MiniMoldorm, 0x00, 0, 0x0c, 0x14, 'Skull Big Chest')
    create_sprite(0x0058, EnemySprite.MiniMoldorm, 0x00, 0, 0x06, 0x16, 'Skull Big Chest')
    create_sprite(0x0058, EnemySprite.Bumper, 0x00, 0, 0x16, 0x16, 'Skull Map Room')
    create_sprite(0x0058, EnemySprite.MiniHelmasaur, 0x00, 0, 0x14, 0x04, 'Skull Pot Circle')
    create_sprite(0x0058, EnemySprite.SparkCW, 0x00, 0, 0x16, 0x06, 'Skull Pot Circle')
    create_sprite(0x0058, EnemySprite.CorrectPullSwitch, 0x00, 0, 0x08, 0x0a)
    create_sprite(0x0058, EnemySprite.HardhatBeetle, 0x00, 0, 0x1b, 0x0b, 'Skull Pot Circle')
    create_sprite(0x0058, EnemySprite.HardhatBeetle, 0x00, 0, 0x16, 0x19, 'Skull Map Room')
    create_sprite(0x0058, EnemySprite.RedBari, 0x00, 0, 0x0a, 0x1a, 'Skull 1 Lobby')
    create_sprite(0x0059, EnemySprite.MiniMoldorm, 0x00, 0, 0x07, 0x10, 'Skull 3 Lobby')
    create_sprite(0x0059, EnemySprite.MiniMoldorm, 0x00, 0, 0x08, 0x16, 'Skull 3 Lobby')
    create_sprite(0x0059, EnemySprite.Bumper, 0x00, 1, 0x14, 0x0f, 'Skull East Bridge')
    create_sprite(0x0059, EnemySprite.Bumper, 0x00, 1, 0x1a, 0x0f, 'Skull East Bridge')
    create_sprite(0x0059, EnemySprite.SpikeBlock, 0x00, 1, 0x1a, 0x0a, 'Skull East Bridge')
    create_sprite(0x0059, EnemySprite.Firesnake, 0x00, 0, 0x08, 0x0b, 'Skull 3 Lobby')
    create_sprite(0x0059, EnemySprite.SpikeBlock, 0x00, 1, 0x15, 0x0d, 'Skull East Bridge')
    create_sprite(0x0059, EnemySprite.SparkCW, 0x00, 1, 0x05, 0x0e, 'Skull 3 Lobby')
    create_sprite(0x0059, EnemySprite.BunnyBeam, 0x00, 1, 0x1a, 0x13, 'Skull East Bridge')
    create_sprite(0x0059, EnemySprite.Gibdo, 0x00, 0, 0x17, 0x14, 'Skull East Bridge')
    create_sprite(0x0059, EnemySprite.Gibdo, 0x00, 1, 0x15, 0x15, 'Skull East Bridge')
    create_sprite(0x0059, EnemySprite.Gibdo, 0x00, 1, 0x1a, 0x15, 'Skull East Bridge')
    create_sprite(0x005a, EnemySprite.HelmasaurKing, 0x00, 0, 0x17, 0x16)
    create_sprite(0x005b, EnemySprite.CrystalSwitch, 0x00, 1, 0x17, 0x0c)
    create_sprite(0x005b, EnemySprite.CrystalSwitch, 0x00, 1, 0x18, 0x13)
    create_sprite(0x005b, EnemySprite.SpikeBlock, 0x00, 1, 0x17, 0x15, 'GT Hidden Spikes')
    create_sprite(0x005b, EnemySprite.GreenEyegoreMimic, 0x00, 1, 0x16, 0x08, 'GT Hidden Spikes')
    create_sprite(0x005b, EnemySprite.RedEyegoreMimic, 0x00, 1, 0x19, 0x08, 'GT Hidden Spikes')
    create_sprite(0x005b, EnemySprite.SpikeBlock, 0x00, 1, 0x14, 0x0e, 'GT Hidden Spikes')
    create_sprite(0x005b, EnemySprite.SpikeBlock, 0x00, 1, 0x1b, 0x10, 'GT Hidden Spikes')
    create_sprite(0x005b, EnemySprite.SpikeBlock, 0x00, 1, 0x17, 0x11, 'GT Hidden Spikes')
    create_sprite(0x005b, EnemySprite.SpikeBlock, 0x00, 1, 0x14, 0x12, 'GT Hidden Spikes')
    create_sprite(0x005c, EnemySprite.WallCannonHorzTop, 0x00, 0, 0x0b, 0x02)
    create_sprite(0x005c, EnemySprite.WallCannonHorzBottom, 0x00, 0, 0x05, 0x0e)
    create_sprite(0x005c, EnemySprite.WallCannonHorzBottom, 0x00, 0, 0x0e, 0x0e)
    create_sprite(0x005c, EnemySprite.Faerie, 0x00, 0, 0x17, 0x18)
    create_sprite(0x005c, EnemySprite.Faerie, 0x00, 0, 0x18, 0x18)
    create_sprite(0x005d, EnemySprite.Stalfos, 0x00, 0, 0x07, 0x05, 'GT Gauntlet 2')
    create_sprite(0x005d, EnemySprite.Beamos, 0x00, 0, 0x08, 0x06, 'GT Gauntlet 2')
    create_sprite(0x005d, EnemySprite.Stalfos, 0x00, 0, 0x03, 0x08, 'GT Gauntlet 2')
    create_sprite(0x005d, EnemySprite.RedZazak, 0x00, 0, 0x15, 0x08, 'GT Gauntlet 1')
    create_sprite(0x005d, EnemySprite.Stalfos, 0x00, 0, 0x17, 0x08, 'GT Gauntlet 1')
    create_sprite(0x005d, EnemySprite.BlueZazak, 0x00, 0, 0x19, 0x08, 'GT Gauntlet 1')
    create_sprite(0x005d, EnemySprite.Stalfos, 0x00, 0, 0x1b, 0x08, 'GT Gauntlet 1')
    create_sprite(0x005d, EnemySprite.Stalfos, 0x00, 0, 0x07, 0x0b, 'GT Gauntlet 2')
    create_sprite(0x005d, EnemySprite.Beamos, 0x00, 0, 0x04, 0x15, 'GT Gauntlet 3')
    create_sprite(0x005d, EnemySprite.BlueZazak, 0x00, 0, 0x0b, 0x15, 'GT Gauntlet 3')
    create_sprite(0x005d, EnemySprite.BlueZazak, 0x00, 0, 0x04, 0x1a, 'GT Gauntlet 3')
    create_sprite(0x005d, EnemySprite.BlueZazak, 0x00, 0, 0x08, 0x1a, 'GT Gauntlet 3')
    create_sprite(0x005d, EnemySprite.Beamos, 0x00, 0, 0x0b, 0x1a, 'GT Gauntlet 3')
    create_sprite(0x005e, 0x0a, SpriteType.Overlord, 0, 0x1b, 0x05)
    create_sprite(0x005e, EnemySprite.Medusa, 0x00, 0, 0x1c, 0x05, 'Ice Falling Square')
    create_sprite(0x005e, EnemySprite.Medusa, 0x00, 0, 0x13, 0x0b, 'Ice Falling Square')
    create_sprite(0x005e, EnemySprite.BigSpike, 0x00, 0, 0x17, 0x14, 'Ice Spike Cross')
    create_sprite(0x005e, EnemySprite.FirebarCW, 0x00, 0, 0x08, 0x18, 'Ice Firebar')
    create_sprite(0x005f, EnemySprite.BlueBari, 0x00, 0, 0x04, 0x18, 'Ice Spike Room')
    create_sprite(0x005f, EnemySprite.BlueBari, 0x00, 0, 0x0b, 0x18, 'Ice Spike Room')
    create_sprite(0x005f, EnemySprite.BlueBari, 0x00, 0, 0x08, 0x1b, 'Ice Spike Room')
    create_sprite(0x0060, EnemySprite.BlueGuard, 0x13, 0, 0x13, 0x08, 'Hyrule Castle West Lobby')
    create_sprite(0x0061, EnemySprite.GreenGuard, 0x01, 0, 0x0c, 0x0e, 'Hyrule Castle Lobby')
    create_sprite(0x0061, EnemySprite.GreenKnifeGuard, 0x00, 0, 0x0d, 0x12, 'Hyrule Castle Lobby')
    create_sprite(0x0061, EnemySprite.GreenKnifeGuard, 0x00, 0, 0x12, 0x12, 'Hyrule Castle Lobby')
    create_sprite(0x0062, EnemySprite.BlueGuard, 0x13, 0, 0x0c, 0x08, 'Hyrule Castle East Lobby')
    create_sprite(0x0062, EnemySprite.GreenGuard, 0x00, 1, 0x0a, 0x0d, 'Hyrule Castle East Lobby')
    create_sprite(0x0062, EnemySprite.GreenGuard, 0x00, 1, 0x11, 0x0e, 'Hyrule Castle East Lobby')
    create_sprite(0x0063, 0x14, SpriteType.Overlord, 0, 0x07, 0x08)
    create_sprite(0x0063, EnemySprite.Beamos, 0x00, 0, 0x07, 0x18, 'Desert Back Lobby')
    create_sprite(0x0064, EnemySprite.Keese, 0x00, 0, 0x05, 0x12, 'Thieves Attic Hint')
    create_sprite(0x0064, EnemySprite.WrongPullSwitch, 0x00, 0, 0x0b, 0x13)
    create_sprite(0x0064, EnemySprite.Keese, 0x00, 0, 0x05, 0x13, 'Thieves Attic Hint')
    create_sprite(0x0064, EnemySprite.BunnyBeam, 0x00, 0, 0x03, 0x16, 'Thieves Attic Hint')
    create_sprite(0x0064, EnemySprite.CricketRat, 0x00, 0, 0x17, 0x17, 'Thieves Cricket Hall Left')
    create_sprite(0x0064, EnemySprite.CricketRat, 0x00, 0, 0x19, 0x19, 'Thieves Cricket Hall Left')
    create_sprite(0x0064, EnemySprite.CricketRat, 0x00, 0, 0x05, 0x1a, 'Thieves Attic')
    create_sprite(0x0064, 0x06, SpriteType.Overlord, 0, 0x09, 0x15)
    create_sprite(0x0064, 0x06, SpriteType.Overlord, 0, 0x07, 0x17)
    create_sprite(0x0064, 0x06, SpriteType.Overlord, 0, 0x09, 0x17)
    create_sprite(0x0064, 0x06, SpriteType.Overlord, 0, 0x0b, 0x17)
    create_sprite(0x0064, 0x06, SpriteType.Overlord, 0, 0x09, 0x19)
    create_sprite(0x0064, 0x06, SpriteType.Overlord, 0, 0x0c, 0x1b)
    create_sprite(0x0065, EnemySprite.CricketRat, 0x00, 0, 0x13, 0x15, 'Thieves Attic Window')
    create_sprite(0x0065, EnemySprite.CricketRat, 0x00, 0, 0x09, 0x17, 'Thieves Cricket Hall Right')
    create_sprite(0x0065, EnemySprite.CricketRat, 0x00, 0, 0x06, 0x18, 'Thieves Cricket Hall Right')
    create_sprite(0x0065, EnemySprite.CricketRat, 0x00, 0, 0x16, 0x19, 'Thieves Attic Window')
    create_sprite(0x0065, EnemySprite.CricketRat, 0x00, 0, 0x16, 0x1c, 'Thieves Attic Window')
    create_sprite(0x0066, EnemySprite.Hover, 0x00, 1, 0x0b, 0x05, 'Swamp Refill')
    create_sprite(0x0066, 0x10, SpriteType.Overlord, 1, 0x04, 0x06)
    create_sprite(0x0066, EnemySprite.BlueBari, 0x00, 0, 0x16, 0x06, 'Swamp Behind Waterfall')
    create_sprite(0x0066, EnemySprite.BlueBari, 0x00, 0, 0x1a, 0x07, 'Swamp Behind Waterfall')
    create_sprite(0x0066, EnemySprite.Waterfall, 0x00, 1, 0x17, 0x14, 'Swamp Waterfall Room')
    create_sprite(0x0066, 0x10, SpriteType.Overlord, 1, 0x01, 0x16)
    create_sprite(0x0066, EnemySprite.Kyameron, 0x00, 1, 0x0f, 0x16, 'Swamp Waterfall Room')
    create_sprite(0x0066, EnemySprite.Hover, 0x00, 1, 0x13, 0x16, 'Swamp Waterfall Room')
    create_sprite(0x0066, EnemySprite.Hover, 0x00, 1, 0x0b, 0x18, 'Swamp Waterfall Room')
    create_sprite(0x0066, EnemySprite.Hover, 0x00, 1, 0x0d, 0x19, 'Swamp Waterfall Room')
    create_sprite(0x0066, 0x11, SpriteType.Overlord, 1, 0x1e, 0x19)
    create_sprite(0x0066, EnemySprite.Hover, 0x00, 1, 0x17, 0x1b, 'Swamp Waterfall Room')
    create_sprite(0x0067, EnemySprite.Bumper, 0x00, 0, 0x07, 0x0c, 'Skull Left Drop')
    create_sprite(0x0067, EnemySprite.BlueBari, 0x00, 0, 0x04, 0x06, 'Skull Left Drop')
    create_sprite(0x0067, EnemySprite.BlueBari, 0x00, 0, 0x0b, 0x06, 'Skull Left Drop')
    create_sprite(0x0067, EnemySprite.HardhatBeetle, 0x00, 0, 0x05, 0x0c, 'Skull Left Drop')
    create_sprite(0x0067, EnemySprite.HardhatBeetle, 0x00, 0, 0x13, 0x0f, 'Skull Compass Room')
    create_sprite(0x0067, EnemySprite.HardhatBeetle, 0x00, 0, 0x05, 0x13, 'Skull Left Drop')
    create_sprite(0x0067, EnemySprite.HardhatBeetle, 0x00, 0, 0x09, 0x13, 'Skull Left Drop')
    create_sprite(0x0067, EnemySprite.FirebarCW, 0x00, 0, 0x18, 0x14, 'Skull Compass Room')
    create_sprite(0x0067, EnemySprite.FirebarCCW, 0x00, 0, 0x07, 0x17, 'Skull Left Drop')
    create_sprite(0x0067, EnemySprite.HardhatBeetle, 0x00, 0, 0x18, 0x1a, 'Skull Compass Room')
    create_sprite(0x0068, EnemySprite.Bumper, 0x00, 0, 0x0e, 0x07)
    create_sprite(0x0068, EnemySprite.Bumper, 0x00, 0, 0x11, 0x07)
    create_sprite(0x0068, EnemySprite.Bumper, 0x00, 0, 0x0c, 0x0b)
    create_sprite(0x0068, EnemySprite.Bumper, 0x00, 0, 0x13, 0x0b)
    create_sprite(0x0068, EnemySprite.Gibdo, 0x00, 0, 0x14, 0x08, 'Skull Compass Room')
    create_sprite(0x0068, 0x09, SpriteType.Overlord, 0, 0x0f, 0x0f)
    create_sprite(0x0068, EnemySprite.Gibdo, 0x00, 0, 0x0e, 0x12, 'Skull Compass Room')
    create_sprite(0x0068, EnemySprite.Gibdo, 0x00, 0, 0x12, 0x12, 'Skull Compass Room')
    create_sprite(0x006a, EnemySprite.Terrorpin, 0x00, 0, 0x17, 0x0a, 'PoD Dark Alley')
    create_sprite(0x006a, EnemySprite.Terrorpin, 0x00, 0, 0x18, 0x0a, 'PoD Dark Alley')
    create_sprite(0x006a, EnemySprite.AntiFairy, 0x00, 0, 0x14, 0x0b, 'PoD Dark Basement')
    create_sprite(0x006a, EnemySprite.AntiFairy, 0x00, 0, 0x1c, 0x0b, 'PoD Dark Basement')
    create_sprite(0x006a, EnemySprite.Terrorpin, 0x00, 0, 0x17, 0x0e, 'PoD Dark Alley')
    create_sprite(0x006a, EnemySprite.Terrorpin, 0x00, 0, 0x18, 0x0e, 'PoD Dark Alley')
    create_sprite(0x006b, EnemySprite.CrystalSwitch, 0x00, 0, 0x07, 0x04)
    create_sprite(0x006b, EnemySprite.CrystalSwitch, 0x00, 0, 0x0b, 0x04)
    create_sprite(0x006b, EnemySprite.GreenEyegoreMimic, 0x00, 0, 0x0a, 0x06, 'GT Crystal Paths')
    create_sprite(0x006b, EnemySprite.RedEyegoreMimic, 0x00, 0, 0x06, 0x09, 'GT Crystal Paths')
    create_sprite(0x006b, EnemySprite.AntiFairy, 0x00, 0, 0x0c, 0x0a, 'GT Crystal Paths')
    create_sprite(0x006b, EnemySprite.Statue, 0x00, 0, 0x06, 0x15, 'GT Mimics 1')
    create_sprite(0x006b, EnemySprite.RedEyegoreMimic, 0x00, 0, 0x03, 0x18, 'GT Mimics 1')
    create_sprite(0x006b, EnemySprite.SpikeBlock, 0x00, 0, 0x04, 0x18, 'GT Mimics 1')
    create_sprite(0x006b, EnemySprite.SpikeBlock, 0x00, 0, 0x04, 0x1b, 'GT Mimics 1')
    create_sprite(0x006b, EnemySprite.RedEyegoreMimic, 0x00, 0, 0x0c, 0x1b, 'GT Mimics 1')
    create_sprite(0x006b, EnemySprite.RedEyegoreMimic, 0x00, 0, 0x17, 0x15, 'GT Mimics 2')
    create_sprite(0x006b, EnemySprite.Beamos, 0x00, 0, 0x1b, 0x15, 'GT Mimics 2')
    create_sprite(0x006b, EnemySprite.Beamos, 0x00, 0, 0x14, 0x1b, 'GT Mimics 2')
    create_sprite(0x006b, EnemySprite.RedEyegoreMimic, 0x00, 0, 0x18, 0x1b, 'GT Mimics 2')
    create_sprite(0x006c, EnemySprite.Lanmolas, 0x00, 0, 0x06, 0x17, 'GT Lanmolas 2')
    create_sprite(0x006c, EnemySprite.Lanmolas, 0x00, 0, 0x09, 0x17, 'GT Lanmolas 2')
    create_sprite(0x006c, EnemySprite.Lanmolas, 0x00, 0, 0x07, 0x19, 'GT Lanmolas 2')
    create_sprite(0x006c, EnemySprite.BunnyBeam, 0x00, 0, 0x17, 0x18, 'GT Beam Dash')
    create_sprite(0x006c, EnemySprite.Medusa, 0x00, 0, 0x03, 0x1c, 'GT Lanmolas 2')
    create_sprite(0x006d, EnemySprite.RedZazak, 0x00, 0, 0x05, 0x06, 'GT Gauntlet 4')
    create_sprite(0x006d, EnemySprite.Beamos, 0x00, 0, 0x0b, 0x06, 'GT Gauntlet 4')
    create_sprite(0x006d, EnemySprite.Beamos, 0x00, 0, 0x04, 0x09, 'GT Gauntlet 4')
    create_sprite(0x006d, EnemySprite.RedZazak, 0x00, 0, 0x0a, 0x0b, 'GT Gauntlet 4')
    create_sprite(0x006d, EnemySprite.Medusa, 0x00, 0, 0x04, 0x15, 'GT Gauntlet 5')
    create_sprite(0x006d, EnemySprite.Beamos, 0x00, 0, 0x0b, 0x15, 'GT Gauntlet 5')
    create_sprite(0x006d, EnemySprite.Stalfos, 0x00, 0, 0x05, 0x18, 'GT Gauntlet 5')
    create_sprite(0x006d, EnemySprite.RedZazak, 0x00, 0, 0x0a, 0x18, 'GT Gauntlet 5')
    create_sprite(0x006d, EnemySprite.SparkCCW, 0x00, 0, 0x06, 0x1a, 'GT Gauntlet 5')
    create_sprite(0x006e, EnemySprite.Pengator, 0x00, 0, 0x13, 0x08, 'Ice Pengator Trap')
    create_sprite(0x006e, EnemySprite.Pengator, 0x00, 0, 0x13, 0x09, 'Ice Pengator Trap')
    create_sprite(0x006e, EnemySprite.Pengator, 0x00, 0, 0x13, 0x0a, 'Ice Pengator Trap')
    create_sprite(0x006e, EnemySprite.Pengator, 0x00, 0, 0x13, 0x0b, 'Ice Pengator Trap')
    create_sprite(0x006e, EnemySprite.Pengator, 0x00, 0, 0x13, 0x0c, 'Ice Pengator Trap')
    create_sprite(0x0071, EnemySprite.GreenGuard, 0x00, 1, 0x06, 0x18, 'Hyrule Dungeon Armory Main')
    create_sprite(0x0071, EnemySprite.BlueGuard, 0x15, 1, 0x1a, 0x18, 'Hyrule Dungeon Armory Boomerang', True, 0xe4)
    create_sprite(0x0072, EnemySprite.BlueGuard, 0x05, 0, 0x11, 0x06, 'Hyrule Dungeon Map Room', True, 0xe4)
    create_sprite(0x0072, EnemySprite.BlueGuard, 0x01, 1, 0x0a, 0x19, 'Hyrule Dungeon North Abyss')
    create_sprite(0x0073, EnemySprite.Debirando, 0x00, 0, 0x18, 0x18, 'Desert Sandworm Corner')
    create_sprite(0x0073, EnemySprite.Beamos, 0x00, 0, 0x17, 0x09, 'Desert Bonk Torch')
    create_sprite(0x0073, EnemySprite.Leever, 0x00, 0, 0x15, 0x15, 'Desert Sandworm Corner')
    create_sprite(0x0073, EnemySprite.Leever, 0x00, 0, 0x1b, 0x18, 'Desert Sandworm Corner')
    create_sprite(0x0073, EnemySprite.Beamos, 0x00, 0, 0x07, 0x19, 'Desert Circle of Pots')
    create_sprite(0x0073, EnemySprite.Leever, 0x00, 0, 0x16, 0x1b, 'Desert Sandworm Corner')
    create_sprite(0x0073, EnemySprite.BonkItem, 0x00, 0, 0x14, 0x06)
    create_sprite(0x0074, EnemySprite.Debirando, 0x00, 0, 0x08, 0x18, 'Desert North Hall')
    create_sprite(0x0074, EnemySprite.Debirando, 0x00, 0, 0x17, 0x18, 'Desert North Hall')
    create_sprite(0x0074, EnemySprite.GreenEyegoreMimic, 0x00, 0, 0x0c, 0x05, 'Desert Map Room')
    create_sprite(0x0074, EnemySprite.GreenEyegoreMimic, 0x00, 0, 0x13, 0x05, 'Desert Map Room')
    create_sprite(0x0074, EnemySprite.Leever, 0x00, 0, 0x0c, 0x0a, 'Desert Map Room')
    create_sprite(0x0074, EnemySprite.Leever, 0x00, 0, 0x13, 0x0a, 'Desert Dead End')
    create_sprite(0x0074, EnemySprite.Leever, 0x00, 0, 0x0e, 0x1b, 'Desert Map Room')
    create_sprite(0x0074, EnemySprite.Leever, 0x00, 0, 0x12, 0x1b, 'Desert Dead End')
    create_sprite(0x0075, EnemySprite.Debirando, 0x00, 0, 0x08, 0x07, 'Desert Trap Room')
    create_sprite(0x0075, EnemySprite.Debirando, 0x00, 0, 0x04, 0x1b, 'Desert Arrow Pot Corner')
    create_sprite(0x0075, EnemySprite.Leever, 0x00, 0, 0x06, 0x05, 'Desert Trap Room')
    create_sprite(0x0075, EnemySprite.Leever, 0x00, 0, 0x0a, 0x05, 'Desert Trap Room')
    create_sprite(0x0075, EnemySprite.Leever, 0x00, 0, 0x06, 0x0a, 'Desert Trap Room')
    create_sprite(0x0075, EnemySprite.Leever, 0x00, 0, 0x0a, 0x0a, 'Desert Trap Room')
    create_sprite(0x0075, EnemySprite.WallCannonVertLeft, 0x00, 0, 0x11, 0x0b)
    create_sprite(0x0075, EnemySprite.WallCannonVertRight, 0x00, 0, 0x1e, 0x0b)
    create_sprite(0x0075, EnemySprite.Leever, 0x00, 0, 0x07, 0x19, 'Desert Arrow Pot Corner')
    create_sprite(0x0075, EnemySprite.Leever, 0x00, 0, 0x09, 0x19, 'Desert Arrow Pot Corner')
    create_sprite(0x0076, EnemySprite.WaterSwitch, 0x00, 0, 0x19, 0x03)
    create_sprite(0x0076, EnemySprite.Hover, 0x00, 0, 0x07, 0x0a, 'Swamp Basement Shallows')
    create_sprite(0x0076, EnemySprite.Kyameron, 0x00, 0, 0x07, 0x0f, 'Swamp Basement Shallows')
    create_sprite(0x0076, EnemySprite.Hover, 0x00, 0, 0x08, 0x11, 'Swamp Basement Shallows')
    create_sprite(0x0076, EnemySprite.Blob, 0x00, 0, 0x1b, 0x19, 'Swamp Flooded Room')
    create_sprite(0x0076, 0x13, SpriteType.Overlord, 0, 0x08, 0x1c)
    create_sprite(0x0076, EnemySprite.BlueBari, 0x00, 0, 0x1b, 0x1c, 'Swamp Flooded Room')
    create_sprite(0x0077, EnemySprite.MiniMoldorm, 0x00, 1, 0x0b, 0x09, 'Hera Back')
    create_sprite(0x0077, EnemySprite.CrystalSwitch, 0x00, 1, 0x10, 0x18)
    create_sprite(0x0077, EnemySprite.CrystalSwitch, 0x00, 1, 0x09, 0x1a)
    create_sprite(0x0077, EnemySprite.CrystalSwitch, 0x00, 1, 0x16, 0x1a)
    create_sprite(0x0077, EnemySprite.Kondongo, 0x00, 1, 0x07, 0x0a, 'Hera Back')
    create_sprite(0x0077, EnemySprite.Kondongo, 0x00, 1, 0x17, 0x0a, 'Hera Back')
    create_sprite(0x007b, EnemySprite.BlueBari, 0x00, 0, 0x0b, 0x07, 'GT Conveyor Star Pits')
    create_sprite(0x007b, EnemySprite.BlueBari, 0x00, 0, 0x16, 0x09, 'GT Conveyor Star Pits')
    create_sprite(0x007b, EnemySprite.FourWayShooter, 0x00, 0, 0x04, 0x15, 'GT DMs Room')
    create_sprite(0x007b, EnemySprite.Stalfos, 0x00, 0, 0x0b, 0x15, 'GT DMs Room')
    create_sprite(0x007b, EnemySprite.Stalfos, 0x00, 0, 0x07, 0x17, 'GT DMs Room')
    create_sprite(0x007b, EnemySprite.FourWayShooter, 0x00, 0, 0x09, 0x17, 'GT DMs Room')
    create_sprite(0x007b, EnemySprite.Statue, 0x00, 0, 0x13, 0x18, 'GT Hidden Star')
    create_sprite(0x007b, EnemySprite.HardhatBeetle, 0x00, 0, 0x17, 0x18, 'GT Hidden Star')
    create_sprite(0x007b, EnemySprite.Stalfos, 0x00, 0, 0x09, 0x19, 'GT DMs Room')
    create_sprite(0x007b, EnemySprite.FourWayShooter, 0x00, 0, 0x05, 0x1a, 'GT DMs Room')
    create_sprite(0x007b, EnemySprite.FourWayShooter, 0x00, 0, 0x0b, 0x1b, 'GT DMs Room')
    create_sprite(0x007c, EnemySprite.MiniMoldorm, 0x00, 0, 0x19, 0x1c, 'GT Randomizer Room')
    create_sprite(0x007c, EnemySprite.FirebarCCW, 0x00, 0, 0x06, 0x0c, 'GT Falling Bridge')
    create_sprite(0x007c, EnemySprite.SpikeBlock, 0x00, 0, 0x07, 0x10, 'GT Falling Bridge')
    create_sprite(0x007c, EnemySprite.FirebarCW, 0x00, 0, 0x09, 0x14, 'GT Falling Bridge')
    create_sprite(0x007c, EnemySprite.HardhatBeetle, 0x00, 0, 0x0b, 0x18, 'GT Falling Bridge')
    create_sprite(0x007c, EnemySprite.BlueBari, 0x00, 0, 0x17, 0x18, 'GT Randomizer Room')
    create_sprite(0x007c, 0x0b, SpriteType.Overlord, 0, 0x07, 0x1a)
    create_sprite(0x007d, EnemySprite.Firesnake, 0x00, 0, 0x11, 0x06, 'GT Firesnake Room')
    create_sprite(0x007d, EnemySprite.Firesnake, 0x00, 0, 0x11, 0x08, 'GT Firesnake Room')
    create_sprite(0x007d, EnemySprite.Firesnake, 0x00, 0, 0x11, 0x0a, 'GT Firesnake Room')
    create_sprite(0x007d, EnemySprite.Firesnake, 0x00, 0, 0x11, 0x0c, 'GT Firesnake Room')
    create_sprite(0x007d, EnemySprite.Stalfos, 0x00, 0, 0x15, 0x16, 'GT Petting Zoo')
    create_sprite(0x007d, EnemySprite.FourWayShooter, 0x00, 0, 0x18, 0x17, 'GT Petting Zoo')
    create_sprite(0x007d, EnemySprite.Firesnake, 0x00, 0, 0x1c, 0x19, 'GT Petting Zoo')
    create_sprite(0x007d, EnemySprite.MiniHelmasaur, 0x00, 0, 0x14, 0x1a, 'GT Petting Zoo')
    create_sprite(0x007d, EnemySprite.RedBari, 0x00, 0, 0x17, 0x1a, 'GT Petting Zoo')
    create_sprite(0x007d, EnemySprite.Firesnake, 0x00, 0, 0x0a, 0x1c, 'GT Warp Maze - Main Rails')
    create_sprite(0x007d, EnemySprite.HardhatBeetle, 0x00, 0, 0x1b, 0x1c, 'GT Petting Zoo')
    create_sprite(0x007e, EnemySprite.Bumper, 0x00, 0, 0x17, 0x11, 'Ice Tall Hint')
    create_sprite(0x007e, EnemySprite.FirebarCCW, 0x00, 0, 0x18, 0x0e, 'Ice Tall Hint')
    create_sprite(0x007e, EnemySprite.Pengator, 0x00, 0, 0x14, 0x0f, 'Ice Tall Hint')
    create_sprite(0x007e, EnemySprite.Freezor, 0x00, 0, 0x07, 0x12, 'Ice Freezors')
    create_sprite(0x007e, EnemySprite.Freezor, 0x00, 0, 0x0a, 0x12, 'Ice Freezors')
    create_sprite(0x007e, EnemySprite.Pengator, 0x00, 0, 0x1b, 0x16, 'Ice Tall Hint')
    create_sprite(0x007e, EnemySprite.FirebarCCW, 0x00, 0, 0x17, 0x17, 'Ice Tall Hint')
    create_sprite(0x007f, EnemySprite.RedBari, 0x00, 0, 0x06, 0x07, 'Ice Hookshot Ledge')
    create_sprite(0x007f, EnemySprite.RedBari, 0x00, 0, 0x08, 0x07, 'Ice Hookshot Ledge')
    create_sprite(0x007f, EnemySprite.RedBari, 0x00, 0, 0x0a, 0x08, 'Ice Hookshot Ledge')
    create_sprite(0x007f, EnemySprite.RedBari, 0x00, 0, 0x07, 0x09, 'Ice Hookshot Ledge')
    create_sprite(0x007f, EnemySprite.BigSpike, 0x00, 0, 0x0b, 0x14, 'Ice Spikeball')
    create_sprite(0x007f, EnemySprite.BigSpike, 0x00, 0, 0x03, 0x17, 'Ice Spikeball')
    create_sprite(0x007f, EnemySprite.BigSpike, 0x00, 0, 0x0b, 0x19, 'Ice Spikeball')
    create_sprite(0x007f, EnemySprite.BigSpike, 0x00, 0, 0x03, 0x1b, 'Ice Spikeball')
    create_sprite(0x0080, EnemySprite.Zelda, 0x00, 0, 0x16, 0x03, 'Hyrule Dungeon Cell')
    create_sprite(0x0080, EnemySprite.GreenGuard, 0x00, 0, 0x07, 0x09, 'Hyrule Dungeon Cellblock')
    create_sprite(0x0080, EnemySprite.BallNChain, 0x00, 0, 0x1a, 0x09, 'Hyrule Dungeon Cellblock', True, 0xe5)
    create_sprite(0x0081, EnemySprite.GreenGuard, 0x1b, 1, 0x0b, 0x0b, 'Hyrule Dungeon Guardroom')
    create_sprite(0x0081, EnemySprite.GreenGuard, 0x03, 1, 0x0e, 0x0b, 'Hyrule Dungeon Guardroom')
    create_sprite(0x0082, EnemySprite.BlueGuard, 0x1b, 1, 0x09, 0x05, 'Hyrule Dungeon South Abyss')
    create_sprite(0x0082, EnemySprite.BlueGuard, 0x03, 1, 0x10, 0x06, 'Hyrule Dungeon South Abyss')
    create_sprite(0x0082, EnemySprite.BlueGuard, 0x03, 1, 0x15, 0x11, 'Hyrule Dungeon South Abyss')
    create_sprite(0x0083, EnemySprite.DebirandoPit, 0x00, 0, 0x1b, 0x08, 'Desert West Wing')
    create_sprite(0x0083, EnemySprite.DebirandoPit, 0x00, 0, 0x14, 0x10, 'Desert West Wing')
    create_sprite(0x0083, EnemySprite.Leever, 0x00, 0, 0x14, 0x05, 'Desert West Wing')
    create_sprite(0x0083, EnemySprite.Faerie, 0x00, 0, 0x07, 0x06)
    create_sprite(0x0083, EnemySprite.Faerie, 0x00, 0, 0x08, 0x08)
    create_sprite(0x0083, EnemySprite.Leever, 0x00, 0, 0x1b, 0x0b, 'Desert West Wing')
    create_sprite(0x0083, EnemySprite.Leever, 0x00, 0, 0x17, 0x10, 'Desert West Wing')
    create_sprite(0x0083, EnemySprite.Beamos, 0x00, 0, 0x08, 0x17, 'Desert West Lobby')
    create_sprite(0x0083, EnemySprite.Leever, 0x00, 0, 0x18, 0x18, 'Desert West Wing')
    create_sprite(0x0083, EnemySprite.Leever, 0x00, 0, 0x14, 0x1b, 'Desert West Wing')
    create_sprite(0x0084, EnemySprite.Leever, 0x00, 0, 0x03, 0x05, 'Desert Left Alcove')
    create_sprite(0x0084, EnemySprite.Leever, 0x00, 0, 0x1b, 0x05, 'Desert Right Alcove')
    create_sprite(0x0084, EnemySprite.Beamos, 0x00, 0, 0x0f, 0x07, 'Desert Main Lobby')
    create_sprite(0x0084, EnemySprite.Leever, 0x00, 0, 0x09, 0x12, 'Desert Main Lobby')
    create_sprite(0x0084, EnemySprite.Leever, 0x00, 0, 0x15, 0x12, 'Desert Main Lobby')
    create_sprite(0x0084, EnemySprite.Leever, 0x00, 0, 0x09, 0x1b, 'Desert Main Lobby')
    create_sprite(0x0084, EnemySprite.Leever, 0x00, 0, 0x15, 0x1b, 'Desert Main Lobby')
    create_sprite(0x0085, EnemySprite.DebirandoPit, 0x00, 0, 0x07, 0x0e, 'Desert East Wing')
    create_sprite(0x0085, EnemySprite.Debirando, 0x00, 0, 0x09, 0x1b, 'Desert East Wing')
    create_sprite(0x0085, EnemySprite.Popo2, 0x00, 0, 0x14, 0x05, 'Desert Compass Room')
    create_sprite(0x0085, EnemySprite.Popo2, 0x00, 0, 0x1b, 0x05, 'Desert Compass Room')
    create_sprite(0x0085, EnemySprite.Popo2, 0x00, 0, 0x16, 0x08, 'Desert Compass Room')
    create_sprite(0x0085, EnemySprite.Beamos, 0x00, 0, 0x18, 0x0a, 'Desert Compass Room')
    create_sprite(0x0085, EnemySprite.Leever, 0x00, 0, 0x03, 0x0e, 'Desert East Wing')
    create_sprite(0x0085, EnemySprite.Leever, 0x00, 0, 0x0c, 0x15, 'Desert East Wing')
    create_sprite(0x0085, EnemySprite.Beamos, 0x00, 0, 0x18, 0x18, 'Desert East Lobby')
    create_sprite(0x0085, EnemySprite.Leever, 0x00, 0, 0x07, 0x1c, 'Desert East Wing')
    create_sprite(0x0087, EnemySprite.MiniMoldorm, 0x00, 0, 0x14, 0x05, 'Hera Tridorm')
    create_sprite(0x0087, EnemySprite.MiniMoldorm, 0x00, 0, 0x1a, 0x07, 'Hera Tridorm')
    create_sprite(0x0087, EnemySprite.MiniMoldorm, 0x00, 0, 0x13, 0x0b, 'Hera Tridorm')
    create_sprite(0x0087, EnemySprite.MiniMoldorm, 0x00, 0, 0x06, 0x19, 'Hera Basement Cage')
    create_sprite(0x0087, 0x14, SpriteType.Overlord, 0, 0x07, 0x08)
    create_sprite(0x0087, EnemySprite.CrystalSwitch, 0x00, 0, 0x17, 0x04)
    create_sprite(0x0087, EnemySprite.CrystalSwitch, 0x00, 0, 0x03, 0x0c)
    create_sprite(0x0087, EnemySprite.CrystalSwitch, 0x00, 0, 0x04, 0x15)
    create_sprite(0x0087, EnemySprite.Stalfos, 0x00, 0, 0x0b, 0x17, 'Hera Basement Cage')
    create_sprite(0x0087, EnemySprite.Stalfos, 0x00, 0, 0x19, 0x18, 'Hera Torches')
    create_sprite(0x0087, EnemySprite.Stalfos, 0x00, 0, 0x04, 0x19, 'Hera Basement Cage')
    create_sprite(0x0087, EnemySprite.SmallKey, 0x00, 0, 0x08, 0x1a, 'Hera Basement Cage')
    create_sprite(0x0087, EnemySprite.Stalfos, 0x00, 0, 0x15, 0x1c, 'Hera Torches')
    create_sprite(0x0089, EnemySprite.Faerie, 0x00, 0, 0x10, 0x0a)
    create_sprite(0x0089, EnemySprite.Faerie, 0x00, 0, 0x0f, 0x0b)
    create_sprite(0x008b, EnemySprite.Bumper, 0x00, 0, 0x15, 0x07, 'GT Conveyor Cross')
    create_sprite(0x008b, EnemySprite.CrystalSwitch, 0x00, 0, 0x04, 0x18, 'GT Hookshot South Platform')
    create_sprite(0x008b, EnemySprite.CrystalSwitch, 0x00, 0, 0x0b, 0x18, 'GT Hookshot South Platform')
    create_sprite(0x008b, EnemySprite.BlueBari, 0x00, 0, 0x1a, 0x04, 'GT Conveyor Cross')
    create_sprite(0x008b, EnemySprite.SpikeBlock, 0x00, 0, 0x03, 0x12, 'GT Hookshot Mid Platform')  # todo: boots may be sufficient - special rule?
    create_sprite(0x008b, EnemySprite.Stalfos, 0x00, 0, 0x07, 0x18, 'GT Hookshot South Platform')
    create_sprite(0x008b, EnemySprite.FirebarCW, 0x00, 0, 0x18, 0x18, 'GT Map Room')
    create_sprite(0x008b, EnemySprite.FirebarCCW, 0x00, 0, 0x18, 0x18, 'GT Map Room')
    create_sprite(0x008c, EnemySprite.WrongPullSwitch, 0x00, 0, 0x1a, 0x03, 'GT Hope Room')
    create_sprite(0x008c, 0x1a, SpriteType.Overlord, 0, 0x18, 0x05)
    create_sprite(0x008c, 0x1a, SpriteType.Overlord, 0, 0x15, 0x06)
    create_sprite(0x008c, 0x1a, SpriteType.Overlord, 0, 0x1a, 0x06)
    create_sprite(0x008c, 0x1a, SpriteType.Overlord, 0, 0x15, 0x0a)
    create_sprite(0x008c, 0x1a, SpriteType.Overlord, 0, 0x1a, 0x0a)
    create_sprite(0x008c, EnemySprite.SparkCW, 0x00, 0, 0x08, 0x08, 'GT Bob\'s Torch',)
    create_sprite(0x008c, EnemySprite.SpikeBlock, 0x00, 0, 0x17, 0x08, 'GT Hope Room')
    create_sprite(0x008c, EnemySprite.Stalfos, 0x00, 0, 0x0b, 0x09, 'GT Bob\'s Torch')
    create_sprite(0x008c, EnemySprite.Stalfos, 0x00, 0, 0x03, 0x0b, 'GT Bob\'s Torch')
    create_sprite(0x008c, EnemySprite.Firesnake, 0x00, 0, 0x05, 0x17, 'GT Big Chest')
    create_sprite(0x008c, EnemySprite.SparkCW, 0x00, 0, 0x16, 0x17, 'GT Bob\'s Room')
    create_sprite(0x008c, EnemySprite.AntiFairy, 0x00, 0, 0x14, 0x18, 'GT Bob\'s Room')
    create_sprite(0x008c, EnemySprite.Firesnake, 0x00, 0, 0x0b, 0x1b, 'GT Big Chest')
    create_sprite(0x008c, EnemySprite.AntiFairy, 0x00, 0, 0x1a, 0x1c, 'GT Bob\'s Room')
    create_sprite(0x008c, EnemySprite.BonkItem, 0x00, 0, 0x09, 0x07)
    create_sprite(0x008d, 0x14, SpriteType.Overlord, 0, 0x07, 0x08)
    create_sprite(0x008d, EnemySprite.FourWayShooter, 0x00, 0, 0x07, 0x04, 'GT Tile Room')
    create_sprite(0x008d, EnemySprite.AntiFairy, 0x00, 0, 0x09, 0x08, 'GT Tile Room')
    create_sprite(0x008d, EnemySprite.BunnyBeam, 0x00, 0, 0x08, 0x09, 'GT Tile Room')
    create_sprite(0x008d, EnemySprite.FourWayShooter, 0x00, 0, 0x09, 0x0c, 'GT Tile Room')
    create_sprite(0x008d, EnemySprite.Gibdo, 0x00, 0, 0x13, 0x0d, 'GT Speed Torch Upper')
    create_sprite(0x008d, 0x09, SpriteType.Overlord, 0, 0x0f, 0x0f)
    create_sprite(0x008d, EnemySprite.SpikeBlock, 0x00, 0, 0x17, 0x10, 'GT Speed Torch')
    create_sprite(0x008d, EnemySprite.Stalfos, 0x00, 0, 0x17, 0x14, 'GT Speed Torch')
    create_sprite(0x008d, EnemySprite.FirebarCW, 0x00, 0, 0x07, 0x18, 'GT Pots n Blocks')
    create_sprite(0x008d, EnemySprite.BlueBari, 0x00, 0, 0x14, 0x1b, 'GT Speed Torch')
    create_sprite(0x008d, EnemySprite.Medusa, 0x00, 0, 0x13, 0x1c, 'GT Speed Torch')
    create_sprite(0x008d, EnemySprite.BlueBari, 0x00, 0, 0x14, 0x1c, 'GT Speed Torch')
    create_sprite(0x008e, EnemySprite.Freezor, 0x00, 0, 0x1b, 0x02, 'Ice Lonely Freezor')
    create_sprite(0x008e, EnemySprite.Blob, 0x00, 0, 0x18, 0x05, 'Ice Lonely Freezor')
    create_sprite(0x008e, EnemySprite.BunnyBeam, 0x00, 0, 0x14, 0x06, 'Ice Lonely Freezor')
    create_sprite(0x008e, EnemySprite.Blob, 0x00, 0, 0x1b, 0x08, 'Ice Lonely Freezor')
    create_sprite(0x008e, EnemySprite.Blob, 0x00, 0, 0x14, 0x09, 'Ice Lonely Freezor')
    create_sprite(0x008e, EnemySprite.Blob, 0x00, 0, 0x16, 0x0a, 'Ice Lonely Freezor')
    create_sprite(0x008e, EnemySprite.Blob, 0x00, 0, 0x14, 0x0b, 'Ice Lonely Freezor')
    create_sprite(0x008e, EnemySprite.Blob, 0x00, 0, 0x18, 0x0b, 'Ice Lonely Freezor')
    create_sprite(0x0090, EnemySprite.Vitreous, 0x00, 0, 0x07, 0x15)
    create_sprite(0x0091, EnemySprite.CrystalSwitch, 0x00, 0, 0x18, 0x04, 'Mire Falling Foes')
    create_sprite(0x0091, EnemySprite.SpikeBlock, 0x00, 0, 0x1b, 0x0e, 'Mire Falling Foes')
    create_sprite(0x0091, 0x08, SpriteType.Overlord, 0, 0x17, 0x0f)
    create_sprite(0x0091, EnemySprite.Medusa, 0x00, 0, 0x17, 0x12, 'Mire Falling Foes')
    create_sprite(0x0091, EnemySprite.BunnyBeam, 0x00, 0, 0x18, 0x12, 'Mire Falling Foes')
    create_sprite(0x0091, EnemySprite.AntiFairy, 0x00, 0, 0x19, 0x12, 'Mire Falling Foes')
    create_sprite(0x0091, EnemySprite.AntiFairy, 0x00, 0, 0x18, 0x18, 'Mire Falling Foes')
    create_sprite(0x0092, EnemySprite.CrystalSwitch, 0x00, 0, 0x18, 0x09, 'Mire Tall Dark and Roomy')
    create_sprite(0x0092, EnemySprite.CrystalSwitch, 0x00, 0, 0x03, 0x0c)
    create_sprite(0x0092, EnemySprite.AntiFairy, 0x00, 0, 0x18, 0x04, 'Mire Tall Dark and Roomy')
    create_sprite(0x0092, EnemySprite.Medusa, 0x00, 0, 0x0b, 0x05, 'Mire Shooter Rupees')
    create_sprite(0x0092, EnemySprite.AntiFairy, 0x00, 0, 0x09, 0x08, 'Mire Shooter Rupees')
    create_sprite(0x0092, EnemySprite.Medusa, 0x00, 0, 0x17, 0x09, 'Mire Tall Dark and Roomy')
    create_sprite(0x0092, EnemySprite.FourWayShooter, 0x00, 0, 0x15, 0x0f, 'Mire Tall Dark and Roomy')
    create_sprite(0x0092, 0x16, SpriteType.Overlord, 0, 0x07, 0x12)
    create_sprite(0x0092, EnemySprite.SpikeBlock, 0x00, 0, 0x19, 0x12, 'Mire Tall Dark and Roomy')
    create_sprite(0x0092, EnemySprite.AntiFairy, 0x00, 0, 0x03, 0x14, 'Mire Crystal Right')
    create_sprite(0x0092, EnemySprite.Stalfos, 0x00, 0, 0x0a, 0x16, 'Mire Crystal Mid')
    create_sprite(0x0092, EnemySprite.AntiFairy, 0x00, 0, 0x03, 0x1b, 'Mire Crystal Right')
    create_sprite(0x0093, EnemySprite.Medusa, 0x00, 0, 0x09, 0x09)
    create_sprite(0x0093, EnemySprite.Medusa, 0x00, 0, 0x16, 0x09)
    create_sprite(0x0093, EnemySprite.Medusa, 0x00, 0, 0x0c, 0x0c)
    create_sprite(0x0093, EnemySprite.Medusa, 0x00, 0, 0x13, 0x0c)
    create_sprite(0x0093, EnemySprite.Blob, 0x00, 0, 0x17, 0x0c, 'Mire Dark Shooters')
    create_sprite(0x0093, EnemySprite.Stalfos, 0x00, 0, 0x04, 0x15, 'Mire Block X')
    create_sprite(0x0093, EnemySprite.Stalfos, 0x00, 0, 0x0c, 0x1c, 'Mire Block X')
    create_sprite(0x0093, EnemySprite.AntiFairy, 0x00, 0, 0x04, 0x1c, 'Mire Block X')
    create_sprite(0x0095, EnemySprite.RedSpearGuard, 0x00, 0, 0x16, 0x0c, 'GT Conveyor Bridge')
    create_sprite(0x0095, EnemySprite.RedSpearGuard, 0x00, 0, 0x17, 0x0c, 'GT Conveyor Bridge')
    create_sprite(0x0095, EnemySprite.RedSpearGuard, 0x00, 0, 0x18, 0x0c, 'GT Conveyor Bridge')
    create_sprite(0x0095, EnemySprite.RedSpearGuard, 0x00, 0, 0x19, 0x0c, 'GT Conveyor Bridge')
    create_sprite(0x0095, 0x0b, SpriteType.Overlord, 0, 0x17, 0x1a)
    create_sprite(0x0096, EnemySprite.FirebarCW, 0x00, 0, 0x08, 0x0b, 'GT Torch Cross')
    create_sprite(0x0096, EnemySprite.LaserEyeRight, 0x00, 0, 0x1e, 0x15)
    create_sprite(0x0096, EnemySprite.LaserEyeRight, 0x00, 0, 0x1e, 0x17)
    create_sprite(0x0096, EnemySprite.LaserEyeRight, 0x00, 0, 0x1e, 0x19)
    create_sprite(0x0096, EnemySprite.LaserEyeRight, 0x00, 0, 0x1e, 0x1b)
    create_sprite(0x0097, 0x15, SpriteType.Overlord, 0, 0x0f, 0x0f)
    create_sprite(0x0098, EnemySprite.Blob, 0x00, 0, 0x10, 0x13, 'Mire Lobby')
    create_sprite(0x0098, EnemySprite.Blob, 0x00, 0, 0x09, 0x14, 'Mire Lobby')
    create_sprite(0x0098, EnemySprite.Blob, 0x00, 0, 0x0c, 0x14, 'Mire Lobby')
    create_sprite(0x0098, EnemySprite.Blob, 0x00, 0, 0x0f, 0x14, 'Mire Lobby')
    create_sprite(0x0098, EnemySprite.Blob, 0x00, 0, 0x08, 0x17, 'Mire Lobby')
    create_sprite(0x0099, EnemySprite.AntiFairy, 0x00, 0, 0x15, 0x06, 'Eastern Rupees')
    create_sprite(0x0099, EnemySprite.AntiFairy, 0x00, 0, 0x1a, 0x08, 'Eastern Rupees')
    create_sprite(0x0099, EnemySprite.GreenEyegoreMimic, 0x00, 0, 0x0e, 0x17, 'Eastern Darkness')
    create_sprite(0x0099, EnemySprite.GreenEyegoreMimic, 0x00, 0, 0x11, 0x17, 'Eastern Darkness', True, 0xe4)
    create_sprite(0x0099, EnemySprite.Popo, 0x00, 0, 0x0d, 0x18, 'Eastern Darkness')
    create_sprite(0x0099, EnemySprite.Popo, 0x00, 0, 0x12, 0x18, 'Eastern Darkness')
    create_sprite(0x0099, EnemySprite.Popo2, 0x00, 0, 0x0e, 0x19, 'Eastern Darkness')
    create_sprite(0x0099, EnemySprite.Popo2, 0x00, 0, 0x0f, 0x19, 'Eastern Darkness')
    create_sprite(0x0099, EnemySprite.Popo2, 0x00, 0, 0x10, 0x19, 'Eastern Darkness')
    create_sprite(0x0099, EnemySprite.Popo2, 0x00, 0, 0x11, 0x19, 'Eastern Darkness')
    create_sprite(0x009b, EnemySprite.CrystalSwitch, 0x00, 0, 0x06, 0x08)
    create_sprite(0x009b, EnemySprite.CrystalSwitch, 0x00, 0, 0x07, 0x08)
    create_sprite(0x009b, EnemySprite.CrystalSwitch, 0x00, 0, 0x14, 0x08)
    create_sprite(0x009b, EnemySprite.SpikeBlock, 0x00, 0, 0x1c, 0x05, 'GT Spike Crystal Right')
    create_sprite(0x009b, EnemySprite.SpikeBlock, 0x00, 0, 0x1c, 0x06, 'GT Spike Crystal Right')
    create_sprite(0x009b, EnemySprite.SpikeBlock, 0x00, 0, 0x1c, 0x07, 'GT Spike Crystal Right')
    create_sprite(0x009b, EnemySprite.FourWayShooter, 0x00, 0, 0x03, 0x08)
    create_sprite(0x009b, EnemySprite.SpikeBlock, 0x00, 0, 0x1c, 0x08, 'GT Spike Crystal Right')
    create_sprite(0x009b, EnemySprite.SpikeBlock, 0x00, 0, 0x1c, 0x09, 'GT Spike Crystal Right')
    create_sprite(0x009b, EnemySprite.SpikeBlock, 0x00, 0, 0x1c, 0x0a, 'GT Spike Crystal Right')
    create_sprite(0x009b, EnemySprite.SpikeBlock, 0x00, 0, 0x1c, 0x0b, 'GT Spike Crystal Right')
    create_sprite(0x009b, EnemySprite.HardhatBeetle, 0x00, 0, 0x17, 0x1a, 'GT Warp Maze - Pit Section')
    create_sprite(0x009b, EnemySprite.HardhatBeetle, 0x00, 0, 0x13, 0x1b, 'GT Warp Maze - Pit Section')
    create_sprite(0x009c, EnemySprite.HardhatBeetle, 0x00, 0, 0x13, 0x09, 'GT Invisible Catwalk')
    create_sprite(0x009c, EnemySprite.MiniHelmasaur, 0x00, 0, 0x0b, 0x0a, 'GT Invisible Catwalk')
    create_sprite(0x009c, EnemySprite.HardhatBeetle, 0x00, 0, 0x11, 0x0f, 'GT Invisible Catwalk')
    create_sprite(0x009c, EnemySprite.HardhatBeetle, 0x00, 0, 0x17, 0x0e, 'GT Invisible Catwalk')
    create_sprite(0x009c, EnemySprite.HardhatBeetle, 0x00, 0, 0x0d, 0x12, 'GT Invisible Catwalk')
    create_sprite(0x009c, EnemySprite.HardhatBeetle, 0x00, 0, 0x09, 0x13, 'GT Invisible Catwalk')
    create_sprite(0x009c, EnemySprite.Firesnake, 0x00, 0, 0x0f, 0x1c, 'GT Invisible Catwalk')
    create_sprite(0x009d, EnemySprite.CrystalSwitch, 0x00, 0, 0x1c, 0x06)
    create_sprite(0x009d, EnemySprite.HardhatBeetle, 0x00, 0, 0x06, 0x04, 'GT Compass Room')
    create_sprite(0x009d, EnemySprite.Gibdo, 0x00, 0, 0x14, 0x04, 'GT Crystal Conveyor Left')
    create_sprite(0x009d, EnemySprite.Gibdo, 0x00, 0, 0x18, 0x09, 'GT Crystal Conveyor')
    create_sprite(0x009d, EnemySprite.HardhatBeetle, 0x00, 0, 0x05, 0x0c, 'GT Compass Room')
    create_sprite(0x009d, EnemySprite.Gibdo, 0x00, 0, 0x13, 0x0c, 'GT Crystal Conveyor Corner')
    create_sprite(0x009d, EnemySprite.BlueBari, 0x00, 0, 0x10, 0x14, 'GT Invisible Bridges')
    create_sprite(0x009d, EnemySprite.BlueBari, 0x00, 0, 0x0b, 0x18, 'GT Invisible Bridges')
    create_sprite(0x009d, EnemySprite.BlueBari, 0x00, 0, 0x11, 0x1c, 'GT Invisible Bridges')
    create_sprite(0x009e, EnemySprite.RedBari, 0x00, 0, 0x18, 0x05, 'Ice Backwards Room')
    create_sprite(0x009e, EnemySprite.RedBari, 0x00, 0, 0x16, 0x08, 'Ice Backwards Room')
    create_sprite(0x009e, EnemySprite.StalfosKnight, 0x00, 0, 0x18, 0x08, 'Ice Backwards Room')
    create_sprite(0x009e, EnemySprite.RedBari, 0x00, 0, 0x19, 0x08, 'Ice Backwards Room')
    create_sprite(0x009e, EnemySprite.Freezor, 0x00, 0, 0x14, 0x12, 'Ice Crystal Left')
    create_sprite(0x009f, EnemySprite.Babasu, 0x00, 0, 0x04, 0x12, 'Ice Many Pots')
    create_sprite(0x009f, EnemySprite.Babasu, 0x00, 0, 0x06, 0x12, 'Ice Many Pots')
    create_sprite(0x009f, EnemySprite.Babasu, 0x00, 0, 0x09, 0x12, 'Ice Many Pots')
    create_sprite(0x009f, EnemySprite.Babasu, 0x00, 0, 0x0b, 0x12, 'Ice Many Pots')
    create_sprite(0x009f, EnemySprite.AntiFairy, 0x00, 0, 0x07, 0x17, 'Ice Many Pots')
    create_sprite(0x009f, EnemySprite.FirebarCW, 0x00, 0, 0x08, 0x18, 'Ice Many Pots')
    create_sprite(0x00a0, EnemySprite.Medusa, 0x00, 0, 0x03, 0x08, 'Mire Antechamber')
    create_sprite(0x00a0, EnemySprite.AntiFairy, 0x00, 0, 0x0e, 0x08, 'Mire Antechamber')
    create_sprite(0x00a0, EnemySprite.Firesnake, 0x00, 0, 0x14, 0x0c, 'Mire Firesnake Skip')
    create_sprite(0x00a1, EnemySprite.CrystalSwitch, 0x00, 0, 0x0a, 0x08)
    create_sprite(0x00a1, EnemySprite.SparkCW, 0x00, 0, 0x18, 0x07, 'Mire Fishbone')
    create_sprite(0x00a1, EnemySprite.SparkCW, 0x00, 0, 0x16, 0x0b, 'Mire Fishbone')
    create_sprite(0x00a1, EnemySprite.Wizzrobe, 0x00, 0, 0x19, 0x10, 'Mire Fishbone')
    create_sprite(0x00a1, EnemySprite.Medusa, 0x00, 0, 0x15, 0x15, 'Mire South Fish')
    create_sprite(0x00a1, EnemySprite.Medusa, 0x00, 0, 0x1a, 0x15, 'Mire South Fish')
    create_sprite(0x00a1, EnemySprite.Stalfos, 0x00, 0, 0x15, 0x19, 'Mire South Fish')
    create_sprite(0x00a1, EnemySprite.BunnyBeam, 0x00, 0, 0x17, 0x19, 'Mire South Fish')
    create_sprite(0x00a1, EnemySprite.Stalfos, 0x00, 0, 0x1b, 0x19, 'Mire South Fish')
    create_sprite(0x00a4, EnemySprite.TrinexxRockHead, 0x00, 0, 0x07, 0x15)
    create_sprite(0x00a4, EnemySprite.TrinexxFireHead, 0x00, 0, 0x07, 0x15)
    create_sprite(0x00a4, EnemySprite.TrinexxIceHead, 0x00, 0, 0x07, 0x15)
    create_sprite(0x00a5, EnemySprite.Wizzrobe, 0x00, 0, 0x16, 0x05, 'GT Wizzrobes 2')
    create_sprite(0x00a5, EnemySprite.Wizzrobe, 0x00, 0, 0x19, 0x05, 'GT Wizzrobes 2')
    create_sprite(0x00a5, EnemySprite.Wizzrobe, 0x00, 0, 0x04, 0x07, 'GT Wizzrobes 1')
    create_sprite(0x00a5, EnemySprite.Wizzrobe, 0x00, 0, 0x0b, 0x07, 'GT Wizzrobes 1')
    create_sprite(0x00a5, EnemySprite.SpikeBlock, 0x00, 0, 0x17, 0x08, 'GT Wizzrobes 2')
    create_sprite(0x00a5, EnemySprite.Wizzrobe, 0x00, 0, 0x15, 0x09, 'GT Wizzrobes 2')
    create_sprite(0x00a5, EnemySprite.Wizzrobe, 0x00, 0, 0x1a, 0x09, 'GT Wizzrobes 2')
    create_sprite(0x00a5, EnemySprite.Wizzrobe, 0x00, 0, 0x08, 0x0a, 'GT Wizzrobes 1')
    create_sprite(0x00a5, EnemySprite.LaserEyeTop, 0x00, 0, 0x0c, 0x12)
    create_sprite(0x00a5, EnemySprite.LaserEyeTop, 0x00, 0, 0x12, 0x12)
    create_sprite(0x00a5, EnemySprite.RedSpearGuard, 0x00, 0, 0x12, 0x17, 'GT Dashing Bridge')
    create_sprite(0x00a5, EnemySprite.BlueGuard, 0x00, 0, 0x13, 0x18, 'GT Dashing Bridge')
    create_sprite(0x00a6, 0x15, SpriteType.Overlord, 0, 0x0f, 0x0f)
    create_sprite(0x00a6, EnemySprite.AntiFairy, 0x00, 0, 0x0c, 0x0e, 'GT Moldorm Pit')
    create_sprite(0x00a7, EnemySprite.Faerie, 0x00, 0, 0x06, 0x08)
    create_sprite(0x00a7, EnemySprite.Faerie, 0x00, 0, 0x06, 0x09)
    create_sprite(0x00a8, EnemySprite.Stalfos, 0x00, 0, 0x16, 0x0e, 'Eastern West Wing')
    create_sprite(0x00a8, EnemySprite.Stalfos, 0x00, 0, 0x1a, 0x0e, 'Eastern West Wing')
    create_sprite(0x00a8, EnemySprite.Stalfos, 0x00, 0, 0x16, 0x12, 'Eastern West Wing')
    create_sprite(0x00a8, EnemySprite.Stalfos, 0x00, 0, 0x1a, 0x12, 'Eastern West Wing')
    create_sprite(0x00a8, 0x18, SpriteType.Overlord, 0, 0x08, 0x16)
    create_sprite(0x00a9, EnemySprite.GreenEyegoreMimic, 0x00, 1, 0x09, 0x05, 'Eastern Courtyard')
    create_sprite(0x00a9, EnemySprite.GreenEyegoreMimic, 0x00, 1, 0x16, 0x05, 'Eastern Courtyard')
    create_sprite(0x00a9, 0x05, SpriteType.Overlord, 1, 0x0d, 0x0c)
    create_sprite(0x00a9, 0x05, SpriteType.Overlord, 1, 0x12, 0x0c)
    create_sprite(0x00a9, 0x05, SpriteType.Overlord, 1, 0x0d, 0x12)
    create_sprite(0x00a9, 0x05, SpriteType.Overlord, 1, 0x12, 0x12)
    create_sprite(0x00a9, EnemySprite.Stalfos, 0x00, 1, 0x0a, 0x10, 'Eastern Courtyard')
    create_sprite(0x00a9, EnemySprite.Stalfos, 0x00, 1, 0x14, 0x10, 'Eastern Courtyard')
    create_sprite(0x00aa, EnemySprite.AntiFairy, 0x00, 0, 0x18, 0x06, 'Eastern Pot Switch')
    create_sprite(0x00aa, EnemySprite.Popo2, 0x00, 0, 0x0a, 0x07, 'Eastern East Wing')
    create_sprite(0x00aa, EnemySprite.Stalfos, 0x00, 0, 0x06, 0x0b, 'Eastern East Wing')
    create_sprite(0x00aa, EnemySprite.Stalfos, 0x00, 0, 0x0c, 0x0c, 'Eastern East Wing')
    create_sprite(0x00aa, EnemySprite.Stalfos, 0x00, 0, 0x0c, 0x13, 'Eastern East Wing')
    create_sprite(0x00aa, EnemySprite.Popo2, 0x00, 0, 0x0a, 0x14, 'Eastern East Wing')
    create_sprite(0x00ab, EnemySprite.CrystalSwitch, 0x00, 0, 0x04, 0x18)
    create_sprite(0x00ab, EnemySprite.SpikeBlock, 0x00, 0, 0x03, 0x15, 'Thieves Spike Switch')
    create_sprite(0x00ab, EnemySprite.SpikeBlock, 0x00, 0, 0x0c, 0x16, 'Thieves Spike Switch')
    create_sprite(0x00ab, EnemySprite.SpikeBlock, 0x00, 0, 0x03, 0x17, 'Thieves Spike Switch')
    create_sprite(0x00ab, EnemySprite.Blob, 0x00, 0, 0x06, 0x18, 'Thieves Spike Switch')
    create_sprite(0x00ab, EnemySprite.SpikeBlock, 0x00, 0, 0x03, 0x19, 'Thieves Spike Switch')
    create_sprite(0x00ab, EnemySprite.SpikeBlock, 0x00, 0, 0x0c, 0x1a, 'Thieves Spike Switch')
    create_sprite(0x00ab, EnemySprite.SpikeBlock, 0x00, 0, 0x03, 0x1b, 'Thieves Spike Switch')
    create_sprite(0x00ac, EnemySprite.Blind, 0x00, 0, 0x19, 0x15)
    create_sprite(0x00ae, EnemySprite.BlueBari, 0x00, 0, 0x13, 0x07, 'Iced T')
    create_sprite(0x00ae, EnemySprite.BlueBari, 0x00, 0, 0x15, 0x07, 'Iced T')
    create_sprite(0x00af, EnemySprite.FirebarCW, 0x00, 0, 0x0a, 0x08, 'Ice Catwalk')
    create_sprite(0x00b0, EnemySprite.RedSpearGuard, 0x00, 0, 0x07, 0x07, 'Tower Red Guards')
    create_sprite(0x00b0, EnemySprite.Keese, 0x00, 0, 0x17, 0x07, 'Tower Red Spears')
    create_sprite(0x00b0, EnemySprite.Keese, 0x00, 0, 0x18, 0x07, 'Tower Red Spears')
    create_sprite(0x00b0, EnemySprite.RedJavelinGuard, 0x00, 0, 0x14, 0x08, 'Tower Red Spears')
    create_sprite(0x00b0, EnemySprite.RedJavelinGuard, 0x00, 0, 0x1b, 0x08, 'Tower Red Spears')
    create_sprite(0x00b0, EnemySprite.RedSpearGuard, 0x00, 0, 0x05, 0x0b, 'Tower Red Guards')
    create_sprite(0x00b0, EnemySprite.BallNChain, 0x00, 0, 0x16, 0x14, 'Tower Pacifist Run')
    create_sprite(0x00b0, EnemySprite.Keese, 0x00, 0, 0x04, 0x16, 'Tower Circle of Pots')
    create_sprite(0x00b0, EnemySprite.Keese, 0x00, 0, 0x0b, 0x16, 'Tower Circle of Pots')
    create_sprite(0x00b0, EnemySprite.RedSpearGuard, 0x00, 0, 0x0a, 0x16, 'Tower Circle of Pots')
    create_sprite(0x00b0, EnemySprite.RedSpearGuard, 0x00, 0, 0x08, 0x18, 'Tower Circle of Pots', True, 0xe4)
    create_sprite(0x00b0, EnemySprite.BluesainBolt, 0x00, 0, 0x1b, 0x1a, 'Tower Pacifist Run')
    create_sprite(0x00b0, EnemySprite.RedJavelinGuard, 0x00, 0, 0x17, 0x1c, 'Tower Pacifist Run')
    create_sprite(0x00b1, EnemySprite.Medusa, 0x00, 0, 0x15, 0x07, 'Mire Spike Barrier')
    create_sprite(0x00b1, EnemySprite.Medusa, 0x00, 0, 0x1a, 0x07, 'Mire Spike Barrier')
    create_sprite(0x00b1, EnemySprite.SpikeBlock, 0x00, 0, 0x16, 0x0e, 'Mire Spike Barrier')
    create_sprite(0x00b1, EnemySprite.SpikeBlock, 0x00, 0, 0x19, 0x11, 'Mire Spike Barrier')
    create_sprite(0x00b1, EnemySprite.Wizzrobe, 0x00, 0, 0x0c, 0x17, 'Mire Square Rail')
    create_sprite(0x00b1, EnemySprite.BigSpike, 0x00, 0, 0x1a, 0x17, 'Mire Spike Barrier')
    create_sprite(0x00b1, EnemySprite.FourWayShooter, 0x00, 0, 0x07, 0x18, 'Mire Square Rail')
    create_sprite(0x00b1, EnemySprite.Wizzrobe, 0x00, 0, 0x03, 0x1a, 'Mire Square Rail')
    create_sprite(0x00b1, EnemySprite.AntiFairy, 0x00, 0, 0x15, 0x1a, 'Mire Spike Barrier')
    create_sprite(0x00b1, EnemySprite.Wizzrobe, 0x00, 0, 0x08, 0x1c, 'Mire Square Rail')
    create_sprite(0x00b2, EnemySprite.Wizzrobe, 0x00, 1, 0x14, 0x08, 'Mire BK Door Room')
    create_sprite(0x00b2, EnemySprite.BunnyBeam, 0x00, 1, 0x0c, 0x0a, 'Mire BK Door Room')
    create_sprite(0x00b2, EnemySprite.AntiFairy, 0x00, 1, 0x12, 0x0a, 'Mire BK Door Room')
    create_sprite(0x00b2, EnemySprite.BunnyBeam, 0x00, 1, 0x13, 0x0a, 'Mire BK Door Room')
    create_sprite(0x00b2, EnemySprite.AntiFairy, 0x00, 1, 0x07, 0x0b, 'Mire BK Door Room')
    create_sprite(0x00b2, EnemySprite.Sluggula, 0x00, 0, 0x04, 0x15, 'Mire Cross')
    create_sprite(0x00b2, EnemySprite.Sluggula, 0x00, 0, 0x0b, 0x15, 'Mire Cross')
    create_sprite(0x00b2, EnemySprite.AntiFairy, 0x00, 0, 0x03, 0x16, 'Mire Cross')
    create_sprite(0x00b2, EnemySprite.Medusa, 0x00, 0, 0x15, 0x18, 'Mire Hidden Shooters')
    create_sprite(0x00b2, EnemySprite.Medusa, 0x00, 0, 0x1a, 0x18, 'Mire Hidden Shooters')
    create_sprite(0x00b2, EnemySprite.Sluggula, 0x00, 0, 0x04, 0x1b, 'Mire Cross')
    create_sprite(0x00b2, EnemySprite.Sluggula, 0x00, 0, 0x0b, 0x1b, 'Mire Cross')
    create_sprite(0x00b2, EnemySprite.Popo, 0x00, 0, 0x14, 0x1b, 'Mire Hidden Shooters')
    create_sprite(0x00b2, EnemySprite.Popo, 0x00, 0, 0x1b, 0x1b, 'Mire Hidden Shooters')
    create_sprite(0x00b3, EnemySprite.Stalfos, 0x00, 0, 0x03, 0x15, 'Mire Spikes')
    create_sprite(0x00b3, EnemySprite.Stalfos, 0x00, 0, 0x0b, 0x15, 'Mire Spikes')
    create_sprite(0x00b3, EnemySprite.Beamos, 0x00, 0, 0x06, 0x18, 'Mire Spikes')
    create_sprite(0x00b3, EnemySprite.FourWayShooter, 0x00, 0, 0x0a, 0x1a, 'Mire Spikes')
    create_sprite(0x00b3, EnemySprite.Stalfos, 0x00, 0, 0x07, 0x1c, 'Mire Spikes')
    create_sprite(0x00b5, EnemySprite.FirebarCW, 0x00, 0, 0x16, 0x0a, 'TR Dark Ride')
    create_sprite(0x00b5, EnemySprite.FirebarCW, 0x00, 0, 0x09, 0x0f, 'TR Dark Ride')
    create_sprite(0x00b5, EnemySprite.FirebarCW, 0x00, 0, 0x16, 0x16, 'TR Dark Ride')
    create_sprite(0x00b6, EnemySprite.Chainchomp, 0x00, 0, 0x06, 0x07, 'TR Chain Chomps Top')
    create_sprite(0x00b6, EnemySprite.Chainchomp, 0x00, 0, 0x0a, 0x07, 'TR Chain Chomps Top')
    create_sprite(0x00b6, EnemySprite.CrystalSwitch, 0x00, 0, 0x03, 0x04)
    create_sprite(0x00b6, EnemySprite.CrystalSwitch, 0x00, 0, 0x0c, 0x04)
    create_sprite(0x00b6, EnemySprite.Faerie, 0x00, 0, 0x17, 0x07)
    create_sprite(0x00b6, EnemySprite.Pokey, 0x00, 0, 0x07, 0x15, 'TR Pokey 1', True, 0xe4)
    create_sprite(0x00b6, 0x14, SpriteType.Overlord, 0, 0x17, 0x18)
    create_sprite(0x00b6, EnemySprite.Blob, 0x00, 0, 0x07, 0x1b, 'TR Pokey 1')
    create_sprite(0x00b6, EnemySprite.Blob, 0x00, 0, 0x08, 0x1b, 'TR Pokey 1')
    create_sprite(0x00b7, EnemySprite.RollerHorizontalLeft, 0x00, 0, 0x04, 0x09, 'TR Roller Room')
    create_sprite(0x00b7, EnemySprite.RollerVerticalUp, 0x00, 0, 0x04, 0x11, 'TR Roller Room')
    create_sprite(0x00b8, EnemySprite.Popo, 0x00, 0, 0x15, 0x0b, 'Eastern Big Key')
    create_sprite(0x00b8, EnemySprite.Popo, 0x00, 0, 0x1b, 0x0b, 'Eastern Big Key')
    create_sprite(0x00b8, EnemySprite.AntiFairyCircle, 0x00, 0, 0x18, 0x0d, 'Eastern Big Key')
    create_sprite(0x00b8, EnemySprite.GreenEyegoreMimic, 0x00, 0, 0x18, 0x13, 'Eastern Big Key')
    create_sprite(0x00b8, EnemySprite.Stalfos, 0x00, 0, 0x14, 0x16, 'Eastern Big Key')
    create_sprite(0x00b8, EnemySprite.Stalfos, 0x00, 0, 0x1c, 0x16, 'Eastern Big Key')
    create_sprite(0x00b9, 0x03, SpriteType.Overlord, 1, 0x11, 0x05)
    create_sprite(0x00ba, EnemySprite.Stalfos, 0x00, 0, 0x14, 0x04, 'Eastern Dark Pots')
    create_sprite(0x00ba, EnemySprite.AntiFairy, 0x00, 0, 0x03, 0x06, 'Eastern Dark Square')
    create_sprite(0x00ba, EnemySprite.Stalfos, 0x00, 0, 0x18, 0x06, 'Eastern Dark Pots')
    create_sprite(0x00ba, EnemySprite.AntiFairy, 0x00, 0, 0x03, 0x09, 'Eastern Dark Square')
    create_sprite(0x00ba, EnemySprite.Popo2, 0x00, 0, 0x0c, 0x09, 'Eastern Dark Square')
    create_sprite(0x00ba, EnemySprite.Stalfos, 0x00, 0, 0x18, 0x0a, 'Eastern Dark Pots')
    create_sprite(0x00ba, EnemySprite.Popo2, 0x00, 0, 0x08, 0x0c, 'Eastern Dark Square')
    create_sprite(0x00bb, EnemySprite.RedZazak, 0x00, 0, 0x1b, 0x04, 'Thieves Triple Bypass')
    create_sprite(0x00bb, EnemySprite.Gibo, 0x00, 0, 0x06, 0x0a, 'Thieves Hellway')
    create_sprite(0x00bb, EnemySprite.RedZazak, 0x00, 0, 0x16, 0x0a, 'Thieves Triple Bypass')
    create_sprite(0x00bb, EnemySprite.Gibo, 0x00, 0, 0x19, 0x0a, 'Thieves Triple Bypass')
    create_sprite(0x00bb, EnemySprite.AntiFairy, 0x00, 0, 0x08, 0x0c, 'Thieves Hellway')
    create_sprite(0x00bb, EnemySprite.Gibo, 0x00, 0, 0x09, 0x0e, 'Thieves Hellway')
    create_sprite(0x00bb, EnemySprite.Firesnake, 0x00, 0, 0x07, 0x10, 'Thieves Hellway')
    create_sprite(0x00bb, EnemySprite.Gibo, 0x00, 0, 0x08, 0x14, 'Thieves Hellway')
    create_sprite(0x00bb, EnemySprite.Gibo, 0x00, 0, 0x19, 0x15, 'Thieves Spike Track')
    create_sprite(0x00bb, EnemySprite.AntiFairy, 0x00, 0, 0x15, 0x16, 'Thieves Spike Track')
    create_sprite(0x00bb, EnemySprite.Gibo, 0x00, 0, 0x17, 0x1a, 'Thieves Spike Track')
    create_sprite(0x00bc, EnemySprite.BlueZazak, 0x00, 0, 0x06, 0x05, 'Thieves Conveyor Maze')
    create_sprite(0x00bc, EnemySprite.Stalfos, 0x00, 0, 0x0c, 0x05, 'Thieves Conveyor Maze')
    create_sprite(0x00bc, EnemySprite.SpikeBlock, 0x00, 0, 0x08, 0x06, 'Thieves Conveyor Maze')
    create_sprite(0x00bc, EnemySprite.RedZazak, 0x00, 0, 0x0a, 0x09, 'Thieves Conveyor Maze')
    create_sprite(0x00bc, EnemySprite.SpikeBlock, 0x00, 0, 0x09, 0x0a, 'Thieves Conveyor Maze')
    create_sprite(0x00bc, EnemySprite.BlueZazak, 0x00, 0, 0x05, 0x0b, 'Thieves Conveyor Maze')
    create_sprite(0x00bc, EnemySprite.Stalfos, 0x00, 0, 0x17, 0x0a, 'Thieves Hallway')
    create_sprite(0x00bc, EnemySprite.Stalfos, 0x00, 0, 0x18, 0x11, 'Thieves Hallway')
    create_sprite(0x00bc, EnemySprite.Stalfos, 0x00, 0, 0x16, 0x16, 'Thieves Hallway')
    create_sprite(0x00bc, EnemySprite.BlueZazak, 0x00, 0, 0x08, 0x17, 'Thieves Pot Alcove Mid')
    create_sprite(0x00bc, EnemySprite.Firesnake, 0x00, 0, 0x07, 0x18, 'Thieves Pot Alcove Mid')
    create_sprite(0x00bc, EnemySprite.RedZazak, 0x00, 0, 0x08, 0x19, 'Thieves Pot Alcove Mid')
    create_sprite(0x00be, EnemySprite.AntiFairy, 0x00, 0, 0x17, 0x08, 'Ice Anti-Fairy')
    create_sprite(0x00be, EnemySprite.Freezor, 0x00, 0, 0x14, 0x12, 'Ice Switch Room')
    create_sprite(0x00be, EnemySprite.BlueBari, 0x00, 0, 0x14, 0x15, 'Ice Switch Room')
    create_sprite(0x00be, EnemySprite.BlueBari, 0x00, 0, 0x1b, 0x15, 'Ice Switch Room')
    create_sprite(0x00be, EnemySprite.StalfosKnight, 0x00, 0, 0x18, 0x16, 'Ice Switch Room')
    create_sprite(0x00be, EnemySprite.BlueBari, 0x00, 0, 0x14, 0x1a, 'Ice Switch Room')
    create_sprite(0x00be, EnemySprite.BlueBari, 0x00, 0, 0x1b, 0x1a, 'Ice Switch Room')
    create_sprite(0x00bf, EnemySprite.CrystalSwitch, 0x00, 0, 0x0b, 0x18)
    create_sprite(0x00bf, EnemySprite.BunnyBeam, 0x00, 0, 0x0c, 0x15, 'Ice Refill')
    create_sprite(0x00c0, EnemySprite.BlueGuard, 0x00, 0, 0x17, 0x05, 'Tower Dark Archers')
    create_sprite(0x00c0, EnemySprite.BlueArcher, 0x00, 0, 0x1a, 0x07, 'Tower Dark Archers')
    create_sprite(0x00c0, EnemySprite.BlueGuard, 0x00, 0, 0x0b, 0x09, 'Tower Dark Pits')
    create_sprite(0x00c0, EnemySprite.BlueArcher, 0x00, 0, 0x14, 0x0b, 'Tower Dark Archers', True, 0xe4)
    create_sprite(0x00c0, EnemySprite.BlueGuard, 0x00, 0, 0x06, 0x0e, 'Tower Dark Pits')
    create_sprite(0x00c0, EnemySprite.BlueGuard, 0x00, 0, 0x04, 0x18, 'Tower Dark Pits')
    create_sprite(0x00c0, EnemySprite.BlueArcher, 0x00, 0, 0x14, 0x1b, 'Tower Dual Statues')
    create_sprite(0x00c0, EnemySprite.BlueGuard, 0x00, 0, 0x1b, 0x1b, 'Tower Dual Statues')
    create_sprite(0x00c1, EnemySprite.CrystalSwitch, 0x00, 0, 0x15, 0x17)
    create_sprite(0x00c1, EnemySprite.Medusa, 0x00, 0, 0x14, 0x05)
    create_sprite(0x00c1, EnemySprite.Medusa, 0x00, 0, 0x1b, 0x05)
    create_sprite(0x00c1, EnemySprite.Stalfos, 0x00, 0, 0x06, 0x0b, 'Mire Compass Room')
    create_sprite(0x00c1, EnemySprite.Stalfos, 0x00, 0, 0x15, 0x0b, 'Mire Wizzrobe Bypass')
    create_sprite(0x00c1, EnemySprite.FloatingSkull, 0x00, 0, 0x17, 0x15, 'Mire Conveyor Crystal')
    create_sprite(0x00c1, EnemySprite.Medusa, 0x00, 0, 0x09, 0x16)
    create_sprite(0x00c1, 0x14, SpriteType.Overlord, 0, 0x07, 0x18)
    create_sprite(0x00c1, EnemySprite.AntiFairy, 0x00, 0, 0x14, 0x19, 'Mire Conveyor Crystal')
    create_sprite(0x00c1, EnemySprite.FourWayShooter, 0x00, 0, 0x18, 0x1a, 'Mire Conveyor Crystal')
    create_sprite(0x00c1, EnemySprite.BlueBari, 0x00, 0, 0x13, 0x1b, 'Mire Conveyor Crystal', True, 0xe4)
    create_sprite(0x00c1, EnemySprite.FloatingSkull, 0x00, 0, 0x1b, 0x1b, 'Mire Conveyor Crystal')
    create_sprite(0x00c2, EnemySprite.Firesnake, 0x00, 1, 0x15, 0x0b, 'Mire Hub')
    create_sprite(0x00c2, EnemySprite.Firesnake, 0x00, 0, 0x0b, 0x0c, 'Mire Hub')
    create_sprite(0x00c2, EnemySprite.Medusa, 0x00, 0, 0x08, 0x10, 'Mire Hub')
    create_sprite(0x00c2, EnemySprite.SparkCW, 0x00, 1, 0x10, 0x12, 'Mire Hub')
    create_sprite(0x00c2, EnemySprite.SparkCW, 0x00, 1, 0x19, 0x12, 'Mire Hub')
    create_sprite(0x00c2, EnemySprite.BunnyBeam, 0x00, 1, 0x10, 0x14, 'Mire Hub')
    create_sprite(0x00c2, EnemySprite.Firesnake, 0x00, 1, 0x08, 0x16, 'Mire Hub')
    create_sprite(0x00c2, EnemySprite.SparkCW, 0x00, 1, 0x16, 0x16, 'Mire Hub')
    create_sprite(0x00c3, EnemySprite.Medusa, 0x00, 0, 0x05, 0x06)
    create_sprite(0x00c3, EnemySprite.LaserEyeRight, 0x00, 0, 0x1e, 0x09)
    create_sprite(0x00c3, EnemySprite.LaserEyeLeft, 0x00, 0, 0x11, 0x0d)
    create_sprite(0x00c3, EnemySprite.LaserEyeRight, 0x00, 0, 0x1e, 0x11)
    create_sprite(0x00c3, EnemySprite.LaserEyeLeft, 0x00, 0, 0x11, 0x15)
    create_sprite(0x00c3, 0x0b, SpriteType.Overlord, 0, 0x17, 0x1a)
    create_sprite(0x00c3, EnemySprite.AntiFairy, 0x00, 0, 0x0a, 0x1b, 'Mire Lone Shooter')
    create_sprite(0x00c3, EnemySprite.Medusa, 0x00, 0, 0x07, 0x1c, 'Mire Lone Shooter')
    create_sprite(0x00c4, EnemySprite.CrystalSwitch, 0x00, 0, 0x0b, 0x0a)
    create_sprite(0x00c4, EnemySprite.CrystalSwitch, 0x00, 0, 0x18, 0x0f)
    create_sprite(0x00c4, EnemySprite.CrystalSwitch, 0x00, 0, 0x1c, 0x1b)
    create_sprite(0x00c4, EnemySprite.CrystalSwitch, 0x00, 0, 0x0f, 0x15)
    create_sprite(0x00c4, EnemySprite.Pokey, 0x00, 0, 0x0f, 0x0e, 'TR Crystal Maze Interior')
    create_sprite(0x00c4, EnemySprite.AntiFairy, 0x00, 0, 0x0b, 0x0f, 'TR Crystal Maze Interior')
    create_sprite(0x00c4, EnemySprite.MiniHelmasaur, 0x00, 0, 0x07, 0x14, 'TR Crystal Maze Interior')
    create_sprite(0x00c4, EnemySprite.MiniHelmasaur, 0x00, 0, 0x18, 0x14, 'TR Crystal Maze Interior')
    create_sprite(0x00c4, EnemySprite.AntiFairy, 0x00, 0, 0x0b, 0x1a, 'TR Crystal Maze Interior')
    create_sprite(0x00c4, EnemySprite.AntiFairy, 0x00, 0, 0x14, 0x1a, 'TR Crystal Maze Interior')
    create_sprite(0x00c5, EnemySprite.LaserEyeRight, 0x00, 0, 0x0e, 0x09)
    create_sprite(0x00c5, EnemySprite.LaserEyeLeft, 0x00, 0, 0x01, 0x0b)
    create_sprite(0x00c5, EnemySprite.LaserEyeRight, 0x00, 0, 0x0e, 0x0d)
    create_sprite(0x00c5, EnemySprite.LaserEyeLeft, 0x00, 0, 0x01, 0x0f)
    create_sprite(0x00c5, EnemySprite.LaserEyeRight, 0x00, 0, 0x0e, 0x11)
    create_sprite(0x00c5, EnemySprite.LaserEyeLeft, 0x00, 0, 0x01, 0x13)
    create_sprite(0x00c5, EnemySprite.MiniHelmasaur, 0x00, 0, 0x07, 0x15, 'TR Dash Bridge')
    create_sprite(0x00c5, EnemySprite.LaserEyeRight, 0x00, 0, 0x0e, 0x15)
    create_sprite(0x00c6, EnemySprite.Stalfos, 0x00, 0, 0x0b, 0x04, 'TR Hub Ledges')
    create_sprite(0x00c6, EnemySprite.Stalfos, 0x00, 0, 0x15, 0x04, 'TR Hub Ledges')
    create_sprite(0x00c6, EnemySprite.BlueBari, 0x00, 0, 0x08, 0x09, 'TR Hub Ledges')
    create_sprite(0x00c6, EnemySprite.BlueBari, 0x00, 0, 0x17, 0x09, 'TR Hub Ledges')
    create_sprite(0x00c6, EnemySprite.FloatingSkull, 0x00, 0, 0x10, 0x0e, 'TR Hub Ledges')
    create_sprite(0x00c6, EnemySprite.BlueBari, 0x00, 0, 0x18, 0x14, 'TR Hub Ledges')
    create_sprite(0x00c6, EnemySprite.BlueBari, 0x00, 0, 0x08, 0x17, 'TR Hub Ledges')
    create_sprite(0x00c8, EnemySprite.ArmosKnight, 0x00, 0, 0x14, 0x15)
    create_sprite(0x00c8, EnemySprite.ArmosKnight, 0x00, 0, 0x17, 0x15)
    create_sprite(0x00c8, EnemySprite.ArmosKnight, 0x00, 0, 0x1a, 0x15)
    create_sprite(0x00c8, EnemySprite.ArmosKnight, 0x00, 0, 0x1a, 0x18)
    create_sprite(0x00c8, EnemySprite.ArmosKnight, 0x00, 0, 0x17, 0x18)
    create_sprite(0x00c8, EnemySprite.ArmosKnight, 0x00, 0, 0x14, 0x18)
    create_sprite(0x00c8, 0x19, SpriteType.Overlord, 0, 0x17, 0x18)
    create_sprite(0x00c9, EnemySprite.Popo2, 0x00, 0, 0x10, 0x05, 'Eastern Lobby Bridge')
    create_sprite(0x00c9, EnemySprite.Popo2, 0x00, 0, 0x0f, 0x06, 'Eastern Lobby Bridge')
    create_sprite(0x00c9, EnemySprite.Popo2, 0x00, 0, 0x10, 0x07, 'Eastern Lobby Bridge')
    create_sprite(0x00cb, EnemySprite.BunnyBeam, 0x00, 0, 0x14, 0x04, 'Thieves Ambush')
    create_sprite(0x00cb, EnemySprite.Firesnake, 0x00, 1, 0x08, 0x09, 'Thieves Ambush')
    create_sprite(0x00cb, EnemySprite.BlueZazak, 0x00, 1, 0x10, 0x0a, 'Thieves Ambush')
    create_sprite(0x00cb, EnemySprite.Blob, 0x00, 0, 0x13, 0x0a, 'Thieves Ambush')
    create_sprite(0x00cb, EnemySprite.SparkCW, 0x00, 1, 0x16, 0x0a, 'Thieves Ambush')
    create_sprite(0x00cb, EnemySprite.Blob, 0x00, 0, 0x1c, 0x0a, 'Thieves Ambush')
    create_sprite(0x00cb, EnemySprite.Stalfos, 0x00, 0, 0x0c, 0x10, 'Thieves Ambush')
    create_sprite(0x00cb, EnemySprite.RedZazak, 0x00, 1, 0x18, 0x15, 'Thieves Ambush')
    create_sprite(0x00cb, EnemySprite.RedZazak, 0x00, 1, 0x08, 0x17, 'Thieves Ambush')
    create_sprite(0x00cb, EnemySprite.Blob, 0x00, 0, 0x0b, 0x17, 'Thieves Ambush')
    create_sprite(0x00cb, EnemySprite.Blob, 0x00, 0, 0x0c, 0x18, 'Thieves Ambush')
    create_sprite(0x00cb, EnemySprite.BunnyBeam, 0x00, 0, 0x14, 0x1c, 'Thieves Ambush')
    create_sprite(0x00cc, EnemySprite.Firesnake, 0x00, 0, 0x13, 0x04, 'Thieves BK Corner')
    create_sprite(0x00cc, EnemySprite.BunnyBeam, 0x00, 1, 0x0b, 0x09, 'Thieves BK Corner')
    create_sprite(0x00cc, EnemySprite.BlueZazak, 0x00, 1, 0x08, 0x0a, 'Thieves BK Corner')
    create_sprite(0x00cc, EnemySprite.SparkCW, 0x00, 1, 0x0e, 0x0a, 'Thieves BK Corner')
    create_sprite(0x00cc, EnemySprite.Blob, 0x00, 0, 0x0c, 0x0b, 'Thieves BK Corner')
    create_sprite(0x00cc, EnemySprite.RedZazak, 0x00, 1, 0x10, 0x0c, 'Thieves BK Corner')
    create_sprite(0x00cc, EnemySprite.BlueZazak, 0x00, 1, 0x18, 0x0c, 'Thieves BK Corner')
    create_sprite(0x00cc, EnemySprite.Firesnake, 0x00, 1, 0x0e, 0x14, 'Thieves BK Corner')
    create_sprite(0x00cc, EnemySprite.Blob, 0x00, 0, 0x1c, 0x15, 'Thieves BK Corner')
    create_sprite(0x00cc, EnemySprite.SparkCW, 0x00, 1, 0x06, 0x16, 'Thieves BK Corner')
    create_sprite(0x00cc, EnemySprite.SparkCW, 0x00, 1, 0x09, 0x16, 'Thieves BK Corner')
    create_sprite(0x00cc, EnemySprite.RedZazak, 0x00, 1, 0x09, 0x18, 'Thieves BK Corner')
    create_sprite(0x00cc, EnemySprite.Blob, 0x00, 0, 0x1c, 0x16, 'Thieves BK Corner')
    create_sprite(0x00cc, EnemySprite.BunnyBeam, 0x00, 1, 0x07, 0x1c, 'Thieves BK Corner')
    create_sprite(0x00ce, EnemySprite.RedBari, 0x00, 0, 0x16, 0x05, 'Ice Antechamber')
    create_sprite(0x00ce, EnemySprite.RedBari, 0x00, 0, 0x19, 0x05, 'Ice Antechamber')
    create_sprite(0x00ce, EnemySprite.CorrectPullSwitch, 0x00, 0, 0x1c, 0x05, 'Ice Antechamber')
    create_sprite(0x00ce, EnemySprite.Statue, 0x00, 0, 0x14, 0x09, 'Ice Antechamber')
    create_sprite(0x00ce, EnemySprite.BlueBari, 0x00, 0, 0x1b, 0x08, 'Ice Antechamber')
    create_sprite(0x00ce, EnemySprite.BlueBari, 0x00, 0, 0x1c, 0x08, 'Ice Antechamber')
    create_sprite(0x00ce, EnemySprite.BlueBari, 0x00, 0, 0x1b, 0x09, 'Ice Antechamber')
    create_sprite(0x00ce, EnemySprite.BlueBari, 0x00, 0, 0x1c, 0x09, 'Ice Antechamber')
    create_sprite(0x00d0, EnemySprite.Keese, 0x00, 0, 0x0b, 0x05, 'Tower Dark Maze')
    create_sprite(0x00d0, EnemySprite.BlueGuard, 0x00, 0, 0x09, 0x07, 'Tower Dark Maze')
    create_sprite(0x00d0, EnemySprite.Keese, 0x00, 0, 0x17, 0x07, 'Tower Lone Statue')
    create_sprite(0x00d0, EnemySprite.BluesainBolt, 0x00, 0, 0x15, 0x0b, 'Tower Lone Statue')
    create_sprite(0x00d0, EnemySprite.Keese, 0x00, 0, 0x09, 0x0c, 'Tower Dark Maze')
    create_sprite(0x00d0, EnemySprite.Keese, 0x00, 0, 0x08, 0x0f, 'Tower Dark Maze')
    create_sprite(0x00d0, EnemySprite.BlueGuard, 0x03, 0, 0x03, 0x10, 'Tower Dark Maze')
    create_sprite(0x00d0, EnemySprite.BlueGuard, 0x00, 0, 0x09, 0x14, 'Tower Dark Maze')
    create_sprite(0x00d0, EnemySprite.BluesainBolt, 0x00, 0, 0x1b, 0x16, 'Tower Dark Chargers')
    create_sprite(0x00d0, EnemySprite.Keese, 0x00, 0, 0x06, 0x19, 'Tower Dark Maze')
    create_sprite(0x00d0, EnemySprite.BluesainBolt, 0x00, 0, 0x1a, 0x19, 'Tower Dark Chargers')
    create_sprite(0x00d1, EnemySprite.Beamos, 0x00, 0, 0x14, 0x06, 'Mire Neglected Room')
    create_sprite(0x00d1, EnemySprite.Beamos, 0x00, 0, 0x1b, 0x06, 'Mire Neglected Room')
    create_sprite(0x00d1, EnemySprite.Wizzrobe, 0x00, 0, 0x04, 0x07, 'Mire Conveyor Barrier')
    create_sprite(0x00d1, EnemySprite.RedBari, 0x00, 0, 0x0c, 0x08, 'Mire Conveyor Barrier')
    create_sprite(0x00d1, EnemySprite.FourWayShooter, 0x00, 0, 0x05, 0x09, 'Mire Conveyor Barrier')
    create_sprite(0x00d1, EnemySprite.Sluggula, 0x00, 0, 0x04, 0x0b, 'Mire Conveyor Barrier')
    create_sprite(0x00d1, EnemySprite.Sluggula, 0x00, 0, 0x0b, 0x0b, 'Mire Conveyor Barrier')
    create_sprite(0x00d1, EnemySprite.Sluggula, 0x00, 0, 0x1b, 0x0b, 'Mire Neglected Room')
    create_sprite(0x00d2, EnemySprite.Wizzrobe, 0x00, 0, 0x18, 0x06, 'Mire 2')
    create_sprite(0x00d2, EnemySprite.Popo, 0x00, 0, 0x1a, 0x07, 'Mire 2')
    create_sprite(0x00d2, EnemySprite.Wizzrobe, 0x00, 0, 0x13, 0x08, 'Mire 2')
    create_sprite(0x00d2, EnemySprite.Wizzrobe, 0x00, 0, 0x1c, 0x08, 'Mire 2')
    create_sprite(0x00d2, EnemySprite.Beamos, 0x00, 0, 0x18, 0x0a, 'Mire 2')
    create_sprite(0x00d2, EnemySprite.Popo, 0x00, 0, 0x16, 0x0c, 'Mire 2')
    create_sprite(0x00d2, EnemySprite.Popo, 0x00, 0, 0x13, 0x0d, 'Mire 2')
    create_sprite(0x00d2, EnemySprite.Wizzrobe, 0x00, 0, 0x13, 0x10, 'Mire 2')
    create_sprite(0x00d2, EnemySprite.Popo, 0x00, 0, 0x14, 0x14, 'Mire 2')
    create_sprite(0x00d2, EnemySprite.Popo, 0x00, 0, 0x1c, 0x14, 'Mire 2')
    create_sprite(0x00d5, EnemySprite.LaserEyeRight, 0x00, 0, 0x0e, 0x09)
    create_sprite(0x00d5, EnemySprite.LaserEyeLeft, 0x00, 0, 0x01, 0x0d)
    create_sprite(0x00d5, EnemySprite.LaserEyeRight, 0x00, 0, 0x0e, 0x11)
    create_sprite(0x00d5, EnemySprite.LaserEyeLeft, 0x00, 0, 0x01, 0x15)
    create_sprite(0x00d5, EnemySprite.HardhatBeetle, 0x00, 0, 0x04, 0x15, 'TR Eye Bridge')
    create_sprite(0x00d6, EnemySprite.LaserEyeTop, 0x00, 0, 0x07, 0x02)
    create_sprite(0x00d6, EnemySprite.Medusa, 0x00, 0, 0x03, 0x16)
    create_sprite(0x00d6, EnemySprite.Medusa, 0x00, 0, 0x0c, 0x16)
    create_sprite(0x00d8, EnemySprite.RedEyegoreMimic, 0x00, 0, 0x17, 0x05, 'Eastern Duo Eyegores')
    create_sprite(0x00d8, EnemySprite.RedEyegoreMimic, 0x00, 0, 0x18, 0x05, 'Eastern Duo Eyegores')
    create_sprite(0x00d8, EnemySprite.Popo2, 0x00, 0, 0x17, 0x09, 'Eastern Duo Eyegores')
    create_sprite(0x00d8, EnemySprite.Popo2, 0x00, 0, 0x18, 0x09, 'Eastern Duo Eyegores')
    create_sprite(0x00d8, EnemySprite.Popo2, 0x00, 0, 0x16, 0x0a, 'Eastern Duo Eyegores')
    create_sprite(0x00d8, EnemySprite.Popo2, 0x00, 0, 0x19, 0x0a, 'Eastern Duo Eyegores')
    create_sprite(0x00d8, EnemySprite.Popo, 0x00, 0, 0x16, 0x0b, 'Eastern Duo Eyegores')
    create_sprite(0x00d8, EnemySprite.Popo, 0x00, 0, 0x19, 0x0b, 'Eastern Duo Eyegores')
    create_sprite(0x00d8, EnemySprite.RedEyegoreMimic, 0x00, 0, 0x17, 0x14, 'Eastern Single Eyegore')
    create_sprite(0x00d8, EnemySprite.Stalfos, 0x00, 0, 0x18, 0x16, 'Eastern Single Eyegore')
    create_sprite(0x00d8, EnemySprite.Stalfos, 0x00, 0, 0x18, 0x1b, 'Eastern Single Eyegore')
    create_sprite(0x00d9, 0x02, SpriteType.Overlord, 0, 0x0c, 0x14)
    create_sprite(0x00d9, EnemySprite.GreenEyegoreMimic, 0x00, 0, 0x18, 0x15, 'Eastern False Switches')
    create_sprite(0x00d9, EnemySprite.GreenEyegoreMimic, 0x00, 0, 0x18, 0x18, 'Eastern False Switches')
    create_sprite(0x00d9, EnemySprite.GreenEyegoreMimic, 0x00, 0, 0x18, 0x1b, 'Eastern False Switches')
    create_sprite(0x00da, EnemySprite.AntiFairy, 0x00, 0, 0x07, 0x18, 'Eastern Attic Start')
    create_sprite(0x00da, EnemySprite.AntiFairy, 0x00, 0, 0x08, 0x18, 'Eastern Attic Start')
    create_sprite(0x00db, EnemySprite.BunnyBeam, 0x00, 0, 0x03, 0x04, 'Thieves Lobby')
    create_sprite(0x00db, EnemySprite.SparkCW, 0x00, 1, 0x0e, 0x0a, 'Thieves Lobby')
    create_sprite(0x00db, EnemySprite.RedZazak, 0x00, 1, 0x17, 0x0b, 'Thieves Lobby')
    create_sprite(0x00db, EnemySprite.BlueZazak, 0x00, 1, 0x0f, 0x0c, 'Thieves Lobby')
    create_sprite(0x00db, EnemySprite.Blob, 0x00, 0, 0x0b, 0x10, 'Thieves Lobby')
    create_sprite(0x00db, EnemySprite.Firesnake, 0x00, 0, 0x14, 0x10, 'Thieves Lobby')
    create_sprite(0x00db, EnemySprite.BlueZazak, 0x00, 1, 0x0f, 0x15, 'Thieves Lobby')
    create_sprite(0x00dc, EnemySprite.BlueZazak, 0x00, 1, 0x09, 0x0a, 'Thieves Compass Room')
    create_sprite(0x00dc, EnemySprite.SparkCCW, 0x00, 1, 0x0e, 0x0a, 'Thieves Compass Room')
    create_sprite(0x00dc, EnemySprite.RedZazak, 0x00, 1, 0x0f, 0x0c, 'Thieves Compass Room')
    create_sprite(0x00dc, EnemySprite.Blob, 0x00, 0, 0x0b, 0x10, 'Thieves Compass Room')
    create_sprite(0x00dc, EnemySprite.Blob, 0x00, 0, 0x16, 0x10, 'Thieves Compass Room')
    create_sprite(0x00dc, EnemySprite.BunnyBeam, 0x00, 1, 0x0c, 0x16, 'Thieves Compass Room')
    create_sprite(0x00dc, EnemySprite.RedZazak, 0x00, 1, 0x0f, 0x16, 'Thieves Compass Room')
    create_sprite(0x00dc, EnemySprite.BlueZazak, 0x00, 1, 0x09, 0x17, 'Thieves Compass Room')
    create_sprite(0x00dc, EnemySprite.Firesnake, 0x00, 1, 0x16, 0x17, 'Thieves Compass Room')
    create_sprite(0x00dc, EnemySprite.Firesnake, 0x00, 0, 0x05, 0x1c, 'Thieves Compass Room')
    create_sprite(0x00dc, EnemySprite.Blob, 0x00, 0, 0x0f, 0x1c, 'Thieves Compass Room')
    create_sprite(0x00de, EnemySprite.KholdstareShell, 0x00, 0, 0x17, 0x05)
    create_sprite(0x00de, EnemySprite.FallingIce, 0x00, 0, 0x17, 0x05)
    create_sprite(0x00de, EnemySprite.Kholdstare, 0x00, 0, 0x17, 0x05)
    create_sprite(0x00df, EnemySprite.MiniMoldorm, 0x00, 1, 0x0c, 0x15, 'Paradox Cave')
    create_sprite(0x00df, EnemySprite.MiniMoldorm, 0x00, 1, 0x0c, 0x16, 'Paradox Cave')
    create_sprite(0x00e0, EnemySprite.BallNChain, 0x00, 0, 0x04, 0x06, 'Tower Gold Knights')
    create_sprite(0x00e0, EnemySprite.BallNChain, 0x00, 0, 0x0b, 0x06, 'Tower Gold Knights')
    create_sprite(0x00e0, EnemySprite.BluesainBolt, 0x00, 0, 0x1a, 0x06, 'Tower Room 03')
    create_sprite(0x00e0, EnemySprite.BluesainBolt, 0x00, 0, 0x1a, 0x09, 'Tower Room 03')
    create_sprite(0x00e1, EnemySprite.HeartPiece, 0x00, 0, 0x17, 0x0d)
    create_sprite(0x00e1, EnemySprite.AdultNpc, 0x00, 1, 0x07, 0x12)
    create_sprite(0x00e2, EnemySprite.Faerie, 0x00, 0, 0x07, 0x06)
    create_sprite(0x00e2, EnemySprite.Faerie, 0x00, 0, 0x08, 0x06)
    create_sprite(0x00e2, EnemySprite.Faerie, 0x00, 0, 0x07, 0x07)
    create_sprite(0x00e2, EnemySprite.Faerie, 0x00, 0, 0x08, 0x07)
    create_sprite(0x00e2, EnemySprite.HeartPiece, 0x00, 0, 0x13, 0x10)
    create_sprite(0x00e3, EnemySprite.MagicBat, 0x00, 1, 0x17, 0x05)
    create_sprite(0x00e4, EnemySprite.Keese, 0x00, 0, 0x19, 0x07, 'Old Man House')
    create_sprite(0x00e4, EnemySprite.Keese, 0x00, 0, 0x18, 0x08, 'Old Man House')
    create_sprite(0x00e4, EnemySprite.Keese, 0x00, 0, 0x17, 0x09, 'Old Man House')
    create_sprite(0x00e4, EnemySprite.OldMan, 0x00, 0, 0x06, 0x16, 'Old Man House')
    create_sprite(0x00e5, EnemySprite.Keese, 0x00, 0, 0x0f, 0x09, 'Old Man House Back')
    create_sprite(0x00e5, EnemySprite.Keese, 0x00, 0, 0x10, 0x09, 'Old Man House Back')
    create_sprite(0x00e5, EnemySprite.Keese, 0x00, 0, 0x11, 0x09, 'Old Man House Back')
    create_sprite(0x00e5, EnemySprite.Keese, 0x00, 0, 0x1b, 0x0e, 'Old Man House Back')
    create_sprite(0x00e5, EnemySprite.Keese, 0x00, 0, 0x0f, 0x12, 'Old Man House Back')
    create_sprite(0x00e5, EnemySprite.Keese, 0x00, 0, 0x11, 0x12, 'Old Man House Back')
    create_sprite(0x00e6, EnemySprite.Keese, 0x00, 0, 0x1b, 0x0b, 'Death Mountain Return Cave (left)')
    create_sprite(0x00e6, EnemySprite.Keese, 0x00, 0, 0x17, 0x0f, 'Death Mountain Return Cave (left)')
    create_sprite(0x00e6, EnemySprite.Keese, 0x00, 0, 0x13, 0x13, 'Death Mountain Return Cave (left)')
    create_sprite(0x00e6, EnemySprite.Keese, 0x00, 0, 0x0f, 0x17, 'Death Mountain Return Cave (left)')
    create_sprite(0x00e6, EnemySprite.Keese, 0x00, 0, 0x0b, 0x1b, 'Death Mountain Return Cave (left)')
    create_sprite(0x00e7, EnemySprite.Keese, 0x00, 0, 0x10, 0x04, 'Death Mountain Return Cave (right)')
    create_sprite(0x00e7, EnemySprite.Keese, 0x00, 0, 0x13, 0x04, 'Death Mountain Return Cave (right)')
    create_sprite(0x00e7, EnemySprite.Keese, 0x00, 0, 0x15, 0x0b, 'Death Mountain Return Cave (right)')
    create_sprite(0x00e7, EnemySprite.Keese, 0x00, 0, 0x0b, 0x0c, 'Death Mountain Return Cave (right)')
    create_sprite(0x00e7, EnemySprite.Keese, 0x00, 0, 0x0b, 0x0d, 'Death Mountain Return Cave (right)')
    create_sprite(0x00e7, EnemySprite.Keese, 0x00, 0, 0x15, 0x0d, 'Death Mountain Return Cave (right)')
    create_sprite(0x00e7, EnemySprite.Keese, 0x00, 0, 0x15, 0x0f, 'Death Mountain Return Cave (right)')
    create_sprite(0x00e8, EnemySprite.HardhatBeetle, 0x00, 0, 0x07, 0x05, 'Superbunny Cave (Bottom)')
    create_sprite(0x00e8, EnemySprite.HardhatBeetle, 0x00, 0, 0x17, 0x08, 'Superbunny Cave (Bottom)')
    create_sprite(0x00e8, EnemySprite.HardhatBeetle, 0x00, 0, 0x07, 0x0c, 'Superbunny Cave (Bottom)')
    create_sprite(0x00e8, EnemySprite.HardhatBeetle, 0x00, 0, 0x19, 0x0c, 'Superbunny Cave (Bottom)')
    create_sprite(0x00ea, EnemySprite.HeartPiece, 0x00, 0, 0x0b, 0x0b)
    create_sprite(0x00eb, EnemySprite.Bumper, 0x00, 0, 0x17, 0x14)
    create_sprite(0x00ee, EnemySprite.MiniMoldorm, 0x00, 0, 0x10, 0x04, 'Spiral Cave (Top)')
    create_sprite(0x00ee, EnemySprite.MiniMoldorm, 0x00, 0, 0x0b, 0x0e, 'Spiral Cave (Top)')
    create_sprite(0x00ee, EnemySprite.MiniMoldorm, 0x00, 0, 0x09, 0x1c, 'Spiral Cave (Top)')
    create_sprite(0x00ee, EnemySprite.BlueBari, 0x00, 0, 0x03, 0x0b, 'Spiral Cave (Top)')
    create_sprite(0x00ee, EnemySprite.BlueBari, 0x00, 0, 0x1c, 0x0c, 'Spiral Cave (Top)')
    create_sprite(0x00ef, EnemySprite.MiniMoldorm, 0x00, 0, 0x17, 0x09, 'Paradox Cave Chest Area')
    create_sprite(0x00ef, EnemySprite.MiniMoldorm, 0x00, 0, 0x14, 0x0a, 'Paradox Cave Chest Area')
    create_sprite(0x00ef, EnemySprite.MiniMoldorm, 0x00, 0, 0x1b, 0x0a, 'Paradox Cave Chest Area')
    create_sprite(0x00ef, EnemySprite.CrystalSwitch, 0x00, 0, 0x18, 0x06)
    create_sprite(0x00f0, EnemySprite.Keese, 0x00, 0, 0x09, 0x03, 'Old Man Cave')
    create_sprite(0x00f0, EnemySprite.Keese, 0x00, 0, 0x10, 0x03, 'Old Man Cave')
    create_sprite(0x00f0, EnemySprite.Keese, 0x00, 0, 0x08, 0x04, 'Old Man Cave')
    create_sprite(0x00f0, EnemySprite.Keese, 0x00, 0, 0x0a, 0x04, 'Old Man Cave')
    create_sprite(0x00f0, EnemySprite.Keese, 0x00, 0, 0x09, 0x07, 'Old Man Cave')
    create_sprite(0x00f0, EnemySprite.Keese, 0x00, 0, 0x03, 0x0a, 'Old Man Cave')
    create_sprite(0x00f0, EnemySprite.Keese, 0x00, 0, 0x05, 0x0a, 'Old Man Cave')
    create_sprite(0x00f0, EnemySprite.Keese, 0x00, 0, 0x0e, 0x0c, 'Old Man Cave')
    create_sprite(0x00f0, EnemySprite.OldMan, 0x00, 0, 0x1b, 0x10, 'Old Man Cave')
    create_sprite(0x00f0, EnemySprite.Keese, 0x00, 0, 0x13, 0x13, 'Old Man Cave')
    create_sprite(0x00f1, EnemySprite.Keese, 0x00, 0, 0x19, 0x10, 'Old Man Cave')
    create_sprite(0x00f1, EnemySprite.Keese, 0x00, 0, 0x1c, 0x10, 'Old Man Cave')
    create_sprite(0x00f1, EnemySprite.Keese, 0x00, 0, 0x18, 0x11, 'Old Man Cave')
    create_sprite(0x00f1, EnemySprite.Keese, 0x00, 0, 0x1d, 0x11, 'Old Man Cave')
    create_sprite(0x00f1, EnemySprite.Keese, 0x00, 0, 0x17, 0x12, 'Old Man Cave')
    create_sprite(0x00f1, EnemySprite.Keese, 0x00, 0, 0x1e, 0x12, 'Old Man Cave')
    create_sprite(0x00f1, EnemySprite.Keese, 0x00, 0, 0x06, 0x1b, 'Old Man Cave')
    create_sprite(0x00f1, EnemySprite.Keese, 0x00, 0, 0x09, 0x1b, 'Old Man Cave')
    create_sprite(0x00f1, EnemySprite.Keese, 0x00, 0, 0x07, 0x1c, 'Old Man Cave')
    create_sprite(0x00f1, EnemySprite.Keese, 0x00, 0, 0x08, 0x1c, 'Old Man Cave')
    create_sprite(0x00f3, EnemySprite.Grandma, 0x00, 0, 0x06, 0x14)
    create_sprite(0x00f4, EnemySprite.ArgueBros, 0x00, 0, 0x17, 0x14)
    create_sprite(0x00f5, EnemySprite.ArgueBros, 0x00, 0, 0x08, 0x14)
    create_sprite(0x00f9, EnemySprite.MiniMoldorm, 0x00, 0, 0x1a, 0x05, 'Spectacle Rock Cave (Bottom)')
    create_sprite(0x00f9, EnemySprite.MiniMoldorm, 0x00, 0, 0x15, 0x0f, 'Spectacle Rock Cave (Bottom)')
    create_sprite(0x00f9, EnemySprite.MiniMoldorm, 0x00, 0, 0x11, 0x13, 'Spectacle Rock Cave (Bottom)')
    create_sprite(0x00f9, EnemySprite.MiniMoldorm, 0x00, 0, 0x0c, 0x17, 'Spectacle Rock Cave (Bottom)')
    create_sprite(0x00fa, EnemySprite.Faerie, 0x00, 0, 0x17, 0x0e)
    create_sprite(0x00fa, EnemySprite.Faerie, 0x00, 0, 0x18, 0x10)
    create_sprite(0x00fa, EnemySprite.Faerie, 0x00, 0, 0x15, 0x11)
    create_sprite(0x00fb, EnemySprite.Bumper, 0x00, 0, 0x17, 0x0d)
    create_sprite(0x00fb, EnemySprite.HardhatBeetle, 0x00, 0, 0x19, 0x0a, 'Bumper Cave')
    create_sprite(0x00fb, EnemySprite.HardhatBeetle, 0x00, 0, 0x15, 0x12, 'Bumper Cave')
    create_sprite(0x00fd, EnemySprite.MiniMoldorm, 0x00, 0, 0x09, 0x0e, 'Fairy Ascension Cave (Bottom)')
    create_sprite(0x00fd, EnemySprite.BlueBari, 0x00, 0, 0x05, 0x08, 'Fairy Ascension Cave (Bottom)')
    create_sprite(0x00fd, EnemySprite.Faerie, 0x00, 0, 0x16, 0x08)
    create_sprite(0x00fd, EnemySprite.Faerie, 0x00, 0, 0x18, 0x08)
    create_sprite(0x00fd, EnemySprite.BlueBari, 0x00, 0, 0x0f, 0x11, 'Fairy Ascension Cave (Bottom)')
    create_sprite(0x00fe, EnemySprite.MiniMoldorm, 0x00, 0, 0x16, 0x12, 'Spiral Cave (Bottom)')
    create_sprite(0x00fe, EnemySprite.MiniMoldorm, 0x00, 0, 0x14, 0x16, 'Spiral Cave (Bottom)')
    create_sprite(0x00fe, EnemySprite.MiniMoldorm, 0x00, 0, 0x1a, 0x16, 'Spiral Cave (Bottom)')
    create_sprite(0x00fe, EnemySprite.BlueBari, 0x00, 0, 0x18, 0x12, 'Spiral Cave (Bottom)')
    create_sprite(0x00fe, EnemySprite.BlueBari, 0x00, 0, 0x18, 0x18, 'Spiral Cave (Bottom)')
    create_sprite(0x00ff, EnemySprite.Shopkeeper, 0x00, 0, 0x07, 0x04)
    create_sprite(0x0100, EnemySprite.Shopkeeper, 0x00, 0, 0x0b, 0x1b)
    create_sprite(0x0101, EnemySprite.RupeePull, 0x00, 0, 0x08, 0x13)
    create_sprite(0x0102, EnemySprite.SickKid, 0x00, 0, 0x03, 0x18)
    create_sprite(0x0103, EnemySprite.Drunkard, 0x00, 0, 0x06, 0x15)
    create_sprite(0x0103, EnemySprite.AdultNpc, 0x00, 0, 0x0a, 0x1b)
    create_sprite(0x0103, EnemySprite.Innkeeper, 0x00, 0, 0x17, 0x17)
    create_sprite(0x0104, EnemySprite.UnclePriest, 0x00, 0, 0x1a, 0x17)
    create_sprite(0x0105, EnemySprite.Wiseman, 0x00, 0, 0x07, 0x18)
    create_sprite(0x0106, EnemySprite.Shopkeeper, 0x00, 0, 0x08, 0x1b)
    create_sprite(0x0107, EnemySprite.BonkItem, 0x00, 0, 0x03, 0x15)
    create_sprite(0x0107, EnemySprite.CricketRat, 0x00, 0, 0x17, 0x1b, 'Light World Bomb Hut')
    create_sprite(0x0107, EnemySprite.CricketRat, 0x00, 0, 0x18, 0x1b, 'Light World Bomb Hut')
    create_sprite(0x0108, EnemySprite.Cucco, 0x00, 0, 0x09, 0x16, 'Chicken House')
    create_sprite(0x0108, EnemySprite.Cucco, 0x00, 0, 0x0c, 0x16, 'Chicken House')
    create_sprite(0x0108, EnemySprite.Cucco, 0x00, 0, 0x09, 0x19, 'Chicken House')
    create_sprite(0x0108, EnemySprite.Cucco, 0x00, 0, 0x06, 0x1a, 'Chicken House')
    create_sprite(0x0109, EnemySprite.MagicShopAssistant, 0x00, 0, 0x0a, 0x1b)
    create_sprite(0x010a, EnemySprite.Wiseman, 0x00, 0, 0x19, 0x04)
    create_sprite(0x010b, EnemySprite.WrongPullSwitch, 0x00, 0, 0x0f, 0x03)
    create_sprite(0x010b, 0x1a, SpriteType.Overlord, 0, 0x0d, 0x06)
    create_sprite(0x010b, 0x1a, SpriteType.Overlord, 0, 0x10, 0x06)
    create_sprite(0x010b, 0x1a, SpriteType.Overlord, 0, 0x12, 0x07)
    create_sprite(0x010b, 0x1a, SpriteType.Overlord, 0, 0x0f, 0x09)
    create_sprite(0x010b, EnemySprite.CorrectPullSwitch, 0x00, 0, 0x12, 0x03)
    create_sprite(0x010b, EnemySprite.AntiFairy, 0x00, 0, 0x0d, 0x07, 'Dam')
    create_sprite(0x010c, EnemySprite.Faerie, 0x00, 0, 0x17, 0x07)
    create_sprite(0x010c, EnemySprite.Faerie, 0x00, 0, 0x18, 0x07)
    create_sprite(0x010c, EnemySprite.Faerie, 0x00, 0, 0x17, 0x08)
    create_sprite(0x010c, EnemySprite.Faerie, 0x00, 0, 0x18, 0x08)
    create_sprite(0x010c, EnemySprite.GreenEyegoreMimic, 0x00, 0, 0x07, 0x14, 'Mimic Cave')
    create_sprite(0x010c, EnemySprite.GreenEyegoreMimic, 0x00, 0, 0x08, 0x14, 'Mimic Cave')
    create_sprite(0x010c, EnemySprite.GreenEyegoreMimic, 0x00, 0, 0x0c, 0x14, 'Mimic Cave')
    create_sprite(0x010c, EnemySprite.GreenEyegoreMimic, 0x00, 0, 0x0c, 0x1a, 'Mimic Cave')
    create_sprite(0x010d, EnemySprite.SparkCW, 0x00, 0, 0x05, 0x16, 'Mimic Cave')
    create_sprite(0x010d, EnemySprite.SparkCCW, 0x00, 0, 0x0a, 0x16, 'Mimic Cave')
    create_sprite(0x010e, EnemySprite.DarkWorldHintNpc, 0x00, 0, 0x06, 0x06)
    create_sprite(0x010e, EnemySprite.DarkWorldHintNpc, 0x00, 0, 0x18, 0x06)
    create_sprite(0x010f, EnemySprite.Shopkeeper, 0x00, 0, 0x07, 0x15)
    create_sprite(0x0110, EnemySprite.Shopkeeper, 0x00, 0, 0x07, 0x15)
    create_sprite(0x0111, EnemySprite.ArcheryNpc, 0x00, 0, 0x0b, 0x1b)
    create_sprite(0x0112, EnemySprite.DarkWorldHintNpc, 0x00, 0, 0x07, 0x0a)
    create_sprite(0x0112, EnemySprite.Shopkeeper, 0x00, 0, 0x17, 0x14)
    create_sprite(0x0114, EnemySprite.FairyPondTrigger, 0x00, 0, 0x07, 0x18)
    create_sprite(0x0114, EnemySprite.DarkWorldHintNpc, 0x00, 0, 0x19, 0x14)
    create_sprite(0x0115, EnemySprite.BigFairy, 0x00, 0, 0x17, 0x16)
    create_sprite(0x0115, EnemySprite.Faerie, 0x00, 0, 0x17, 0x07)
    create_sprite(0x0115, EnemySprite.Faerie, 0x00, 0, 0x18, 0x07)
    create_sprite(0x0115, EnemySprite.Faerie, 0x00, 0, 0x17, 0x08)
    create_sprite(0x0115, EnemySprite.Faerie, 0x00, 0, 0x18, 0x08)
    # create_sprite(0x0115, EnemySprite.FairyPondTrigger, 0x00, 0, 0x07, 0x09)  # todo: I think this is gone
    create_sprite(0x0116, EnemySprite.FairyPondTrigger, 0x00, 0, 0x17, 0x18)
    create_sprite(0x0118, EnemySprite.Shopkeeper, 0x00, 0, 0x19, 0x1b)
    create_sprite(0x0119, EnemySprite.AdultNpc, 0x00, 0, 0x0e, 0x18)
    create_sprite(0x011a, EnemySprite.DarkWorldHintNpc, 0x00, 0, 0x18, 0x17)
    create_sprite(0x011b, EnemySprite.HeartPiece, 0x00, 0, 0x18, 0x09)
    create_sprite(0x011b, EnemySprite.HeartPiece, 0x00, 1, 0x05, 0x16)
    create_sprite(0x011c, EnemySprite.BombShopGuy, 0x00, 0, 0x09, 0x19)
    create_sprite(0x011e, EnemySprite.Faerie, 0x00, 0, 0x05, 0x07)
    create_sprite(0x011e, EnemySprite.Faerie, 0x00, 0, 0x06, 0x07)
    create_sprite(0x011e, EnemySprite.Faerie, 0x00, 0, 0x05, 0x08)
    create_sprite(0x011e, EnemySprite.Faerie, 0x00, 0, 0x06, 0x08)
    create_sprite(0x011e, EnemySprite.Shopkeeper, 0x00, 0, 0x18, 0x16)
    create_sprite(0x011f, EnemySprite.Shopkeeper, 0x00, 0, 0x17, 0x16)
    create_sprite(0x0120, EnemySprite.GoodBee, 0x00, 0, 0x17, 0x07)
    create_sprite(0x0120, EnemySprite.Faerie, 0x00, 0, 0x1b, 0x08)
    create_sprite(0x0120, EnemySprite.Faerie, 0x00, 0, 0x1a, 0x09)
    create_sprite(0x0121, EnemySprite.Smithy, 0x00, 0, 0x04, 0x17)
    create_sprite(0x0122, EnemySprite.FortuneTeller, 0x00, 0, 0x07, 0x18)
    create_sprite(0x0122, EnemySprite.FortuneTeller, 0x00, 0, 0x17, 0x18)
    create_sprite(0x0123, EnemySprite.MiniMoldorm, 0x00, 0, 0x03, 0x16, 'Mini Moldorm Cave')
    create_sprite(0x0123, EnemySprite.MiniMoldorm, 0x00, 0, 0x0c, 0x16, 'Mini Moldorm Cave')
    create_sprite(0x0123, EnemySprite.MiniMoldorm, 0x00, 0, 0x08, 0x17, 'Mini Moldorm Cave')
    create_sprite(0x0123, EnemySprite.MiniMoldorm, 0x00, 0, 0x03, 0x1a, 'Mini Moldorm Cave')
    create_sprite(0x0123, EnemySprite.Shopkeeper, 0x00, 0, 0x08, 0x05)
    create_sprite(0x0124, EnemySprite.Shopkeeper, 0x00, 0, 0x08, 0x16)
    create_sprite(0x0125, EnemySprite.Shopkeeper, 0x00, 0, 0x08, 0x16)
    create_sprite(0x0126, EnemySprite.Faerie, 0x00, 0, 0x07, 0x15)
    create_sprite(0x0126, EnemySprite.Faerie, 0x00, 0, 0x08, 0x15)
    create_sprite(0x0126, EnemySprite.Faerie, 0x00, 0, 0x07, 0x16)
    create_sprite(0x0126, EnemySprite.Faerie, 0x00, 0, 0x08, 0x16)
    create_sprite(0x0126, EnemySprite.HeartPiece, 0x00, 0, 0x1c, 0x14)
    create_sprite(0x0127, EnemySprite.HeartPiece, 0x00, 0, 0x07, 0x16)


def kill_rules(world, player, stats):

    def h(enemy):
        return stats[enemy].health
    defeat_rules = {
        EnemySprite.MiniHelmasaur: defeat_rule(world, player, h(EnemySprite.MiniHelmasaur),
                                               bomb=2, silver=3, fire=None),
        EnemySprite.MiniMoldorm: defeat_rule(world, player, h(EnemySprite.MiniMoldorm), ice=1, hook=True),
        EnemySprite.Sluggula: defeat_rule(world, player, h(EnemySprite.Sluggula), bomb=None),
        # too hard to hit red biris with arrows
        EnemySprite.RedBari: defeat_rule(world, player, h(EnemySprite.RedBari) * 3, arrow=None, ice=2, hook=True),
        EnemySprite.BlueBari: defeat_rule(world, player, h(EnemySprite.BlueBari), ice=2, hook=True),
        EnemySprite.HardhatBeetle: defeat_rule(world, player, h(EnemySprite.HardhatBeetle),
                                               arrow=None, bomb=None, fire=None),
        EnemySprite.BlueGuard: defeat_rule(world, player, h(EnemySprite.BlueGuard), ice=1),
        EnemySprite.GreenGuard: defeat_rule(world, player, h(EnemySprite.GreenGuard)),
        EnemySprite.RedSpearGuard: defeat_rule(world, player, h(EnemySprite.RedSpearGuard)),
        EnemySprite.BluesainBolt: defeat_rule(world, player, h(EnemySprite.BluesainBolt)),
        EnemySprite.UsainBolt: defeat_rule(world, player, h(EnemySprite.UsainBolt)),
        EnemySprite.BlueArcher: defeat_rule(world, player, h(EnemySprite.BlueArcher)),
        EnemySprite.GreenBushGuard: defeat_rule(world, player, h(EnemySprite.GreenBushGuard), ice=1),
        EnemySprite.RedJavelinGuard: defeat_rule(world, player, h(EnemySprite.RedJavelinGuard)),
        EnemySprite.RedBushGuard: defeat_rule(world, player, h(EnemySprite.RedBushGuard)),
        EnemySprite.BombGuard: defeat_rule(world, player, h(EnemySprite.BombGuard)),
        EnemySprite.GreenKnifeGuard: defeat_rule(world, player, h(EnemySprite.GreenKnifeGuard)),
        EnemySprite.Popo: defeat_rule(world, player, h(EnemySprite.Popo), hook=True),
        EnemySprite.Popo2: defeat_rule(world, player, h(EnemySprite.Popo2), hook=True),
        EnemySprite.Debirando: defeat_rule(world, player, h(EnemySprite.Debirando), fire=1, ice=1, boomerang=True),
        EnemySprite.BallNChain: defeat_rule(world, player, h(EnemySprite.BallNChain)),
        EnemySprite.CannonTrooper: defeat_rule(world, player, h(EnemySprite.CannonTrooper), fire=1, ice=1),
        EnemySprite.CricketRat: defeat_rule(world, player, h(EnemySprite.CricketRat), hook=True),
        EnemySprite.Snake: defeat_rule(world, player, h(EnemySprite.Snake), hook=True),
        EnemySprite.Keese: defeat_rule(world, player, h(EnemySprite.Keese), hook=True, boomerang=True),
        EnemySprite.Leever: defeat_rule(world, player, h(EnemySprite.Leever)),
        EnemySprite.FloatingSkull: defeat_rule(world, player, h(EnemySprite.FloatingSkull), bomb=2),
        EnemySprite.Hover: defeat_rule(world, player, h(EnemySprite.Hover), hook=True),
        EnemySprite.GreenEyegoreMimic: defeat_rule(world, player, h(EnemySprite.GreenEyegoreMimic),
                                                   arrow=2, silver=2, fire=None),
        EnemySprite.RedEyegoreMimic: can_bow_kill(world, player, arrow_damage[1], silver_damage[1],
                                                  h(EnemySprite.RedEyegoreMimic)),
        EnemySprite.Kondongo: defeat_rule(world, player, h(EnemySprite.Kondongo), bomb=None, fire=1),
        EnemySprite.Gibdo: defeat_rule(world, player, h(EnemySprite.Gibdo), arrow=0),
        EnemySprite.Terrorpin: has('Hammer', player),
        EnemySprite.Blob: defeat_rule(world, player, h(EnemySprite.Blob), hook=True, bomb=2),
        # bombs are required for quick kills, but cannot collapse him
        EnemySprite.StalfosKnight: and_rule(can_use_bombs(world,  player),
                                            defeat_rule(world, player, h(EnemySprite.StalfosKnight),
                                                        bomb=None, arrow=None, fire=None, boomerang=True)),
        EnemySprite.Pengator: defeat_rule(world, player, h(EnemySprite.Pengator),
                                          fire=1, bomb=2, hook=True, boomerang=True),
        EnemySprite.Wizzrobe: defeat_rule(world, player, h(EnemySprite.Wizzrobe), fire=1, ice=1),
        EnemySprite.Babasu: defeat_rule(world, player, h(EnemySprite.Babasu), ice=2, hook=True),
        EnemySprite.Freezor: or_rule(has('Fire Rod', player), and_rule(has_sword(player), has('Bombos', player))),
        EnemySprite.BlueZazak: defeat_rule(world, player, h(EnemySprite.BlueZazak), bomb=2),
        EnemySprite.RedZazak: defeat_rule(world, player, h(EnemySprite.RedZazak), bomb=2),
        EnemySprite.Stalfos: defeat_rule(world, player, h(EnemySprite.Stalfos), fire=1, ice=2, boomerang=True),
        EnemySprite.Gibo: defeat_rule(world, player, h(EnemySprite.Gibo), arrow=3, fire=None),
        EnemySprite.Pokey: defeat_rule(world, player, h(EnemySprite.Pokey), silver=2, ice=1),
    }
    return defeat_rules


def or_rule(*rules):
    return RuleFactory.disj(rules)


def and_rule(*rules):
    return RuleFactory.conj(rules)


def has(item, player, count=1):
    return RuleFactory.item(item, player, count)


def has_sword(player):
    return or_rule(
        has('Fighter Sword', player), has('Master Sword', player),
        has('Tempered Sword', player), has('Golden Sword', player)
    )


def can_extend_magic(world, player, magic, flag_t=False):
    potion_shops = (find_shops_that_sell('Blue Potion', world, player) |
                    find_shops_that_sell('Green Potion', world, player))
    return RuleFactory.extend_magic(player, magic, world.difficulty_adjustments[player], potion_shops, flag_t)


# class 0 damage (subtypes 1 and 2)
def has_boomerang(player):
    return or_rule(has('Blue Boomerang', player), has('Red_Boomerang', player))


class_1_damage = {1: 2, 2: 64, 3: 4}  # somaria, byrna
arrow_damage = {0: 0, 1: 2, 2: 64, 3: 16}  # normal arrows (0 is for when silvers work, but wooden do not)
silver_damage = {1: 100, 2: 24, 3: 100}  # silvers
bomb_damage = {1: 4, 2: 64, 6: 32}  # bombs
ice_rod_damage = {1: 8, 2: 64, 4: 4}  # ice rod
fire_rod_damage = {1: 8, 2: 64, 4: 4, 5: 16}  # fire rod


# assumes 8 hits per magic bar - a little generous
def can_byrna_kill(world, player, damage, health):
    magic_needed = math.ceil(health / damage)
    if magic_needed > 8:
        return and_rule(has('Cane of Byrna', player), can_extend_magic(world, player, magic_needed))
    else:
        return has('Cane of Byrna', player)


# assumes 64 hits per somaria magic bar (max is like 80)
def can_somaria_kill(world, player, damage, health):
    magic_needed = hits = math.ceil(health / (damage * 64))
    if magic_needed > 8:
        return and_rule(has('Cane of Somaria', player), can_extend_magic(world, player, magic_needed))
    else:
        return has('Cane of Somaria', player)


# assume hitting 8 of 10 bombs?
def can_bombs_kill(world, player, damage, health):
    bombs_needed = math.ceil(health / damage)
    if bombs_needed > 8:
        return RuleFactory.static_rule(False)
    return can_use_bombs(world, player)


# assume all 8 hit
def can_ice_rod_kill(world, player, damage, health):
    magic_needed = math.ceil(health / damage)
    if magic_needed > 8:
        return and_rule(has('Ice Rod', player), can_extend_magic(world, player, magic_needed))
    else:
        return has('Ice Rod', player)


# assume all 8 hit
def can_fire_rod_kill(world, player, damage, health):
    magic_needed = math.ceil(health / damage)
    if magic_needed > 8:
        return and_rule(has('Fire Rod', player), can_extend_magic(world, player, magic_needed))
    else:
        return has('Fire Rod', player)


# 20/30 arrows hit
def can_bow_kill(world, player, damage, silver_damage, health):
    wood_arrows_needed = math.ceil(health / damage) if damage != 0 else 999
    if wood_arrows_needed > 20:
        silvers_arrows_needed = math.ceil(health / silver_damage)
        if silvers_arrows_needed > 20:
            return RuleFactory.static_rule(False)
        return and_rule(can_shoot_arrows(world, player), has('Silver Arrows', player))
    return can_shoot_arrows(world, player)


# main enemy types
def defeat_rule(world, player, health, class1=1,
                arrow: typing.Optional[int] = 1, silver=1,
                bomb: typing.Optional[int] = 1,
                fire: typing.Union[str, int, None] = 'Burn',
                ice=None, hook=False, boomerang=False):
    rules = [has_blunt_weapon(player),
             can_somaria_kill(world, player, class_1_damage[class1], health),
             can_byrna_kill(world, player, class_1_damage[class1], health)]
    if arrow is not None:
        rules.append(can_bow_kill(world, player, arrow_damage[arrow], silver_damage[silver], health))
    if bomb is not None:
        rules.append(can_bombs_kill(world, player, bomb_damage[bomb], health))
    if hook:
        rules.append(has('Hookshot', player))
    if fire is not None:
        if fire == 'Burn':
            rules.append(has('Fire Rod', player))
        else:
            rules.append(can_fire_rod_kill(world, player, fire_rod_damage[fire], health))
    if ice is not None:
        rules.append(can_ice_rod_kill(world, player, ice_rod_damage[fire], health))
    if boomerang:
        rules.append(has_boomerang(player))
    return or_rule(rules)


def has_blunt_weapon(player):
    return or_rule(has_sword(player), has('Hammer', player))


def find_shops_that_sell(item, world, player):
    return {shop.region for shop in world.shops[player] if shop.has_unlimited(item) and shop.region.player == player}


def can_shoot_arrows(world, player):
    if world.retro[player]:
        # todo: Non-progressive silvers grant wooden arrows, but progressive bows do not.
        # Always require shop arrows to be safe
        shops = find_shops_that_sell('Single Arrow', world, player)
        # retro+shopsanity, shops may not sell the Single Arrow
        return and_rule(has('Bow', player), or_rule(RuleFactory.unlimited('Single Arrow', player, shops),
                                                    has('Single Arrow', player)))
    return has('Bow', player)


def can_use_bombs(world, player):
    return or_rule(RuleFactory.static_rule(not world.bombag[player]), has('Bomb Upgrade (+10)', player))

