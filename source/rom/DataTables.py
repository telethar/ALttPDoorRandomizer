from Utils import snes_to_pc

from source.dungeon.EnemyList import EnemyTable, init_vanilla_sprites, vanilla_sprites
from source.dungeon.RoomHeader import init_room_headers
from source.dungeon.RoomList import Room0127
from source.enemizer.SpriteSheets import init_sprite_sheets, init_sprite_requirements


class DataTables:
    def __init__(self):
        self.room_headers = None
        self.room_list = None  # todo: for boss rando
        self.sprite_sheets = None
        self.uw_enemy_table = None
        self.ow_enemy_tables = None  # todo : data migration
        self.pot_secret_table = None  # todo : migrate storage

        # associated data
        self.sprite_requirements = None

    def write_to_rom(self, rom):
        for header in self.room_headers.values():
            header.write_to_rom(rom, snes_to_pc(0x30DA00))  # new header table, bank30, tables.asm
        # room list
        for sheet in self.sprite_sheets.values():
            sheet.write_to_rom(snes_to_pc(0x00DB97))  # bank 00, SheetsTable_AA3
        if self.uw_enemy_table.size() > 0x2800:
            raise Exception('Sprite table is too big for current area')
        self.uw_enemy_table.write_sprite_data_to_rom(rom)


def init_data_tables(world, player):
    data_tables = DataTables()
    data_tables.room_headers = init_room_headers()
    data_tables.room_list = {}
    # if world.pottery[player] not in ['none']:
    #     data_tables.room_list[0x0127] = Room0127
    data_tables.sprite_requirements = init_sprite_requirements()
    data_tables.sprite_sheets = init_sprite_sheets(data_tables.sprite_requirements)
    init_vanilla_sprites()
    uw_table = data_tables.uw_enemy_table = EnemyTable()
    for room, sprite_list in vanilla_sprites.items():
        for sprite in sprite_list:
            uw_table.room_map[room].append(sprite.copy())
    return data_tables
