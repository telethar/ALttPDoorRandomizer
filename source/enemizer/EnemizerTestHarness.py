from types import SimpleNamespace
from collections import Counter, defaultdict

from source.dungeon.EnemyList import enemy_names, SpriteType
from source.enemizer.Enemizer import randomize_underworld_rooms
from source.enemizer.SpriteSheets import randomize_underworld_sprite_sheets
from source.rom.DataTables import init_data_tables
import RaceRandom as random

if __name__ == '__main__':
    random.seed(42)

    stats = defaultdict(Counter)
    column_headers = {}

    for trial in range(0, 100):
        world = SimpleNamespace(pottery={1: 'none'})
        data_tables = init_data_tables(world, 1)

        randomize_underworld_sprite_sheets(data_tables.sprite_sheets)
        randomize_underworld_rooms(data_tables)
        for room_id, enemy_list in data_tables.uw_enemy_table.room_map.items():
            # print(f'Room {hex(room_id)}:')
            for i, sprite in enumerate(enemy_list):
                if sprite.sub_type == SpriteType.Overlord:
                    result = f'O{hex(sprite.kind)}'
                else:
                    result = enemy_names[sprite.kind]
                if result not in column_headers:
                    column_headers[result] = None
                stats[(room_id, i)][result] += 1
    with open('result.csv', 'w') as result_file:
        result_file.write('room_id,slot,')
        result_file.write(','.join(column_headers.keys()))
        result_file.write('\n')

        for key, counter in stats.items():
            rid, slot = key
            result_file.write(f'{rid},{slot}')
            for result_item in column_headers.keys():
                result_file.write(f',{counter[result_item]}')
            result_file.write('\n')

