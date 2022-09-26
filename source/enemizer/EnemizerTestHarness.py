from source.dungeon.EnemyList import enemy_names, SpriteType
from source.enemizer.Enemizer import randomize_underworld_rooms
from source.enemizer.SpriteSheets import randomize_underworld_sprite_sheets
from source.rom.DataTables import init_data_tables
import RaceRandom as random

if __name__ == '__main__':
    random.seed(42)
    data_tables = init_data_tables(None, None)

    randomize_underworld_sprite_sheets(data_tables.sprite_sheets)
    randomize_underworld_rooms(data_tables)
    for room_id, enemy_list in data_tables.uw_enemy_table.room_map.items():
        print(f'Room {hex(room_id)}:')
        for i, sprite in enumerate(enemy_list):
            if sprite.sub_type == SpriteType.Overlord:
                print(f'  Overlord #{i+1} {hex(sprite.kind)}:')
            else:
                print(f'  Enemy #{i+1} {enemy_names[sprite.kind]}:')
