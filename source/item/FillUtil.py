from collections import defaultdict

from Dungeons import dungeon_prize

class ItemPoolConfig(object):

    def __init__(self):
        self.reserved_locations = defaultdict(set)


def create_item_pool_config(world):
    config = ItemPoolConfig()
    if world.algorithm in ['balanced']:
        for player in range(1, world.players+1):
            if world.restrict_boss_items[player]:
                for dungeon in dungeon_prize:
                    if dungeon.startswith('Thieves'):
                        dungeon = "Thieves' Town"
                    config.reserved_locations[player].add(f'{dungeon} - Boss')
    world.item_pool_config = config
