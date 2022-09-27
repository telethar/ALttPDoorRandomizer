from Utils import snes_to_pc, int24_as_bytes, int16_as_bytes

from source.dungeon.EnemyList import EnemyTable, init_vanilla_sprites, vanilla_sprites
from source.dungeon.RoomHeader import init_room_headers
from source.dungeon.RoomList import Room0127
from source.enemizer.SpriteSheets import init_sprite_sheets, init_sprite_requirements


class DataTables:
    def __init__(self):
        self.room_headers = None
        self.room_list = None
        self.sprite_sheets = None
        self.uw_enemy_table = None
        self.ow_enemy_table = None  # todo : data migration
        self.pot_secret_table = None

        # associated data
        self.sprite_requirements = None

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
            rom.write_bytes(0x1F8000 + room_id * 3, int24_as_bytes(room_start_address))
            door_start, bytes_written = room.write_to_rom(snes_to_pc(room_start_address), rom)
            rom.write_bytes(0x1F83C0 + room_id * 3, int24_as_bytes(room_start_address + door_start))
            room_start_address += bytes_written
            # todo: room data doors pointers at 1F83C0
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
        # todo: write ow enemy table


def init_data_tables(world, player):
    data_tables = DataTables()
    data_tables.room_headers = init_room_headers()
    data_tables.room_list = {}
    if world.pottery[player] not in ['none']:
        data_tables.room_list[0x0127] = Room0127
    data_tables.sprite_requirements = init_sprite_requirements()
    data_tables.sprite_sheets = init_sprite_sheets(data_tables.sprite_requirements)
    init_vanilla_sprites()
    uw_table = data_tables.uw_enemy_table = EnemyTable()
    for room, sprite_list in vanilla_sprites.items():
        for sprite in sprite_list:
            uw_table.room_map[room].append(sprite.copy())
    return data_tables
