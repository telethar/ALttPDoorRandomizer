# Volatile Notes

## New Features

## Restricted Item Placement Algorithm


The "Item Sorting" option or ```--algorithm``` has been updated with new placement algorithms. Older algorithms have been removed.
 
 When referenced below, Major Items include all Y items, all A items, all equipment (swords, shields, & armor) and Heart Containers. Dungeon items are considered major if shuffled outside of dungeons. Bomb and arrows upgrades are Major if shopsanity is turned on. The arrow quiver and universal small keys are Major if retro is turned on. Triforce Pieces are Major if that is the goal, and the Bomb Bag is Major if that is enabled.
 
 Here are the current fill options:

### Balanced 

This one stays the same as before and is recommended for the most random distribution of items.

### Equitable

This one is currently under development and may not fill correctly. It is a new method that should allow item and key logic to interact. (Vanilla key placement in PoD is theoretically possible, but isn't yet.)

### Vanilla Fill 

This fill attempts to place all items in their vanilla locations when possible. Obviously shuffling entrances or the dungeon interiors will often prevent items from being placed in their vanilla location. If the vanilla fill is not possible, then other locations are tried in sequence preferring "major" locations (see below), then heart piece locations, then the rest except for GT locations which are preferred last. Note the PoD small key that is normally found in the dark maze in vanilla is move to Harmless Hellway due to the placement algorithm limitation.

### Major Location Restriction

This fill attempts to place major items in major locations. Major locations are where the major items are found in the vanilla game. This includes the spot next to Uncle in the Sewers, and the Boomerang chest in Hyrule Castle.

This location pool is expanded to where dungeon items are locations if those dungeon items are shuffled. The Capacity Fairy locations are included if Shopsanity is on. If retro is enabled in addition to shopsanity, then the Old Man Sword Cave and one location in each retro cave is included. Key drop locations can be included if small or big key shuffle is on. This gives a very good balance between overworld and underworld locations though the dungeons ones will be on bosses and in big chests generally. Seeds do become more linear but usually easier to figure out.

### Dungeon Restriction

The fill attempts to place all major items in dungeons. It will overflow to the overworld if there are more items than locations (e.g. Triforce hunt.) This fill does attempt to run the GT trash fill when possible. Seeds are typically very linear but tend to be more difficult.

### District Restriction
 
The world is divided up into different regions or districts. Each dungeon is it's own district. The overworld consists of the following districts:

Light world:

* Kakariko (The main screen, blacksmith screen, and library/maze race screens)
* Northwest Hyrule (The lost woods and fortune teller all the way to the rive west of the potion shop)
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

Bombos Table, Lake Hylia Island, Bumper Cave Ledge, the Floating Island, Cave 45, the Graveyard Cave, Checkerboard Cave and Mimic Cave are considered part of the dark world region that you mirror from to get there (except in inverted where these are only accessible in the Light World). Note that Spectacle Rock is always part of light Death Mountain.

In multiworld, the districts chosen apply to all players.  

### CLI values:

```balanced, equitable, vanilla_fill, major_only, dungeon_only, district```

## New Hints

Based on the district algorithm above (whether it is enabled or not,) new hints can appear stating that a district or dungeon is considered a "foolish" choice. The means there are no advancement items in that district (or that the district was not chosen if the district restriction is used).


### Overworld Map shows dungeon location

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

The map and compass are logically required to defeat a boss. This prevents both of those from appearing on the dungeon boss. Note that this does affect item placement logic and the placement algorithm as maps and compasses are considered as required items to beat a boss.

##### dungeon

Same as above but both small keys and bigs keys of the dungeon are not allowed on a boss. (Note: this does not affect universal keys as they are not dungeon-specific)

# Unstable Notes

## New Features

### Shuffle SFX

Shuffles a large portion of the sounds effects. Can be used with the adjuster.

CLI: ```--shuffle_sfx```
 
### Bomb Logic 

When enabling this option, you do not start with bomb capacity but rather you must find 1 of 2 bomb bags. (They are represented by the +10 capacity item.) Bomb capacity upgrades are otherwise unavailable.
 
CLI: ```--bombbag```


## Bug Fixes and Notes.

* 0.5.1.7
	* Baserom update
	* Fix for Inverted Mode: Dark Lake Hylia shop defaults to selling a blue potion
	* Fix for Ijwu's enemizer: Boss door in Thieves' Town no longer closes after the maiden hint if Blind is shuffled to Theives' Town in boss shuffle + crossed mode
	* No logic now sets the AllowAccidentalMajorGlitches flag in the rom appropriately
	* Houlihan room now exits wherever Link's House is shuffled to
	* Rom fixes from Catobat and Codemann8. Thanks!
* 0.5.1.6
	* Rules fixes for TT (Boss and Cell) can now have TT Big Key if not otherwise required (boss shuffle + crossed dungeon)
	* BUg fix for money balancing
	* Add some bomb assumptions for bosses in bombbag mode
* 0.5.1.5
	* Fix for hard pool capacity upgrades missing
	* Bonk Fairy (Light) is no longer in logic for ER Standard and is forbidden to be a connector, so rain state isn't exitable
	* Bug fix for retro + enemizer and arrows appearing under pots
	* Added bombbag and shufflelinks to settings code
	* Catobat fixes:
		* Fairy refills in spoiler
		* Subweights support in mystery
		* More defaults for mystery weights
		* Less camera jank for straight stair transitions
		* Bug with Straight stairs with vanilla doors where Link's walking animation stopped early is fixed		 
* 0.5.1.4
	* Revert quadrant glitch fix for baserom
	* Fix for inverted
* 0.5.1.3
	* Certain lobbies forbidden in standard when rupee bow is enabled
	* PoD EG disarmed when mirroring (except in nologic)
	* Fixed issue with key logic
	* Updated baserom
* 0.5.1.2
	* Allowed Blind's Cell to be shuffled anywhere if Blind is not the boss of Thieves Town
	* Remove unique annotation from a FastEnum that was causing problems
	* Updated prevent mixed_travel setting to prevent more mixed travel
	* Prevent key door loops on the same supertile where you could have spent 2 keys on one logical door
	* Promoted dynamic soft-lock prevention on "stonewalls" from experimental to be the primary prevention (Stonewalls are now never pre-opened)
	* Fix to money balancing algorithm with small item_pool, thanks Catobat
	* Many fixes and refinements to key logic and generation	
* 0.5.1.1
	* Shop hints in ER are now more generic instead of using "near X" because they aren't near that anymore
	* Added memory location for mutliworld scripts to read what item was just obtain (longer than one frame)
	* Fix for bias in boss shuffle "full"
	* Fix for certain lone big chests in keysanity (allowed you to get contents without big key)
	* Fix for pinball checking
	* Fix for multi-entrance dungeons
	* 2 fixes for big key placement logic
		* ensure big key is placed early if the validator assumes it)
		* Open big key doors appropriately when generating rules and big key is forced somewhere
	* Updated cutoff entrances for intensity 3
* 0.5.1.0
	* Large logic refactor introducing a new method of key logic 
	* Some performance optimization
	* Some outstanding bug fixes (boss shuffle "full" picks three unique bosses to be duplicated, e.g.)
* 0.5.0.3
	* Fixed a bug in retro+vanilla and big key placement
	* Fixed a problem with shops not registering in the Multiclient until you visit one
	* Fixed a bug in the Mystery code with sfx
* 0.5.0.2
	* --shuffle_sfx option added 
* 0.5.0.1
	* --bombbag option added 
* 0.5.0.0
	* Handles headered roms for enemizer (Thanks compiling)
	* Warning added for earlier version of python (Thanks compiling)
	* Minor logic issue for defeating Aga in standard (Thanks compiling)
	* Fix for boss music in non-DR modes (Thanks codemann8)

# Known Issues

* Shopsanity Issues
	* Hints for items in shops can be misleading (ER)
	* Forfeit in Multiworld not granting all shop items
* Potential keylocks in multi-entrance dungeons
* Incorrect vanilla key logic for Mire