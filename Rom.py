import bisect
import collections
import io
import json
import hashlib
import logging
import os

import Items
import RaceRandom as random
import struct
import sys
try:
    import bps.apply
    import bps.io
except ImportError:
    raise Exception('Could not load BPS module')

from BaseClasses import ShopType, Region, Location, Door, DoorType, RegionType, LocationType
from DoorShuffle import compass_data, DROptions, boss_indicator, dungeon_portals
from Dungeons import dungeon_music_addresses, dungeon_table
from Regions import location_table, shop_to_location_table, retro_shops
from RoomData import DoorKind
from Text import MultiByteTextMapper, CompressedTextMapper, text_addresses, Credits, TextTable
from Text import Uncle_texts, Ganon1_texts, Ganon_Phase_3_No_Silvers_texts, TavernMan_texts, Sahasrahla2_texts
from Text import Triforce_texts, Blind_texts, BombShop2_texts, junk_texts
from Text import KingsReturn_texts, Sanctuary_texts, Kakariko_texts, Blacksmiths_texts, DeathMountain_texts
from Text import LostWoods_texts, WishingWell_texts, DesertPalace_texts, MountainTower_texts, LinksHouse_texts
from Text import Lumberjacks_texts, SickKid_texts, FluteBoy_texts, Zora_texts, MagicShop_texts, Sahasrahla_names
from Utils import local_path, int16_as_bytes, int32_as_bytes, snes_to_pc
from Items import ItemFactory
from source.overworld.EntranceData import door_addresses
from source.overworld.EntranceShuffle2 import exit_ids, ow_prize_table
from InitialSram import InitialSram

from source.classes.SFX import randomize_sfx
from source.item.FillUtil import valid_pot_items
from source.dungeon.EnemyList import EnemySprite, setup_enemy_dungeon_tables
from source.dungeon.RoomObject import DoorObject
from source.enemizer.Bossmizer import boss_writes
from source.enemizer.Enemizer import write_enemy_shuffle_settings


JAP10HASH = '03a63945398191337e896e5771f77173'
RANDOMIZERBASEHASH = '1cbe62592c0e9a7d224232c62292ecc9'


class JsonRom(object):

    def __init__(self, name=None, hash=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None
        self.patches = {}
        self.addresses = []
        self.initial_sram = InitialSram()

    def write_byte(self, address, value):
        self.write_bytes(address, [value])

    def write_bytes(self, startaddress, values):
        if not values:
            return
        values = list(values)

        pos = bisect.bisect_right(self.addresses, startaddress)
        intervalstart = self.addresses[pos-1] if pos else None
        intervalpatch = self.patches[str(intervalstart)] if pos else None

        if pos and startaddress <= intervalstart + len(intervalpatch): # merge with previous segment
            offset = startaddress - intervalstart
            intervalpatch[offset:offset+len(values)] = values
            startaddress = intervalstart
            values = intervalpatch
        else: # new segment
            self.addresses.insert(pos, startaddress)
            self.patches[str(startaddress)] = values
            pos = pos + 1

        while pos < len(self.addresses) and self.addresses[pos] <= startaddress + len(values): # merge the next segment into this one
            intervalstart = self.addresses[pos]
            values.extend(self.patches[str(intervalstart)][startaddress+len(values)-intervalstart:])
            del self.patches[str(intervalstart)]
            del self.addresses[pos]

    def write_initial_sram(self):
        self.write_bytes(0x183000, self.initial_sram.get_initial_sram())

    def write_to_file(self, file):
        with open(file, 'w') as stream:
            json.dump([self.patches], stream)

    def get_hash(self):
        h = hashlib.md5()
        h.update(json.dumps([self.patches]).encode('utf-8'))
        return h.hexdigest()


class LocalRom(object):

    def __init__(self, file, patch=True, name=None, hash=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None
        self.file = file
        self.initial_sram = InitialSram()
        self.has_smc_header = False
        if not os.path.isfile(file):
            raise RuntimeError("Could not find valid local base rom for patching at expected path %s." % file)
        with open(file, 'rb') as stream:
            self.buffer, self.has_smc_header = read_rom(stream)
        if patch:
            self.patch_base_rom()
            self.orig_buffer = self.buffer.copy()

    def write_byte(self, address, value):
        self.buffer[address] = value

    def write_bytes(self, startaddress, values):
        self.buffer[startaddress:startaddress + len(values)] = values

    def write_initial_sram(self):
        self.write_bytes(0x183000, self.initial_sram.get_initial_sram())

    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)

    @staticmethod
    def fromJsonRom(rom, file, rom_size = 0x200000):
        ret = LocalRom(file, True, rom.name, rom.hash)
        ret.buffer.extend(bytearray([0x00] * (rom_size - len(ret.buffer))))
        for address, values in rom.patches.items():
            ret.write_bytes(int(address), values)
        return ret

    def verify_base_rom(self):
        # verify correct checksum of baserom
        basemd5 = hashlib.md5()
        basemd5.update(self.buffer)
        if JAP10HASH != basemd5.hexdigest():
            raise RuntimeError('Supplied Base Rom does not match known MD5 for JAP(1.0) release.')

    def patch_base_rom(self):
        # verify correct checksum of baserom
        basemd5 = hashlib.md5()
        basemd5.update(self.buffer)
        if JAP10HASH != basemd5.hexdigest():
            logging.getLogger('').warning('Supplied Base Rom does not match known MD5 for JAP(1.0) release. Will try to patch anyway.')

        orig_buffer = self.buffer.copy()

        # extend to 2MB
        self.buffer.extend(bytearray([0x00] * (0x200000 - len(self.buffer))))

        # load randomizer patches
        with open(local_path('data/base2current.bps'), 'rb') as stream:
            bps.apply.apply_to_bytearrays(bps.io.read_bps(stream), orig_buffer, self.buffer)

        self.create_json_patch(orig_buffer)

        # verify md5
        patchedmd5 = hashlib.md5()
        patchedmd5.update(self.buffer)
        if RANDOMIZERBASEHASH != patchedmd5.hexdigest():
            raise RuntimeError('Provided Base Rom unsuitable for patching. Please provide a JAP(1.0) "Zelda no Densetsu - Kamigami no Triforce (Japan).sfc" rom to use as a base.')

    def create_json_patch(self, orig_buffer):
        # extend to 2MB
        orig_buffer.extend(bytearray([0x00] * (len(self.buffer) - len(orig_buffer))))

        i = 0
        patches = []

        while i < len(self.buffer):
            if self.buffer[i] == orig_buffer[i]:
                i += 1
                continue

            patch_start = i
            patch_contents = []
            while self.buffer[i] != orig_buffer[i]:
                patch_contents.append(self.buffer[i])
                i += 1
            patches.append({patch_start: patch_contents})

        with open(local_path('data/base2current.json'), 'w') as fp:
            json.dump(patches, fp, separators=(',', ':'))

    def write_crc(self):
        crc = (sum(self.buffer[:0x7FDC] + self.buffer[0x7FE0:]) + 0x01FE) & 0xFFFF
        inv = crc ^ 0xFFFF
        self.write_bytes(0x7FDC, [inv & 0xFF, (inv >> 8) & 0xFF, crc & 0xFF, (crc >> 8) & 0xFF])

    def get_hash(self):
        h = hashlib.md5()
        h.update(self.buffer)
        return h.hexdigest()

def write_int16(rom, address, value):
    rom.write_bytes(address, int16_as_bytes(value))

def write_int32(rom, address, value):
    rom.write_bytes(address, int32_as_bytes(value))

def write_int16s(rom,  startaddress, values):
    for i, value in enumerate(values):
        write_int16(rom, startaddress + (i * 2), value)

def write_int32s(rom, startaddress, values):
    for i, value in enumerate(values):
        write_int32(rom, startaddress + (i * 4), value)

def read_rom(stream):
    "Reads rom into bytearray and strips off any smc header"
    buffer = bytearray(stream.read())
    has_smc_header = False
    if len(buffer)%0x400 == 0x200:
        buffer = buffer[0x200:]
        has_smc_header = True
    return buffer, has_smc_header


_sprite_table = {}
def _populate_sprite_table():
    if not _sprite_table:
        for dir in [local_path(os.path.join("data","sprites","official")), local_path(os.path.join("data","sprites","unofficial"))]:
            for file in os.listdir(dir):
                filepath = os.path.join(dir, file)
                if not os.path.isfile(filepath):
                    continue
                sprite = Sprite(filepath)
                if sprite.valid:
                    _sprite_table[sprite.name.lower()] = filepath

def get_sprite_from_name(name):
    _populate_sprite_table()
    name = name.lower()
    if name in ['random', 'randomonhit']:
        return Sprite(random.choice(list(_sprite_table.values())))
    if name == ('(default link)'):
        name = 'link'
    return Sprite(_sprite_table[name]) if name in _sprite_table else None

class Sprite(object):
    default_palette = [255, 127, 126, 35, 183, 17, 158, 54, 165, 20, 255, 1, 120, 16, 157,
                       89, 71, 54, 104, 59, 74, 10, 239, 18, 92, 42, 113, 21, 24, 122,
                       255, 127, 126, 35, 183, 17, 158, 54, 165, 20, 255, 1, 120, 16, 157,
                       89, 128, 105, 145, 118, 184, 38, 127, 67, 92, 42, 153, 17, 24, 122,
                       255, 127, 126, 35, 183, 17, 158, 54, 165, 20, 255, 1, 120, 16, 157,
                       89, 87, 16, 126, 69, 243, 109, 185, 126, 92, 42, 39, 34, 24, 122,
                       255, 127, 126, 35, 218, 17, 158, 54, 165, 20, 255, 1, 120, 16, 151,
                       61, 71, 54, 104, 59, 74, 10, 239, 18, 126, 86, 114, 24, 24, 122]

    default_glove_palette = [246, 82, 118, 3]

    def __init__(self, filename):
        with open(filename, 'rb') as file:
            filedata = bytearray(file.read())
        self.name = os.path.basename(filename)
        self.author_name = None
        self.valid = True
        if len(filedata) == 0x7000:
            # sprite file with graphics and without palette data
            self.sprite = filedata[:0x7000]
            self.palette = list(self.default_palette)
            self.glove_palette = list(self.default_glove_palette)
        elif len(filedata) == 0x7078:
            # sprite file with graphics and palette data
            self.sprite = filedata[:0x7000]
            self.palette = filedata[0x7000:]
            self.glove_palette = filedata[0x7036:0x7038] + filedata[0x7054:0x7056]
        elif len(filedata) == 0x707C:
            # sprite file with graphics and palette data including gloves
            self.sprite = filedata[:0x7000]
            self.palette = filedata[0x7000:0x7078]
            self.glove_palette = filedata[0x7078:]
        elif len(filedata) in [0x100000, 0x200000]:
            # full rom with patched sprite, extract it
            self.sprite = filedata[0x80000:0x87000]
            self.palette = filedata[0xDD308:0xDD380]
            self.glove_palette = filedata[0xDEDF5:0xDEDF9]
        elif filedata.startswith(b'ZSPR'):
            result = self.parse_zspr(filedata, 1)
            if result is None:
                self.valid = False
                return
            (sprite, palette, self.name, self.author_name) = result
            if len(sprite) != 0x7000:
                self.valid = False
                return
            self.sprite = sprite
            if len(palette) == 0:
                self.palette = list(self.default_palette)
                self.glove_palette = list(self.default_glove_palette)
            elif len(palette) == 0x78:
                self.palette = palette
                self.glove_palette = list(self.default_glove_palette)
            elif len(palette) == 0x7C:
                self.palette = palette[:0x78]
                self.glove_palette = palette[0x78:]
            else:
                self.valid = False
        else:
            self.valid = False

    @staticmethod
    def default_link_sprite():
        return get_sprite_from_name('Link')

    def decode8(self, pos):
        arr = [[0 for _ in range(8)] for _ in range(8)]
        for y in range(8):
            for x in range(8):
                position = 1<<(7-x)
                val = 0
                if self.sprite[pos+2*y] & position:
                    val += 1
                if self.sprite[pos+2*y+1] & position:
                    val += 2
                if self.sprite[pos+2*y+16] & position:
                    val += 4
                if self.sprite[pos+2*y+17] & position:
                    val += 8
                arr[y][x] = val
        return arr

    def decode16(self, pos):
        arr = [[0 for _ in range(16)] for _ in range(16)]
        top_left = self.decode8(pos)
        top_right = self.decode8(pos+0x20)
        bottom_left = self.decode8(pos+0x200)
        bottom_right = self.decode8(pos+0x220)
        for x in range(8):
            for y in range(8):
                arr[y][x] = top_left[y][x]
                arr[y][x+8] = top_right[y][x]
                arr[y+8][x] = bottom_left[y][x]
                arr[y+8][x+8] = bottom_right[y][x]
        return arr

    def parse_zspr(self, filedata, expected_kind):
        logger = logging.getLogger('')
        headerstr = "<4xBHHIHIHH6x"
        headersize = struct.calcsize(headerstr)
        if len(filedata) < headersize:
            return None
        (version, csum, icsum, sprite_offset, sprite_size, palette_offset, palette_size, kind) = struct.unpack_from(headerstr, filedata)
        if version not in [1]:
            logger.error('Error parsing ZSPR file: Version %g not supported', version)
            return None
        if kind != expected_kind:
            return None

        stream = io.BytesIO(filedata)
        stream.seek(headersize)

        def read_utf16le(stream):
            "Decodes a null-terminated UTF-16_LE string of unknown size from a stream"
            raw = bytearray()
            while True:
                char = stream.read(2)
                if char in [b'', b'\x00\x00']:
                    break
                raw += char
            return raw.decode('utf-16_le')

        sprite_name = read_utf16le(stream)
        author_name = read_utf16le(stream)

        real_csum = sum(filedata) % 0x10000
        if real_csum != csum or real_csum ^ 0xFFFF != icsum:
            logger.warning('ZSPR file has incorrect checksum. It may be corrupted.')

        sprite = filedata[sprite_offset:sprite_offset + sprite_size]
        palette = filedata[palette_offset:palette_offset + palette_size]

        if len(sprite) != sprite_size or len(palette) != palette_size:
            logger.error('Error parsing ZSPR file: Unexpected end of file')
            return None

        return (sprite, palette, sprite_name, author_name)

    def decode_palette(self):
        "Returns the palettes as an array of arrays of 15 colors"
        def array_chunk(arr, size):
            return list(zip(*[iter(arr)] * size))
        def make_int16(pair):
            return pair[1]<<8 | pair[0]
        def expand_color(i):
            return ((i & 0x1F) * 8, (i>>5 & 0x1F) * 8, (i>>10 & 0x1F) * 8)
        raw_palette = self.palette
        if raw_palette is None:
            raw_palette = Sprite.default_palette
        # turn palette data into a list of RGB tuples with 8 bit values
        palette_as_colors = [expand_color(make_int16(chnk)) for chnk in array_chunk(raw_palette, 2)]

        # split into palettes of 15 colors
        return array_chunk(palette_as_colors, 15)


def handle_native_dungeon(location, itemid):
    # Keys in their native dungeon should use the original item code for keys
    if location.parent_region.dungeon and location.player == location.item.player:
        if location.parent_region.dungeon.name == location.item.dungeon:
            if location.item.bigkey:
                return 0x32
            if location.item.smallkey:
                return 0x24
            if location.item.map:
                return 0x33
            if location.item.compass:
                return 0x25
    return itemid


def patch_rom(world, rom, player, team, is_mystery=False):
    random.seed(world.rom_seeds[player])

    # progressive bow silver arrow hint hack
    prog_bow_locs = world.find_items('Progressive Bow', player)
    if len(prog_bow_locs) > 1:
        # only pick a distingushed bow if we have at least two
        distinguished_prog_bow_loc = random.choice(prog_bow_locs)
        distinguished_prog_bow_loc.item.code = 0x65

    # patch items
    pot_mw_index = 0
    for location in world.get_locations():
        if location.player != player:
            continue
        itemid = location.item.code if location.item is not None else 0x5A
        if location.type == LocationType.Pot:
            if location.item.name in valid_pot_items and location.item.player == player:
                location.pot.item = valid_pot_items[location.item.name]
            else:
                code = handle_native_dungeon(location, itemid)
                standing_item_flag = 0x80
                if location.item.player != player:
                    standing_item_flag |= 0x40
                    rom.write_byte(0x142800 + pot_mw_index * 2, code)
                    rom.write_byte(0x142800 + pot_mw_index * 2 + 1, location.item.player)
                    code = pot_mw_index
                    pot_mw_index += 1
                location.pot.indicator = standing_item_flag
                location.pot.standing_item_code = code
            continue
        elif location.type == LocationType.Drop:  # handled in the sprite table routine
            continue
        if location.address is None or (type(location.address) is int and location.address >= 0x400000):
            continue

        if not location.crystal:
            if location.item is not None:
                # Keys in their native dungeon should use the original item code for keys
                itemid = handle_native_dungeon(location, itemid)
                if world.remote_items[player]:
                    itemid = list(location_table.keys()).index(location.name) + 1
                    assert itemid < 0x100
                    rom.write_byte(location.player_address, 0xFF)
                elif location.item.player != player:
                    if location.player_address is not None:
                        rom.write_byte(location.player_address, location.item.player)
                    else:
                        itemid = 0x5A
            rom.write_byte(location.address, itemid)
        else:
            # crystals
            for address, value in zip(location.address, itemid):
                rom.write_byte(address, value)

            # patch music
            music_addresses = dungeon_music_addresses[location.name]
            if world.mapshuffle[player]:
                music = random.choice([0x11, 0x16])
            else:
                music = 0x11 if 'Pendant' in location.item.name else 0x16
            for music_address in music_addresses:
                rom.write_byte(music_address, music)

    if world.mapshuffle[player]:
        rom.write_byte(0x155C9, random.choice([0x11, 0x16]))  # Randomize GT music too with map shuffle

    # fix for swamp drains if necessary
    swamp1location = world.get_location('Swamp Palace - Trench 1 Pot Key', player)
    if not swamp1location.pot.indicator:
        rom.write_byte(0x142A53, 0)
    swamp2location = world.get_location('Swamp Palace - Trench 2 Pot Key', player)
    if not swamp2location.pot.indicator:
        rom.write_byte(0x142A54, 0)

    # patch entrance/exits/holes
    for region in world.regions:
        for exit in region.exits:
            if exit.target is not None and exit.player == player:
                if isinstance(exit.addresses, tuple):
                    offset = exit.target
                    room_id, ow_area, vram_loc, scroll_y, scroll_x, link_y, link_x, camera_y, camera_x, unknown_1, unknown_2, door_1, door_2 = exit.addresses
                    #room id is deliberately not written


                    rom.write_byte(0x15B8C + offset, ow_area)
                    write_int16(rom, 0x15BDB + 2 * offset, vram_loc)
                    write_int16(rom, 0x15C79 + 2 * offset, scroll_y)
                    write_int16(rom, 0x15D17 + 2 * offset, scroll_x)

                    # for positioning fixups we abuse the roomid as a way of identifying which exit data we are appling
                    # Thanks to Zarby89 for originally finding these values
                    # todo fix screen scrolling

                    if world.shuffle[player] not in ['insanity'] and \
                            exit.name in ['Eastern Palace Exit', 'Tower of Hera Exit', 'Thieves Town Exit', 'Ice Palace Exit', 'Misery Mire Exit',
                                          'Palace of Darkness Exit', 'Swamp Palace Exit', 'Ganons Tower Exit', 'Desert Palace Exit (North)', 'Agahnims Tower Exit', 'Spiral Cave Exit (Top)',
                                          'Superbunny Cave Exit (Bottom)', 'Turtle Rock Ledge Exit (East)']:
                        # For exits that connot be reached from another, no need to apply offset fixes.
                        write_int16(rom, 0x15DB5 + 2 * offset, link_y) # same as final else
                    elif room_id == 0x0059 and world.fix_skullwoods_exit[player]:
                        write_int16(rom, 0x15DB5 + 2 * offset, 0x00F8)
                    elif room_id == 0x004a and world.fix_palaceofdarkness_exit[player]:
                        write_int16(rom, 0x15DB5 + 2 * offset, 0x0640)
                    elif room_id == 0x00d6 and world.fix_trock_exit[player]:
                        write_int16(rom, 0x15DB5 + 2 * offset, 0x0134)
                    elif room_id == 0x000c and world.fix_gtower_exit[player]: # fix ganons tower exit point
                        write_int16(rom, 0x15DB5 + 2 * offset, 0x00A4)
                    else:
                        write_int16(rom, 0x15DB5 + 2 * offset, link_y)

                    write_int16(rom, 0x15E53 + 2 * offset, link_x)
                    write_int16(rom, 0x15EF1 + 2 * offset, camera_y)
                    write_int16(rom, 0x15F8F + 2 * offset, camera_x)
                    rom.write_byte(0x1602D + offset, unknown_1)
                    rom.write_byte(0x1607C + offset, unknown_2)
                    write_int16(rom, 0x160CB + 2 * offset, door_1)
                    write_int16(rom, 0x16169 + 2 * offset, door_2)
                elif isinstance(exit.addresses, list):
                    # is hole
                    for address in exit.addresses:
                        rom.write_byte(address, exit.target)
                else:
                    # patch door table
                    rom.write_byte(0xDBB73 + exit.addresses, exit.target)
                    if exit.name == 'Tavern North':
                        rom.write_byte(0x157D0, exit.target)
    if world.mode[player] == 'inverted':
        patch_shuffled_dark_sanc(world, rom, player)

    # setup dr option flags based on experimental, etc.
    dr_flags = DROptions.NoOptions
    if world.mirrorscroll[player]:
        dr_flags |= DROptions.Town_Portal
    if world.doorShuffle[player] == 'vanilla':
        dr_flags |= DROptions.Eternal_Mini_Bosses 
    if world.doorShuffle[player] not in  ['vanilla', 'basic']:
        dr_flags |= DROptions.Map_Info
    if ((world.collection_rate[player] or world.goal[player] == 'completionist')
       and world.goal[player] not in ['triforcehunt', 'trinity', 'ganonhunt']):
        dr_flags |= DROptions.Debug
        rom.write_byte(snes_to_pc(0x308039), 1)
    if world.doorShuffle[player] not in ['vanilla', 'basic'] and world.logic[player] != 'nologic'\
       and world.mixed_travel[player] == 'prevent':
        # PoD Falling Bridge or Hammjump
        # 1FA607: db $2D, $79, $69 ; 0x0069: Vertical Rail ↕ | { 0B, 1E } | Size: 05
        # 1FA60A: db $14, $99, $5D ; 0x005D: Large Horizontal Rail ↔ | { 05, 26 } | Size: 01
        rom.write_bytes(0xfa607, [0x2d, 0x79, 0x69, 0x14, 0x99, 0x5d])
        # PoD Arena
        # 1FA573: db $D4, $B2, $22 ; 0x0022: Horizontal Rail ↔ | { 35, 2C } | Size: 02
        # 1FA576: db $D4, $CE, $22 ; 0x0022: Horizontal Rail ↔ | { 35, 33 } | Size: 01
        # 1FA579: db $D9, $AE, $69 ; 0x0069: Vertical Rail ↕ | { 36, 2B } | Size: 06
        rom.write_bytes(0xfa573, [0xd4, 0xb2, 0x22, 0xd4, 0xce, 0x22, 0xd9, 0xae, 0x69])
        # Mire BK Pond
        # 1FB1FC: db $C8, $9D, $69 ; 0x0069: Vertical Rail ↕ | { 32, 27 } | Size: 01
        # 1FB1FF: db $B4, $AC, $5D ; 0x005D: Large Horizontal Rail ↔ | { 2D, 2B } | Size: 00
        rom.write_bytes(0xfb1fc, [0xc8, 0x9d, 0x69, 0xb4, 0xac, 0x5d])
    if world.standardize_palettes[player] == 'original':
        dr_flags |= DROptions.OriginalPalettes
    dr_flags |= DROptions.DarkWorld_Spawns  # no longer experimental
    if world.logic[player] not in ['owglitches', 'hybridglitches', 'nologic']:
        dr_flags |= DROptions.Fix_EG
    if world.door_type_mode[player] in ['big', 'all', 'chaos']:
        dr_flags |= DROptions.BigKeyDoor_Shuffle
    if world.dropshuffle[player] in ['underworld']:
        dr_flags |= DROptions.EnemyDropIndicator

    my_locations = world.get_filled_locations(player)
    valid_locations = [l for l in my_locations if ((l.type == LocationType.Pot and not l.forced_item)
                                                   or (l.type == LocationType.Drop and not l.forced_item)
                                                   or (l.type == LocationType.Normal and not l.forced_item)
                                                   or (l.type == LocationType.Shop and world.shopsanity[player]))]
    valid_loc_by_dungeon = valid_dungeon_locations(valid_locations)

    # fix hc big key problems (map and compass too)
    if (world.doorShuffle[player] != 'vanilla' or world.dropshuffle[player] != 'none'
            or world.pottery[player] not in ['none', 'cave']):
        rom.write_byte(0x151f1, 2)
        rom.write_byte(0x15270, 2)
        sanctuary = world.get_region('Sanctuary', player)
        rom.write_byte(0x1597b, sanctuary.dungeon.dungeon_id*2)
        update_compasses(rom, valid_loc_by_dungeon, world, player)

    def should_be_bunny(region, mode):
        if mode != 'inverted':
            return region.is_dark_world and not region.is_light_world
        else:
            return region.is_light_world and not region.is_dark_world

    # dark world spawns
    sanc_region = world.get_region('Sanctuary', player)
    if should_be_bunny(sanc_region, world.mode[player]):
        rom.write_bytes(0x13fff2, [0x12, 0x00])

    lh_name = 'Links House'
    links_house = world.get_region(lh_name, player)
    if should_be_bunny(links_house, world.mode[player]):
        rom.write_bytes(0x13fff0, [0x04, 0x01])

    old_man_house = world.get_region('Old Man House', player)
    if should_be_bunny(old_man_house, world.mode[player]):
        rom.write_bytes(0x13fff4, [0xe4, 0x00])

    # patch doors
    if world.doorShuffle[player] not in ['vanilla', 'basic']:
        rom.write_byte(0x138002, 2)
        for name, layout in world.key_layout[player].items():
            offset = compass_data[name][4]//2
            if world.keyshuffle[player] == 'universal':
                rom.write_byte(0x187010+offset, layout.max_chests + layout.max_drops)
            else:
                rom.write_byte(0x13f020+offset, layout.max_chests + layout.max_drops)  # not currently used
                rom.write_byte(0x187010+offset, layout.max_chests)
            builder = world.dungeon_layouts[player][name]
            bk_status = 1 if builder.bk_required else 0
            bk_status = 2 if builder.bk_provided else bk_status
            rom.write_byte(0x13f040+offset*2, bk_status)
        if player in world.sanc_portal.keys():
            rom.write_byte(0x159a6, world.sanc_portal[player].ent_offset)
            sanc_region = world.sanc_portal[player].door.entrance.parent_region
            if sanc_region.is_dark_world and not sanc_region.is_light_world:
                rom.write_byte(0x13ff00, 1)
        for room in world.rooms:
            if room.player == player and room.palette is not None:
                rom.write_byte(0x13f200+room.index, room.palette)
    if world.doorShuffle[player] == 'basic':
        rom.write_byte(0x138002, 1)
    for door in world.doors:
        if door.dest is not None and isinstance(door.dest, Door) and\
             door.player == player and door.type in [DoorType.Normal, DoorType.SpiralStairs,
                                                     DoorType.Open, DoorType.StraightStairs, DoorType.Ladder]:
            rom.write_bytes(door.getAddress(), door.dest.getTarget(door))
    for paired_door in world.paired_doors[player]:
        rom.write_bytes(paired_door.address_a(world, player), paired_door.rom_data_a(world, player))
        rom.write_bytes(paired_door.address_b(world, player), paired_door.rom_data_b(world, player))
    if world.doorShuffle[player] != 'vanilla':
        for name, pair in boss_indicator.items():
            dungeon_id, boss_door = pair
            boss_region = world.get_door(boss_door, player).entrance.parent_region
            opposite_door = next(iter(x for x in boss_region.entrances if x.name != 'Skull Final Drop WS')).door
            if opposite_door and isinstance(opposite_door, Door) and opposite_door.roomIndex > -1:
                dungeon_name = opposite_door.entrance.parent_region.dungeon.name
                dungeon_id = boss_indicator[dungeon_name][0]
                rom.write_byte(0x13f000+dungeon_id, opposite_door.roomIndex)
            elif not opposite_door:
                rom.write_byte(0x13f000+dungeon_id, 0)  # no supertile preceeding boss
    if is_mystery:
        dr_flags |= DROptions.Hide_Total
    rom.write_byte(0x138004, dr_flags.value & 0xff)
    rom.write_byte(0x138005, (dr_flags.value & 0xff00) >> 8)
    if dr_flags & DROptions.Town_Portal and world.mode[player] == 'inverted':
        rom.write_byte(0x138006, 1)

    # swap in non-ER Lobby Shuffle Inverted - but only then
    if world.mode[player] == 'inverted' and world.intensity[player] >= 3 and world.doorShuffle[player] != 'vanilla' and world.shuffle[player] == 'vanilla':
        aga_portal = world.get_portal('Agahnims Tower', player)
        gt_portal = world.get_portal('Ganons Tower', player)
        aga_portal.exit_offset, gt_portal.exit_offset = gt_portal.exit_offset, aga_portal.exit_offset
        aga_portal.default = False
        gt_portal.default = False

    for portal in world.dungeon_portals[player]:
        if not portal.default:
            offset = portal.ent_offset
            rom.write_byte(0x14577 + offset*2, portal.current_room())
            rom.write_bytes(0x14681 + offset*8, portal.relative_coords())
            rom.write_bytes(0x14aa9 + offset*2, portal.scroll_x())
            rom.write_bytes(0x14bb3 + offset*2, portal.scroll_y())
            rom.write_bytes(0x14cbd + offset*2, portal.link_y())
            rom.write_bytes(0x14dc7 + offset*2, portal.link_x())
            rom.write_bytes(0x14fdb + offset*2, portal.camera_x())
            rom.write_byte(0x152f9 + offset, portal.bg_setting())
            rom.write_byte(0x1537e + offset, portal.hv_scroll())
            rom.write_byte(0x15403 + offset, portal.scroll_quad())
            rom.write_byte(0x15aee + portal.exit_offset, portal.current_room())
            if portal.boss_exit_idx > -1:
                rom.write_byte(0x7939 + portal.boss_exit_idx, portal.current_room())

    # fix exits, if not fixed during exit patching
    if world.fix_skullwoods_exit[player] and world.shuffle[player] == 'vanilla':
        write_int16(rom, 0x15DB5 + 2 * exit_ids['Skull Woods Final Section Exit'][1], 0x00F8)
    elif world.force_fix[player]['sw']:
        write_int16(rom, 0x15DB5 + world.force_fix[player]['sw'].exit_offset, 0x00F8)
    if world.force_fix[player]['pod']:
        write_int16(rom, 0x15DB5 + world.force_fix[player]['pod'].exit_offset, 0x0640)
    if world.force_fix[player]['tr']:
        write_int16(rom, 0x15DB5 + world.force_fix[player]['tr'].exit_offset, 0x0134)
    if world.force_fix[player]['gt']:
        write_int16(rom, 0x15DB5 + world.force_fix[player]['gt'].exit_offset, 0x00A4)

    write_custom_shops(rom, world, player)

    def credits_digit(num):
        # top: $54 is 1, 55 2, etc , so 57=4, 5C=9
        # bot: $7A is 1, 7B is 2, etc so 7D=4, 82=9 (zero unknown...)
        return 0x53+int(num), 0x79+int(num)

    credits_total = len(valid_locations)

    if world.dropshuffle[player] != 'none' or world.pottery[player] != 'none':
        rom.write_byte(0x142A50, 1)  # StandingItemsOn
    multiClientFlags = ((0x1 if world.dropshuffle[player] != 'none' else 0)
                        | (0x2 if world.shopsanity[player] else 0)
                        | (0x4 if world.take_any[player] != 'none' else 0)
                        | (0x8 if world.pottery[player] != 'none' else 0)
                        | (0x10 if is_mystery else 0))
    rom.write_byte(0x142A51, multiClientFlags)
    # StandingItemCounterMask
    rom.write_byte(0x142A55, ((0x1 if world.pottery[player] not in ['none', 'cave'] else 0)
                              | (0x2 if world.dropshuffle[player] != 'none' else 0)))
    if world.pottery[player] not in ['none', 'keys']:
        # Cuccos should not prevent kill rooms from opening
        rom.write_byte(snes_to_pc(0x0DB457), 0x40)
    rom.write_byte(snes_to_pc(0x28AA56), 0 if world.pottery[player] == 'none' else 1)

    write_int16(rom, 0x180196, credits_total)  # dynamic credits
    if credits_total != 216:
        # collection rate address (hi):
        cr_address = 0x238055
        cr_pc = snes_to_pc(cr_address)  # convert to pc
        first_top, first_bot = credits_digit((credits_total // 100) % 10)
        mid_top, mid_bot = credits_digit((credits_total // 10) % 10)
        last_top, last_bot = credits_digit(credits_total % 10)
        if credits_total >= 1000:
            thousands_top, thousands_bot = credits_digit((credits_total // 1000) % 10)
            rom.write_byte(cr_pc, 0xDB)  # slash
            rom.write_byte(cr_pc+1, thousands_top)
            rom.write_byte(cr_pc+0x1e, 0xEE)  # slash
            rom.write_byte(cr_pc+0x1f, thousands_bot)
            # modify stat config
            stat_address = 0x239864
            stat_pc = snes_to_pc(stat_address)
            rom.write_byte(stat_pc, 0xa9)  # change to pos 21 (from b1)
            rom.write_byte(stat_pc+2, 0xc0)  # change to 12 bits (from a0)
            rom.write_byte(stat_pc+3, 0x80)  # change to four digits (from 60)

        # top half
        rom.write_byte(cr_pc+2, first_top)
        rom.write_byte(cr_pc+3, mid_top)
        rom.write_byte(cr_pc+4, last_top)
        # bottom half
        rom.write_byte(cr_pc+0x20, first_bot)
        rom.write_byte(cr_pc+0x21, mid_bot)
        rom.write_byte(cr_pc+0x22, last_bot)

    # patch medallion requirements
    if world.required_medallions[player][0] == 'Bombos':
        rom.write_byte(0x180022, 0x00)  # requirement
        rom.write_byte(0x4FF2, 0x31)  # sprite
        rom.write_byte(0x50D1, 0x80)
        rom.write_byte(0x51B0, 0x00)
    elif world.required_medallions[player][0] == 'Quake':
        rom.write_byte(0x180022, 0x02)  # requirement
        rom.write_byte(0x4FF2, 0x31)  # sprite
        rom.write_byte(0x50D1, 0x88)
        rom.write_byte(0x51B0, 0x00)
    if world.required_medallions[player][1] == 'Bombos':
        rom.write_byte(0x180023, 0x00)  # requirement
        rom.write_byte(0x5020, 0x31)  # sprite
        rom.write_byte(0x50FF, 0x90)
        rom.write_byte(0x51DE, 0x00)
    elif world.required_medallions[player][1] == 'Ether':
        rom.write_byte(0x180023, 0x01)  # requirement
        rom.write_byte(0x5020, 0x31)  # sprite
        rom.write_byte(0x50FF, 0x98)
        rom.write_byte(0x51DE, 0x00)

    # set open mode:
    if world.mode[player] in ['open', 'inverted']:
        init_open_mode_sram(rom)
    if world.mode[player] == 'inverted':
        set_inverted_mode(world, player, rom)
    elif world.mode[player] == 'standard':
        init_standard_mode_sram(rom)

    uncle_location = world.get_location('Link\'s Uncle', player)
    if uncle_location.item is None or uncle_location.item.name not in ['Master Sword', 'Tempered Sword', 'Fighter Sword', 'Golden Sword', 'Progressive Sword']:
        # disable sword sprite from uncle
        rom.write_bytes(0x6D263, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
        rom.write_bytes(0x6D26B, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
        rom.write_bytes(0x6D293, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
        rom.write_bytes(0x6D29B, [0x00, 0x00, 0xf7, 0xff, 0x00, 0x0E])
        rom.write_bytes(0x6D2B3, [0x00, 0x00, 0xf6, 0xff, 0x02, 0x0E])
        rom.write_bytes(0x6D2BB, [0x00, 0x00, 0xf6, 0xff, 0x02, 0x0E])
        rom.write_bytes(0x6D2E3, [0x00, 0x00, 0xf7, 0xff, 0x02, 0x0E])
        rom.write_bytes(0x6D2EB, [0x00, 0x00, 0xf7, 0xff, 0x02, 0x0E])
        rom.write_bytes(0x6D31B, [0x00, 0x00, 0xe4, 0xff, 0x08, 0x0E])
        rom.write_bytes(0x6D323, [0x00, 0x00, 0xe4, 0xff, 0x08, 0x0E])

    # set light cones
    rom.write_byte(0x180038, 0x01 if world.sewer_light_cone[player] else 0x00)

    GREEN_TWENTY_RUPEES = 0x47
    TRIFORCE_PIECE = ItemFactory('Triforce Piece', player).code
    GREEN_CLOCK = ItemFactory('Green Clock', player).code

    rom.write_byte(0x18004F, 0x01)  # Byrna Invulnerability: on

    # handle difficulty_adjustments
    if world.difficulty_adjustments[player] == 'hard':
        rom.write_byte(0x180181, 0x01) # Make silver arrows work only on ganon
        rom.write_byte(0x180182, 0x00) # Don't auto equip silvers on pickup
        # Powdered Fairies Prize
        rom.write_byte(0x36DD0, 0xD8)  # One Heart
        # potion heal amount
        rom.write_byte(0x180084, 0x38)  # Seven Hearts
        # potion magic restore amount
        rom.write_byte(0x180085, 0x40)  # Half Magic
        #Cape magic cost
        rom.write_bytes(0x3ADA7, [0x02, 0x04, 0x08])
        # Byrna Invulnerability: off
        rom.write_byte(0x18004F, 0x00)
        #Disable catching fairies
        rom.write_byte(0x34FD6, 0x80)
        overflow_replacement = GREEN_TWENTY_RUPEES
        # Rupoor negative value
        write_int16(rom, 0x180036, world.rupoor_cost)
        # Set stun items
        rom.write_byte(0x180180, 0x02) # Hookshot only
    elif world.difficulty_adjustments[player] == 'expert':
        rom.write_byte(0x180181, 0x01) # Make silver arrows work only on ganon
        rom.write_byte(0x180182, 0x00) # Don't auto equip silvers on pickup
        # Powdered Fairies Prize
        rom.write_byte(0x36DD0, 0xD8)  # One Heart
        # potion heal amount
        rom.write_byte(0x180084, 0x20)  # 4 Hearts
        # potion magic restore amount
        rom.write_byte(0x180085, 0x20)  # Quarter Magic
        #Cape magic cost
        rom.write_bytes(0x3ADA7, [0x02, 0x04, 0x08])
        # Byrna Invulnerability: off
        rom.write_byte(0x18004F, 0x00)
        #Disable catching fairies
        rom.write_byte(0x34FD6, 0x80)
        overflow_replacement = GREEN_TWENTY_RUPEES
        # Rupoor negative value
        write_int16(rom, 0x180036, world.rupoor_cost)
        # Set stun items
        rom.write_byte(0x180180, 0x00) # Nothing
    else:
        rom.write_byte(0x180181, 0x00) # Make silver arrows freely usable
        rom.write_byte(0x180182, 0x01) # auto equip silvers on pickup
        # Powdered Fairies Prize
        rom.write_byte(0x36DD0, 0xE3)  # fairy
        # potion heal amount
        rom.write_byte(0x180084, 0xA0)  # full
        # potion magic restore amount
        rom.write_byte(0x180085, 0x80)  # full
        #Cape magic cost
        rom.write_bytes(0x3ADA7, [0x04, 0x08, 0x10])
        # Byrna Invulnerability: on
        rom.write_byte(0x18004F, 0x01)
        #Enable catching fairies
        rom.write_byte(0x34FD6, 0xF0)
        # Rupoor negative value
        write_int16(rom, 0x180036, world.rupoor_cost)
        # Set stun items
        rom.write_byte(0x180180, 0x03) # All standard items
        #Set overflow items for progressive equipment
        if world.timer in ['timed', 'timed-countdown', 'timed-ohko']:
            overflow_replacement = GREEN_CLOCK
        else:
            overflow_replacement = GREEN_TWENTY_RUPEES

    #Byrna residual magic cost
    rom.write_bytes(0x45C42, [0x04, 0x02, 0x01])

    difficulty = world.difficulty_requirements[player]

    #Set overflow items for progressive equipment
    rom.write_bytes(0x180090,
                    [difficulty.progressive_sword_limit if world.swords[player] != 'swordless' else 0, overflow_replacement,
                     difficulty.progressive_shield_limit, overflow_replacement,
                     difficulty.progressive_armor_limit, overflow_replacement,
                     difficulty.progressive_bottle_limit, overflow_replacement])

    #Work around for json patch ordering issues - write bow limit separately so that it is replaced in the patch
    rom.write_bytes(0x180098, [difficulty.progressive_bow_limit, overflow_replacement])

    if difficulty.progressive_bow_limit < 2 and world.swords[player] == 'swordless':
        rom.write_bytes(0x180098, [2, overflow_replacement])

    # set up game internal RNG seed
    for i in range(1024):
        rom.write_byte(0x178000 + i, random.randint(0, 255))

    # shuffle prize packs
    prizes = [0xD8, 0xD8, 0xD8, 0xD8, 0xD9, 0xD8, 0xD8, 0xD9,
              0xDA, 0xD9, 0xDA, 0xDB, 0xDA, 0xD9, 0xDA, 0xDA,
              0xE0, 0xDF, 0xDF, 0xDA, 0xE0, 0xDF, 0xD8, 0xDF,
              0xDC, 0xDC, 0xDC, 0xDD, 0xDC, 0xDC, 0xDE, 0xDC,
              0xE1, 0xD8, 0xE1, 0xE2, 0xE1, 0xD8, 0xE1, 0xE2,
              0xDF, 0xD9, 0xD8, 0xE1, 0xDF, 0xDC, 0xD9, 0xD8,
              0xD8, 0xE3, 0xE0, 0xDB, 0xDE, 0xD8, 0xDB, 0xE2,
              0xD9, 0xDA, 0xDB, 0xD9, 0xDB, 0xD9, 0xDB]
    dig_prizes = [0xB2, 0xD8, 0xD8, 0xD8, 0xD8, 0xD8, 0xD8, 0xD8, 0xD8,
                  0xD9, 0xD9, 0xD9, 0xD9, 0xD9, 0xDA, 0xDA, 0xDA, 0xDA, 0xDA,
                  0xDB, 0xDB, 0xDB, 0xDB, 0xDB, 0xDC, 0xDC, 0xDC, 0xDC, 0xDC,
                  0xDD, 0xDD, 0xDD, 0xDD, 0xDD, 0xDE, 0xDE, 0xDE, 0xDE, 0xDE,
                  0xDF, 0xDF, 0xDF, 0xDF, 0xDF, 0xE0, 0xE0, 0xE0, 0xE0, 0xE0,
                  0xE1, 0xE1, 0xE1, 0xE1, 0xE1, 0xE2, 0xE2, 0xE2, 0xE2, 0xE2,
                  0xE3, 0xE3, 0xE3, 0xE3, 0xE3]

    def chunk(l,n):
        return [l[i:i+n] for i in range(0, len(l), n)]

    # randomize last 7 slots
    possible_prizes = {
        'Small Heart': 0xD8, 'Fairy': 0xE3,
        'Rupee (1)': 0xD9, 'Rupees (5)': 0xDA, 'Rupees (20)': 0xDB,
        'Big Magic': 0xE0, 'Small Magic': 0xDF,
        'Single Bomb': 0xDC, 'Bombs (4)': 0xDD,
        'Bombs (8)': 0xDE, 'Arrows (5)': 0xE1, 'Arrows (10)': 0xE2
    }  #weights, if desired 13, 1, 9, 7, 6, 3, 6, 7, 1, 2, 5, 3
    uniform_prizes = list(possible_prizes.values())
    prizes[-7:] = random.sample(prizes, 7)

    #shuffle order of 7 main packs
    packs = chunk(prizes[:56], 8)
    random.shuffle(packs)
    prizes[:56] = [drop for pack in packs for drop in pack]

    if world.customizer:
        drops = world.customizer.get_drops()
        if drops:
            for player, drop_config in drops.items():
                for pack_num in range(1, 8):
                    if f'Pack {pack_num}' in drop_config:
                        for idx, prize in enumerate(drop_config[f'Pack {pack_num}']):
                            chosen = random.choice(uniform_prizes) if prize == 'Random' else possible_prizes[prize]
                            prizes[(pack_num-1)*8 + idx] = chosen
                for tree_pull_tier in range(1, 4):
                    if f'Tree Pull Tier {tree_pull_tier}' in drop_config:
                        prize = drop_config[f'Tree Pull Tier {tree_pull_tier}']
                        chosen = random.choice(uniform_prizes) if prize == 'Random' else possible_prizes[prize]
                        prizes[63-tree_pull_tier] = chosen  # (62 through 60 in reverse)
                for key, pos in {'Crab Normal': 59, 'Crab Special': 58, 'Stun Prize': 57, 'Fish': 56}.items():
                    if key in drop_config:
                        prize = drop_config[key]
                        chosen = random.choice(uniform_prizes) if prize == 'Random' else possible_prizes[prize]
                        prizes[pos] = chosen

    if world.difficulty_adjustments[player] in ['hard', 'expert']:
        prize_replacements = {0xE0: 0xDF, # Fairy -> heart
                              0xE3: 0xD8} # Big magic -> small magic
        prizes = [prize_replacements.get(prize, prize) for prize in prizes]
        dig_prizes = [prize_replacements.get(prize, prize) for prize in dig_prizes]

    if world.bow_mode[player].startswith('retro'):
        prize_replacements = {0xE1: 0xDA, #5 Arrows -> Blue Rupee
                              0xE2: 0xDB} #10 Arrows -> Red Rupee
        prizes = [prize_replacements.get(prize, prize) for prize in prizes]
        dig_prizes = [prize_replacements.get(prize, prize) for prize in dig_prizes]
    rom.write_bytes(0x180100, dig_prizes)

    # write tree pull prizes
    rom.write_byte(0xEFBD4, prizes.pop())
    rom.write_byte(0xEFBD5, prizes.pop())
    rom.write_byte(0xEFBD6, prizes.pop())

    # rupee crab prizes
    rom.write_byte(0x329C8, prizes.pop())  # first prize
    rom.write_byte(0x329C4, prizes.pop())  # final prize

    # stunned enemy prize
    rom.write_byte(0x37993, prizes.pop())

    # saved fish prize
    rom.write_byte(0xE82CC, prizes.pop())

    # fill enemy prize packs
    rom.write_bytes(0x37A78, prizes)

    # set bonk prizes
    bonk_prizes = [0x79, 0xE3, 0x79, 0xAC, 0xAC, 0xE0, 0xDC, 0xAC, 0xE3, 0xE3, 0xDA, 0xE3, 0xDA, 0xD8, 0xAC, 0xAC, 0xE3, 0xD8, 0xE3, 0xE3, 0xE3, 0xE3, 0xE3, 0xE3, 0xDC, 0xDB, 0xE3, 0xDA, 0x79, 0x79, 0xE3, 0xE3,
                   0xDA, 0x79, 0xAC, 0xAC, 0x79, 0xE3, 0x79, 0xAC, 0xAC, 0xE0, 0xDC, 0xE3, 0x79, 0xDE, 0xE3, 0xAC, 0xDB, 0x79, 0xE3, 0xD8, 0xAC, 0x79, 0xE3, 0xDB, 0xDB, 0xE3, 0xE3, 0x79, 0xD8, 0xDD]
    bonk_addresses = [0x4CF6C, 0x4CFBA, 0x4CFE0, 0x4CFFB, 0x4D018, 0x4D01B, 0x4D028, 0x4D03C, 0x4D059, 0x4D07A, 0x4D09E, 0x4D0A8, 0x4D0AB, 0x4D0AE, 0x4D0BE, 0x4D0DD,
                      0x4D16A, 0x4D1E5, 0x4D1EE, 0x4D20B, 0x4CBBF, 0x4CBBF, 0x4CC17, 0x4CC1A, 0x4CC4A, 0x4CC4D, 0x4CC53, 0x4CC69, 0x4CC6F, 0x4CC7C, 0x4CCEF, 0x4CD51,
                      0x4CDC0, 0x4CDC3, 0x4CDC6, 0x4CE37, 0x4D2DE, 0x4D32F, 0x4D355, 0x4D367, 0x4D384, 0x4D387, 0x4D397, 0x4D39E, 0x4D3AB, 0x4D3AE, 0x4D3D1, 0x4D3D7,
                      0x4D3F8, 0x4D416, 0x4D420, 0x4D423, 0x4D42D, 0x4D449, 0x4D48C, 0x4D4D9, 0x4D4DC, 0x4D4E3, 0x4D504, 0x4D507, 0x4D55E, 0x4D56A]
    if world.shuffle_bonk_prizes:
        random.shuffle(bonk_prizes)
    for prize, address in zip(bonk_prizes, bonk_addresses):
        rom.write_byte(address, prize)

    # Fill in item substitutions table
    rom.write_bytes(0x184000, [
        # original_item, limit, replacement_item, filler
        0x12, 0x01, 0x35, 0xFF, # lamp -> 5 rupees
        0x51, 0x00 if world.bombbag[player] else 0x06, 0x31 if world.bombbag[player] else 0x52, 0xFF, # 6 +5 bomb upgrades -> +10 bomb upgrade. If bombbag -> turns into Bombs (10)
        0x53, 0x06, 0x54, 0xFF, # 6 +5 arrow upgrades -> +10 arrow upgrade
        0x58, 0x01, 0x36 if world.bow_mode[player].startswith('retro') else 0x43, 0xFF, # silver arrows -> single arrow (red 20 in retro mode)
        0x3E, difficulty.boss_heart_container_limit, 0x47, 0xff, # boss heart -> green 20
        0x17, difficulty.heart_piece_limit, 0x47, 0xff, # piece of heart -> green 20
        0xFF, 0xFF, 0xFF, 0xFF, # end of table sentinel
    ])

    # set Fountain bottle exchange items
    rom.write_byte(0x348FF, ItemFactory(world.bottle_refills[player][0], player).code)
    rom.write_byte(0x3493B, ItemFactory(world.bottle_refills[player][1], player).code)

    #enable Fat Fairy Chests
    rom.write_bytes(0x1FC16, [0xB1, 0xC6, 0xF9, 0xC9, 0xC6, 0xF9])
    # set Fat Fairy Bow/Sword prizes to be disappointing
    rom.write_byte(0x34914, 0x3A)  # Bow and Arrow
    rom.write_byte(0x180028, 0x49)  # Fighter Sword
    # enable Waterfall fairy chests
    rom.write_bytes(0xE9AE, [0x14, 0x01])
    rom.write_bytes(0xE9CF, [0x14, 0x01])
    rom.write_bytes(0x1F714, [225, 0, 16, 172, 13, 41, 154, 1, 88, 152, 15, 17, 177, 97, 252, 77, 129, 32, 218, 2, 44, 225, 97, 252, 190, 129, 97, 177, 98, 84, 218, 2,
                              253, 141, 131, 68, 225, 98, 253, 30, 131, 49, 165, 201, 49, 164, 105, 49, 192, 34, 77, 164, 105, 49, 198, 249, 73, 198, 249, 16, 153, 160, 92, 153,
                              162, 11, 152, 96, 13, 232, 192, 85, 232, 192, 11, 146, 0, 115, 152, 96, 254, 105, 0, 152, 163, 97, 254, 107, 129, 254, 171, 133, 169, 200, 97, 254,
                              174, 129, 255, 105, 2, 216, 163, 98, 255, 107, 131, 255, 43, 135, 201, 200, 98, 255, 46, 131, 254, 161, 0, 170, 33, 97, 254, 166, 129, 255, 33, 2,
                              202, 33, 98, 255, 38, 131, 187, 35, 250, 195, 35, 250, 187, 43, 250, 195, 43, 250, 187, 83, 250, 195, 83, 250, 176, 160, 61, 152, 19, 192, 152, 82,
                              192, 136, 0, 96, 144, 0, 96, 232, 0, 96, 240, 0, 96, 152, 202, 192, 216, 202, 192, 216, 19, 192, 216, 82, 192, 252, 189, 133, 253, 29, 135, 255,
                              255, 255, 255, 240, 255, 128, 46, 97, 14, 129, 14, 255, 255])
    # set Waterfall fairy prizes to be disappointing
    rom.write_byte(0x348DB, 0x3A)  # Red Boomerang becomes Red Boomerang
    rom.write_byte(0x348EB, 0x05)  # Blue Shield becomes Blue Shield

    # Remove Statues for upgrade fairy
    rom.write_bytes(0x01F810, [0x1A, 0x1E, 0x01, 0x1A, 0x1E, 0x01])


    rom.write_byte(0x180029, 0x01) # Smithy quick item give

    # set swordless mode settings
    rom.write_byte(0x18003F, 0x01 if world.swords[player] == 'swordless' else 0x00)  # hammer can harm ganon
    rom.write_byte(0x180041, 0x01 if world.swords[player] == 'swordless' else 0x00)  # swordless medallions
    rom.write_byte(0x180044, 0x01 if world.swords[player] == 'swordless' else 0x00)  # hammer activates tablets
    if world.swords[player] == 'swordless':
        rom.initial_sram.set_swordless_curtains()  # open curtains

    # set up clocks for timed modes
    if world.shuffle[player] == 'vanilla':
        ERtimeincrease = 0
    elif world.shuffle[player] in ['dungeonssimple', 'dungeonsfull']:
        ERtimeincrease = 10
    else:
        ERtimeincrease = 20
    if world.keyshuffle[player] != 'none' or world.bigkeyshuffle[player] or world.mapshuffle[player]:
        ERtimeincrease = ERtimeincrease + 15
    if world.clock_mode == 'none':
        rom.write_bytes(0x180190, [0x00, 0x00, 0x00])  # turn off clock mode
        write_int32(rom, 0x180200, 0)  # red clock adjustment time (in frames, sint32)
        write_int32(rom, 0x180204, 0)  # blue clock adjustment time (in frames, sint32)
        write_int32(rom, 0x180208, 0)  # green clock adjustment time (in frames, sint32)
        rom.initial_sram.set_starting_timer(0)  # starting time (in frames, sint32)
    elif world.clock_mode == 'ohko':
        rom.write_bytes(0x180190, [0x01, 0x02, 0x01])  # ohko timer with resetable timer functionality
        write_int32(rom, 0x180200, 0)  # red clock adjustment time (in frames, sint32)
        write_int32(rom, 0x180204, 0)  # blue clock adjustment time (in frames, sint32)
        write_int32(rom, 0x180208, 0)  # green clock adjustment time (in frames, sint32)
        rom.initial_sram.set_starting_timer(0)  # starting time (in frames, sint32)
    elif world.clock_mode == 'countdown-ohko':
        rom.write_bytes(0x180190, [0x01, 0x02, 0x01])  # ohko timer with resetable timer functionality
        write_int32(rom, 0x180200, -100 * 60 * 60 * 60)  # red clock adjustment time (in frames, sint32)
        write_int32(rom, 0x180204, 2 * 60 * 60)  # blue clock adjustment time (in frames, sint32)
        write_int32(rom, 0x180208, 4 * 60 * 60)  # green clock adjustment time (in frames, sint32)
        if world.difficulty_adjustments == 'normal':
            rom.initial_sram.set_starting_timer((10 + ERtimeincrease) * 60)  # starting time (in seconds)
        else:
            rom.initial_sram.set_starting_timer(int((5 + ERtimeincrease / 2) * 60))  # starting time (in seconds)
    if world.clock_mode == 'stopwatch':
        rom.write_bytes(0x180190, [0x02, 0x01, 0x00])  # set stopwatch mode
        write_int32(rom, 0x180200, -2 * 60 * 60)  # red clock adjustment time (in frames, sint32)
        write_int32(rom, 0x180204, 2 * 60 * 60)  # blue clock adjustment time (in frames, sint32)
        write_int32(rom, 0x180208, 4 * 60 * 60)  # green clock adjustment time (in frames, sint32)
        rom.initial_sram.set_starting_timer(0)  # starting time (in frames, sint32)
    if world.clock_mode == 'countdown':
        rom.write_bytes(0x180190, [0x01, 0x01, 0x00])  # set countdown, with no reset available
        write_int32(rom, 0x180200, -2 * 60 * 60)  # red clock adjustment time (in frames, sint32)
        write_int32(rom, 0x180204, 2 * 60 * 60)  # blue clock adjustment time (in frames, sint32)
        write_int32(rom, 0x180208, 4 * 60 * 60)  # green clock adjustment time (in frames, sint32)
        rom.initial_sram.set_starting_timer((40 + ERtimeincrease) * 60)  # starting time (in seconds)

    # set up goals for treasure hunt
    rom.write_bytes(0x180165, [0x0E, 0x28] if world.treasure_hunt_icon[player] == 'Triforce Piece' else [0x0D, 0x28])
    if world.goal[player] in ['triforcehunt', 'trinity', 'ganonhunt']:
        rom.write_bytes(0x180167, int16_as_bytes(world.treasure_hunt_count[player]))
    rom.write_byte(0x180194, 1)  # Must turn in triforced pieces (instant win not enabled)

    rom.write_bytes(0x180213, [0x00, 0x01])  # Not a Tournament Seed

    gametype = 0x04 # item
    if (world.shuffle[player] != 'vanilla' or world.doorShuffle[player] != 'vanilla'
       or world.dropshuffle[player] != 'none' or world.pottery[player] != 'none'):
        gametype |= 0x02  # entrance/door
    rom.write_byte(0x180211, gametype)  # Game type

    # assorted fixes
    rom.write_byte(0x1800A2, 0x01 if world.fix_fake_world[player] else 0x00)  # remain in real dark world when dying in dark world dungeon before killing aga1
    rom.write_byte(0x180169, 0x01 if world.lock_aga_door_in_escape else 0x00)  # Lock or unlock aga tower door during escape sequence.
    if world.mode[player] == 'inverted':
        rom.write_byte(0x180169, 0x02)  # lock aga/ganon tower door with crystals in inverted
    rom.write_byte(0x180171, 0x01 if world.ganon_at_pyramid[player] else 0x00)  # Enable respawning on pyramid after ganon death
    rom.write_byte(0x180173, 0x01) # Bob is enabled
    rom.write_byte(0x180195, 0x08)  # Spike Cave Damage
    rom.write_bytes(0x18016B, [0x04, 0x02, 0x01]) # Set spike cave and MM spike room Byrna usage
    rom.write_bytes(0x18016E, [0x04, 0x08, 0x10]) # Set spike cave and MM spike room Cape usage
    rom.write_bytes(0x50563, [0x3F, 0x14]) # disable below ganon chest
    rom.write_byte(0x50599, 0x00) # disable below ganon chest
    rom.write_bytes(0xE9A5, [0x7E, 0x00, 0x24]) # disable below ganon chest
    if world.is_pyramid_open(player):
        rom.initial_sram.pre_open_pyramid_hole()
    if world.crystals_needed_for_gt[player] == 0:
        rom.initial_sram.pre_open_ganons_tower()
    rom.write_byte(0xF5D73, 0xF0) # bees are catchable
    rom.write_byte(0xF5F10, 0xF0) # bees are catchable
    rom.write_byte(0x180086, 0x00 if world.aga_randomness[player] else 0x01)  # set blue ball and ganon warp randomness
    rom.write_byte(0x1800A0, 0x01)  # return to light world on s+q without mirror
    rom.write_byte(0x1800A1, 0x01)  # enable overworld screen transition draining for water level inside swamp
    rom.write_byte(0x180174, 0x01 if world.fix_fake_world[player] else 0x00)
    rom.write_byte(0x18017E, 0x01) # Fairy fountains only trade in bottles

    # Starting equipment
    if world.pseudoboots[player]:
        rom.write_byte(0x18008E, 0x01)
    rom.initial_sram.set_starting_equipment(world, player)

    rom.write_byte(0x18004A, 0x00 if world.mode[player] != 'inverted' else 0x01)  # Inverted mode
    rom.write_byte(0x18005D, 0x00) # Hammer always breaks barrier
    rom.write_byte(0x2AF79, 0xD0 if world.mode[player] != 'inverted' else 0xF0) # vortexes: Normal  (D0=light to dark, F0=dark to light, 42 = both)
    rom.write_byte(0x3A943, 0xD0 if world.mode[player] != 'inverted' else 0xF0) # Mirror: Normal  (D0=Dark to Light, F0=light to dark, 42 = both)
    rom.write_byte(0x3A96D, 0xF0 if world.mode[player] != 'inverted' else 0xD0) # Residual Portal: Normal  (F0= Light Side, D0=Dark Side, 42 = both (Darth Vader))
    rom.write_byte(0x3A9A7, 0xD0) # Residual Portal: Normal  (D0= Light Side, F0=Dark Side, 42 = both (Darth Vader))

    rom.write_bytes(0x180080, [50, 50, 70, 70]) # values to fill for Capacity Upgrades (Bomb5, Bomb10, Arrow5, Arrow10)

    rom.write_byte(0x18004D, ((0x01 if 'arrows' in world.escape_assist[player] else 0x00) |
                              (0x02 if 'bombs' in world.escape_assist[player] else 0x00) |
                              (0x04 if 'magic' in world.escape_assist[player] else 0x00))) # Escape assist

    if world.goal[player] in ['pedestal', 'triforcehunt']:
        rom.write_byte(0x1801A8, 0x01)  # make ganon invincible
    elif world.goal[player] in ['dungeons']:
        rom.write_byte(0x1801A8, 0x02)  # make ganon invincible until all dungeons are beat
    elif world.goal[player] in ['crystals', 'trinity']:
        rom.write_byte(0x1801A8, 0x04)  # make ganon invincible until all crystals
    elif world.goal[player] in ['ganonhunt']:
        rom.write_byte(0x1801A8, 0x05)  # make ganon invincible until all triforce pieces collected
    elif world.goal[player] in ['completionist']:
        rom.write_byte(0x1801A8, 0x0B)  # make ganon invincible until everything is collected
    else:
        rom.write_byte(0x1801A8, 0x03)  # make ganon invincible until all crystals and aga 2 are collected

    rom.write_byte(0x18019A, world.crystals_needed_for_gt[player])
    rom.write_byte(0x1801A6, world.crystals_needed_for_ganon[player])
    rom.write_byte(0x1801A2, 0x00)  # ped requirement is vanilla, set to 0x1 for special requirements

    # block HC upstairs doors in rain state in standard mode
    prevent_rain = world.mode[player] == 'standard' and world.shuffle[player] != 'vanilla' and world.logic[player] != 'nologic'
    rom.write_byte(0x18008A, 0x01 if prevent_rain else 0x00)
    # block sanc door in rain state and the dungeon is not vanilla
    block_sanc = world.mode[player] == 'standard' and world.doorShuffle[player] != 'vanilla' and world.logic[player] != 'nologic'
    rom.write_byte(0x13f0fa, 0x01 if block_sanc else 0x00)

    if prevent_rain:
        portals = [world.get_portal('Hyrule Castle East', player), world.get_portal('Hyrule Castle West', player)]
        for idx, portal in enumerate(portals):
            x = idx*2
            room_idx = portal.door.roomIndex
            room = world.get_room(room_idx, player)
            write_int16(rom, 0x13f0f0+x, room_idx)
            rom.write_byte(0x13f0f6+x, room.position(portal.door).value)
            rom.write_byte(0x13f0f7+x, room.kind(portal.door).value)

    # Bitfield - enable text box to show with free roaming items
    #
    # ---o bmcs
    # o - enabled for outside dungeon items
    # b - enabled for inside big keys
    # m - enabled for inside maps
    # c - enabled for inside compasses
    # s - enabled for inside small keys
    rom.write_byte(0x18016A, 0x10 | ((0x01 if world.keyshuffle[player] == 'wild' else 0x00)
                                     | (0x02 if world.compassshuffle[player] else 0x00)
                                     | (0x04 if world.mapshuffle[player] else 0x00)
                                     | (0x08 if world.bigkeyshuffle[player] else 0x00)))  # free roaming item text boxes
    rom.write_byte(0x18003B, 0x01 if world.mapshuffle[player] else 0x00)  # maps showing crystals on overworld

    # compasses showing dungeon count
    compass_mode = 0x00
    if world.clock_mode != 'none' or world.dungeon_counters[player] == 'off':
        compass_mode = 0x00  # Currently must be off if timer is on, because they use same HUD location
        rom.write_byte(0x18003C, 0x00)
    elif world.dungeon_counters[player] == 'on':
        compass_mode = 0x02  # always on
    elif (world.compassshuffle[player] or world.doorShuffle[player] != 'vanilla' or world.dropshuffle[player] != 'none'
          or world.dungeon_counters[player] == 'pickup' or world.pottery[player] not in ['none', 'cave']):
        compass_mode = 0x01  # show on pickup
    if world.shuffle[player] != 'vanilla' and world.overworld_map[player] != 'default':
        compass_mode |= 0x80  # turn on locating dungeons
        x_map_position_generic = [0x3c0, 0xbc0, 0x7c0, 0x1c0, 0x5c0, 0xdc0, 0x7c0, 0xbc0, 0x9c0, 0x3c0]
        for idx, x_map in enumerate(x_map_position_generic):
            rom.write_bytes(0x53df6+idx*2, int16_as_bytes(x_map))
            rom.write_bytes(0x53e16+idx*2, int16_as_bytes(0xFC0))
        if world.overworld_map[player] == 'compass':
            compass_mode |= 0x20  # check for compass
            if world.compassshuffle[player]:
                compass_mode |= 0x40  # compasses are wild
        elif world.overworld_map[player] == 'map':
            if world.mapshuffle[player]:
                compass_mode |= 0x40  # maps are wild
        for dungeon, portal_list in dungeon_portals.items():
            ow_map_index = dungeon_table[dungeon].map_index
            if len(portal_list) == 1:
                portal_idx = 0
            else:
                if world.doorShuffle[player] not in ['vanilla', 'basic']:
                    # the random choice excludes sanctuary
                    portal_idx = next((i for i, elem in enumerate(portal_list)
                                       if world.get_portal(elem, player).chosen), random.choice([1, 2, 3]))
                else:
                    portal_idx = {'Hyrule Castle': 0, 'Desert Palace': 0, 'Skull Woods': 3, 'Turtle Rock': 3}[dungeon]
            portal = world.get_portal(portal_list[portal_idx], player)
            entrance = portal.find_portal_entrance()
            world_indicator = 0x01 if entrance.parent_region.type == RegionType.DarkWorld else 0x00
            coords = ow_prize_table[entrance.name]
            # figure out compass entrances and what world (light/dark)
            rom.write_bytes(0x53E36+ow_map_index*2, int16_as_bytes(coords[0]))
            rom.write_bytes(0x53E56+ow_map_index*2, int16_as_bytes(coords[1]))
            rom.write_byte(0x53EA6+ow_map_index, world_indicator)
    # in crossed doors - flip the compass exists flags
    if world.doorShuffle[player] not in ['vanilla', 'basic']:
        for dungeon, portal_list in dungeon_portals.items():
            ow_map_index = dungeon_table[dungeon].map_index
            exists_flag = any(x for x in world.get_dungeon(dungeon, player).dungeon_items if x.type == 'Compass')
            rom.write_byte(0x53E96+ow_map_index, 0x1 if exists_flag else 0x0)

    rom.write_byte(0x18003C, compass_mode)

    # Bitfield - enable free items to show up in menu
    #
    # ---edcba
    # e - Bosses
    # d - Compass
    # c - Map
    # b - Big Key
    # a - Small Key
    #
    enable_menu_map_check = world.overworld_map[player] != 'default' and world.shuffle[player] != 'vanilla'
    rom.write_byte(0x180045, ((0x01 if world.keyshuffle[player] == 'wild' else 0x00)
                              | (0x02 if world.bigkeyshuffle[player] else 0x00)
                              | (0x04 if world.mapshuffle[player] or enable_menu_map_check else 0x00)
                              | (0x08 if world.compassshuffle[player] else 0x00)  # free roaming items in menu
                              | (0x10 if world.logic[player] == 'nologic' else 0)))  # boss icon

    # Map reveals
    reveal_bytes = {
        "Eastern Palace": 0x2000,
        "Desert Palace": 0x1000,
        "Tower of Hera": 0x0020,
        "Palace of Darkness": 0x0200,
        "Thieves Town": 0x0010,
        "Skull Woods": 0x0080,
        "Swamp Palace": 0x0400,
        "Ice Palace": 0x0040,
        "Misery Mire": 0x0100,
        "Turtle Rock": 0x0008,
    }

    def get_reveal_bytes(itemName):
        locations = world.find_items(itemName, player)
        if len(locations) < 1:
            return 0x0000
        location = locations[0]
        if location.parent_region and location.parent_region.dungeon:
            return reveal_bytes.get(location.parent_region.dungeon.name, 0x0000)
        return 0x0000

    write_int16(rom, 0x18017A, get_reveal_bytes('Green Pendant') if world.mapshuffle[player] else 0x0000) # Sahasrahla reveal
    write_int16(rom, 0x18017C, get_reveal_bytes('Crystal 5')|get_reveal_bytes('Crystal 6') if world.mapshuffle[player] else 0x0000) # Bomb Shop Reveal

    rom.write_byte(0x180172, 0x01 if world.keyshuffle[player] == 'universal' else 0x00)  # universal keys
    rom.write_byte(0x180175, 0x01 if world.bow_mode[player].startswith('retro') else 0x00)  # rupee bow
    rom.write_byte(0x180176, 0x0A if world.bow_mode[player].startswith('retro') else 0x00)  # wood arrow cost
    rom.write_byte(0x180178, 0x32 if world.bow_mode[player].startswith('retro') else 0x00)  # silver arrow cost
    # rupees replace arrows under pots for original and enemizer code
    rom.write_byte(0x301FC, 0xDA if world.bow_mode[player].startswith('retro') else 0xE1)
    rom.write_byte(snes_to_pc(0x36837D), 0xDA if world.bow_mode[player].startswith('retro') else 0xE1)
    rom.write_byte(0x30052, 0xDB if world.bow_mode[player].startswith('retro') else 0xE2) # replace arrows in fish prize from bottle merchant
    rom.write_bytes(0xECB4E, [0xA9, 0x00, 0xEA, 0xEA] if world.bow_mode[player].startswith('retro') else [0xAF, 0x77, 0xF3, 0x7E])  # Thief steals rupees instead of arrows
    rom.write_bytes(0xF0D96, [0xA9, 0x00, 0xEA, 0xEA] if world.bow_mode[player].startswith('retro') else [0xAF, 0x77, 0xF3, 0x7E])  # Pikit steals rupees instead of arrows
    rom.write_bytes(0xEDA5, [0x35, 0x41] if world.bow_mode[player].startswith('retro') else [0x43, 0x44])  # Chest game gives rupees instead of arrows
    digging_game_rng = random.randint(1, 30)  # set rng for digging game
    rom.write_byte(0x180020, digging_game_rng)
    rom.write_byte(0xEFD95, digging_game_rng)
    glitches_enabled = world.logic[player] in ['owglitches', 'hybridglitches', 'nologic']
    rom.write_byte(0x1800A3, 0x01)  # enable correct world setting behaviour after agahnim kills
    rom.write_byte(0x1800A4, 0x01 if not glitches_enabled else 0x00)  # enable POD EG fix
    rom.write_byte(0x180042, 0x01 if world.save_and_quit_from_boss else 0x00)  # Allow Save and Quit after boss kill
    rom.write_byte(0x180358, 0x01 if glitches_enabled else 0x00)
    rom.write_byte(0x18008B, 0x01 if glitches_enabled else 0x00)

    # remove shield from uncle
    rom.write_bytes(0x6D253, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
    rom.write_bytes(0x6D25B, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
    rom.write_bytes(0x6D283, [0x00, 0x00, 0xf6, 0xff, 0x00, 0x0E])
    rom.write_bytes(0x6D28B, [0x00, 0x00, 0xf7, 0xff, 0x00, 0x0E])
    rom.write_bytes(0x6D2CB, [0x00, 0x00, 0xf6, 0xff, 0x02, 0x0E])
    rom.write_bytes(0x6D2FB, [0x00, 0x00, 0xf7, 0xff, 0x02, 0x0E])
    rom.write_bytes(0x6D313, [0x00, 0x00, 0xe4, 0xff, 0x08, 0x0E])

    rom.write_byte(0x18004E, 0)  # Escape Fill (nothing)
    write_int16(rom, 0x180183, 300)  # Escape fill rupee bow
    rom.write_bytes(0x180185, [0, 0, 0])  # Uncle respawn refills (magic, bombs, arrows)
    rom.write_bytes(0x180188, [0, 0, 0])  # Zelda respawn refills (magic, bombs, arrows)
    rom.write_bytes(0x18018B, [0, 0, 0])  # Mantle respawn refills (magic, bombs, arrows)
    bow_max, bomb_max, magic_max = 0, 0, 0
    bow_small, magic_small = 0, 0
    if world.mode[player] == 'standard':
        if uncle_location.item is not None and uncle_location.item.name in ['Bow', 'Progressive Bow']:
            rom.write_byte(0x18004E, 1)  # Escape Fill (arrows)
            write_int16(rom, 0x180183, 300)  # Escape fill rupee bow
            rom.write_bytes(0x180185, [0, 0, 70])  # Uncle respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x180188, [0, 0, 10])  # Zelda respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x18018B, [0, 0, 10])  # Mantle respawn refills (magic, bombs, arrows)
            bow_max, bow_small = 70, 10
        elif uncle_location.item is not None and uncle_location.item.name in ['Bomb Upgrade (+10)' if world.bombbag[player] else 'Bombs (10)']:
            rom.write_byte(0x18004E, 2)  # Escape Fill (bombs)
            rom.write_bytes(0x180185, [0, 50, 0])  # Uncle respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x180188, [0, 3, 0])  # Zelda respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x18018B, [0, 3, 0])  # Mantle respawn refills (magic, bombs, arrows)
            bomb_max = 50
        elif uncle_location.item is not None and uncle_location.item.name in ['Cane of Somaria', 'Cane of Byrna', 'Fire Rod']:
            rom.write_byte(0x18004E, 4)  # Escape Fill (magic)
            rom.write_bytes(0x180185, [0x80, 0, 0])  # Uncle respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x180188, [0x20, 0, 0])  # Zelda respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x18018B, [0x20, 0, 0])  # Mantle respawn refills (magic, bombs, arrows)
            magic_max, magic_small = 0x80, 0x20
        if world.doorShuffle[player] not in ['vanilla', 'basic']:
            # Uncle respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x180185, [max(0x20, magic_max), max(3, bomb_max), max(10, bow_max)])
            # Zelda respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x180188, [max(0x20, magic_max), max(3, bomb_max), max(10, bow_max)])
            # Mantle respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x18018B, [max(0x20, magic_max), max(3, bomb_max), max(10, bow_max)])
        elif world.doorShuffle[player] == 'basic':  # just in case a bomb is needed to get to a chest
            rom.write_bytes(0x180185, [max(0x00, magic_max), max(3, bomb_max), max(0, bow_max)])
            rom.write_bytes(0x180188, [magic_small, 3, bow_small])  # Zelda respawn refills (magic, bombs, arrows)
            rom.write_bytes(0x18018B, [magic_small, 3, bow_small])  # Mantle respawn refills (magic, bombs, arrows)

    # patch swamp: Need to enable permanent drain of water as dam or swamp were moved
    rom.write_byte(0x18003D, 0x01 if world.swamp_patch_required[player] else 0x00)

    # powder patch: remove the need to leave the screen after powder, since it causes problems for potion shop at race game
    # temporarally we are just nopping out this check we will conver this to a rom fix soon.
    rom.write_bytes(0x02F539, [0xEA, 0xEA, 0xEA, 0xEA, 0xEA] if world.powder_patch_required[player] else [0xAD, 0xBF, 0x0A, 0xF0, 0x4F])

    # allow smith into multi-entrance caves in appropriate shuffles
    if world.shuffle[player] in ['restricted', 'simple', 'full', 'lite', 'lean', 'swapped', 'crossed', 'insanity']:
        rom.write_byte(0x18004C, 0x01)

    # set correct flag for hera basement item
    hera_basement = world.get_location('Tower of Hera - Basement Cage', player)
    is_small_key_this_dungeon = False
    if hera_basement.item is not None and hera_basement.item.smallkey:
        item_dungeon = hera_basement.item.name.split('(')[1][:-1]
        if item_dungeon == 'Escape':
            item_dungeon = 'Hyrule Castle'
        is_small_key_this_dungeon = hera_basement.parent_region.dungeon.name == item_dungeon
    # hera small key is 11th in list, 10th sprite because of overlord
    if is_small_key_this_dungeon:
        world.data_tables[player].uw_enemy_table.room_map[0x87][11].kind = EnemySprite.SmallKey
    else:
        world.data_tables[player].uw_enemy_table.room_map[0x87][11].kind = EnemySprite.HeartPiece

    # fix trock doors for reverse entrances
    if world.fix_trock_doors[player]:
        if world.get_door('TR Lazy Eyes SE', player).entranceFlag:
            world.get_room(0x23, player).change(0, DoorKind.CaveEntrance)
        if world.get_door('TR Eye Bridge SW', player).entranceFlag:
            world.get_room(0xd5, player).change(0, DoorKind.CaveEntrance)
        # do this conditionally - don't mess with doors
        if world.doorShuffle[player] == 'vanilla':
            rom.initial_sram.pre_open_tr_bomb_doors()  # preopen bombable exits

    if world.boss_shuffle[player] != 'none' or world.doorShuffle[player] != 'vanilla':
        rom.write_byte(snes_to_pc(0x30835A), 1)  # fix Prize On The Eyes

    if world.boss_shuffle[player] != 'none':
        boss_writes(world, player, rom)
    write_enemy_shuffle_settings(world, player, rom)

    if (world.doorShuffle[player] != 'vanilla' or world.dropshuffle[player] != 'none'
       or world.pottery[player] != 'none'):
        for room in world.rooms:
            if room.player == player and room.modified:
                if room.index in world.data_tables[player].room_list:
                    t = [DoorObject(x[0], x[1]) for x in room.doorList]
                    world.data_tables[player].room_list[room.index].doors = t
                else:
                    rom.write_bytes(room.address(), room.rom_data())

    if world.data_tables[player]:
        colorize_pots = (world.pottery[player] != 'vanilla', 'lottery'
                         and (world.colorizepots[player] or world.pottery[player] in ['reduced', 'clustered']))
        setup_enemy_dungeon_tables(world, player)
        world.data_tables[player].write_to_rom(rom, colorize_pots, world.enemy_shuffle[player] == 'random')

    write_enemizer_tweaks(rom, world, player)
    write_strings(rom, world, player, team)

    # write initial sram
    rom.write_initial_sram()

    rom.write_byte(0x187E30, 1 if world.remote_items[player] else 0)

    # set rom name
    # 21 bytes
    from Main import __version__
    seedstring = f'{world.seed:09}' if isinstance(world.seed, int) else world.seed
    rom.name = bytearray(f'DR{__version__.split("-")[0].replace(".","")[0:3]}_{team+1}_{player}_{seedstring}\0', 'utf8')[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x7FC0, rom.name)

    rom.write_bytes(0x138010, bytearray(__version__, 'utf8'))

    # set player names
    for p in range(1, min(world.players, 255) + 1):
        rom.write_bytes(0x195FFC + ((p - 1) * 32), hud_format_text(world.player_names[p][team]))

    # Write title screen Code
    hashint = int(rom.get_hash(), 16)
    code = [
        (hashint >> 20) & 0x1F,
        (hashint >> 15) & 0x1F,
        (hashint >> 10) & 0x1F,
        (hashint >> 5) & 0x1F,
        hashint & 0x1F,
    ]
    rom.write_bytes(0x180215, code)
    rom.hash = code

    return rom

try:
    import RaceRom
except ImportError:
    RaceRom = None

def patch_race_rom(rom):
    rom.write_bytes(0x180213, [0x01, 0x00]) # Tournament Seed

    if 'RaceRom' in sys.modules:
        RaceRom.encrypt(rom)

def write_custom_shops(rom, world, player):
    shops = [shop for shop in world.shops[player] if shop.custom and shop.region.player == player]

    shop_data = bytearray()
    items_data = bytearray()

    for shop_id, shop in enumerate(shops):
        if shop_id == len(shops) - 1:
            shop_id = 0xFF
        bytes = shop.get_bytes()
        bytes[0] = shop_id
        bytes[-1] = shop.sram_address
        shop_data.extend(bytes)
        # [id][item][price-low][price-high][max][repl_id][repl_price-low][repl_price-high][player][sram]
        for index, item in enumerate(shop.inventory):
            if item is None:
                break
            if world.shopsanity[player] or shop.type == ShopType.TakeAny:
                rom.write_byte(0x186E40 + shop.sram_address + index, 1)
            if world.shopsanity[player] and shop.region.name in shop_to_location_table:
                loc_item = world.get_location(shop_to_location_table[shop.region.name][index], player).item
            elif world.shopsanity[player] and shop.region.name in retro_shops:
                loc_item = world.get_location(retro_shops[shop.region.name][index], player).item
            else:
                loc_item = ItemFactory(item['item'], player)
            if (not world.shopsanity[player] and shop.region.name == 'Capacity Upgrade'
               and world.difficulty[player] != 'normal'):
                # it's a BeeTrap -- surprise!!!
                item_id, price, replace, replace_price, item_max = Items.item_table['Bee Trap'][3], [0, 0], 0xFF, [0, 0], 1
            else:
                item_id = loc_item.code
                price = int16_as_bytes(item['price'])
                replace = ItemFactory(item['replacement'], player).code if item['replacement'] else 0xFF
                replace_price = int16_as_bytes(item['replacement_price'])
                item_max = item['max']
            item_player = 0 if item['player'] == player else item['player']
            item_data = [shop_id,  item_id] + price + [item_max, replace] + replace_price + [item_player]
            items_data.extend(item_data)

    rom.write_bytes(0x184800, shop_data)

    items_data.extend([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
    rom.write_bytes(0x184900, items_data)


def write_enemizer_tweaks(rom, world, player):
    if world.enemy_shuffle[player] != 'none':
        rom.write_byte(snes_to_pc(0x1DF6D8), 0)  # lets enemies walk on water instead of clipping into infinity?
        rom.write_byte(snes_to_pc(0x0DB6B3), 0x82)  # hovers don't need water necessarily?


def hud_format_text(text):
    output = bytes()
    for char in text.lower():
        if 'a' <= char <= 'z':
            output += bytes([0x5d + ord(char) - ord('a'), 0x29])
        elif '0' <= char <= '8':
            output += bytes([0x77 + ord(char) - ord('0'), 0x29])
        elif char == '9':
            output += b'\x4b\x29'
        elif char == ' ':
            output += b'\x7f\x00'
        else:
            output += b'\x2a\x29'
    while len(output) < 32:
        output += b'\x7f\x00'
    return output[:32]


def apply_rom_settings(rom, beep, color, quickswap, fastmenu, disable_music, sprite,
                       ow_palettes, uw_palettes, reduce_flashing, shuffle_sfx, msu_resume):

    if not os.path.exists("data/sprites/official/001.link.1.zspr") and rom.orig_buffer:
        dump_zspr(rom.orig_buffer[0x80000:0x87000], rom.orig_buffer[0xdd308:0xdd380],
                  rom.orig_buffer[0xdedf5:0xdedf9], "data/sprites/official/001.link.1.zspr", "Nintendo", "Link")

    if msu_resume:
        rom.write_bytes(0x18021D, [0x8, 0x7])
    else:
        rom.write_bytes(0x18021D, [0, 0])  # default to off for now

    if sprite and not isinstance(sprite, Sprite):
        sprite = Sprite(sprite) if os.path.isfile(sprite) else get_sprite_from_name(sprite)

    # enable instant item menu
    if fastmenu == 'instant':
        rom.write_byte(0x6DD9A, 0x20)
        rom.write_byte(0x6DF2A, 0x20)
        rom.write_byte(0x6E0E9, 0x20)
    else:
        rom.write_byte(0x6DD9A, 0x11)
        rom.write_byte(0x6DF2A, 0x12)
        rom.write_byte(0x6E0E9, 0x12)
    if fastmenu == 'instant':
        rom.write_byte(0x180048, 0xE8)
    elif fastmenu == 'double':
        rom.write_byte(0x180048, 0x10)
    elif fastmenu == 'triple':
        rom.write_byte(0x180048, 0x18)
    elif fastmenu == 'quadruple':
        rom.write_byte(0x180048, 0x20)
    elif fastmenu == 'half':
        rom.write_byte(0x180048, 0x04)
    else:
        rom.write_byte(0x180048, 0x08)

    rom.write_byte(0x18004B, 0x01 if quickswap else 0x00)

    rom.write_byte(0x0CFE18, 0x00 if disable_music else rom.orig_buffer[0x0CFE18] if rom.orig_buffer else 0x70)
    rom.write_byte(0x0CFEC1, 0x00 if disable_music else rom.orig_buffer[0x0CFEC1] if rom.orig_buffer else 0xC0)
    rom.write_bytes(0x0D0000, [0x00, 0x00] if disable_music else rom.orig_buffer[0x0D0000:0x0D0002] if rom.orig_buffer else [0xDA, 0x58])
    rom.write_bytes(0x0D00E7, [0xC4, 0x58] if disable_music else rom.orig_buffer[0x0D00E7:0x0D00E9] if rom.orig_buffer else [0xDA, 0x58])

    rom.write_byte(0x18021A, 1 if disable_music else 0x00)

    # set heart beep rate
    rom.write_byte(0x180033, {'off': 0x00, 'half': 0x40, 'quarter': 0x80, 'normal': 0x20, 'double': 0x10}[beep])

    # set heart color
    if color == 'random':
        color = random.choice(['red', 'blue', 'green', 'yellow'])
    rom.write_byte(0x187020, {'red': 0, 'blue': 1, 'green': 2, 'yellow': 3}[color])

    # write link sprite if required
    if sprite is not None:
        write_sprite(rom, sprite)

    # sprite author credits
    padded_author = sprite.author_name if sprite is not None else "Nintendo"
    padded_author = padded_author[:28] if len(padded_author) > 28 else padded_author
    padded_author = padded_author.center(28).upper()

    def convert_char_to_credits(char):
        char_map = {
            " ": (0x9F, 0x9F), "0": (0x53, 0x79), "1": (0x54, 0x7A), "2": (0x55, 0x7B), "3": (0x56, 0x7C),
            "4": (0x57, 0x7D), "5": (0x58, 0x7E), "6": (0x59, 0x7F), "7": (0x5A, 0x80), "8": (0x5B, 0x81),
            "9": (0x5C, 0x82), "A": (0x5D, 0x83), "B": (0x5E, 0x84), "C": (0x5F, 0x85), "D": (0x60, 0x86),
            "E": (0x61, 0x87), "F": (0x62, 0x88), "G": (0x63, 0x89), "H": (0x64, 0x8A), "I": (0x65, 0x8B),
            "J": (0x66, 0x8C), "K": (0x67, 0x8D), "L": (0x68, 0x8E), "M": (0x69, 0x8F), "N": (0x6A, 0x90),
            "O": (0x6B, 0x91), "P": (0x6C, 0x92), "Q": (0x6D, 0x93), "R": (0x6E, 0x94), "S": (0x6F, 0x95),
            "T": (0x70, 0x96), "U": (0x71, 0x97), "V": (0x72, 0x98), "W": (0x73, 0x99), "X": (0x74, 0x9A),
            "Y": (0x75, 0x9B), "Z": (0x76, 0x9C), "'": (0xD9, 0xEC), ".": (0xDC, 0xEF), "/": (0xDB, 0xEE),
            ":": (0xDD, 0xF0), "_": (0xDE, 0xF1)}
        return char_map[char] if char in char_map else (0x9F, 0x9F)

    character_bytes = map(convert_char_to_credits, padded_author)
    for i, pair in enumerate(character_bytes):
        rom.write_byte(0x118002 + i, pair[0])
        rom.write_byte(0x118020 + i, pair[1])

    if reduce_flashing:
        rom.write_byte(0x18017f, 1)

    default_ow_palettes(rom)
    if ow_palettes == 'random':
        randomize_ow_palettes(rom)
    elif ow_palettes == 'blackout':
        blackout_ow_palettes(rom)

    default_uw_palettes(rom)
    if uw_palettes == 'random':
        randomize_uw_palettes(rom)
    elif uw_palettes == 'blackout':
        blackout_uw_palettes(rom)

    if shuffle_sfx:
        randomize_sfx(rom)

    if isinstance(rom, LocalRom):
        rom.write_crc()


# .zspr file dumping logic copied with permission from SpriteSomething:
# https://github.com/Artheau/SpriteSomething/blob/master/source/meta/classes/spritelib.py#L443 (thanks miketrethewey!)
def dump_zspr(basesprite, basepalette, baseglove, outfilename, author_name, sprite_name):
    palettes = basepalette
    # Add glove data
    palettes.extend(baseglove)
    HEADER_STRING = b"ZSPR"
    VERSION = 0x01
    SPRITE_TYPE = 0x01  # this format has "1" for the player sprite
    RESERVED_BYTES = b'\x00\x00\x00\x00\x00\x00'
    QUAD_BYTE_NULL_CHAR = b'\x00\x00\x00\x00'
    DOUBLE_BYTE_NULL_CHAR = b'\x00\x00'
    SINGLE_BYTE_NULL_CHAR = b'\x00'

    write_buffer = bytearray()

    write_buffer.extend(HEADER_STRING)
    write_buffer.extend(struct.pack('B', VERSION)) # as_u8
    checksum_start = len(write_buffer)
    write_buffer.extend(QUAD_BYTE_NULL_CHAR)  # checksum
    sprite_sheet_pointer = len(write_buffer)
    write_buffer.extend(QUAD_BYTE_NULL_CHAR)
    write_buffer.extend(struct.pack('<H', len(basesprite)))  # as_u16
    palettes_pointer = len(write_buffer)
    write_buffer.extend(QUAD_BYTE_NULL_CHAR)
    write_buffer.extend(struct.pack('<H', len(palettes)))  # as_u16
    write_buffer.extend(struct.pack('<H', SPRITE_TYPE))  # as_u16
    write_buffer.extend(RESERVED_BYTES)
    # sprite.name
    write_buffer.extend(sprite_name.encode('utf-16-le'))
    write_buffer.extend(DOUBLE_BYTE_NULL_CHAR)
    # author.name
    write_buffer.extend(author_name.encode('utf-16-le'))
    write_buffer.extend(DOUBLE_BYTE_NULL_CHAR)
    # author.name-short
    write_buffer.extend(author_name.encode('ascii'))
    write_buffer.extend(SINGLE_BYTE_NULL_CHAR)
    write_buffer[sprite_sheet_pointer:sprite_sheet_pointer +
                                      4] = struct.pack('<L', len(write_buffer)) # as_u32
    write_buffer.extend(basesprite)
    write_buffer[palettes_pointer:palettes_pointer +
                                  4] = struct.pack('<L', len(write_buffer)) # as_u32
    write_buffer.extend(palettes)

    checksum = (sum(write_buffer) + 0xFF + 0xFF) % 0x10000
    checksum_complement = 0xFFFF - checksum

    write_buffer[checksum_start:checksum_start +
                                2] = struct.pack('<H', checksum) # as_u16
    write_buffer[checksum_start + 2:checksum_start +
                                    4] = struct.pack('<H', checksum_complement) # as_u16

    with open('%s' % outfilename, "wb") as zspr_file:
        zspr_file.write(write_buffer)

def write_sprite(rom, sprite):
    if not sprite.valid:
        return
    rom.write_bytes(0x80000, sprite.sprite)
    rom.write_bytes(0xDD308, sprite.palette)
    rom.write_bytes(0xDEDF5, sprite.glove_palette)

def set_color(rom, address, color, shade):
    r = round(min(color[0], 0xFF) * pow(0.8, shade) * 0x1F / 0xFF)
    g = round(min(color[1], 0xFF) * pow(0.8, shade) * 0x1F / 0xFF)
    b = round(min(color[2], 0xFF) * pow(0.8, shade) * 0x1F / 0xFF)

    rom.write_bytes(address, ((b << 10) | (g << 5) | (r << 0)).to_bytes(2, byteorder='little', signed=False))

def default_ow_palettes(rom):
    if not rom.orig_buffer:
        return
    rom.write_bytes(0xDE604, rom.orig_buffer[0xDE604:0xDEBB4])

    for address in [0x067FB4, 0x067F94, 0x067FC6, 0x067FE6, 0x067FE1, 0x05FEA9, 0x05FEB3]:
        rom.write_bytes(address, rom.orig_buffer[address:address+2])

def randomize_ow_palettes(rom):
    grass, grass2, grass3, dirt, dirt2, water, clouds, dwdirt,\
        dwgrass, dwwater, dwdmdirt, dwdmgrass, dwdmclouds1, dwdmclouds2 = [[random.randint(60, 215) for _ in range(3)] for _ in range(14)]
    dwtree = [c + random.randint(-20, 10) for c in dwgrass]
    treeleaf = [c + random.randint(-20, 10) for c in grass]

    patches = {0x067FB4: (grass, 0), 0x067F94: (grass, 0), 0x067FC6: (grass, 0), 0x067FE6: (grass, 0), 0x067FE1: (grass, 3), 0x05FEA9: (grass, 0), 0x05FEB3: (dwgrass, 1),
               0x0DD4AC: (grass, 2), 0x0DE6DE: (grass2, 2), 0x0DE6E0: (grass2, 1), 0x0DD4AE: (grass2, 1), 0x0DE9FA: (grass2, 1), 0x0DEA0E: (grass2, 1), 0x0DE9FE: (grass2, 0),
               0x0DD3D2: (grass2, 2), 0x0DE88C: (grass2, 2), 0x0DE8A8: (grass2, 2), 0x0DE9F8: (grass2, 2), 0x0DEA4E: (grass2, 2), 0x0DEAF6: (grass2, 2), 0x0DEB2E: (grass2, 2), 0x0DEB4A: (grass2, 2),
               0x0DE892: (grass, 1), 0x0DE886: (grass, 0), 0x0DE6D2: (grass, 0), 0x0DE6FA: (grass, 3), 0x0DE6FC: (grass, 0), 0x0DE6FE: (grass, 0), 0x0DE70A: (grass, 0), 0x0DE708: (grass, 2), 0x0DE70C: (grass, 1),
               0x0DE6D4: (dirt, 2), 0x0DE6CA: (dirt, 5), 0x0DE6CC: (dirt, 4), 0x0DE6CE: (dirt, 3), 0x0DE6E2: (dirt, 2), 0x0DE6D8: (dirt, 5), 0x0DE6DA: (dirt, 4), 0x0DE6DC: (dirt, 2),
               0x0DE6F0: (dirt, 2), 0x0DE6E6: (dirt, 5), 0x0DE6E8: (dirt, 4), 0x0DE6EA: (dirt, 2), 0x0DE6EC: (dirt, 4), 0x0DE6EE: (dirt, 2),
               0x0DE91E: (grass, 0),
               0x0DE920: (dirt, 2), 0x0DE916: (dirt, 3), 0x0DE934: (dirt, 3),
               0x0DE92C: (grass, 0), 0x0DE93A: (grass, 0), 0x0DE91C: (grass, 1), 0x0DE92A: (grass, 1), 0x0DEA1C: (grass, 0), 0x0DEA2A: (grass, 0), 0x0DEA30: (grass, 0),
               0x0DEA2E: (dirt, 5),
               0x0DE884: (grass, 3), 0x0DE8AE: (grass, 3), 0x0DE8BE: (grass, 3), 0x0DE8E4: (grass, 3), 0x0DE938: (grass, 3), 0x0DE9C4: (grass, 3), 0x0DE6D0: (grass, 4),
               0x0DE890: (treeleaf, 1), 0x0DE894: (treeleaf, 0),
               0x0DE924: (water, 3), 0x0DE668: (water, 3), 0x0DE66A: (water, 2), 0x0DE670: (water, 1), 0x0DE918: (water, 1), 0x0DE66C: (water, 0), 0x0DE91A: (water, 0), 0x0DE92E: (water, 1), 0x0DEA1A: (water, 1), 0x0DEA16: (water, 3), 0x0DEA10: (water, 4),
               0x0DE66E: (dirt, 3), 0x0DE672: (dirt, 2), 0x0DE932: (dirt, 4), 0x0DE936: (dirt, 2), 0x0DE93C: (dirt, 1),
               0x0DE756: (dirt2, 4), 0x0DE764: (dirt2, 4), 0x0DE772: (dirt2, 4), 0x0DE994: (dirt2, 4), 0x0DE9A2: (dirt2, 4), 0x0DE758: (dirt2, 3), 0x0DE766: (dirt2, 3), 0x0DE774: (dirt2, 3),
               0x0DE996: (dirt2, 3), 0x0DE9A4: (dirt2, 3), 0x0DE75A: (dirt2, 2), 0x0DE768: (dirt2, 2), 0x0DE776: (dirt2, 2), 0x0DE778: (dirt2, 2), 0x0DE998: (dirt2, 2), 0x0DE9A6: (dirt2, 2),
               0x0DE9AC: (dirt2, 1), 0x0DE99E: (dirt2, 1), 0x0DE760: (dirt2, 1), 0x0DE77A: (dirt2, 1), 0x0DE77C: (dirt2, 1), 0x0DE798: (dirt2, 1), 0x0DE980: (dirt2, 1),
               0x0DE75C: (grass3, 2), 0x0DE786: (grass3, 2), 0x0DE794: (grass3, 2), 0x0DE99A: (grass3, 2), 0x0DE75E: (grass3, 1), 0x0DE788: (grass3, 1), 0x0DE796: (grass3, 1), 0x0DE99C: (grass3, 1),
               0x0DE76A: (clouds, 2), 0x0DE9A8: (clouds, 2), 0x0DE76E: (clouds, 0), 0x0DE9AA: (clouds, 0), 0x0DE8DA: (clouds, 0), 0x0DE8D8: (clouds, 0), 0x0DE8D0: (clouds, 0), 0x0DE98C: (clouds, 2), 0x0DE990: (clouds, 0),
               0x0DEB34: (dwtree, 4), 0x0DEB30: (dwtree, 3), 0x0DEB32: (dwtree, 1),
               0x0DE710: (dwdirt, 5), 0x0DE71E: (dwdirt, 5), 0x0DE72C: (dwdirt, 5), 0x0DEAD6: (dwdirt, 5), 0x0DE712: (dwdirt, 4), 0x0DE720: (dwdirt, 4), 0x0DE72E: (dwdirt, 4), 0x0DE660: (dwdirt, 4),
               0x0DEAD8: (dwdirt, 4), 0x0DEADA: (dwdirt, 3), 0x0DE714: (dwdirt, 3), 0x0DE722: (dwdirt, 3), 0x0DE730: (dwdirt, 3), 0x0DE732: (dwdirt, 3), 0x0DE734: (dwdirt, 2), 0x0DE736: (dwdirt, 2),
               0x0DE728: (dwdirt, 2), 0x0DE71A: (dwdirt, 2), 0x0DE664: (dwdirt, 2), 0x0DEAE0: (dwdirt, 2),
               0x0DE716: (dwgrass, 3), 0x0DE740: (dwgrass, 3), 0x0DE74E: (dwgrass, 3), 0x0DEAC0: (dwgrass, 3), 0x0DEACE: (dwgrass, 3), 0x0DEADC: (dwgrass, 3), 0x0DEB24: (dwgrass, 3), 0x0DE752: (dwgrass, 2),
               0x0DE718: (dwgrass, 1), 0x0DE742: (dwgrass, 1), 0x0DE750: (dwgrass, 1), 0x0DEB26: (dwgrass, 1), 0x0DEAC2: (dwgrass, 1), 0x0DEAD0: (dwgrass, 1), 0x0DEADE: (dwgrass, 1),
               0x0DE65A: (dwwater, 5), 0x0DE65C: (dwwater, 3), 0x0DEAC8: (dwwater, 3), 0x0DEAD2: (dwwater, 2), 0x0DEABC: (dwwater, 2), 0x0DE662: (dwwater, 2), 0x0DE65E: (dwwater, 1), 0x0DEABE: (dwwater, 1), 0x0DEA98: (dwwater, 2),
               0x0DE79A: (dwdmdirt, 6), 0x0DE7A8: (dwdmdirt, 6), 0x0DE7B6: (dwdmdirt, 6), 0x0DEB60: (dwdmdirt, 6), 0x0DEB6E: (dwdmdirt, 6), 0x0DE93E: (dwdmdirt, 6), 0x0DE94C: (dwdmdirt, 6), 0x0DEBA6: (dwdmdirt, 6),
               0x0DE79C: (dwdmdirt, 4), 0x0DE7AA: (dwdmdirt, 4), 0x0DE7B8: (dwdmdirt, 4), 0x0DEB70: (dwdmdirt, 4), 0x0DEBA8: (dwdmdirt, 4), 0x0DEB72: (dwdmdirt, 3), 0x0DEB74: (dwdmdirt, 3), 0x0DE79E: (dwdmdirt, 3), 0x0DE7AC: (dwdmdirt, 3), 0x0DEBAA: (dwdmdirt, 3), 0x0DE7A0: (dwdmdirt, 3),
               0x0DE7BC: (dwdmgrass, 3),
               0x0DEBAC: (dwdmdirt, 2), 0x0DE7AE: (dwdmdirt, 2), 0x0DE7C2: (dwdmdirt, 2), 0x0DE7A6: (dwdmdirt, 2), 0x0DEB7A: (dwdmdirt, 2), 0x0DEB6C: (dwdmdirt, 2), 0x0DE7C0: (dwdmdirt, 2),
               0x0DE7A2: (dwdmgrass, 3), 0x0DE7BE: (dwdmgrass, 3), 0x0DE7CC: (dwdmgrass, 3), 0x0DE7DA: (dwdmgrass, 3), 0x0DEB6A: (dwdmgrass, 3), 0x0DE948: (dwdmgrass, 3), 0x0DE956: (dwdmgrass, 3), 0x0DE964: (dwdmgrass, 3), 0x0DE7CE: (dwdmgrass, 1), 0x0DE7A4: (dwdmgrass, 1), 0x0DEBA2: (dwdmgrass, 1), 0x0DEBB0: (dwdmgrass, 1),
               0x0DE644: (dwdmclouds1, 2), 0x0DEB84: (dwdmclouds1, 2), 0x0DE648: (dwdmclouds1, 1), 0x0DEB88: (dwdmclouds1, 1),
               0x0DEBAE: (dwdmclouds2, 2), 0x0DE7B0: (dwdmclouds2, 2), 0x0DE7B4: (dwdmclouds2, 0), 0x0DEB78: (dwdmclouds2, 0), 0x0DEBB2: (dwdmclouds2, 0)
               }
    for address, (color, shade) in patches.items():
        set_color(rom, address, color, shade)

def blackout_ow_palettes(rom):
    rom.write_bytes(0xDE604, [0] * 0xC4)
    for i in range(0xDE6C8, 0xDE86C, 70):
        rom.write_bytes(i, [0] * 64)
        rom.write_bytes(i+66, [0] * 4)
    rom.write_bytes(0xDE86C, [0] * 0x348)

    for address in [0x067FB4, 0x067F94, 0x067FC6, 0x067FE6, 0x067FE1, 0x05FEA9, 0x05FEB3]:
        rom.write_bytes(address, [0,0])

def default_uw_palettes(rom):
    if not rom.orig_buffer:
        return
    rom.write_bytes(0xDD734, rom.orig_buffer[0xDD734:0xDE544])

def randomize_uw_palettes(rom):
    for dungeon in range(20):
        wall, pot, chest, floor1, floor2, floor3 = [[random.randint(60, 240) for _ in range(3)] for _ in range(6)]

        for i in range(5):
            shade = 10 - (i * 2)
            set_color(rom, 0x0DD734 + (0xB4 * dungeon) + (i * 2), wall, shade)
            set_color(rom, 0x0DD770 + (0xB4 * dungeon) + (i * 2), wall, shade)
            set_color(rom, 0x0DD744 + (0xB4 * dungeon) + (i * 2), wall, shade)
            if dungeon == 0:
                set_color(rom, 0x0DD7CA + (0xB4 * dungeon) + (i * 2), wall, shade)

        if dungeon == 2:
            set_color(rom, 0x0DD74E + (0xB4 * dungeon), wall, 3)
            set_color(rom, 0x0DD750 + (0xB4 * dungeon), wall, 5)
            set_color(rom, 0x0DD73E + (0xB4 * dungeon), wall, 3)
            set_color(rom, 0x0DD740 + (0xB4 * dungeon), wall, 5)

        set_color(rom, 0x0DD7E4 + (0xB4 * dungeon), wall, 4)
        set_color(rom, 0x0DD7E6 + (0xB4 * dungeon), wall, 2)

        set_color(rom, 0xDD7DA + (0xB4 * dungeon), wall, 10)
        set_color(rom, 0xDD7DC + (0xB4 * dungeon), wall, 8)

        set_color(rom, 0x0DD75A + (0xB4 * dungeon), pot, 7)
        set_color(rom, 0x0DD75C + (0xB4 * dungeon), pot, 1)
        set_color(rom, 0x0DD75E + (0xB4 * dungeon), pot, 3)

        set_color(rom, 0x0DD76A + (0xB4 * dungeon), wall, 7)
        set_color(rom, 0x0DD76C + (0xB4 * dungeon), wall, 2)
        set_color(rom, 0x0DD76E + (0xB4 * dungeon), wall, 4)

        set_color(rom, 0x0DD7AE + (0xB4 * dungeon), chest, 2)
        set_color(rom, 0x0DD7B0 + (0xB4 * dungeon), chest, 0)

        for i in range(3):
            shade = 6 - (i * 2)
            set_color(rom, 0x0DD764 + (0xB4 * dungeon) + (i * 2), floor1, shade)
            set_color(rom, 0x0DD782 + (0xB4 * dungeon) + (i * 2), floor1, shade + 3)

            set_color(rom, 0x0DD7A0 + (0xB4 * dungeon) + (i * 2), floor2, shade)
            set_color(rom, 0x0DD7BE + (0xB4 * dungeon) + (i * 2), floor2, shade + 3)

        set_color(rom, 0x0DD7E2 + (0xB4 * dungeon), floor3, 3)
        set_color(rom, 0x0DD796 + (0xB4 * dungeon), floor3, 4)

def blackout_uw_palettes(rom):
    for i in range(0xDD734, 0xDE544, 180):
        rom.write_bytes(i, [0] * 38)
        rom.write_bytes(i+44, [0] * 76)
        rom.write_bytes(i+136, [0] * 44)

def get_hash_string(hash):
    return ", ".join([hash_alphabet[code & 0x1F] for code in hash])

def write_string_to_rom(rom, target, string):
    address, maxbytes = text_addresses[target]
    rom.write_bytes(address, MultiByteTextMapper.convert(string, maxbytes))


def write_strings(rom, world, player, team):
    tt = TextTable()
    tt.removeUnwantedText()
    if world.shuffle[player] != 'vanilla':
        tt['houlihan_room'] = CompressedTextMapper.convert(
            "    Crosskeys\n"
            "    Tournament\n"
            "    Winners\n{HARP}\n"
            "    ~~~2022~~~\n     Schulzer\n\n"
            "    ~~~2021~~~\n      Goomba\n\n"
            "    ~~~2020~~~\n    Linlinlin\n\n"
            "    ~~~2019~~~\n      Kohrek\n"
        )

    # Let's keep this guy's text accurate to the shuffle setting.
    if world.shuffle[player] in ['vanilla', 'dungeonsfull', 'dungeonssimple']:
        tt['kakariko_flophouse_man_no_flippers'] = 'I really hate mowing my yard.\n{PAGEBREAK}\nI should move.'
        tt['kakariko_flophouse_man'] = 'I really hate mowing my yard.\n{PAGEBREAK}\nI should move.'

    def hint_text(dest, ped_hint=False):
        if not dest:
            return "nothing"
        if ped_hint:
            hint = dest.pedestal_hint_text if dest.pedestal_hint_text else "unknown item"
        else:
            if isinstance(dest, Region) and dest.type == RegionType.Dungeon and dest.dungeon:
                hint = dest.dungeon.name
            else:
                hint = dest.hint_text if dest.hint_text else "something"
        if dest.player != player:
            if ped_hint:
                hint += f" for {world.player_names[dest.player][team]}!"
            elif type(dest) in [Region, Location]:
                hint += f" in {world.player_names[dest.player][team]}'s world"
            else:
                hint += f" for {world.player_names[dest.player][team]}"
        return hint

    # For hints, first we write hints about entrances, some from the inconvenient list others from all reasonable entrances.
    if world.hints[player]:
        tt['sign_north_of_links_house'] = '> Randomizer The telepathic tiles can have hints!'
        hint_locations = HintLocations.copy()
        random.shuffle(hint_locations)
        all_entrances = [entrance for entrance in world.get_entrances() if entrance.player == player]
        random.shuffle(all_entrances)

        # First we take care of the one inconvenient dungeon in the appropriately simple shuffles.
        entrances_to_hint = {}
        entrances_to_hint.update(InconvenientDungeonEntrances)
        if world.shuffle_ganon:
            if world.mode[player] == 'inverted':
                entrances_to_hint.update({'Agahnims Tower': 'The sealed castle door'})
            else:
                entrances_to_hint.update({'Ganons Tower': 'Ganon\'s Tower'})
        if world.shuffle[player] in ['simple', 'restricted']:
            for entrance in all_entrances:
                if entrance.name in entrances_to_hint:
                    this_hint = entrances_to_hint[entrance.name] + ' leads to ' + hint_text(entrance.connected_region) + '.'
                    tt[hint_locations.pop(0)] = this_hint
                    entrances_to_hint = {}
                    break
        # Now we write inconvenient locations for most shuffles and finish taking care of the less chaotic ones.
        entrances_to_hint.update(InconvenientOtherEntrances)
        if world.shuffle[player] in ['vanilla', 'dungeonssimple', 'dungeonsfull', 'lite', 'lean', 'swapped']:
            hint_count = 0
        elif world.shuffle[player] in ['simple', 'restricted']:
            hint_count = 2
        else:
            hint_count = 4
        for entrance in all_entrances:
            if hint_count > 0:
                if entrance.name in entrances_to_hint:
                    this_hint = entrances_to_hint[entrance.name] + ' leads to ' + hint_text(entrance.connected_region) + '.'
                    tt[hint_locations.pop(0)] = this_hint
                    entrances_to_hint.pop(entrance.name)
                    hint_count -= 1
            else:
                break

        # Next we handle hints for randomly selected other entrances, curating the selection intelligently based on shuffle.
        if world.shuffle[player] not in ['simple', 'restricted']:
            entrances_to_hint.update(ConnectorEntrances)
            entrances_to_hint.update(DungeonEntrances)
            if world.mode[player] == 'inverted':
                entrances_to_hint.update({'Ganons Tower': 'The dark mountain tower'})
            else:
                entrances_to_hint.update({'Agahnims Tower': 'The sealed castle door'})
        elif world.shuffle[player] == 'restricted':
            entrances_to_hint.update(ConnectorEntrances)
        entrances_to_hint.update(ItemEntrances)
        if world.shuffle[player] not in ['lite', 'lean']:
            entrances_to_hint.update(ShopEntrances)
            entrances_to_hint.update(OtherEntrances)
        elif world.shopsanity[player]:
            entrances_to_hint.update(ShopEntrances)
        if world.shufflelinks[player] and world.shuffle[player] not in ['vanilla', 'dungeonssimple', 'dungeonsfull']:
            if world.mode[player] == 'inverted':
                entrances_to_hint.update({'Big Bomb Shop': 'The old hero\'s dark home'})
            else:
                entrances_to_hint.update({'Links House': 'The hero\'s old residence'})
        if world.shuffletavern[player] and world.shuffle[player] not in ['vanilla', 'dungeonssimple', 'dungeonsfull']:
            entrances_to_hint.update({'Tavern North': 'A backdoor'})
        if world.mode[player] == 'inverted':
            entrances_to_hint.update({'Links House': 'The old hero\'s light home'})
        else:
            entrances_to_hint.update({'Big Bomb Shop': 'The old bomb shop'})
        if world.shuffle[player] in ['insanity']:
            entrances_to_hint.update(InsanityEntrances)
            if world.shuffle_ganon:
                if world.mode[player] == 'inverted':
                    entrances_to_hint.update({'Inverted Pyramid Entrance': 'The extra castle passage'})
                else:
                    entrances_to_hint.update({'Pyramid Entrance': 'The pyramid ledge'})
        hint_count = 4 if world.shuffle[player] not in ['vanilla', 'dungeonssimple', 'dungeonsfull', 'swapped'] else 0
        hint_count -= 2 if world.shuffle[player] not in ['simple', 'restricted'] else 0
        for entrance in all_entrances:
            if entrance.name in entrances_to_hint:
                if hint_count > 0:
                    this_hint = entrances_to_hint[entrance.name] + ' leads to ' + hint_text(entrance.connected_region) + '.'
                    tt[hint_locations.pop(0)] = this_hint
                    entrances_to_hint.pop(entrance.name)
                    hint_count -= 1
                else:
                    break

        # Next we write a few hints for specific inconvenient locations. We don't make many because in entrance this is highly unpredictable.
        locations_to_hint = InconvenientLocations.copy()
        if world.doorShuffle[player] == 'vanilla':
            locations_to_hint.extend(InconvenientDungeonLocations)
        if world.shuffle[player] in ['vanilla', 'dungeonssimple', 'dungeonsfull']:
            locations_to_hint.extend(InconvenientVanillaLocations)
        random.shuffle(locations_to_hint)
        hint_count = 3 if world.shuffle[player] not in ['vanilla', 'dungeonssimple', 'dungeonsfull', 'swapped'] else 5
        hint_count -= 2 if world.doorShuffle[player] not in ['vanilla', 'basic'] else 0
        del locations_to_hint[hint_count:]
        for location in locations_to_hint:
            if location == 'Swamp Left':
                if random.randint(0, 1) == 0:
                    first_item = hint_text(world.get_location('Swamp Palace - West Chest', player).item)
                    second_item = hint_text(world.get_location('Swamp Palace - Big Key Chest', player).item)
                else:
                    second_item = hint_text(world.get_location('Swamp Palace - West Chest', player).item)
                    first_item = hint_text(world.get_location('Swamp Palace - Big Key Chest', player).item)
                this_hint = f'The westmost chests in Swamp Palace contain {first_item} and {second_item}.'
                tt[hint_locations.pop(0)] = this_hint
            elif location == 'Mire Left':
                if random.randint(0, 1) == 0:
                    first_item = hint_text(world.get_location('Misery Mire - Compass Chest', player).item)
                    second_item = hint_text(world.get_location('Misery Mire - Big Key Chest', player).item)
                else:
                    second_item = hint_text(world.get_location('Misery Mire - Compass Chest', player).item)
                    first_item = hint_text(world.get_location('Misery Mire - Big Key Chest', player).item)
                this_hint = f'The westmost chests in Misery Mire contain {first_item} and {second_item}.'
                tt[hint_locations.pop(0)] = this_hint
            elif location == 'Tower of Hera - Big Key Chest':
                item = hint_text(world.get_location(location, player).item)
                this_hint = f'Waiting in the Tower of Hera basement leads to {item}.'
                tt[hint_locations.pop(0)] = this_hint
            elif location == 'Ganons Tower - Big Chest':
                item = hint_text(world.get_location(location, player).item)
                this_hint = f'The big chest in Ganon\'s Tower contains {item}.'
                tt[hint_locations.pop(0)] = this_hint
            elif location == 'Thieves\' Town - Big Chest':
                item = hint_text(world.get_location(location, player).item)
                this_hint = f'The big chest in Thieves\' Town contains {item}.'
                tt[hint_locations.pop(0)] = this_hint
            elif location == 'Ice Palace - Big Chest':
                item = hint_text(world.get_location(location, player).item)
                this_hint = f'The big chest in Ice Palace contains {item}.'
                tt[hint_locations.pop(0)] = this_hint
            elif location == 'Eastern Palace - Big Key Chest':
                item = hint_text(world.get_location(location, player).item)
                this_hint = f'The antifairy guarded chest in Eastern Palace contains {item}.'
                tt[hint_locations.pop(0)] = this_hint
            elif location == 'Sahasrahla':
                item = hint_text(world.get_location(location, player).item)
                this_hint = f'Sahasrahla seeks a green pendant for {item}.'
                tt[hint_locations.pop(0)] = this_hint
            elif location == 'Graveyard Cave':
                item = hint_text(world.get_location(location, player).item)
                this_hint = f'The cave north of the graveyard contains {item}.'
                tt[hint_locations.pop(0)] = this_hint
            else:
                this_hint = f'{location} contains {hint_text(world.get_location(location, player).item)}.'
                tt[hint_locations.pop(0)] = this_hint

        # Lastly we write hints to show where certain interesting items are.
        # It is done the way it is to re-use the silver code and also to give one hint per each type of item regardless
        # of how many exist. This supports many settings well.
        items_to_hint = RelevantItems.copy()
        if world.keyshuffle[player] == 'wild':
            items_to_hint.extend(SmallKeys)
        if world.bigkeyshuffle[player]:
            items_to_hint.extend(BigKeys)
        random.shuffle(items_to_hint)
        hint_count = 5 if world.shuffle[player] not in ['vanilla', 'dungeonssimple', 'dungeonsfull', 'swapped'] else 8
        hint_count += 2 if world.doorShuffle[player] not in ['vanilla', 'basic'] else 0
        while hint_count > 0 and len(items_to_hint) > 0:
            this_item = items_to_hint.pop(0)
            this_location = world.find_items_not_key_only(this_item, player)
            if this_location:
                random.shuffle(this_location)
                item_name = this_location[0].item.hint_text
                item_name = item_name[0].upper() + item_name[1:]
                this_hint = f'{item_name} can be found {hint_text(this_location[0])}.'
                tt[hint_locations.pop(0)] = this_hint
                hint_count -= 1

        # Adding a hint for the Thieves' Town Attic location in mixed door shuffles.
        if world.doorShuffle[player] not in ['vanilla', 'basic']:
            attic_hint = world.get_location("Thieves' Town - Attic", player).parent_region.dungeon.name
            this_hint = 'A cracked floor can be found in ' + attic_hint + '.'
            if world.intensity[player] < 2 and hint_locations[0] == 'telepathic_tile_thieves_town_upstairs':
                tt[hint_locations.pop(1)] = this_hint
            else:
                tt[hint_locations.pop(0)] = this_hint

        hint_candidates = []
        for name, district in world.districts[player].items():
            hint_type = 'foolish'
            choices = []
            item_count, item_type = 0, 'useful'
            for loc_name in district.locations:
                location_item = world.get_location(loc_name, player).item
                if location_item.advancement:
                    if 'Heart Container' in location_item.name or location_item.compass or location_item.map:
                        continue
                    itm_type = 'useful' if useful_item_for_hint(location_item, world) else 'vital'
                    hint_type = 'path'
                    if item_type == itm_type:
                        choices.append(location_item)
                        item_count += 1
                    elif itm_type == 'vital':
                        item_type = 'vital'
                        item_count = 1
                        choices.clear()
                        choices.append(location_item)
            if hint_type == 'foolish':
                if district.dungeons and world.shuffle[player] != 'vanilla':
                    choices.extend(district.dungeons)
                    hint_type = 'dungeon_path'
                elif district.access_points and world.shuffle[player] not in ['vanilla', 'dungeonssimple',
                                                                              'dungeonsfull']:
                    choices.extend([x.hint_text for x in district.access_points])
                    hint_type = 'connector'
            if hint_type == 'foolish':
                hint_candidates.append((hint_type, f'{name} is a foolish choice'))
            elif hint_type == 'dungeon_path':
                dungeon_choice = random.choice(choices)  # prefer required dungeons...
                hint_candidates.append((hint_type, f'{name} is on the path to {dungeon_choice}'))
            elif hint_type == 'connector':
                access_point = random.choice(choices)  # prefer required access...
                hint_candidates.append((hint_type, f'{name} can reach {access_point}'))
            elif hint_type == 'path':
                if item_count == 1:
                    the_item = text_for_item(next(iter(choices)), world, player, team)
                    hint_candidates.append((hint_type, f'{name} conceals only {the_item}'))
                else:
                    hint_candidates.append((hint_type, f'{name} conceals {item_count} {item_type} items'))
        district_hints = min(len(hint_candidates), len(hint_locations))
        random.shuffle(hint_candidates)
        hint_candidates.sort(key=lambda x: 1 if x[0] == 'foolish' else 0)
        foolish_only = min(2, district_hints)  # 2 foolish only
        for i in range(0, foolish_only):
            tt[hint_locations.pop(0)] = hint_candidates.pop(0)[1]
        random.shuffle(hint_candidates)
        district_hints -= foolish_only  # the rest can be anything
        for i in range(0, district_hints):
            tt[hint_locations.pop(0)] = hint_candidates.pop(0)[1]
        if len(hint_locations) > 0:
            # All remaining hint slots are filled with junk hints. It is done this way to ensure the same junk hint
            # isn't selected twice.
            junk_hints = junk_texts.copy()
            random.shuffle(junk_hints)
            for location in hint_locations:
                tt[location] = junk_hints.pop(0)

    # We still need the older hints of course. Those are done here.

    no_silver_text = Ganon_Phase_3_No_Silvers_texts[random.randint(0, len(Ganon_Phase_3_No_Silvers_texts) - 1)]

    silverarrows = world.find_items('Silver Arrows', player)
    random.shuffle(silverarrows)
    if silverarrows:
        hint_phrase = hint_text(silverarrows[0]).replace("Ganon's", "my")
        silverarrow_hint = f'Did you find the silver arrows {hint_phrase}?'
    else:
        silverarrow_hint = no_silver_text
    tt['ganon_phase_3_no_silvers'] = silverarrow_hint
    tt['ganon_phase_3_no_silvers_alt'] = silverarrow_hint

    prog_bow_locs = world.find_items('Progressive Bow', player)
    distinguished_prog_bow_loc = next((location for location in prog_bow_locs if location.item.code == 0x65), None)
    progressive_silvers = world.difficulty_requirements[player].progressive_bow_limit >= 2 or world.swords[player] == 'swordless'
    if distinguished_prog_bow_loc:
        prog_bow_locs.remove(distinguished_prog_bow_loc)
        hint_phrase = hint_text(distinguished_prog_bow_loc).replace("Ganon's", "my")
        silverarrow_hint = f'Did you find the silver arrows {hint_phrase}?' if progressive_silvers else no_silver_text
        tt['ganon_phase_3_no_silvers'] = silverarrow_hint
    if any(prog_bow_locs):
        hint_phrase = hint_text(random.choice(prog_bow_locs)).replace("Ganon's", "my")
        silverarrow_hint = f'Did you find the silver arrows {hint_phrase}?' if progressive_silvers else no_silver_text
        tt['ganon_phase_3_no_silvers_alt'] = silverarrow_hint

    crystal5 = world.find_items('Crystal 5', player)[0]
    crystal6 = world.find_items('Crystal 6', player)[0]
    tt['bomb_shop'] = 'Big Bomb?\nMy supply is blocked until you clear %s and %s.' % (crystal5.hint_text, crystal6.hint_text)

    greenpendant = world.find_items('Green Pendant', player)[0]
    tt['sahasrahla_bring_courage'] = 'I lost my family heirloom in %s' % greenpendant.hint_text

    tt['sign_ganons_tower'] = ('You need %d crystal to enter.' if world.crystals_needed_for_gt[player] == 1 else 'You need %d crystals to enter.') % world.crystals_needed_for_gt[player]

    ganon_crystals_singular = 'You need %d crystal to beat Ganon.'
    ganon_crystals_plural = 'You need %d crystals to beat Ganon.'

    if world.goal[player] == 'ganon':
        ganon_crystals_singular = 'To beat Ganon you must collect %d crystal and defeat his minion at the top of his tower.'
        ganon_crystals_plural = 'To beat Ganon you must collect %d crystals and defeat his minion at the top of his tower.'

    tt['sign_ganon'] = (ganon_crystals_singular if world.crystals_needed_for_ganon[player] == 1 else ganon_crystals_plural) % world.crystals_needed_for_ganon[player]

    if world.goal[player] in ['dungeons']:
        tt['sign_ganon'] = 'You need to complete all the dungeons.'

    if world.boots_hint[player]:
        starting_boots = next((i for i in world.precollected_items if i.player == player
                               and i.name == 'Pegasus Boots'), None)
        if starting_boots:
            uncle_text = 'Lonk! Boots\nare on\nyour feet.'
        else:
            boots_location = next((l for l in world.get_locations()
                                   if l.player == player and l.item and l.item.name == 'Pegasus Boots'), None)
            if boots_location:
                district = next((d for k, d in world.districts[player].items()
                                 if boots_location.name in d.locations), 'Zebes')
                uncle_text = f'Lonk! Boots\nare in {district.name}'
            else:
                uncle_text = "I couldn't\nfind the Boots\ntoday.\nRIP me."

        tt['uncle_leaving_text'] = uncle_text
    else:
        tt['uncle_leaving_text'] = Uncle_texts[random.randint(0, len(Uncle_texts) - 1)]
    tt['end_triforce'] = "{NOBORDER}\n" + Triforce_texts[random.randint(0, len(Triforce_texts) - 1)]
    tt['bomb_shop_big_bomb'] = BombShop2_texts[random.randint(0, len(BombShop2_texts) - 1)]

    # this is what shows after getting the green pendant item in rando
    tt['sahasrahla_quest_have_master_sword'] = Sahasrahla2_texts[random.randint(0, len(Sahasrahla2_texts) - 1)]
    tt['blind_by_the_light'] = Blind_texts[random.randint(0, len(Blind_texts) - 1)]

    if world.goal[player] in ['triforcehunt']:
        tt['ganon_fall_in_alt'] = 'Why are you even here?\n You can\'t even hurt me! Get the Triforce Pieces.'
        tt['ganon_phase_3_alt'] = 'Seriously? Go Away, I will not Die.'
        tt['sign_ganon'] = 'Go find the Triforce pieces... Ganon is invincible!'
        tt['murahdahla'] = "Hello @. I\nam Murahdahla, brother of\nSahasrahla and Aginah. Behold the power of\ninvisibility.\n\n\n\n… … …\n\nWait! you can see me? I knew I should have\nhidden in  a hollow tree. If you bring\n%d triforce pieces, I can reassemble it." % int(world.treasure_hunt_count[player])
    elif world.goal[player] in ['pedestal']:
        tt['ganon_fall_in_alt'] = 'Why are you even here?\n You can\'t even hurt me! Your goal is at the pedestal.'
        tt['ganon_phase_3_alt'] = 'Seriously? Go Away, I will not Die.'
        tt['sign_ganon'] = 'You need to get to the pedestal... Ganon is invincible!'
    else:
        if world.goal[player] == 'trinity':
            trinity_crystal_text = ('%d crystal to beat Ganon.' if world.crystals_needed_for_ganon[player] == 1 else '%d crystals to beat Ganon.') % world.crystals_needed_for_ganon[player]
            tt['sign_ganon'] = 'Three ways to victory! %s Get to it!' % trinity_crystal_text
            tt['murahdahla'] = "Hello @. I\nam Murahdahla, brother of\nSahasrahla and Aginah. Behold the power of\ninvisibility.\n\n\n\n… … …\n\nWait! you can see me? I knew I should have\nhidden in  a hollow tree. If you bring\n%d triforce pieces, I can reassemble it." % int(world.treasure_hunt_count[player])
        elif world.goal[player] == 'ganonhunt':
            tt['sign_ganon'] = 'Go find the Triforce pieces to beat Ganon'
        elif world.goal[player] == 'completionist':
            tt['sign_ganon'] = 'Ganon only respects those who have done everything'
        tt['ganon_fall_in'] = Ganon1_texts[random.randint(0, len(Ganon1_texts) - 1)]
        tt['ganon_fall_in_alt'] = 'You cannot defeat me until you finish your goal!'
        tt['ganon_phase_3_alt'] = 'Got wax in\nyour ears?\nI can not die!'

    tt['kakariko_tavern_fisherman'] = TavernMan_texts[random.randint(0, len(TavernMan_texts) - 1)]

    pedestalitem = world.get_location('Master Sword Pedestal', player).item
    pedestal_text = 'Some Hot Air' if pedestalitem is None else hint_text(pedestalitem, True) if pedestalitem.pedestal_hint_text is not None else 'Unknown Item'
    tt['mastersword_pedestal_translated'] = pedestal_text
    pedestal_credit_text = 'and the Hot Air' if pedestalitem is None else pedestalitem.pedestal_credit_text if pedestalitem.pedestal_credit_text is not None else 'and the Unknown Item'

    etheritem = world.get_location('Ether Tablet', player).item
    ether_text = 'Some Hot Air' if etheritem is None else hint_text(etheritem, True) if etheritem.pedestal_hint_text is not None else 'Unknown Item'
    tt['tablet_ether_book'] = ether_text
    bombositem = world.get_location('Bombos Tablet', player).item
    bombos_text = 'Some Hot Air' if bombositem is None else hint_text(bombositem, True) if bombositem.pedestal_hint_text is not None else 'Unknown Item'
    tt['tablet_bombos_book'] = bombos_text

    # attic hint
    if world.doorShuffle[player]  not in ['vanilla', 'basic']:
        attic_hint = world.get_location("Thieves' Town - Attic", player).parent_region.dungeon.name
        tt['blind_not_that_way'] = f'{attic_hint} is too bright for my eyes'
        # see tagalog.asm tables at 957,967 or Follower_HandleTrigger in JPDASM
        # also the baserom table at org $09A4C2 in hooks.asm (Escort text)
        rom.write_byte(0x04a4be, 0xac)  # change the room to blind's room
        rom.write_byte(0x04a526, 0xb8)  # y coordinate, shifted down
        rom.write_byte(0x04a529, 0x19)  # x tile shifted right a few tiles
        rom.write_byte(0x04a52e, 0x06)  # follower set to blind maiden

    # inverted spawn menu changes
    if world.mode[player] == 'inverted':
        tt['menu_start_2'] = "{MENU}\n{SPEED0}\n≥@'s House\n Dark Chapel\n{CHOICE3}"
        tt['menu_start_3'] = "{MENU}\n{SPEED0}\n≥@'s House\n Dark Chapel\n Mountain Cave\n{CHOICE2}"
        tt['intro_main'] = CompressedTextMapper.convert(
                            "{INTRO}\n Episode  III\n{PAUSE3}\n A Link to\n   the Past\n"
                            + "{PAUSE3}\nInverted\n  Randomizer\n{PAUSE3}\nAfter mostly disregarding what happened in the first two games.\n"
                            + "{PAUSE3}\nLink has been transported to the Dark World\n{PAUSE3}\nWhile he was slumbering\n"
                            + "{PAUSE3}\nWhatever will happen?\n{PAUSE3}\n{CHANGEPIC}\nGanon has moved around all the items in Hyrule.\n"
                            + "{PAUSE7}\nYou will have to find all the items necessary to beat Ganon.\n"
                            + "{PAUSE7}\nThis is your chance to be a hero.\n{PAUSE3}\n{CHANGEPIC}\n"
                            + "You must get the 7 crystals to beat Ganon.\n{PAUSE9}\n{CHANGEPIC}", False)
    rom.write_bytes(0xE0000, tt.getBytes())

    credits = Credits()

    sickkiditem = world.get_location('Sick Kid', player).item
    sickkiditem_text = random.choice(SickKid_texts) if sickkiditem is None or sickkiditem.sickkid_credit_text is None else sickkiditem.sickkid_credit_text

    zoraitem = world.get_location('King Zora', player).item
    zoraitem_text = random.choice(Zora_texts) if zoraitem is None or zoraitem.zora_credit_text is None else zoraitem.zora_credit_text

    magicshopitem = world.get_location('Potion Shop', player).item
    magicshopitem_text = random.choice(MagicShop_texts) if magicshopitem is None or magicshopitem.magicshop_credit_text is None else magicshopitem.magicshop_credit_text

    fluteboyitem = world.get_location('Flute Spot', player).item
    fluteboyitem_text = random.choice(FluteBoy_texts) if fluteboyitem is None or fluteboyitem.fluteboy_credit_text is None else fluteboyitem.fluteboy_credit_text

    credits.update_credits_line('castle', 0, random.choice(KingsReturn_texts))
    credits.update_credits_line('sanctuary', 0, random.choice(Sanctuary_texts))

    credits.update_credits_line('kakariko', 0, random.choice(Kakariko_texts).format(random.choice(Sahasrahla_names)))
    credits.update_credits_line('desert', 0, random.choice(DesertPalace_texts))
    credits.update_credits_line('hera', 0, random.choice(MountainTower_texts))
    credits.update_credits_line('house', 0, random.choice(LinksHouse_texts))
    credits.update_credits_line('zora', 0, zoraitem_text)
    credits.update_credits_line('witch', 0, magicshopitem_text)
    credits.update_credits_line('lumberjacks', 0, random.choice(Lumberjacks_texts))
    credits.update_credits_line('grove', 0, fluteboyitem_text)
    credits.update_credits_line('well', 0, random.choice(WishingWell_texts))
    credits.update_credits_line('smithy', 0, random.choice(Blacksmiths_texts))
    credits.update_credits_line('kakariko2', 0, sickkiditem_text)
    credits.update_credits_line('bridge', 0, random.choice(DeathMountain_texts))
    credits.update_credits_line('woods', 0, random.choice(LostWoods_texts))
    credits.update_credits_line('pedestal', 0, pedestal_credit_text)

    (pointers, data) = credits.get_bytes()
    rom.write_bytes(0x181500, data)
    rom.write_bytes(0x76CC0, [byte for p in pointers for byte in [p & 0xFF, p >> 8 & 0xFF]])


useful_item_names = {
    'Mushroom', 'Shovel', 'Magic Powder', 'Progressive Shield', 'Progressive Armor', 'Blue Mail',  'Red Mail',
    'Mirror Shield', 'Blue Boomerang', 'Red Boomerang', 'Bug Catching Net', 'Cane of Byrna', 'Cape',
    'Magic Upgrade (1/2)', 'Magic Upgrade (1/4)', 'Ether', 'Quake'}


def useful_item_for_hint(item, world):
    return 'Bottle' in item.name or (item.name in useful_item_names
                                     and item.name not in world.required_medallions[item.player])


def text_for_item(item, world, player, team):
    if item.player == player:
        return item.hint_text
    else:
        return f'{item.hint_text} for {world.player_names[item.player][team]}'

def init_open_mode_sram(rom):
        rom.initial_sram.pre_open_castle_gate()
        rom.initial_sram.set_progress_indicator(0x02)
        rom.initial_sram.set_progress_flags(0x14)
        rom.initial_sram.set_starting_entrance(0x01)

def init_standard_mode_sram(rom):
        rom.initial_sram.set_progress_indicator(0x00)
        rom.initial_sram.set_progress_flags(0x0)
        rom.initial_sram.set_starting_entrance(0x00)

def set_inverted_mode(world, player, rom):
    rom.write_byte(snes_to_pc(0x0283E0), 0xF0)  # residual portals
    rom.write_byte(snes_to_pc(0x02B34D), 0xF0)
    rom.write_byte(snes_to_pc(0x06DB78), 0x8B)
    rom.write_byte(snes_to_pc(0x05AF79), 0xF0)
    rom.write_byte(snes_to_pc(0x0DB3C5), 0xC6)
    rom.write_byte(snes_to_pc(0x07A3F4), 0xF0)  # duck
    write_int16s(rom, snes_to_pc(0x02E849), [0x0043, 0x0056, 0x0058, 0x006C, 0x006F, 0x0070, 0x007B, 0x007F, 0x001B])  # dw flute
    write_int16(rom, snes_to_pc(0x02E8D5), 0x07C8)
    write_int16(rom, snes_to_pc(0x02E8F7), 0x01F8)
    rom.write_byte(snes_to_pc(0x08D40C), 0xD0)  # morph proof
    rom.write_byte(snes_to_pc(0x1BC428), 0x00)  # remove diggable light world portals
    rom.write_byte(snes_to_pc(0x1BC43A), 0x00)
    rom.write_byte(snes_to_pc(0x1BC590), 0x00)
    rom.write_byte(snes_to_pc(0x1BC5A1), 0x00)
    rom.write_byte(snes_to_pc(0x1BC5B1), 0x00)
    rom.write_byte(snes_to_pc(0x1BC5C7), 0x00)
    # the following bytes should only be written in vanilla
    # or they'll overwrite the randomizer's shuffles
    if world.shuffle[player] == 'vanilla':
        rom.write_byte(0xDBB73 + 0x23, 0x37)  # switch AT and GT
        rom.write_byte(0xDBB73 + 0x36, 0x24)
        if world.doorShuffle[player] == 'vanilla' or world.intensity[player] < 3:
            write_int16(rom, 0x15AEE + 2*0x38, 0x00E0)
            write_int16(rom, 0x15AEE + 2*0x25, 0x000C)
    if world.shuffle[player] in ['vanilla', 'dungeonssimple', 'dungeonsfull']:
        rom.write_byte(0x15B8C, 0x6C)
        rom.write_byte(0xDBB73 + 0x00, 0x53)  # switch bomb shop and links house
        rom.write_byte(0xDBB73 + 0x52, 0x01)
        rom.write_byte(0xDBB73 + 0x15, 0x06)  # bumper and old man cave
        write_int16(rom, 0x15AEE + 2*0x17, 0x00F0)
        rom.write_byte(0xDBB73 + 0x05, 0x16)
        write_int16(rom, 0x15AEE + 2*0x07, 0x00FB)
        rom.write_byte(0xDBB73 + 0x2D, 0x17)
        write_int16(rom, 0x15AEE + 2*0x2F, 0x00EB)
        rom.write_byte(0xDBB73 + 0x06, 0x2E)
        write_int16(rom, 0x15AEE + 2*0x08, 0x00E6)
        rom.write_byte(0xDBB73 + 0x16, 0x5E)
        rom.write_byte(0xDBB73 + 0x6F, 0x07)  # DDM fairy to old man cave
        write_int16(rom, 0x15AEE + 2*0x18, 0x00F1)
        rom.write_byte(0x15B8C + 0x18, 0x43)
        write_int16(rom, 0x15BDB + 2 * 0x18, 0x1400)
        write_int16(rom, 0x15C79 + 2 * 0x18, 0x0294)
        write_int16(rom, 0x15D17 + 2 * 0x18, 0x0600)
        write_int16(rom, 0x15DB5 + 2 * 0x18, 0x02E8)
        write_int16(rom, 0x15E53 + 2 * 0x18, 0x0678)
        write_int16(rom, 0x15EF1 + 2 * 0x18, 0x0303)
        write_int16(rom, 0x15F8F + 2 * 0x18, 0x0685)
        rom.write_byte(0x1602D + 0x18, 0x0A)
        rom.write_byte(0x1607C + 0x18, 0xF6)
        write_int16(rom, 0x160CB + 2 * 0x18, 0x0000)
        write_int16(rom, 0x16169 + 2 * 0x18, 0x0000)
    write_int16(rom, 0x15AEE + 2 * 0x3D, 0x0003)  # pyramid exit and houlihan
    rom.write_byte(0x15B8C + 0x3D, 0x5B)
    write_int16(rom, 0x15BDB + 2 * 0x3D, 0x0B0E)
    write_int16(rom, 0x15C79 + 2 * 0x3D, 0x075A)
    write_int16(rom, 0x15D17 + 2 * 0x3D, 0x0674)
    write_int16(rom, 0x15DB5 + 2 * 0x3D, 0x07A8)
    write_int16(rom, 0x15E53 + 2 * 0x3D, 0x06E8)
    write_int16(rom, 0x15EF1 + 2 * 0x3D, 0x07C7)
    write_int16(rom, 0x15F8F + 2 * 0x3D, 0x06F3)
    rom.write_byte(0x1602D + 0x3D, 0x06)
    rom.write_byte(0x1607C + 0x3D, 0xFA)
    write_int16(rom, 0x160CB + 2 * 0x3D, 0x0000)
    write_int16(rom, 0x16169 + 2 * 0x3D, 0x0000)
    write_int16(rom, snes_to_pc(0x02D8D4), 0x112)  # change sactuary spawn point to dark sanc
    rom.write_bytes(snes_to_pc(0x02D8E8), [0x22, 0x22, 0x22, 0x23, 0x04, 0x04, 0x04, 0x05])
    write_int16(rom, snes_to_pc(0x02D91A), 0x0400)
    write_int16(rom, snes_to_pc(0x02D928), 0x222E)
    write_int16(rom, snes_to_pc(0x02D936), 0x229A)
    write_int16(rom, snes_to_pc(0x02D944), 0x0480)
    write_int16(rom, snes_to_pc(0x02D952), 0x00A5)
    write_int16(rom, snes_to_pc(0x02D960), 0x007F)
    rom.write_byte(snes_to_pc(0x02D96D), 0x14)
    rom.write_byte(snes_to_pc(0x02D974), 0x00)
    rom.write_byte(snes_to_pc(0x02D97B), 0xFF)
    rom.write_byte(snes_to_pc(0x02D982), 0x00)
    rom.write_byte(snes_to_pc(0x02D989), 0x02)
    rom.write_byte(snes_to_pc(0x02D990), 0x00)
    write_int16(rom, snes_to_pc(0x02D998), 0x0000)
    write_int16(rom, snes_to_pc(0x02D9A6), 0x005A)
    rom.write_byte(snes_to_pc(0x02D9B3), 0x12)
    # keep the old man spawn point at old man house unless shuffle is vanilla
    if world.shuffle[player] in ['vanilla', 'dungeonsfull', 'dungeonssimple']:
        rom.write_bytes(snes_to_pc(0x308350), [0x00, 0x00, 0x01])
        write_int16(rom, snes_to_pc(0x02D8DE), 0x00F1)
        rom.write_bytes(snes_to_pc(0x02D910), [0x1F, 0x1E, 0x1F, 0x1F, 0x03, 0x02, 0x03, 0x03])
        write_int16(rom, snes_to_pc(0x02D924), 0x0300)
        write_int16(rom, snes_to_pc(0x02D932), 0x1F10)
        write_int16(rom, snes_to_pc(0x02D940), 0x1FC0)
        write_int16(rom, snes_to_pc(0x02D94E), 0x0378)
        write_int16(rom, snes_to_pc(0x02D95C), 0x0187)
        write_int16(rom, snes_to_pc(0x02D96A), 0x017F)
        rom.write_byte(snes_to_pc(0x02D972), 0x06)
        rom.write_byte(snes_to_pc(0x02D979), 0x00)
        rom.write_byte(snes_to_pc(0x02D980), 0xFF)
        rom.write_byte(snes_to_pc(0x02D987), 0x00)
        rom.write_byte(snes_to_pc(0x02D98E), 0x22)
        rom.write_byte(snes_to_pc(0x02D995), 0x12)
        write_int16(rom, snes_to_pc(0x02D9A2), 0x0000)
        write_int16(rom, snes_to_pc(0x02D9B0), 0x0007)
        rom.write_byte(snes_to_pc(0x02D9B8), 0x12)
        rom.write_bytes(0x180247, [0x00, 0x5A, 0x00, 0x00, 0x00, 0x00, 0x00])
    write_int16(rom, 0x15AEE + 2 * 0x06, 0x0020)  # post aga hyrule castle spawn
    rom.write_byte(0x15B8C + 0x06, 0x1B)
    write_int16(rom, 0x15BDB + 2 * 0x06, 0x00AE)
    write_int16(rom, 0x15C79 + 2 * 0x06, 0x0610)
    write_int16(rom, 0x15D17 + 2 * 0x06, 0x077E)
    write_int16(rom, 0x15DB5 + 2 * 0x06, 0x0672)
    write_int16(rom, 0x15E53 + 2 * 0x06, 0x07F8)
    write_int16(rom, 0x15EF1 + 2 * 0x06, 0x067D)
    write_int16(rom, 0x15F8F + 2 * 0x06, 0x0803)
    rom.write_byte(0x1602D + 0x06, 0x00)
    rom.write_byte(0x1607C + 0x06, 0xF2)
    write_int16(rom, 0x160CB + 2 * 0x06, 0x0000)
    write_int16(rom, 0x16169 + 2 * 0x06, 0x0000)
    write_int16(rom, snes_to_pc(0x02E87B), 0x00AE)  # move flute splot 9
    write_int16(rom, snes_to_pc(0x02E89D), 0x0610)
    write_int16(rom, snes_to_pc(0x02E8BF), 0x077E)
    write_int16(rom, snes_to_pc(0x02E8E1), 0x0672)
    write_int16(rom, snes_to_pc(0x02E903), 0x07F8)
    write_int16(rom, snes_to_pc(0x02E925), 0x067D)
    write_int16(rom, snes_to_pc(0x02E947), 0x0803)
    write_int16(rom, snes_to_pc(0x02E969), 0x0000)
    write_int16(rom, snes_to_pc(0x02E98B), 0xFFF2)
    rom.write_byte(snes_to_pc(0x1AF696), 0xF0)  # bat sprite retreat
    rom.write_byte(snes_to_pc(0x1AF6B2), 0x33)
    rom.write_bytes(snes_to_pc(0x1AF730), [0x6A, 0x9E, 0x0C, 0x00, 0x7A, 0x9E, 0x0C,
                                           0x00, 0x8A, 0x9E, 0x0C, 0x00, 0x6A, 0xAE,
                                           0x0C, 0x00, 0x7A, 0xAE, 0x0C, 0x00, 0x8A,
                                           0xAE, 0x0C, 0x00, 0x67, 0x97, 0x0C, 0x00,
                                           0x8D, 0x97, 0x0C, 0x00])
    write_int16s(rom, snes_to_pc(0x0FF1C8), [0x190F, 0x190F, 0x190F, 0x194C, 0x190F,
                                                 0x194B, 0x190F, 0x195C, 0x594B, 0x194C,
                                                 0x19EE, 0x19EE, 0x194B, 0x19EE, 0x19EE,
                                                 0x19EE, 0x594B, 0x190F, 0x595C, 0x190F,
                                                 0x190F, 0x195B, 0x190F, 0x190F, 0x19EE,
                                                 0x19EE, 0x195C, 0x19EE, 0x19EE, 0x19EE,
                                                 0x19EE, 0x595C, 0x595B, 0x190F, 0x190F,
                                                 0x190F])
    write_int16s(rom, snes_to_pc(0x0FA480), [0x190F, 0x196B, 0x9D04, 0x9D04, 0x196B,
                                                 0x190F, 0x9D04, 0x9D04])
    write_int16s(rom, snes_to_pc(0x1bb810), [0x00BE, 0x00C0, 0x013E])
    write_int16s(rom, snes_to_pc(0x1bb836), [0x001B, 0x001B, 0x001B])
    write_int16(rom, snes_to_pc(0x308300), 0x0140)  # new pyramid hole entrance
    write_int16(rom, snes_to_pc(0x308320), 0x001B)
    if world.shuffle[player] in ['vanilla', 'dungeonssimple', 'dungeonsfull']:
        rom.write_byte(snes_to_pc(0x308340), 0x7B)
    write_int16(rom, snes_to_pc(0x1af504), 0x148B)
    write_int16(rom, snes_to_pc(0x1af50c), 0x149B)
    write_int16(rom, snes_to_pc(0x1af514), 0x14A4)
    write_int16(rom, snes_to_pc(0x1af51c), 0x1489)
    write_int16(rom, snes_to_pc(0x1af524), 0x14AC)
    write_int16(rom, snes_to_pc(0x1af52c), 0x54AC)
    write_int16(rom, snes_to_pc(0x1af534), 0x148C)
    write_int16(rom, snes_to_pc(0x1af53c), 0x548C)
    write_int16(rom, snes_to_pc(0x1af544), 0x1484)
    write_int16(rom, snes_to_pc(0x1af54c), 0x5484)
    write_int16(rom, snes_to_pc(0x1af554), 0x14A2)
    write_int16(rom, snes_to_pc(0x1af55c), 0x54A2)
    write_int16(rom, snes_to_pc(0x1af564), 0x14A0)
    write_int16(rom, snes_to_pc(0x1af56c), 0x54A0)
    write_int16(rom, snes_to_pc(0x1af574), 0x148E)
    write_int16(rom, snes_to_pc(0x1af57c), 0x548E)
    write_int16(rom, snes_to_pc(0x1af584), 0x14AE)
    write_int16(rom, snes_to_pc(0x1af58c), 0x54AE)
    rom.write_byte(snes_to_pc(0x00DB9D), 0x1A)  # castle hole graphics
    rom.write_byte(snes_to_pc(0x00DC09), 0x1A)
    rom.write_byte(snes_to_pc(0x00D009), 0x31)
    rom.write_byte(snes_to_pc(0x00D0e8), 0xE0)
    rom.write_byte(snes_to_pc(0x00D1c7), 0x00)
    write_int16(rom, snes_to_pc(0x1BE8DA), 0x39AD)
    rom.write_bytes(0x0086E, [0x5C, 0x00, 0xA0, 0xA1])  # TR tail
    rom.write_bytes(snes_to_pc(0x1BC67A), [0x2E, 0x0B, 0x82])  # add warps under rocks
    rom.write_bytes(snes_to_pc(0x1BC81E), [0x94, 0x1D, 0x82])
    rom.write_bytes(snes_to_pc(0x1BC655), [0x4A, 0x1D, 0x82])
    rom.write_bytes(snes_to_pc(0x1BC80D), [0xB2, 0x0B, 0x82])
    rom.write_bytes(snes_to_pc(0x1BC3DF), [0xD8, 0xD1])
    rom.write_bytes(snes_to_pc(0x1BD1D8), [0xA8, 0x02, 0x82, 0xFF, 0xFF])
    rom.write_bytes(snes_to_pc(0x1BC85A), [0x50, 0x0F, 0x82])
    write_int16(rom, 0xDB96F + 2 * 0x35, 0x001B)  # move pyramid exit door
    write_int16(rom, 0xDBA71 + 2 * 0x35, 0x06A4)
    if world.shuffle[player] in ['vanilla', 'dungeonssimple', 'dungeonsfull']:
        rom.write_byte(0xDBB73 + 0x35, 0x36)
    # rom.write_byte(snes_to_pc(0x09D436), 0xF3)  # remove castle gate warp
    del world.data_tables[player].ow_enemy_table[0xab][5]
    if world.shuffle[player] in ['vanilla', 'dungeonssimple', 'dungeonsfull']:
        write_int16(rom, 0x15AEE + 2 * 0x37, 0x0010)  # pyramid exit to new hc area
        rom.write_byte(0x15B8C + 0x37, 0x1B)
        write_int16(rom, 0x15BDB + 2 * 0x37, 0x0418)
        write_int16(rom, 0x15C79 + 2 * 0x37, 0x0679)
        write_int16(rom, 0x15D17 + 2 * 0x37, 0x06B4)
        write_int16(rom, 0x15DB5 + 2 * 0x37, 0x06C6)
        write_int16(rom, 0x15E53 + 2 * 0x37, 0x0738)
        write_int16(rom, 0x15EF1 + 2 * 0x37, 0x06E6)
        write_int16(rom, 0x15F8F + 2 * 0x37, 0x0733)
        rom.write_byte(0x1602D + 0x37, 0x07)
        rom.write_byte(0x1607C + 0x37, 0xF9)
        write_int16(rom, 0x160CB + 2 * 0x37, 0x0000)
        write_int16(rom, 0x16169 + 2 * 0x37, 0x0000)
    rom.write_bytes(snes_to_pc(0x1BC387), [0xDD, 0xD1])
    rom.write_bytes(snes_to_pc(0x1BD1DD), [0xA4, 0x06, 0x82, 0x9E, 0x06, 0x82, 0xFF, 0xFF])
    rom.write_byte(0x180089, 0x01)  # open TR after exit
    rom.write_byte(snes_to_pc(0x0ABFBB), 0x90)
    rom.write_byte(snes_to_pc(0x0280A6), 0xD0)
    rom.write_bytes(snes_to_pc(0x06B2AB), [0xF0, 0xE1, 0x05])

def patch_shuffled_dark_sanc(world, rom, player):
    dark_sanc = world.get_region('Dark Sanctuary Hint', player)
    dark_sanc_entrance = str([i for i in dark_sanc.entrances if i.parent_region.name != 'Menu'][0].name)
    room_id, ow_area, vram_loc, scroll_y, scroll_x, link_y, link_x, camera_y, camera_x, unknown_1, unknown_2, door_1, door_2 = door_addresses[dark_sanc_entrance][1]
    if dark_sanc_entrance == 'Tavern North':
        link_y -= 0x10  # rom code assumes south-facing doors and adds $10 to the y-coordinate
    door_index = door_addresses[str(dark_sanc_entrance)][0]

    rom.write_byte(0x180241, 0x01)
    rom.write_byte(0x180248, door_index + 1)
    write_int16(rom, 0x180250, room_id)
    rom.write_byte(0x180252, ow_area)
    write_int16s(rom, 0x180253, [vram_loc, scroll_y, scroll_x, link_y, link_x, camera_y, camera_x])
    rom.write_bytes(0x180262, [unknown_1, unknown_2, 0x00])


def valid_dungeon_locations(valid_locations):
    dungeon_locations = collections.defaultdict(set)
    for l in valid_locations:
        if l.parent_region.dungeon:
            dungeon_locations[l.parent_region.dungeon.name].add(l)
    return dungeon_locations


def update_compasses(rom, dungeon_locations, world, player):
    layouts = world.dungeon_layouts[player]
    provided_dungeon = False
    for name, builder in layouts.items():
        dungeon_id = compass_data[name][4]
        dungeon_count = len(dungeon_locations[name])
        rom.write_bytes(0x187040 + dungeon_id, int16_as_bytes(dungeon_count))
        # total tiles
        rom.write_bytes(0x187060 + dungeon_id, int16_as_bytes(((dungeon_count // 100) % 10) + 0x2490))
        rom.write_bytes(0x187080 + dungeon_id, int16_as_bytes(((dungeon_count // 10) % 10) + 0x2490))
        rom.write_bytes(0x1870A0 + dungeon_id, int16_as_bytes((dungeon_count % 10) + 0x2490))
        if builder.bk_provided:
            if provided_dungeon:
                logging.getLogger('').warning('Multiple dungeons have forced BKs! Compass code might need updating?')
            rom.write_byte(0x186FFF, dungeon_id)
            provided_dungeon = True
    if not provided_dungeon:
        rom.write_byte(0x186FFF, 0xff)



InconvenientDungeonEntrances = {'Turtle Rock': 'Turtle Rock Main',
                                'Misery Mire': 'Misery Mire',
                                'Ice Palace': 'Ice Palace',
                                'Skull Woods Final Section': 'The back of Skull Woods',
                                }

InconvenientOtherEntrances = {'Death Mountain Return Cave (West)': 'The SW DM foothills cave',
                              'Mimic Cave': 'Mimic Ledge',
                              'Hammer Peg Cave': 'The rows of pegs',
                              'Pyramid Fairy': 'The crack on the pyramid'
                              }

ConnectorEntrances = {'Elder House (East)': 'Elder House',
                      'Elder House (West)': 'Elder House',
                      'Two Brothers House (East)': 'Eastern Quarreling Brothers\' house',
                      'Old Man Cave (West)': 'The lower DM entrance',
                      'Bumper Cave (Bottom)': 'The lower Bumper Cave',
                      'Superbunny Cave (Top)': 'The summit of dark DM cave',
                      'Superbunny Cave (Bottom)': 'The base of east dark DM',
                      'Hookshot Cave': 'The rock on dark DM',
                      'Two Brothers House (West)': 'The door near the race game',
                      'Old Man Cave (East)': 'The SW-most cave on west DM',
                      'Old Man House (Bottom)': 'A cave with a door on west DM',
                      'Old Man House (Top)': 'The eastmost cave on west DM',
                      'Death Mountain Return Cave (East)': 'The westmost cave on west DM',
                      'Spectacle Rock Cave Peak': 'The highest cave on west DM',
                      'Spectacle Rock Cave': 'The right ledge on west DM',
                      'Spectacle Rock Cave (Bottom)': 'The left ledge on west DM',
                      'Paradox Cave (Bottom)': 'The right paired cave on east DM',
                      'Paradox Cave (Middle)': 'The southmost cave on east DM',
                      'Paradox Cave (Top)': 'The east DM summit cave',
                      'Fairy Ascension Cave (Bottom)': 'The east DM cave behind rocks',
                      'Fairy Ascension Cave (Top)': 'The central ledge on east DM',
                      'Spiral Cave': 'The left ledge on east DM',
                      'Spiral Cave (Bottom)': 'The SWmost cave on east DM'
                      }

DungeonEntrances = {'Eastern Palace': 'Eastern Palace',
                    'Hyrule Castle Entrance (South)': 'The ground level castle door',
                    'Thieves Town': 'Thieves\' Town',
                    'Swamp Palace': 'Swamp Palace',
                    'Dark Death Mountain Ledge (West)': 'The East dark DM connector ledge',
                    'Dark Death Mountain Ledge (East)': 'The East dark DM connector ledge',
                    'Desert Palace Entrance (South)': 'The book sealed passage',
                    'Tower of Hera': 'The Tower of Hera',
                    'Palace of Darkness': 'Palace of Darkness',
                    'Hyrule Castle Entrance (West)': 'The left castle door',
                    'Hyrule Castle Entrance (East)': 'The right castle door',
                    'Desert Palace Entrance (West)': 'The westmost building in the desert',
                    'Desert Palace Entrance (North)': 'The northmost cave in the desert'
                    }

ItemEntrances = {'Blinds Hideout': 'Blind\'s old house',
                 'Chicken House': 'The chicken lady\'s house',
                 'Aginahs Cave': 'The open desert cave',
                 'Sahasrahlas Hut': 'The house near armos',
                 'Blacksmiths Hut': 'The old smithery',
                 'Sick Kids House': 'The central house in Kakariko',
                 'Mini Moldorm Cave': 'The cave south of Lake Hylia',
                 'Ice Rod Cave': 'The sealed cave SE Lake Hylia',
                 'Library': 'The old library',
                 'Potion Shop': 'The witch\'s building',
                 'Dam': 'The old dam',
                 'Waterfall of Wishing': 'Going behind the waterfall',
                 'Bonk Rock Cave': 'The rock pile near Sanctuary',
                 'Graveyard Cave': 'The graveyard ledge',
                 'Checkerboard Cave': 'The NE desert ledge',
                 'Cave 45': 'The ledge south of haunted grove',
                 'Kings Grave': 'The northeastmost grave',
                 'C-Shaped House': 'The NE house in Village of Outcasts',
                 'Mire Shed': 'The western hut in the mire',
                 'Spike Cave': 'The ledge cave on west dark DM',
                 'Hype Cave': 'The cave south of the old bomb shop',
                 'Brewery': 'The Village of Outcasts building with no door',
                 'Chest Game': 'The westmost building in the Village of Outcasts',
                 }

ShopEntrances = {'Lake Hylia Shop': 'The cave NW Lake Hylia',
                 'Kakariko Shop': 'The old Kakariko shop',
                 'Capacity Upgrade': 'The cave on the island',
                 'Dark Lake Hylia Shop': 'The building NW dark Lake Hylia',
                 'Dark World Shop': 'The hammer sealed building',
                 'Red Shield Shop': 'The fenced in building',
                 'Dark Death Mountain Shop': 'The base of east dark DM',
                 'Dark Potion Shop': 'The building near the catfish',
                 'Dark Lumberjack Shop': 'The northmost Dark World building'
                 }

OtherEntrances = {'Lake Hylia Fairy': 'A cave NE of Lake Hylia',
                  'Light Hype Fairy': 'The cave south of your house',
                  'Desert Fairy': 'The cave near the desert',
                  'Lost Woods Gamble': 'A tree trunk door',
                  'Fortune Teller (Light)': 'A building NE of Kakariko',
                  'Snitch Lady (East)': 'A house guarded by a snitch',
                  'Snitch Lady (West)': 'A house guarded by a snitch',
                  'Bush Covered House': 'A house with an uncut lawn',
                  'Tavern (Front)': 'A building with a backdoor',
                  'Light World Bomb Hut': 'A Kakariko building with no door',
                  'Long Fairy Cave': 'The eastmost portal cave',
                  'Good Bee Cave': 'The open cave SE Lake Hylia',
                  '20 Rupee Cave': 'The rock SE Lake Hylia',
                  '50 Rupee Cave': 'The rock near the desert',
                  'Lumberjack House': 'The lumberjack house',
                  'Lake Hylia Fortune Teller': 'The building NW Lake Hylia',
                  'Kakariko Gamble Game': 'The old Kakariko gambling den',
                  'Bonk Fairy (Light)': 'The rock pile near your home',
                  'Hookshot Fairy': 'The left paired cave on east DM',
                  'Bonk Fairy (Dark)': 'The rock pile near the old bomb shop',
                  'Dark Lake Hylia Fairy': 'The cave NE dark Lake Hylia',
                  'Dark Death Mountain Fairy': 'The SW cave on dark DM',
                  'East Dark World Hint': 'The dark cave near the eastmost portal',
                  'Mire Hint': 'The cave east of the mire',
                  'Palace of Darkness Hint': 'The building south of Kiki',
                  'Dark Lake Hylia Ledge Spike Cave': 'The rock SE dark Lake Hylia',
                  'Archery Game': 'The old archery game',
                  'Dark Lake Hylia Ledge Hint': 'The open cave SE dark Lake Hylia',
                  'Mire Fairy': 'The eastern hut in the mire',
                  'Dark Lake Hylia Ledge Fairy': 'The sealed cave SE dark Lake Hylia',
                  'Fortune Teller (Dark)': 'The building NE the Village of Outcasts',
                  'Dark Sanctuary Hint': 'The dark sanctuary cave'
                  }

InsanityEntrances = {'Sanctuary': 'Sanctuary',
                     'Lumberjack Tree Cave': 'The cave Behind Lumberjacks',
                     'Lost Woods Hideout Stump': 'The stump in Lost Woods',
                     'North Fairy Cave': 'The cave East of Graveyard',
                     'Bat Cave Cave': 'The cave in eastern Kakariko',
                     'Kakariko Well Cave': 'The cave in northern Kakariko',
                     'Hyrule Castle Secret Entrance Stairs': 'The tunnel near the castle',
                     'Skull Woods First Section Door': 'The southeastmost skull',
                     'Skull Woods Second Section Door (East)': 'The central open skull',
                     'Skull Woods Second Section Door (West)': 'The westmost open skull',
                     'Desert Palace Entrance (East)': 'The eastern building in the desert',
                     'Turtle Rock Isolated Ledge Entrance': 'The isolated ledge on east dark DM',
                     'Bumper Cave (Top)': 'The upper Bumper Cave',
                     'Hookshot Cave Back Entrance': 'The stairs on the floating island'
                     }

HintLocations = ['telepathic_tile_eastern_palace',
                 'telepathic_tile_tower_of_hera_floor_4',
                 'telepathic_tile_spectacle_rock',
                 'telepathic_tile_swamp_entrance',
                 'telepathic_tile_thieves_town_upstairs',
                 'telepathic_tile_misery_mire',
                 'telepathic_tile_palace_of_darkness',
                 'telepathic_tile_desert_bonk_torch_room',
                 'telepathic_tile_castle_tower',
                 'telepathic_tile_ice_large_room',
                 'telepathic_tile_turtle_rock',
                 'telepathic_tile_ice_entrance',
                 'telepathic_tile_ice_stalfos_knights_room',
                 'telepathic_tile_tower_of_hera_entrance',
                 'telepathic_tile_south_east_darkworld_cave',
                 'dark_palace_tree_dude',
                 'dark_sanctuary_hint_0',
                 'dark_sanctuary_hint_1',
                 'dark_sanctuary_yes',
                 'dark_sanctuary_hint_2']

InconvenientLocations = ['Spike Cave',
                         'Sahasrahla',
                         'Purple Chest',
                         'Magic Bat']

InconvenientDungeonLocations = ['Swamp Left',
                                'Mire Left',
                                'Eastern Palace - Big Key Chest',
                                'Tower of Hera - Big Key Chest',
                                'Thieves\' Town - Big Chest',
                                'Ice Palace - Big Chest',
                                'Ganons Tower - Big Chest']

InconvenientVanillaLocations = ['Graveyard Cave',
                                'Mimic Cave']

RelevantItems = ['Bow',
                 'Progressive Bow',
                 'Book of Mudora',
                 'Hammer',
                 'Hookshot',
                 'Magic Mirror',
                 'Ocarina',
                 'Ocarina (Activated)',
                 'Pegasus Boots',
                 'Power Glove',
                 'Cape',
                 'Mushroom',
                 'Shovel',
                 'Lamp',
                 'Magic Powder',
                 'Moon Pearl',
                 'Cane of Somaria',
                 'Fire Rod',
                 'Flippers',
                 'Ice Rod',
                 'Titans Mitts',
                 'Ether',
                 'Bombos',
                 'Quake',
                 'Bottle',
                 'Bottle (Red Potion)',
                 'Bottle (Green Potion)',
                 'Bottle (Blue Potion)',
                 'Bottle (Fairy)',
                 'Bottle (Bee)',
                 'Bottle (Good Bee)',
                 'Master Sword',
                 'Tempered Sword',
                 'Fighter Sword',
                 'Golden Sword',
                 'Progressive Sword',
                 'Progressive Glove',
                 'Master Sword',
                 'Power Star',
                 'Triforce Piece',
                 'Single Arrow',
                 'Blue Mail',
                 'Red Mail',
                 'Progressive Armor',
                 'Blue Boomerang',
                 'Red Boomerang',
                 'Blue Shield',
                 'Red Shield',
                 'Mirror Shield',
                 'Progressive Shield',
                 'Bug Catching Net',
                 'Cane of Byrna',
                 'Magic Upgrade (1/2)',
                 'Magic Upgrade (1/4)'
                 ]

SmallKeys = ['Small Key (Eastern Palace)',
             'Small Key (Escape)',
             'Small Key (Desert Palace)',
             'Small Key (Tower of Hera)',
             'Small Key (Agahnims Tower)',
             'Small Key (Palace of Darkness)',
             'Small Key (Thieves Town)',
             'Small Key (Swamp Palace)',
             'Small Key (Skull Woods)',
             'Small Key (Ice Palace)',
             'Small Key (Misery Mire)',
             'Small Key (Turtle Rock)',
             'Small Key (Ganons Tower)',
             ]

BigKeys = ['Big Key (Eastern Palace)',
           'Big Key (Desert Palace)',
           'Big Key (Tower of Hera)',
           'Big Key (Palace of Darkness)',
           'Big Key (Thieves Town)',
           'Big Key (Swamp Palace)',
           'Big Key (Skull Woods)',
           'Big Key (Ice Palace)',
           'Big Key (Misery Mire)',
           'Big Key (Turtle Rock)',
           'Big Key (Ganons Tower)'
           ]

hash_alphabet = [
    "Bow", "Boomerang", "Hookshot", "Bomb", "Mushroom", "Powder", "Rod", "Pendant", "Bombos", "Ether", "Quake",
    "Lamp", "Hammer", "Shovel", "Ocarina", "Bug Net", "Book", "Bottle", "Potion", "Cane", "Cape", "Mirror", "Boots",
    "Gloves", "Flippers", "Pearl", "Shield", "Tunic", "Heart", "Map", "Compass", "Key"
]
