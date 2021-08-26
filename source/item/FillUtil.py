from collections import defaultdict

from Dungeons import dungeon_table

class ItemPoolConfig(object):

    def __init__(self):
        self.reserved_locations = defaultdict(set)


def create_item_pool_config(world):
    world.item_pool_config = config = ItemPoolConfig()
    player_set = set()
    for player in range(1, world.players+1):
        if world.restrict_boss_items[player] != 'none':
            player_set.add(player)
        if world.restrict_boss_items[player] == 'dungeon':
            for dungeon, info in dungeon_table.items():
                if info.prize:
                    d_name = "Thieves' Town" if dungeon.startswith('Thieves') else dungeon
                    config.reserved_locations[player].add(f'{d_name} - Boss')
    for dungeon in world.dungeons:
        for item in dungeon.all_items:
            if item.map or item.compass:
                item.advancement = True
