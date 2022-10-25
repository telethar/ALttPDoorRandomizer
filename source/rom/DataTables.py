from collections import defaultdict

from Utils import snes_to_pc, int24_as_bytes, int16_as_bytes

from source.dungeon.EnemyList import EnemyTable, init_vanilla_sprites, vanilla_sprites, init_enemy_stats
from source.dungeon.RoomHeader import init_room_headers
from source.dungeon.RoomList import Room0127
from source.enemizer.OwEnemyList import init_vanilla_sprites_ow, vanilla_sprites_ow
from source.enemizer.SpriteSheets import init_sprite_sheets, init_sprite_requirements


def convert_area_id_to_offset(area_id):
    if area_id < 0x40:
        return area_id
    if 0x40 <= area_id < 0x80:
        return area_id + 0x40
    if 0x90 <= area_id < 0xCF:
        return area_id - 0x50
    raise Exception(f'{hex(area_id)} is not a valid area id for offset math')


class DataTables:
    def __init__(self):
        self.room_headers = None
        self.room_list = None
        self.sprite_sheets = None
        self.uw_enemy_table = None
        self.ow_enemy_table = None
        self.pot_secret_table = None
        self.overworld_sprite_sheets = None

        # associated data
        self.sprite_requirements = None
        self.enemy_stats = None

    def write_to_rom(self, rom, colorize_pots=False):
        if self.pot_secret_table.size() > 0x11c0:
            raise Exception('Pot table is too big for current area')
        self.pot_secret_table.write_pot_data_to_rom(rom, colorize_pots)
        for room_id, header in self.room_headers.items():
            data_location = (0x30DA00 + room_id * 14) & 0xFFFF
            rom.write_bytes(snes_to_pc(0x04F1E2) + room_id * 2, int16_as_bytes(data_location))
            header.write_to_rom(rom, snes_to_pc(0x30DA00))  # new header table, bank30, tables.asm
        room_start_address = 0x378000
        for room_id, room in self.room_list.items():
            rom.write_bytes(snes_to_pc(0x1F8000 + room_id * 3), int24_as_bytes(room_start_address))
            door_start, bytes_written = room.write_to_rom(snes_to_pc(room_start_address), rom)
            rom.write_bytes(snes_to_pc(0x1F83C0 + room_id * 3), int24_as_bytes(room_start_address + door_start))
            room_start_address += bytes_written
            if room_start_address > 0x380000:
                raise Exception('Room list exceeded bank size')
        #  size notes: bank 03 uses 140E bytes
        # bank 0A uses 372A bytes
        # bank 1F uses 77CE bytes: total is about a bank and a half
        # probably should reuse bank 1F if writing all the rooms out
        for sheet in self.sprite_sheets.values():
            sheet.write_to_rom(rom, snes_to_pc(0x00DB97))  # bank 00, SheetsTable_AA3
        if self.uw_enemy_table.size() > 0x2800:
            raise Exception('Sprite table is too big for current area')
        self.uw_enemy_table.write_sprite_data_to_rom(rom)
        for area_id, sheet_number in self.overworld_sprite_sheets.items():
            if area_id in [0x80, 0x81]:
                offset = area_id - 0x80  # 02E575 for special areas?
                rom.write_byte(snes_to_pc(0x02E576+offset), sheet_number)
            else:
                offset = convert_area_id_to_offset(area_id)
                rom.write_byte(snes_to_pc(0x00FA81+offset), sheet_number)
            # _00FA81 is LW normal
            # _00FAC1 is LW post-aga
            # _00FB01 is DW
        for area, sprite_list in vanilla_sprites_ow.items():
            for sprite in sprite_list:
                rom.write_bytes(snes_to_pc(sprite.original_address), sprite.sprite_data_ow())


def init_data_tables(world, player):
    data_tables = DataTables()
    data_tables.room_headers = init_room_headers()
    data_tables.room_list = {}
    if world.pottery[player] not in ['none']:
        data_tables.room_list[0x0127] = Room0127
    data_tables.sprite_requirements = init_sprite_requirements()
    data_tables.sprite_sheets = init_sprite_sheets(data_tables.sprite_requirements)
    init_vanilla_sprites()
    data_tables.enemy_stats = init_enemy_stats()
    uw_table = data_tables.uw_enemy_table = EnemyTable()
    for room, sprite_list in vanilla_sprites.items():
        for sprite in sprite_list:
            uw_table.room_map[room].append(sprite.copy())
    data_tables.overworld_sprite_sheets = {}
    data_tables.ow_enemy_table = defaultdict(list)
    init_vanilla_sprites_ow()
    for area, sprite_list in vanilla_sprites_ow.items():
        for sprite in sprite_list:
            data_tables.ow_enemy_table[area].append(sprite.copy())
    return data_tables
