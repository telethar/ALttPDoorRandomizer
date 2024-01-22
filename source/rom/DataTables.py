from collections import defaultdict

from Utils import snes_to_pc, int24_as_bytes, int16_as_bytes, load_cached_yaml

from source.dungeon.EnemyList import EnemyTable, init_vanilla_sprites, vanilla_sprites, init_enemy_stats, EnemySprite
from source.dungeon.EnemyList import sprite_translation
from source.dungeon.RoomHeader import init_room_headers
from source.dungeon.RoomList import Room0127
from source.enemizer.OwEnemyList import init_vanilla_sprites_ow, vanilla_sprites_ow
from source.enemizer.SpriteSheets import init_sprite_sheets, init_sprite_requirements, SheetChoice


def convert_area_id_to_offset(area_id):
    if area_id < 0x40:
        return area_id
    if 0x40 <= area_id < 0x80:
        return area_id + 0x40
    if 0x90 <= area_id <= 0xCF:
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
        self.room_requirements = None
        self.enemy_stats = None
        self.enemy_damage = None
        self.bush_sprite_table = {}

        # enemizer conditions
        self.uw_enemy_denials = {}
        self.ow_enemy_denials = {}
        self.uw_enemy_drop_denials = {}
        self.sheet_choices = []
        denial_data = load_cached_yaml(['source', 'enemizer', 'enemy_deny.yaml'])
        for denial in denial_data['UwGeneralDeny']:
            self.uw_enemy_denials[denial[0], denial[1]] = {sprite_translation[x] for x in denial[2]}
        for denial in denial_data['OwGeneralDeny']:
            self.ow_enemy_denials[denial[0], denial[1]] = {sprite_translation[x] for x in denial[2]}
        for denial in denial_data['UwEnemyDrop']:
            self.uw_enemy_drop_denials[denial[0], denial[1]] = {sprite_translation[x] for x in denial[2]}
        weights = load_cached_yaml(['source', 'enemizer', 'enemy_weight.yaml'])
        self.uw_weights = {sprite_translation[k]: v for k, v in weights['UW'].items()}
        self.ow_weights = {sprite_translation[k]: v for k, v in weights['OW'].items()}
        sheet_weights = load_cached_yaml(['source', 'enemizer', 'sheet_weight.yaml'])
        for item in sheet_weights['SheetChoices']:
            choice = SheetChoice(tuple(item['slots']), item['assignments'], item['weight'])
            self.sheet_choices.append(choice)

    def write_to_rom(self, rom, colorize_pots=False, increase_bush_sprite_chance=False):
        if self.pot_secret_table.size() > 0x11c0:
            raise Exception('Pot table is too big for current area')
        self.pot_secret_table.write_pot_data_to_rom(rom, colorize_pots, self)
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
        self.uw_enemy_table.check_special_bitmasks_size()
        self.uw_enemy_table.write_special_bitmask_table(rom)
        for area_id, sheet in self.overworld_sprite_sheets.items():
            if area_id in [0x80, 0x81]:
                offset = area_id - 0x80  # 02E575 for special areas?
                rom.write_byte(snes_to_pc(0x02E576+offset), sheet.id)
            else:
                offset = convert_area_id_to_offset(area_id)
                rom.write_byte(snes_to_pc(0x00FA81+offset), sheet.id)
            # _00FA81 is LW normal
            # _00FAC1 is LW post-aga
            # _00FB01 is DW
        for area, sprite_list in self.ow_enemy_table.items():
            for sprite in sprite_list:
                rom.write_bytes(snes_to_pc(sprite.original_address), sprite.sprite_data_ow())
        for sprite, stats in self.enemy_stats.items():
            # write health to rom
            if stats.health is not None:
                if isinstance(stats.health, tuple):
                    if sprite == EnemySprite.Octorok4Way:  # skip this one
                        continue
                    if sprite in special_health_table:
                        a1, a2 = special_health_table[sprite]
                        rom.write_byte(snes_to_pc(a1), stats.health[0])
                        rom.write_byte(snes_to_pc(a2), stats.health[1])
                else:
                    rom.write_byte(snes_to_pc(0x0DB173+int(sprite)), stats.health)
            # write damage class to rom
            if stats.damage is not None:
                if isinstance(stats.damage, tuple):
                    if sprite == EnemySprite.Octorok4Way:  # skip this one
                        continue
                    if sprite in special_damage_table:
                        a1, a2 = special_damage_table[sprite]
                        rom.write_byte(snes_to_pc(a1), stats.dmask | stats.damage[0])
                        rom.write_byte(snes_to_pc(a2), stats.dmask | stats.damage[1])
                else:
                    rom.write_byte(snes_to_pc(0x0DB266+int(sprite)), stats.dmask | stats.damage)
        # write damage table to rom
        for idx, damage_list in self.enemy_damage.items():
            rom.write_bytes(snes_to_pc(0x06F42D + idx * 3), damage_list)
        # write bush spawns to rom:
        for area_id, bush_sprite in self.bush_sprite_table.items():
            rom.write_byte(snes_to_pc(0x368120 + area_id), bush_sprite.sprite)
        if increase_bush_sprite_chance:
            rom.write_bytes(snes_to_pc(0x1AFBBB), [
                0x01, 0x0F, 0x0F, 0x0F, 0x0F, 0x0F, 0x0F, 0x12,
                0x0F, 0x01, 0x0F, 0x0F, 0x11, 0x0F, 0x0F, 0x03
            ])


special_health_table = {
    EnemySprite.Octorok: (0x068F76, 0x068F77),
    EnemySprite.HardhatBeetle: (0x06911F, 0x069120),
    EnemySprite.Tektite: (0x068D97, 0x068D98),
    EnemySprite.CricketRat: (0x068876, 0x068877),
    EnemySprite.Keese: (0x06888A, 0x06888B),
    EnemySprite.Snake: (0x0688A6, 0x0688A7),
    EnemySprite.Raven: (0x068965, 0x068966)
}

special_damage_table = {
    EnemySprite.Octorok: (0x068F74, 0x068F75),
    EnemySprite.Tektite: (0x068D99, 0x068D9A),
    EnemySprite.CricketRat: (0x068874, 0x068875),
    EnemySprite.Keese: (0x068888, 0x068889),
    EnemySprite.Snake: (0x0688A4, 0x0688A5),
    EnemySprite.Raven: (0x068963, 0x068964)
}


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
    data_tables.enemy_damage = {k: list(v) for k, v in world.damage_table[player].enemy_damage.items()}
    # todo: more denials based on enemy drops
    return data_tables


def get_uw_enemy_table():
    init_vanilla_sprites()
    uw_table = EnemyTable()
    for room, sprite_list in vanilla_sprites.items():
        for sprite in sprite_list:
            uw_table.room_map[room].append(sprite.copy())
    return uw_table

