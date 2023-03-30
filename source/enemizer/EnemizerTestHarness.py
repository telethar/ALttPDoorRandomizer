from types import SimpleNamespace
from collections import Counter, defaultdict

from source.dungeon.EnemyList import enemy_names, SpriteType
from source.enemizer.Enemizer import randomize_underworld_rooms
from source.enemizer.SpriteSheets import randomize_underworld_sprite_sheets, randomize_overworld_sprite_sheets
from source.rom.DataTables import init_data_tables
from source.enemizer.DamageTables import DamageTable
import RaceRandom as random


def calculate_odds():
    ctr_uw = Counter()
    ctr_ow = Counter()
    for trial in range(0, 100):
        world = SimpleNamespace(pottery={1: 'none'}, damage_table={1: DamageTable()})
        data_tables = init_data_tables(world, 1)

        randomize_underworld_sprite_sheets(data_tables.sprite_sheets, data_tables)
        randomize_overworld_sprite_sheets(data_tables.sprite_sheets)

        for num in range(65, 124):
            sheet = data_tables.sprite_sheets[num]
            ret = []
            for req in data_tables.sprite_requirements.values():
                if not isinstance(req, dict) and sheet.valid_sprite(req) and not req.overlord and not req.static:
                    ret.append(enemy_names[req.sprite])
            for x in ret:
                ctr_uw[x] += 1

        for num in range(1, 64):
            sheet = data_tables.sprite_sheets[num]
            ret = []
            for req in data_tables.sprite_requirements.values():
                if not isinstance(req, dict) and sheet.valid_sprite(req) and not req.overlord and not req.static:
                    ret.append(enemy_names[req.sprite])
            for x in ret:
                ctr_ow[x] += 1
    ttl = sum(ctr_uw.values())
    print(f'UW:  # Total {ttl}')
    for k, v in ctr_uw.items():
        weight = round(.01 * ttl * 100 / v)
        print(f'  {k}: {weight}   # {v*100/ttl:.5f}% raw:{v}')
    ttl = sum(ctr_ow.values())
    print(f'OW:  # Total {ttl}')
    for k, v in ctr_ow.items():
        weight = round(.01 * ttl * 100 / v)
        print(f'  {k}: {weight}  # {v*100/ttl:.5f}% raw:{v}')


if __name__ == '__main__':
    calculate_odds()
    # random.seed(42)
    #
    # stats = defaultdict(Counter)
    # column_headers = {}
    #
    # for trial in range(0, 100):
    #     world = SimpleNamespace(pottery={1: 'none'})
    #     data_tables = init_data_tables(world, 1)
    #
    #     randomize_underworld_sprite_sheets(data_tables.sprite_sheets)
    #     randomize_underworld_rooms(data_tables)
    #     for room_id, enemy_list in data_tables.uw_enemy_table.room_map.items():
    #         # print(f'Room {hex(room_id)}:')
    #         for i, sprite in enumerate(enemy_list):
    #             if sprite.sub_type == SpriteType.Overlord:
    #                 result = f'O{hex(sprite.kind)}'
    #             else:
    #                 result = enemy_names[sprite.kind]
    #             if result not in column_headers:
    #                 column_headers[result] = None
    #             stats[(room_id, i)][result] += 1
    # with open('result.csv', 'w') as result_file:
    #     result_file.write('room_id,slot,')
    #     result_file.write(','.join(column_headers.keys()))
    #     result_file.write('\n')
    #
    #     for key, counter in stats.items():
    #         rid, slot = key
    #         result_file.write(f'{rid},{slot}')
    #         for result_item in column_headers.keys():
    #             result_file.write(f',{counter[result_item]}')
    #         result_file.write('\n')

