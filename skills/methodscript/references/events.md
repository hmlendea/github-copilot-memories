# MethodScript Event Reference

Extracted from the official MethodScript 3.3.5 Event API documentation (`https://methodscript.com/docs/3.3.5/Event_API.html`). Each entry gives the bound event name, a behaviour summary, the prefilter fields usable as `bind_event` conditions, the event data keys, and the mutable fields.

## BlockEvents

### block_break

- Behaviour: This event is called when a block is broken. Cancelling the event cancels the breakage.
- Prefilters: player: <String Match>; block: <String Match>
- Event data: player: The player's name; block: the block type that was broken; location: the locationArray of this block; drops; xp
- Mutable: drops: an array of arrays of items the block will drop; xp: the xp that this block will drop, if any

### block_burn

- Behaviour: This event is called when a block is burned away.
- Prefilters: block: <String Match>
- Event data: block: the block type that was burned; location: the location array of the burned block; firelocation: the location array of the fire (or null)

### block_dispense

- Behaviour: This event is called when a block dispenses an item.
- Prefilters: type: <String Match> Type of dispensing block; itemname: <String Match> Item type to be dispensed
- Event data: type; item: Item array of item to be dispensed. If the item type exists in the dispenser, one will be removed from the block's inventory. (ignores item quantity); velocity: Returns an associative array with the x/y/z/magnitude components of item velocity.; location: Location array of dispensing block
- Mutable: item; velocity

### block_explode

- Behaviour: Called when a block explodes (like beds in the nether) or a plugin creates an explosion.
- Event data: location: The location of the explosion.; blocks: An array of block locations that will be destroyed by this explosion.; yield: Decimal percentage of blocks destroyed that will drop items.
- Mutable: blocks; yield

### block_fade

- Behaviour: Called when a block fades, melts or disappears based on world conditions.
- Prefilters: block: <String Match> Block type that is fading; world: <String Match>
- Event data: block: The block type that is fading; newblock: The block type after the fades; location: the location of the block that will fade

### block_form

- Behaviour: Called when a block is formed or spreads based on world conditions. Cancelling this event will cause the block to not be formed.
- Prefilters: newblock: <String Match> Type of new block state
- Event data: location: The location of the formed block; block: Type of old block state; newblock: Type of new block state

### block_from_to

- Behaviour: This event is called when a water or lava is flowed and ender dragon egg is teleported. Cancelling the event cancels the flow or teleport.
- Prefilters: block: <String Match>; world: <String Match>; toblock: <String Match>; toworld: <String Match>; face: <String Match>
- Event data: block: the source block type; location: the locationArray of the source block; toblock: the target block type; tolocation: the target block's locationArray
- Mutable: block; toblock

### block_grow

- Behaviour: This event is called when a block grows naturally. If the event is cancelled, the block will not grow.
- Prefilters: block: <String Match> The block name before the growth; newblock: <String Match> The block name after the growth; world: <Macro>
- Event data: block: The block type before the growth; newblock: The block type after the growth; location: the location of the block that will grow

### block_ignite

- Behaviour: This event is called when a block ignited by a block or entity.
- Prefilters: player: <Macro>; cause: <Macro>; world: <String Match>
- Event data: player: The player's name; ignitingentity: entity ID, if caused by entity; ignitingblock: the block's type, if caused by block; ignitingblocklocation: the block's location that ignited; location: the locationArray that got ignited; cause: the cause of ignition, one of LAVA, FLINT_AND_STEEL, SPREAD, LIGHTNING, FIREBALL, ENDER_CRYSTAL, EXPLOSION, ARROW

### block_place

- Behaviour: This event is called when a player places a block. Cancelling the event cancels placing the block.
- Prefilters: player: <String Match>; block: <String Match>
- Event data: player: The player's name; block: the block type that was placed; against: a block array of the block being placed against; oldblock: the old block type that was replaced; location: A locationArray for this block; item: the item used to the place the block; hand: hand used to place the block
- Mutable: block

### note_play

- Behaviour: This event is called when a noteblock is activated via player interaction or redstone. The instrument may be one of PIANO, BASS_DRUM, SNARE_DRUM, STICKS, BASS_GUITAR, FLUTE, BELL, GUITAR, CHIME, XYLOPHONE, IRON_XYLOPHONE...
- Event data: location: The location of the noteblock; instrument: The name of the sound; tone: The note played (eg. F#); octave: The octave the tone was played (0 - 2)

### piston_extend

- Behaviour: This event is called when a piston is extended. Cancelling the event cancels the move.
- Event data: location: the locationArray of this piston; direction: direction of travel; sticky: true if the piston is sticky, false otherwise; affectedBlocks: blocks pushed/pulled

### piston_retract

- Behaviour: This event is called when a piston is retracted. Cancelling the event cancels the move.
- Event data: location: the locationArray of this piston; direction: direction of travel; sticky: true if the piston is sticky, false otherwise; affectedBlocks: blocks pushed/pulled

### sign_changed

- Behaviour: This event is called when a player changes a sign. Cancelling the event cancels any edits completely.
- Prefilters: player: <String Match>; 1: <Regex>; 2: <Regex>; 3: <Regex>; 4: <Regex>
- Event data: player: The player's name; location: A location array of the sign; text: An array with keys 0 thru 3 defining every line on the sign; side: The side of the sign the text was changed, FRONT or BACK
- Mutable: 1; 2; 3; 4; text: An array with keys 0 thru 3 defining every line on the sign

## CmdlineEvents

### cmdline_prompt_input

- Behaviour: Fired when a command is issued from the interactive prompt. If the event is not cancelled, the interpreter will handle it as normal. Otherwise, the event can be cancelled, and custom handling can be triggered.
- Event data: command: The command that was triggered; shellMode: If the shell is in shell mode (activated with $$)

### shutdown

- Behaviour: Fired the process is being shut down. This is not guaranteed to run, because some cases may cause the process to die unexpectedly.

## EntityEvents

### creature_spawn

- Behaviour: Fired when a living entity spawns on the server.
- Prefilters: type: <Macro>; reason: <Macro> One of BEEHIVE, BREEDING, BUCKET, BUILD_COPPERGOLEM, BUILD_IRONGOLEM, BUILD_SNOWMAN, BUILD_WITHER, COMMAND, CUSTOM, DEFAULT, EGG, JOCKEY, LIGHTNING, NATURAL, PATROL, PIGLIN_ZOMBIFIED, RAID, REINFORCEMENTS, SHOULDER_ENTITY, SLIME_SPLIT, SPAWNER, SPAWNER_EGG, VILLAGE_DEFENSE, VILLAGE_INVASION, NETHER_PORTAL, DISPENSE_EGG, INFECTION, CURED, OCELOT_BABY, SILVERFISH_BLOCK, MOUNT, TRAP, ENDER_PEARL, DROWNED, SHEARED, EXPLOSION, FROZEN, SPELL, METAMORPHOSIS, DUPLICATION, ENCHANTMENT, TRIAL_SPAWNER, POTION_EFFECT, REHYDRATION (Paper), REANIMATE
- Event data: type: the type of creature spawning; id: the entityID of the creature; reason: the reason this creature is spawning; location: locationArray of the event
- Mutable: type: Spawn a different entity instead. This will fire a new event. If the entity type is living, it will fire creature_spawn event with a reason of 'CUSTOM'.

### entity_change_block

- Behaviour: Fires when an entity change block in some way.
- Prefilters: from: <String Match> the block name before the change; to: <String Match> the block name after change; location: <Location Match> the location of the block changed
- Event data: entity: the entity ID of the entity which changed block; from; to; location: the location of the block changed

### entity_damage

- Behaviour: Fires when any loaded entity takes damage.
- Prefilters: id: <Macro> The entityID; type: <Macro> The type of entity being damaged; cause: <Macro> One of CONTACT, ENTITY_ATTACK, PROJECTILE, SUFFOCATION, FALL, FIRE, FIRE_TICK, LAVA, DROWNING, BLOCK_EXPLOSION, ENTITY_EXPLOSION, VOID, LIGHTNING, SUICIDE, STARVATION, POISON, MAGIC, MELTING, WITHER, FALLING_BLOCK, THORNS, DRAGON_BREATH, FLY_INTO_WALL, HOT_FLOOR, CAMPFIRE, CRAMMING, ENTITY_SWEEP_ATTACK, DRYOUT, FREEZE, SONIC_BOOM, KILL, WORLD_BORDER, or CUSTOM; world: <String Match>
- Event data: type: The type of entity the got damaged; id: The entityID of the victim; player: the player who got damaged (only present if type is PLAYER); world; location; cause: The type of damage; amount; finalamount: health entity will lose after modifiers; damager: If the source of damage is a player this will contain their name, otherwise it will be the entityID of the damager (only available when an entity causes damage); damagertype: The type of entity that caused the damage, if there's a damager.; shooter: The name of the player who shot, otherwise the entityID (only available when damager is a projectile)
- Mutable: amount: raw amount of damage (in half hearts)

### entity_damage_player

- Behaviour: This event is called when a player is damaged by another entity.
- Prefilters: player: <String Match>; id: <Macro>; damager: <Macro>
- Event data: player: The player being damaged; damager: The type of entity causing damage; amount: raw amount of damage caused; finalamount: health player will lose after modifiers; cause: the cause of damage; data: the attacking player's name or the shooter if damager is a projectile; id: The entity UUID of the damager; location
- Mutable: amount

### entity_death

- Behaviour: Fires when any living entity dies.
- Prefilters: id: <Macro> The entityID; type: <Macro> The type of entity dying.
- Event data: type; id: The entityID; drops: an array of item arrays of each stack; xp; cause: the last entity_damage object for this entity; location: where the entity was when it died
- Mutable: drops: an array of item arrays of what will be dropped, replaces the normal drops, can be null; xp: the amount of xp to drop

### entity_enter_portal

- Behaviour: Fires when an entity touches a portal block.
- Prefilters: type: <Macro> the type of entity; portaltype: <String Match> The type of portal (PORTAL or END_PORTAL); world: <Macro> the world in which the portal was entered
- Event data: id: the entityID of the entity; location: the location of the block touched; type; portaltype

### entity_explode

- Behaviour: Fires when an explosion occurs. Cancelling this event only protects blocks. Entities are handled in damage events.
- Prefilters: id: <Macro> The entity UUID; type: <Macro> The type of entity exploding
- Event data: id; type; location: Where the explosion occurs; blocks; yield
- Mutable: blocks: An array of blocks destroyed by the explosion.; yield: Percent of the blocks destroyed that should drop items. A value greater than 100 will cause more drops than the original blocks.

### entity_interact

- Behaviour: Fires when a non-player entity physically interacts with and triggers a block. (eg. pressure plates, redstone ore, farmland, tripwire, doors, and wooden button)
- Prefilters: type: <String Match> the entity type; block: <String Match> The block name the entity is interacting with.
- Event data: entity: the ID of the entity that interacted with the block; block; location: the location of the interaction

### entity_portal_travel

- Behaviour: Fired when an entity travels through a portal.
- Prefilters: type: <Macro>
- Event data: id: The UUID of entity; type: The type of entity; from: The location the entity is coming from; to: The location the entity is going to. Returns null when using nether portal and "allow-nether" in server.properties is set to false or when using end portal and "allow-end" in bukkit.yml is set to false.; searchradius: The search radius for finding an available portal.
- Mutable: to; searchradius

### entity_potion

- Behaviour: Called when a potion effect is modified on an entity. If the event is cancelled, no change will be made on the entity.
- Prefilters: action: <String Match> The action which will be performed on the potion effect type; cause: <String Match> The cause why the effect has changed
- Event data: action: The action which will be performed on the potion effect type; cause: The cause why the effect has changed; newPotion: The new potion effect of the changed type which will be applied; oldPotion: The old potion effect of the changed type, which will be removed; id: UUID entity

### entity_regain_health

- Behaviour: Fired when an entity regained the health.
- Prefilters: reason: <Macro>
- Event data: id: The entity ID of regained entity; amount: The amount of regained the health; cause: The cause of regain, one of REGEN, SATIATED, EATING, ENDER_CRYSTAL, MAGIC, MAGIC_REGEN, WITHER_SPAWN, WITHER, CUSTOM; player: The regained player
- Mutable: amount

### entity_toggle_glide

- Behaviour: This event is called when an entity toggles it's gliding state (Using Elytra).
- Prefilters: type: <Macro> The entity type of the entity; id: <Macro> The entity id of the entity; player: <Macro> The player triggering the event
- Event data: id: The entityID of the entity; type: The entity type of the entity; gliding: true if the entity is entering gliding mode, false if the entity is leaving it; player: If the entity is a player, this will contain their name, otherwise null

### entity_toggle_swim

- Behaviour: This event is called when an entity's swimming status is toggled
- Prefilters: type: <String IC Match> The entity type of the entity that toggled swimming; id: <String IC Match> The ID of the entity that toggled swimming; player: <Player Match> The player that toggled swimming
- Event data: id: The entityID of the entity; type: The entity type of the entity; swimming: true if the entity is entering swimming mode, false if the entity is leaving it; player: If the entity is a player, this will contain their name, otherwise null

### entity_unleash

- Behaviour: This event is called when a leash is broken.
- Prefilters: type: <Macro>; reason: <Macro>
- Event data: id: The entityID of the entity; type: The entity type of the entity; reason: The reason the leash broke. Can be one of HOLDER_GONE, PLAYER_UNLEASH, DISTANCE, LEASHED_GONE (Paper-only 26.1.2+), SHEAR (Spigot-only 1.21.6+), FIREWORK (Spigot-only 1.21.6+), UNKNOWN

### firework_explode

- Behaviour: Fires when a firework rocket explodes.
- Event data: id: The entityID of the firework rocket; location: Where the firework rocket is exploding

### hanging_break

- Behaviour: This event is called when a hanged entity is broken.
- Prefilters: type: <Macro> The entity type of the hanging entity; cause: <Macro> The cause of the removing; world: <Macro>
- Event data: id: The entityID of the hanging entity; type: The entity type of the hanging entity, can be ITEM_FRAME, PAINTING or LEASH_HITCH; cause: The cause of the removing, can be DEFAULT, ENTITY, EXPLOSION, OBSTRUCTION, or PHYSICS; location: Where was the hanging entity before the removing; remover: If the hanging entity has been removed by an other entity, this will contain its entityID, otherwise null; player: If the hanging entity has been removed by a player, this will contain their name, otherwise null

### hanging_place

- Behaviour: This event is called when a player attempts to place an item frame, painting, or leash.
- Prefilters: type: <Macro> The type of hanging entity; player: <Macro> The player placing the entity; world: <Macro> The world the entity is in
- Event data: id: The UUID of the hanging entity.; type: The type of the hanging entity (ITEM_FRAME, GLOW_ITEM_FRAME, PAINTING, or LEASE_HITCH); location: Where the entity was placed.; against: The location array of the block the hanging is being placed on.; face: The face of the block the hanging is being placed.; player: The name of the player placing the entity, or null.; item: The item array of the hanging being placed, or null. (MC 1.17.1+); hand: The hand used to place the item, or null. Can be main_hand or off_hand. (MC 1.19.2+)

### item_despawn

- Behaviour: Fires when an item entity is removed from the world because it has existed for 5 minutes. Cancelling the event will allow the item to exist for 5 more minutes.
- Prefilters: itemname: <String Match> the type of item that despawned
- Event data: location: where the item is; id: the item's entityID; item: the itemstack of the entity

### item_drop

- Behaviour: This event is called when a player drops an item.
- Prefilters: player: <Macro>; itemname: <String Match>
- Event data: player: The player; id: The item's entityID; item: An item array representing the item being dropped.
- Mutable: item: setting this to null removes the dropped item

### item_pickup

- Behaviour: This event is called when a player picks up an item.
- Prefilters: player: <Macro>; itemname: <String Match>
- Event data: player: The player; item: An item array representing the item being picked up; remaining: Other items left on the ground.
- Mutable: item: setting this to null will remove the item from the world

### item_spawn

- Behaviour: Fires when an item entity comes into existence.
- Prefilters: itemname: <String Match> the type of item that spawned
- Event data: location: Where the item spawns; id: The item's entityID; item: An item array representing the item being spawned.
- Mutable: item: the itemstack of the entity

### player_interact_at_entity

- Behaviour: Fires when a player right clicks an entity. This event is like player_interact_entity but also has the click position. On versions prior to MC 26.1, cancelling this event only cancels interactions with Armor Stand entiti...
- Prefilters: clicked: <Macro> the type of entity being clicked; hand: <String Match> The hand the player clicked with, can be either main_hand or off_hand; x: <Expression> offset of clicked location from entity location on the x axis; y: <Expression>; z: <Expression>
- Event data: player: the player clicking; clicked; hand; id: the id of the entity; data: if a player is clicked, this will contain their name; position: offset of clicked location from entity location in an xyz array.

### player_interact_entity

- Behaviour: Fires when a player right clicks an entity. Note, not all entities are clickable. Interactions with Armor Stands do not trigger this event for clients before MC 26.1.
- Prefilters: clicked: <Macro> the type of entity being clicked; hand: <String Match> The hand the player clicked with, can be either main_hand or off_hand
- Event data: player: the player clicking; clicked; hand; id: the id of the entity; data: if a player is clicked, this will contain their name

### potion_splash

- Behaviour: Called when a splash potion lands.
- Prefilters: id: <String Match> The splash potion entity uuid.
- Event data: id; entities: An associative array of living entities affected by the splash, where the key is a UUID and the value is a double with a range of 0.0 - 1.0 for the intensity of the effect.
- Mutable: entities: Set an entity's intensity to 0 to make them unaffected.

### projectile_hit

- Behaviour: Fires when a projectile collides with something.
- Prefilters: id: <Macro> The UUID of the projectile; type: <Macro> the entity type of the projectile; hittype: <String Match> the type of object hit, either ENTITY or BLOCK
- Event data: type; id; location: the projectile's location upon impact; shooter; hittype; hit: the entity id or block location array of the hit object.; hitface: the face that was hit on the block, if a block was hit
- Mutable: shooter: the entityID of the mob/player that fired the projectile, or location array if it is from a dispenser

### projectile_launch

- Behaviour: This event is called when a projectile is launched. Cancelling the event will only cancel the launching of the projectile. For instance when a player shoots an arrow with a bow, if the event is cancelled the bow will sti...
- Prefilters: type: <Macro> The entity type of the projectile; world: <Macro>; shootertype: <Macro> The entity type of the shooter, or 'block', or 'null'
- Event data: id: The entityID of the projectile; type: The entity type of the projectile; shooter: entityID or dispenser location of the shooter (can be null for dispensers in Paper shootertype: entity type of the shooter or 'block' if a dispenser (can be null for dispensers in Paper player: the player which has launched the projectile (null if the shooter is not a player); location: from where the projectile is launched; velocity: the velocity of the projectile
- Mutable: velocity

### target_player

- Behaviour: This event is called when a player is targeted by a mob.
- Prefilters: player: <Macro>; mobtype: <Macro>; reason: <Macro>
- Event data: player: The player's name; mobtype: The type of mob targeting the player (this will be all capitals!); id: The UUID of the mob; reason: The reason the entity is targeting the player. Can be one of TARGET_DIED, CLOSEST_PLAYER, TARGET_ATTACKED_ENTITY, FORGOT_TARGET, TARGET_ATTACKED_OWNER, OWNER_ATTACKED_TARGET, RANDOM_TARGET, DEFEND_VILLAGE, TARGET_ATTACKED_NEARBY_ENTITY, REINFORCEMENT_TARGET, COLLISION, CLOSEST_ENTITY, FOLLOW_LEADER, TEMPT, CUSTOM, TARGET_OTHER_LEVEL, TARGET_INVALID, or UNKNOWN
- Mutable: player: target a different player, or null to make the mob re-look for targets

## InventoryEvents

### inventory_click

- Behaviour: Fired when a player interacts with any inventory GUI. See also inventory_drag.
- Prefilters: virtual: <Boolean Match> If the inventory is virtually held in CH; slottype: <Macro> ARMOR, CONTAINER, CRAFTING, FUEL, OUTSIDE, QUICKBAR, or RESULT; clicktype: <Macro> LEFT, SHIFT_LEFT, RIGHT, SHIFT_RIGHT, WINDOW_BORDER_LEFT, WINDOW_BORDER_RIGHT, MIDDLE, NUMBER_KEY, DOUBLE_CLICK, DROP, CONTROL_DROP, CREATIVE, SWAP_OFFHAND, or UNKNOWN; action: <Macro> NOTHING, PICKUP_ALL, PICKUP_SOME, PICKUP_HALF, PICKUP_ONE, PLACE_ALL, PLACE_SOME, PLACE_ONE, SWAP_WITH_CURSOR, DROP_ALL_CURSOR, DROP_ONE_CURSOR, DROP_ALL_SLOT, DROP_ONE_SLOT, MOVE_TO_OTHER_INVENTORY, HOTBAR_MOVE_AND_READD, HOTBAR_SWAP, CLONE_STACK, COLLECT_TO_CURSOR, PICKUP_FROM_BUNDLE, PICKUP_ALL_INTO_BUNDLE, PICKUP_SOME_INTO_BUNDLE, PLACE_FROM_BUNDLE, PLACE_ALL_INTO_BUNDLE, PLACE_SOME_INTO_BUNDLE, or UNKNOWN; slotitem: <String Match> The item type; player: <Macro>
- Event data: slottype: The type of slot being clicked; clicktype: The type of input; action: The resulting action; slotitem: The item in the clicked slot; player: The player who clicked; viewers: Every player looking at this inventory; leftclick: If left mouse click; rightclick: If right mouse click; keyboardclick: If key press; shiftclick: If shift held; creativeclick: If action could only be performed in creative mode, like clone stack.; slot: The slot number clicked. Will be -999 if the click occurred outside the window.; rawslot: The slot number clicked in the whole inventory window. This will be higher than inventorysize if the click did not occur in the open inventory.; inventorytype: The type of open inventory (if self-inventory, this will be CRAFTING); inventorysize: Number of slots in the open inventory; cursoritem: The item on the cursor; inventory: An array of all the items in the open inventory; hotbarbutton: The hotbar slot (0-8) if a number key was pressed, or -1 none.
- Mutable: slotitem: The item to put in the clicked slot; cursoritem: The item to put on the cursor

### inventory_close

- Behaviour: Fired when a player closes an inventory.
- Prefilters: virtual: <Boolean Match> Whether or not this inventory is virtually stored in CH
- Event data: player: The player; inventory: the inventory items in this inventory; inventorytype: type of inventory; virtual; holder: block location array, entity UUID, or virtual id for this inventory (can be null)

### inventory_drag

- Behaviour: Fired when a player clicks (by left or right mouse button) a slot in an inventory and then drags the mouse across slots.
- Prefilters: virtual: <Boolean Match> Whether or not this inventory is virtually stored in CH; world: <Macro> World name; type: <String Match> Can be SINGLE, or EVEN; cursoritem: <String Match> old item type held by the cursor before event starts
- Event data: player: The player who clicked; newcursoritem: item on cursor, after event; oldcursoritem: item on cursor, before event; slots: used slots; rawslots: used slots, as the numbers of the slots in whole inventory window; newitems: array of items which are dropped in selected slots; inventorytype; inventorysize: number of slots in opened inventory
- Mutable: cursoritem: the item on the cursor, after event

### inventory_open

- Behaviour: Fired when a player opens an inventory.
- Prefilters: virtual: <Boolean Match> Whether or not this inventory is virtually stored in CH
- Event data: player: The player; inventory: the inventory items in this inventory; inventorytype: type of inventory; virtual; holder: block location array, entity UUID, or virtual id for this inventory (can be null)

### item_enchant

- Behaviour: Fired when a player enchants an item.
- Event data: player: The player that enchanted the item; item: The item to be enchanted; inventorytype: type of inventory; levels: The minimum amount of levels the player required; enchants: Array of added enchantments; location: Location of the used enchantment table; option: The listed option the player clicked (0-2). Can be used to get level cost.; levelhint: The level displayed as a hint to the player (MC 1.20.1+); enchanthint: The enchantment displayed as a hint to the player (MC 1.20.1+)
- Mutable: levels: The amount of levels required; item: The item to be enchanted; enchants: The enchants to add to the item

### item_held

- Behaviour: Fires when a player changes which quickbar slot they have selected.
- Prefilters: player: <String Match>
- Event data: player; to; from: the slot the player is switching from
- Mutable: to: the slot that the player is switching to

### item_pre_anvil

- Behaviour: Fires when a slot other than the result is clicked in an anvil. Can fire multiple times per click.
- Event data: player: the player using the anvil.; first_item: the first item being used in the recipe.; second_item: the second item being used in the recipe.; result: the result of the recipe.; max_repair_cost: the maximum possible cost of this repair.; level_repair_cost: how many levels are needed to perform this repair.; item_repair_cost: how many items are needed to perform this repair (MC 1.18.1+).
- Mutable: result: the result of the recipe.; level_repair_cost: how many levels are needed to perform this repair.; item_repair_cost: how many items are needed to perform this repair (MC 1.18.1+).; max_repair_cost: the maximum possible cost of this repair. Values exceeding 40 will be respected, but may still show as too expensive on the client.

### item_pre_craft

- Behaviour: Fires when a slot is clicked in a crafting matrix. Can also fire when clearing an inventory with the the /clear command or shift-clicking the 'Destroy Item' button in creative mode.
- Event data: player: the name of the player who clicked; viewers; matrix: an array of item arrays in the crafting matrix; result; isRepair: true if this event was triggered by a repair operation; recipe: an array of data about the formed recipe, or null if there is not one
- Mutable: result: the item array product of the recipe.

### item_pre_enchant

- Behaviour: Fired when a player places an item in an enchantment table
- Event data: player: The player that placed the item; item: The item to be enchanted; inventorytype: Type of inventory; enchantmentbonus: the amount of bookshelves influencing the enchantment table; expcosts: The offered costs of the 3 options; location: Location of the used enchantment table
- Mutable: item: The item to be enchanted; expcosts: The costs of the 3 options on the enchantment table

### item_pre_grindstone

- Behaviour: Fires when a slot other than the result is clicked in a grindstone. (MC 1.19.3+) Can fire multiple times per click.
- Event data: player: the player using the grindstone.; upper_item: the first item being used in the recipe.; lower_item: the second item being used in the recipe.; result: the result of the recipe.
- Mutable: result: the result of the grindstone recipe.

### item_pre_smithing

- Behaviour: Fires when a slot other than the result is clicked in a smithing table. Can fire multiple times per click.
- Event data: player: the player using the smithing table.; first_item: the first item being used in the recipe.; second_item: the second item being used in the recipe.; third_item: the third item being used in the recipe. (MC 1.20+); recipe: information about the formed recipe, or null if there's not one.; result: the result of the recipe.
- Mutable: result: the result of the smithing table recipe. While the result will appear on the client-side, all items must be populated before a recipe can be executed.

### item_swap

- Behaviour: Fires when a player swaps the items between their main and off hands.
- Prefilters: player: <Macro>; main_hand: <String Match> The name of the item being swapped to the main hand (or AIR); off_hand: <String Match> The name of the item being swapped to the off hand (or AIR)
- Event data: player; main_hand: The item array being swapped to the main hand (or null); off_hand: The item array being swapped to the off hand (or null)
- Mutable: main_hand; off_hand

## PlayerEvents

### async_player_chat

- Behaviour: Fires when any player sends a chat message. The event handler is run on the async thread, and not the main server thread, which can lead to undefined results if your code accesses non-threadsafe methods, hence why this f...
- Prefilters: player: <Player Match> The player chatting
- Event data: message: The chat message to be sent; recipients: An array of players that will receive the chat message; format: The "printf" format string, by default "<%1$s> %2$s". The first parameter is the player's display name, and the second one is the message.
- Mutable: message; recipients: Players in this array that are not online are ignored; format: Clients that are configured to only see secure chat will not see modified messages.

### book_edited

- Behaviour: Fires when a player clicks done after modifying a book and quill or signs a book.
- Prefilters: signing: <Boolean Match> Whether or not the book is being signed; player: <Player Match> The player that edited the book
- Event data: player: The player that edited the book; slot: The inventory slot number where the book is; oldbook: The book before the editing (an array with keys title, author and pages); newbook: The book after the editing (an array with keys title, author and pages); signing: Whether or not the book is being signed
- Mutable: title; author; pages; signing

### exp_change

- Behaviour: Fires when a player's experience changes naturally.
- Prefilters: player: <Player Match> The player whose exp is changing
- Event data: player; amount
- Mutable: amount: an integer of the amount of exp that will be added to the player's total exp

### food_level_changed

- Behaviour: Fires when a player's food level changes. Cancelling the event will cause the change to not be applied.
- Prefilters: player: <String Match> The player whose food level changed
- Event data: player: the player; level: the new food level to be applied; difference: the difference between the old level and the new; item: The item array for the item that caused this change, or null if none
- Mutable: level: A different level to be applied

### gamemode_change

- Behaviour: Fires when something causes a player's gamemode to change. Cancelling the event will cancel the change. The mode itself cannot be modified.
- Prefilters: newmode: <Enum Match> gamemode being changed to, one of SURVIVAL, CREATIVE, ADVENTURE, or SPECTATOR; player: <Macro> The player changing game modes
- Event data: player: player whose mode is changing; newmode

### player_advancement_done

- Behaviour: Fires when a player completes all criteria to unlock an advancement or recipe.
- Prefilters: advancement: <Macro> The namespaced key of the advancement completed
- Event data: player; advancement; title: The advancement display title, if one exists (MC 1.17.1+ on Paper, 1.18.2+ on Spigot)

### player_bucket_empty

- Behaviour: Fired when a player empties a bucket in their hand into the world.
- Event data: player: the player who used the bucket.; location: where the bucket was emptied to.; hand: hand the player was holding the bucket in, either main_hand or off_hand (MC 1.19.2+).; item: the bucket item the player ended up with.

### player_bucket_fill

- Behaviour: Fired when a player fills a bucket in their hand from the world.
- Event data: player: the player who used the bucket.; location: where the bucket was filled from.; hand: hand the player was holding the bucket in, either main_hand or off_hand (MC 1.19.2+).; item: the bucket item the player ended up with.

### player_chat

- Behaviour: Fires when any player sends a chat message.
- Prefilters: player: <Player Match> The player chatting
- Event data: message: The message to be sent; format; recipients: An array of players that will receive the chat message
- Mutable: message: The chat message to be sent; recipients: An array of players that will receive the chat message; format: The "printf" format string, by default "<%1$s> %2$s". The first parameter is the player's display name, and the second one is the message.

### player_command

- Behaviour: Fires when a player runs a command. This fires before CommandHelper aliases.
- Prefilters: command: <String Match> The entire command string; prefix: <String Match> Just the first part of the command; player: <Player Match> The player running the command
- Event data: command: The entire command the player ran; prefix: Just the first part of the command, i.e. '/cmd' in '/cmd blah blah'
- Mutable: command

### player_consume

- Behaviour: Fires when a player is finishes eating/drinking an item. Cancelling the event will cause any effects to not be applied and the item to not be taken from the player.
- Prefilters: itemname: <Material Match> The item being consumed; player: <Player Match> The player consuming the item
- Event data: player: The player consuming the item; item: The item being consumed; hand: Either the main_hand or off_hand from which the item is consumed (MC 1.19.2+)
- Mutable: item: A different item to be consumed, changing this will cause the original item to remain in the inventory

### player_death

- Behaviour: Fires when a player dies.
- Prefilters: player: <Macro> The player that died.
- Event data: player: The player that died; drops: An array of the items that will be dropped, or null; xp: The amount of experience that will be dropped; cause: The cause of death; death_message: The death message, or null if absent; keep_inventory: If the player will keep their inventory; keep_level: If the player will keep their experience and their level; new_exp: The player's experience when they will respawn; new_level: The player's level when they will respawn; new_total_exp: The player's total experience when they will respawn; killer: The name of the killer if a player killed them, otherwise null
- Mutable: xp; drops: The items will be replaced by the given items; death_message; keep_inventory; keep_level; new_exp; new_level; new_total_exp

### player_enter_bed

- Behaviour: Fires when a player interacts with a bed.
- Prefilters: result: <Enum Match> The outcome of the attempt to enter this bed. Can be one of NOT_POSSIBLE_HERE, NOT_POSSIBLE_NOW, NOT_SAFE, OK, OTHER_PROBLEM, TOO_FAR_AWAY, OBSTRUCTED, or EXPLOSION; location: <Location Match> The location of the bed; player: <Player Match> The player interacting with the bed
- Event data: location: The location of the bed; player: The player interacting with the bed; result: The outcome of this attempt to enter bed. Can be one of NOT_POSSIBLE_HERE, NOT_POSSIBLE_NOW, NOT_SAFE, OK, OTHER_PROBLEM, TOO_FAR_AWAY, OBSTRUCTED, or EXPLOSION

### player_fish

- Behaviour: Fires when a player casts or reels a fishing rod.
- Prefilters: world: <World Match> The world the fishing happens in.; state: <Enum Match> Can be one of CAUGHT_ENTITY, CAUGHT_FISH, FAILED_ATTEMPT, FISHING, IN_GROUND, BITE, REEL_IN, or LURED.; player: <Player Match> The player who is fishing.
- Event data: player; world; state; xp; hook: the fishhook entity id; caught: the id of the snared entity, can be a fish item; hand: the hand the fishing rod is in, only when state is FISHING (MC 1.19.2+)
- Mutable: xp: the exp the player will get from catching a fish

### player_interact

- Behaviour: Fires when a player left or right clicks. Dropping items can also fire this event for the main_hand if the player is not facing a block or is in adventure mode.
- Prefilters: button: <String IC Match> "left" or "right". If they left or right clicked; block: <Material Match> The block type the player interacts with, or null if nothing; itemname: <Material Match> The item type they are holding when they interacted, or null; hand: <String IC Match> The hand the player clicked with.; player: <Player Match> The player that triggered the event
- Event data: action: Can be left_click_block, right_click_block, left_click_air, or right_click_air.; player; hand: The hand used, can be either main_hand or off_hand.; item: The item array in the hand used, or null if there is nothing in that hand.; block: The type of block clicked, or null if no block was clicked.; location: The location array of the block clicked (exists only if block clicked); facing: The face of the block clicked; position: Vector array of the position on the block that was right clicked. (exists only if block right-clicked) (MC 1.20.1+)

### player_join

- Behaviour: Fires when a player has finished login and is now joining the server and world. Cancelling the event does not prevent them from joining. See the player_login event or pkick().
- Prefilters: world: <World Match> The world the player is joining into; join_message: <Regex> The join message that displays in chat; player: <Player Match> The player joining
- Event data: player: The player joining; world; join_message: The message that displays in chat; first_login: True if this is the first time the player has logged in.
- Mutable: join_message: Setting to null will prevent any message from displaying in chat

### player_kick

- Behaviour: Fires when a player is kicked from the game.
- Prefilters: reason: <Macro> The message shown to the player getting kicked; player: <Player Match> The kicked player
- Event data: player: the kicked player; message: the message shown to all online players; reason: the message shown to the player getting kicked
- Mutable: message; reason

### player_leave_bed

- Behaviour: Fires when a player leaves a bed.
- Prefilters: location: <Location Match> The location of the bed; player: <Player Match> The player leaving the bed
- Event data: location: The location of the bed; player: The player leaving the bed

### player_login

- Behaviour: Fires when a player connects to the server and is about to join. This event cannot be cancelled. Instead, you can deny them by setting 'result' to KICK_BANNED, KICK_WHITELIST, KICK_OTHER, or KICK_FULL.
- Prefilters: player: <Player Match> The player that is connecting
- Event data: player: The player that is connecting; uuid: The player's unique id; kickmsg: The kick message the player will see if kicked; ip: the player's IP address; hostname: The hostname used to reach the server; result: the default response to their logging in
- Mutable: kickmsg; result

### player_move

- Behaviour: Fires when a player moves a certain distance, defined by the threshold prefilter, which defaults to 1 meter. Prefilters are encouraged if you have a lot of players.
- Prefilters: world: <World Match> The world the event is happening in. This is just based on the location of the from event, which can be filtered on instead.; threshold: <custom prefilter> The minimum distance the player must have travelled before the event will be triggered. This is based on the 3D distance in whole meters.; from: <Location Match> The location the player moved from.; to: <Location Match> The location the player moved to.; player: <Player Match> The player that moved. Switching worlds does not trigger this event.
- Event data: player; world; from: The location the player moved from; to: The location the player moved to

### player_portal_travel

- Behaviour: Fires when a player travels after entering a portal.
- Prefilters: type: <Enum Match> The type of portal occurring, either NETHER_PORTAL or END_PORTAL; from: <Location Match> The location where the player is coming from; to: <Location Match> The location the player is teleporting to. Returns null when using nether portal and "allow-nether" in server.properties is set to false or when using end portal and "allow-end" in bukkit.yml is set to false.; player: <Player Match> The player that entered the portal
- Event data: player: The player that entered the portal; from: The location the player is coming from; to: The location the player is teleporting to. Returns null when using nether portal and "allow-nether" in server.properties is set to false or when using end portal and "allow-end" in bukkit.yml is set to false.; type: the type of portal occurring; creationallowed: If a new portal can be created.; creationradius: Gets the maximum radius from the given location to create a portal.; searchradius: Gets the search radius for finding an available portal.
- Mutable: to; creationradius; searchradius; creationallowed

### player_quit

- Behaviour: Fires when a player disconnects.
- Prefilters: player: <Player Match> The quitting player.
- Event data: message: The message to be sent
- Mutable: message

### player_spawn

- Behaviour: Fires when a player respawns. The player may not exist in the player list during this event.
- Prefilters: world: <String Match> The world of the spawn. Deprecated in favor of location.; x: <Expression> The x location of the spawn. Deprecated in favor of location.; y: <Expression> The y location of the spawn. Deprecated in favor of location.; z: <Expression> The z location of the spawn. Deprecated in favor of location.; location: <Location Match> The location the spawn is happening in.; player: <Player Match> The player respawning
- Event data: player: The player that is respawning; location: The location they are going to respawn at; bed_spawn: If the respawn location is the player's bed; anchor_spawn: If the respawn location is the player's respawn anchor; reason: One of DEATH, END_PORTAL, or PLUGIN (MC 1.19.4+)
- Mutable: location

### player_stop_using_item

- Behaviour: Fires when a player stops using an item such as shields, bows, crossbows, tridents, brushes, goat horns, or spyglasses (not including when changing the held item).
- Prefilters: itemname: <Material Match> The item type being used; player: <Player Match> The player that was using the item.
- Event data: player; item: The item that was used.; ticks: The number of ticks the item was used.

### player_teleport

- Behaviour: Fires when a player is teleported for any reason, except when respawning.
- Prefilters: type: <Enum Match> The teleportation cause.; from: <Location Match> The location the player is teleporting from.; to: <Location Match> The location the player is teleporting to.; player: <Player Match> The player teleporting.
- Event data: player; from: The location the player is teleporting from; to: The location the player is teleporting to; type: the type of teleport cause, one of COMMAND, END_PORTAL, ENDER_PEARL, NETHER_PORTAL, PLUGIN, SPECTATE, END_GATEWAY, CHORUS_FRUIT, DISMOUNT, EXIT_BED, UNKNOWN
- Mutable: to

### player_toggle_flight

- Behaviour: Fires when a player toggles their flying state, typically by double tapping their jump key.
- Prefilters: world: <Macro> The world the player is in.; flying: <Boolean Match> Whether or not the player is trying to start or stop flying; player: <Player Match> The player who toggled their flying state
- Event data: player: The player who toggled their flying state; flying: Whether or not the player is trying to start or stop flying; location: Where the player is

### player_toggle_sneak

- Behaviour: Fires when a player changes their sneaking state.
- Prefilters: sneaking: <Boolean Match> Whether or not the player is now sneaking; world: <Macro> The world of the player; player: <Player Match> The player who changed their sneaking state
- Event data: player: The player who changed their sneaking state; sneaking: Whether or not the player is now sneaking; location: Where the player is

### player_toggle_sprint

- Behaviour: Fires when a player changes their sprinting state.
- Prefilters: sprinting: <Boolean Match> Whether or not the player is now sprinting.; world: <Macro> The world the player is in.; player: <Player Match> The player who changed their sprinting state.
- Event data: player: The player who changed their sprinting state; sprinting: Whether or not the player is now sprinting; location: Where the player is

### pressure_plate_activated

- Behaviour: Fires when a player steps on any block that is modifiable when stepped or stomped on. These blocks include pressure plates, redstone ore, farmland, tripwire, turtle eggs, shriekers, big dripleaves, etc.
- Prefilters: location: <Location Match> The location of the block; player: <Player Match> The player interacting with the block
- Event data: location: The location of the block; activated: (deprecated); player: The player associated with this event

### resource_pack_status

- Behaviour: Fires when a player's client responds to a request to download and load a resource pack. Two of these events may be fired for each request: first when the client accepts the pack, and later when the client successfully l...
- Prefilters: status: <Enum Match> The status received from the client: ACCEPTED, DECLINED, DISCARDED, DOWNLOADED, FAILED_DOWNLOAD, FAILED_RELOAD, INVALID_URL, or SUCCESSFULLY_LOADED; player: <Player Match> The player requesting the resource pack
- Event data: player; id: The UUID of the resource pack (MC 1.20.4+); status: The resource pack status received from the client, one of

### world_changed

- Behaviour: Fires when a player changes worlds, so it is not cancellable. To prevent a player from changing worlds, consider cancelling or modifying player_teleport and player_spawn events.
- Prefilters: from: <World Match> The world the player is coming from.; to: <World Match> The world the player is now in; player: <Player Match> The player that switched worlds.
- Event data: player; from: The world the player is coming from; to: The world the player is now in

## PluginEvents

### plugin_message_received

- Behaviour: Fires when a player's client sends a plugin message.
- Prefilters: channel: <String Match>
- Event data: player: the player; channel: the channel used; bytes: byte array of the data sent

## ServerEvents

### broadcast_message

- Behaviour: Fired when a message is broadcasted on the server.
- Prefilters: message: <String Match>
- Event data: message: The message that will be broadcasted; player_recipients: An array of players who will receive the message.
- Mutable: message

### redstone_changed

- Behaviour: Fired when a redstone activatable block is toggled, either on or off, AND the block has been set to be monitored with the monitor_redstone function.
- Prefilters: location: <Location Match>
- Event data: location: The location of the block; active: Whether or not the block is now active, or disabled.

### server_command

- Behaviour: This event is fired off when any command is run from the console or commandblock. This fires before CommandHelper aliases, allowing you to insert control beforehand.
- Prefilters: prefix: <String Match> The first part of the command, i.e. 'cmd' in '/cmd blah blah'; type: <String Match> The command sender type
- Event data: command: The entire command; prefix: The prefix of the command; sendertype: The command sender type. This is one of console, command_block, command_minecart or null if the sender is unknown to CommandHelper.
- Mutable: command

### server_ping

- Behaviour: Fired when a user who has saved this server looks at their serverlist.
- Prefilters: players: <Math Match>; maxplayers: <Math Match>
- Event data: ip: The address the ping is coming from; players: The number of players online; maxplayers: The number of slots on the server; motd: The message a player is shown on the serverlist; list: The list of connected players
- Mutable: motd; maxplayers; list: It is only possible to remove players, the added players will be ignored. This will also change the player count.

### tab_complete_command

- Behaviour: This will fire if a tab completer has not been set for a command registered with register_command(), or if the set tab completer doesn't return an array.
- Event data: command: The command name that was registered.; alias: The alias the player entered to run the command.; args: The given arguments after the alias.; completions: The available completions for the last argument.; sender: The player that ran the command.
- Mutable: completions

## VehicleEvents

### vehicle_collide

- Behaviour: Fires when a vehicle runs into something. If it ran into a block, event data will contain block info. If it ran into an entity, event data will contain info and options relevant to hitting an entity.
- Prefilters: type: <Macro> The entitytype of the vehicle; collisiontype: <String Match> One of BLOCK or ENTITY; hittype: <Macro> Matches an entitytype in an enitity collision; hittype: <String Match> Matches a block in a block collision
- Event data: type; id: The entityID of the vehicle; entity: the entityID of the entity that was hit; block: the location of the block that was hit; collisiontype; collide; pickup
- Mutable: collide: whether the vehicle hits the entity or passes through it; pickup: whether or not the vehicle pick up the entity; both fields can only be modified for entity collisions

### vehicle_destroy

- Behaviour: Fires when a vehicle is destroyed.
- Prefilters: vehicletype: <Macro> the entitytype of the vehicle
- Event data: vehicletype; vehicle: entityID; damager: If the source of damage is a player this will contain their name, otherwise it will be the entityID of the damager (only available when an entity causes damage); shooter: The name of the player who shot, otherwise the entityID (only available when damager is a projectile)

### vehicle_enter

- Behaviour: Fires when an entity enters a vehicle.
- Prefilters: vehicletype: <Macro> the entitytype of the vehicle; passengertype: <Macro> the enitytype of the passenger
- Event data: vehicletype; passengertype; vehicle: entityID; passenger: entityID; player: player name if passenger is a player, null otherwise

### vehicle_leave

- Behaviour: Fires when an entity leaves a vehicle.
- Prefilters: vehicletype: <Macro> the entitytype of the vehicle; passengertype: <Macro> the enitytype of the passenger
- Event data: vehicletype; passengertype; vehicle: entityID; passenger: entityID; player: player name if passenger is a player, null otherwise

### vehicle_move

- Behaviour: Fires when a vehicle is moving. Due to the high frequency of this event, prefilters are extremely important to use -- especially threshold.
- Prefilters: vehicletype: <Macro> the entitytype of the vehicle; passengertype: <Macro> the enitytype of the passenger; world: <String Match> the world the vehicle is in; from: <Location Match> This should be a location array (x, y, z, world).; to: <Location Match> The location the vehicle is now in.; threshold: The minimum distance the vehicle must have travelled before the event will be triggered. This is based on the 3D distance, and is measured in block units.
- Event data: world; from: Get the previous position; to: Get the next position; vehicletype; passengertype; id: entityID; passenger: entityID; player: player name if passenger is a player, null otherwise

## WeatherEvents

### lightning_strike

- Behaviour: Fires when lightning strikes or the lightning strike effect occurs.
- Prefilters: world: <Macro> the world; location: <Location Match> the lightning strike location; is_effect: <Boolean Match> whether the strike was real or just an effect
- Event data: world: the name of the world in which the strike occurred; id: the lightning entityID; location: locationArray of the event; is_effect: the data value for the block being changed; cause: The cause of the strike (COMMAND, CUSTOM, SPAWNER, TRIDENT, TRAP, WEATHER, or UNKNOWN)

### thunder_change

- Behaviour: Fires when thunder begins or ends.
- Prefilters: world: <Macro> the world; has_thunder: <Boolean Match> if it is thundering
- Event data: world: the name of the world in which thunder is changing; has_thunder: if the world is thundering

### weather_change

- Behaviour: Fires when rain starts or stops.
- Prefilters: world: <Macro> the world; has_rain: <Boolean Match> if it is raining
- Event data: world: the name of the world in which the weather changed; has_rain: if it is raining

## WorldEvents

### tree_grow

- Behaviour: Fires when a tree grows.
- Prefilters: world: <Macro>; player: <Macro>; type: <Macro>; bonemeal: <Boolean Match>
- Event data: world: The world in which the tree has grown.; type: The tree type, can be one of TREE, BIG_TREE, REDWOOD, TALL_REDWOOD, BIRCH, JUNGLE, SMALL_JUNGLE, JUNGLE_BUSH, RED_MUSHROOM, BROWN_MUSHROOM, SWAMP, ACACIA, DARK_OAK, COCOA_TREE, MEGA_REDWOOD, MEGA_PINE, TALL_BIRCH, CHORUS_PLANT, CRIMSON_FUNGUS, WARPED_FUNGUS, AZALEA, MANGROVE, TALL_MANGROVE, CHERRY, PALE_OAK, PALE_OAK_CREAKING, ORANGE_POPLAR, RED_POPLAR, or YELLOW_POPLAR; blocks: An array containing all locations of grown blocks.; location: The location of the sapling.; bonemeal: If the tree has grown due to a bonemeal or not.; player: The player who used the bonemeal, or null if no bonemeal was used.

### world_load

- Behaviour: Fires when a world is loaded.
- Prefilters: world: <Macro>
- Event data: world: The loaded world.

### world_save

- Behaviour: Fires when a world is saved.
- Prefilters: world: <Macro>
- Event data: world: The saved world.

### world_unload

- Behaviour: Fires when a world is unloaded.
- Prefilters: world: <Macro>
- Event data: world: The unloaded world.
