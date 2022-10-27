## New Features

## Pottery Lottery and Key Drop Shuffle Changes

### Pottery

New pottery option that control which pots (and large blocks) are in the locations pool:

* None: No pots are in the pool, like normal randomizer
* Key Pots: The pots that have keys are in the pool. This is about half of the old keydropshuffle option
* Cave Pots: The pots that are not found in dungeons are in the pool. (Includes the large block in Spike Cave). Does
not include key pots. 
* CaveKeys: Both non-dungeon pots and pots that used to have keys are in the pool.
* Reduced: Same as CaveKeys but also roughly a quarter of dungeon pots are added to the location pool picked at random. This is a dynamic mode so pots in the pool will be colored. Pots out of the pool will have vanilla contents.
* Clustered: Like reduced but pots are grouped by logical sets and roughly 50% of pots are chosen from those group. This is a dynamic mode like the above.
* Nonempty: All pots that had some sort of objects under them are chosen to be in the location pool. This excludes most large blocks and some pots out of dungeons. 
* Dungeon Pots: The pots that are in dungeons are in the pool. (Includes serveral large blocks) 
* Lottery: All pots and large blocks are in the pool

By default, switches remain in their vanilla location (unless you turn on the legacy option below)

CLI `--pottery <option>` from `none, keys, cave, cavekeys, reduced, clustered, nonempty, dungeon, lottery`

Note for multiworld: due to the design of the pottery lottery, only 256 items for other players can be under pots in your world.

### Colorize Pots

If the pottery mode is dynamic, this option is forced to be on (clustered and reduced). It is allowed to be on in all other pottery modes. Exceptions include "none" where no pots would be colored, and "lottery" where all pots would be. This option colors the pots differently that have been chosen to be part of the location pool. If not specified, you are expected to remember the pottery setting you chose. Note that Mystery will colorize all pots if lottery is chosen randomly.

CLI `--colorizepots`

### Shuffle key drops

Enemies that drop keys can have their drop shuffled into the pool. This is the other half of the keydropshuffle option.

CLI `--dropshuffle`

#### Legacy options

"Drop and Pot Keys" or `--keydropshuffle` is still availabe for use. This simply sets the pottery to keys and turns dropshuffle on as well to have the same behavior as the old setting.

The old "Pot Shuffle" option is still available under "Pot Shuffle (Legacy)" or `--shufflepots` and works the same by shuffling all pots on a supertile. It works with the lottery option as well to move the switches to any valid pot on the supertile regardless of the pots chosen in the pottery mode. This may increase the number of pot locations slightly depending on the mode.

#### Tracking Notes

The sram locations for pots and sprite drops are now final, please reach out for assistance or investigate the rom changes if needed.

## New Options

### Collection Rate

You can set the collection rate counter on using the "Display Collection Rate" on the Game Options tab are using the CLI option `--collection_rate`. Mystery seeds will not display the total.

### Goal: Trinity

Triforces are placed behind Ganon, on the pedestal, and on Murahdahla with 8/10 triforce pieces required. Recommend to run with 4-5 Crystal requirement for Ganon. Automatically pre-opens the pyramid.

### Boss Shuffle: Unique

At least one boss each of the prize bosses will be present guarding the prizes. GT bosses can be anything.

### MSU Resume

Turns on msu resume support. Found on "Game Options" tab, the "Adjust/Patch" tab, or use the `--msu_resume` CLI option. 

### BPS Patch

Creates a bps patch for the seed. Found on the "Generation Setup" tab called "Create BPS Patches" or `--bps`. Can turn off generating a rom using the existing "Create Patched ROM" option or `--suppress_rom`. There is an option on the Adjust/Patch tab to select a bps file to apply to the Base Rom selected on the Generation Setup tab using the Patch Rom button. Selected adjustments will be applied during patching.

## New Font

Font updated to support lowercase English. Lowercase vs. uppercase typos may exist. Note, you can use lowercase English letters on the file name.

## Customizer

Please refer to [the documentation](docs/Customizer.md) and examples of customizer [here](docs/customizer_example.yaml) and [here](docs/multi_mystery_example.yaml)
note that entrance customization is only available with experimental features turned on.

## Experimental Entrance Shuffle

To support customizer and future entrance shuffle modes (perhaps even customizable ones), the entrance shuffle algorithm has been re-written. It is currently in an unstable state, and will use the old method unless you turn experimental features on. I'm currently in the process of evaluating most modes with different combinations of settings and checking the distribution of entrances. Entrance customization is only supported with this new experimental entrance shuffle. The experimental entrance shuffle includes prototypes of Lean and Lite entrance shuffles from the OWR branch.

## Restricted Item Placement Algorithm

The "Item Sorting" option or ```--algorithm``` has been updated with new placement algorithms. Older algorithms have been removed.
 
 When referenced below, Major Items include all Y items, all A items, all equipment (swords, shields, & armor) and Heart Containers. Dungeon items are considered major if shuffled outside of dungeons. Bomb and arrows upgrades are Major if shopsanity is turned on. The arrow quiver and universal small keys are Major if retro is turned on. Triforce Pieces are Major if that is the goal, and the Bomb Bag is Major if that is enabled.
 
 Here are the current fill options:

### Balanced 

This one stays the same as before and is recommended for the most random distribution of items.

### Vanilla Fill 

This fill attempts to place all items in their vanilla locations when possible. Obviously shuffling entrances or the dungeon interiors will often prevent items from being placed in their vanilla location. If the vanilla fill is not possible, then other locations are tried in sequence preferring "major" locations (see below), then heart piece locations, then the rest except for GT locations which are preferred last. Note the PoD small key that is normally found in the dark maze in vanilla is move to Harmless Hellway due to the placement algorithm limitation.

### Major Location Restriction

This fill attempts to place major items in major locations. Major locations are where the major items are found in the vanilla game. This includes the spot next to Uncle in the Sewers, and the Boomerang chest in Hyrule Castle.

This location pool is expanded to where dungeon items are locations if those dungeon items are shuffled. The Capacity Fairy locations are included if Shopsanity is on. If retro is enabled in addition to shopsanity, then the Old Man Sword Cave and one location in each retro cave is included. Key drop locations can be included if small or big key shuffle is on. This gives a very good balance between overworld and underworld locations though the dungeons ones will be on bosses and in big chests generally. Seeds do become more linear but usually easier to figure out.

### Dungeon Restriction

The fill attempts to place all major items in dungeons. It will overflow to the overworld if there are more items than locations (e.g. Triforce hunt.) This fill does attempt to run the GT trash fill when possible. Seeds are typically very linear but tend to be more difficult.

### District Restriction
 
The world is divided up into different regions or districts. Each dungeon is its own district. The overworld consists of the following districts:

Light world:

* Kakariko (The main screen, blacksmith screen, and library/maze race screens)
* Northwest Hyrule (The lost woods and fortune teller screens all the way to the river west of the potion shop)
* Central Hyrule (Hyrule castle, Link's House, the marsh, and the haunted grove)
* Desert (From the thief to the main desert screen)
* Lake Hylia (Around the lake)
* Eastern Hyrule (The eastern wild, the potion shop, and Zora's Domain)
* Death Mountain

Dark world:

* East Dark World (The pyramid, Palace of darkness, and Catfish)
* South Dark World (The dark lake, swamp area, to the dig game)
* Northwest Dark World (Village of Outcasts, to the Dark Sanctuary and screens in between)
* The Mire
* Dark Death Mountain

These districts are chosen at random and then filled with major items. If a location is part of a chosen district, but there are no more major items to place, a single green rupee is placed in the extra to indicate that as a placeholder. All other single green rupees are changed to be a blue rupee in order to not give false positives.

In entrance shuffle, what is shuffled to the entrances is considered instead of where the interior was originally. For example, if Blind's Hut is shuffled to the Dam, then the 5 chests in Blind's Hut are part of Central Hyrule instead of Kakariko.

Note: Bombos Tablet, Lake Hylia Island, Bumper Cave Ledge, the Floating Island, Cave 45, the Graveyard Cave, Checkerboard Cave and Mimic Cave are considered part of the light world region rather than the dark world region you mirror from.

In multiworld, the districts chosen apply to all players.  

### CLI values:

```balanced, vanilla_fill, major_only, dungeon_only, district```

## New Hints

Based on the district algorithm above (whether it is enabled or not,) new hints can appear about that district or dungeon. For each district and dungeon, it is evaluated whether it contains vital items and how many. If it has not any vital item, items then it moves onto useful items. Useful items are generally safeties or convenience items: shields, mails, half magic, bottles, medallions that aren't required, etc. If it contains none of those and is an overworld district, then it checks for a couple more things. First, if dungeons are shuffled, it looks to see if any are in the district, if so, one of those dungeons is picked for the hint. Then, if connectors are shuffled, it checks to see if you can get to unique region through a connector in that district. If none of the above apply, the district or dungeon is considered completely foolish.

## Overworld Map shows Dungeon Entrances

Option to move indicators on overworld map to reference dungeon location. The non-default options include indicators for Hyrule Castle, Agahnim's Tower, and Ganon's Tower.

CLI ```--overworld_map```

#### Options

##### default

Status quo. Showing only the prize markers on the vanilla dungeon locations.

##### compass

The compass item controls whether the marker is moved to the dungeons locations. If you possess the compass but not the map, only a glowing X will be present regardless of dungeon prize type, if you only possess the map, the prizes will be shown in predicable locations at the bottom of the overworld map instead of the vanilla location. Light world dungeons on the light world map and dark world dungeons on the dark world map. If you posses both map and compass, then the prize of the dungeon and the location will be on the map.

If you do not shuffle the compass or map outside of the dungeon, the non-shuffled items are not needed to display the information. If a dungeon does not have a map or compass, it is not needed for the information. Talking to the bomb shop or Sahasrahla furnishes you with complete information as well as map information.

##### map

The map item plays double duty in this mode and only possession of the map will show both prize and location of the dungeon. If you do not shuffle maps or the dungeon does not have a map, the information will be displayed without needing to find any items.

## Restricted Dungeon Items on Bosses

You may now restrict the items that can appear on the boss, like the popular ambrosia preset does.

CLI: ```--restrict_boss_items <option>```

#### Options

##### none

As before, the boss may have any item including any dungeon item that could occur there.

##### mapcompass

~~The map and compass are logically required to defeat a boss. This prevents both of those from appearing on the dungeon boss. Note that this does affect item placement logic and the placement algorithm as maps and compasses are considered as required items to beat a boss.~~

Currently bugged, not recommended for use.

##### dungeon

Same as above but both small keys and bigs keys of the dungeon are not allowed on a boss. (Note: this does not affect universal keys as they are not dungeon-specific)

# Bug Fixes and Notes

#### StandardThrone

* Bug fixes
	* Fix HC Ledge entrances after rescuing Zelda, also includes the throne spawn point now.
* Original Release
	* Changed standard dungeon generation to always have Throne Room in hyrule castle and always have sanctuary behind it
	* S&Q/death in standard after moving the tapestry but before delivering Zelda will result in spawning at the tapestry
	* Mirror scroll will return you to Zelda's cell instead of last entrance. This reverts to normal behavior once the tapestry open trigger is reached

#### Customizer

* Fixed an issue where Interior Key Doors were missing from custom yaml output
* Updated lite/lean ER for pottery settings

* Fixed an issue with lite/lean ER not generating
* Fixed up the GUI selection of the customizer file.
* Fixed up the item_pool section to skip a lot of pool manipulations. Key items will be added (like the bow) if not detected. Extra dungeon items can be added to the pool and will be confined to the dungeon if possible (and not shuffled). If the pool isn't full, junk items are added to the pool to fill it out.

#### Main

* 1.1.1
  * Fixed a logic bug with Bumper Cave where the pots were accessible without Cape or Hookshot from the top entrance
  * Fixed a pot coloring issue with hammer peg cave