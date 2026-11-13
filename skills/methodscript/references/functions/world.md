# MethodScript Function Reference: World

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Provides functions for manipulating a world

38 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `create_world(name, type, environment, [seed, [generator]])` -> void (throws FormatException; CastException) [restricted] - Creates or loads a world. The 'name' is the same as the directory name for the world. If a world directory by that name already exists, it will be loaded.
- `distance(locationA, locationB)` -> double (throws RangeException; FormatException; InvalidWorldException; IllegalArgumentException) - Returns the distance between two locations.
- `get_chunk_loc([locationArray])` -> array (throws FormatException; InsufficientArgumentsException; NotFoundException) - Returns an array of (x, z, world) coordinates of the chunk of either the location specified or the location of the player running the command.
- `get_difficulty(world)` -> string (throws InvalidWorldException) [restricted] - Returns the difficulty of the world, It will be one of PEACEFUL, EASY, NORMAL, or HARD.
- `get_force_loaded_chunks([world])` -> array (throws InvalidWorldException) - Gets an array of all chunk coordinates that are persistently loaded.
- `get_gamerule(world, [gameRule])` -> mixed (throws InvalidWorldException; FormatException) [restricted] - Returns an associative array containing the values of all existing gamerules for the given world. If the gameRule parameter is specified, the function only returns that one value instead of an array.
- `get_loaded_chunks([world])` -> array (throws CastException; FormatException; InvalidWorldException; NotFoundException) [restricted] - Gets an array of all currently loaded chunks for a world. The current player's world is used if one is not provided. The chunk objects are associative arrays with the keys: x, z, and world.
- `get_pitch(location_from, location_to)` -> double (throws InvalidWorldException; FormatException) [restricted] - Calculate pitch from one location to another. This will be from -90.0 to 90.0, which is up and down respectively.
- `get_pvp(world)` -> boolean (throws InvalidWorldException) [restricted] - Returns if PVP is allowed in the world.
- `get_spawn([world])` -> array (throws InvalidWorldException; FormatException) [restricted] - Returns a location array for the specified world, or the current player's world if one is not specified.
- `get_temperature(locationArray)` -> double (throws FormatException) - Returns the current temperature at the location given.
- `get_vector(locationArray, [magnitude])` -> array (throws RangeException; FormatException) - Returns a vector from the yaw and pitch in a location array. Only the yaw and pitch keys are required in the array. The second parameter, that defines the magnitude of the vector, defaults to 1.0.
- `get_world_autosave(world_name)` -> boolean (throws InvalidWorldException) [restricted] - Fetch the world's current auto-save state.
- `get_world_border(world_name)` -> array (throws InvalidWorldException) [restricted] - Returns an associative array of all information about the world's border. The keys are width, center, damagebuffer, damageamount, warningtime, warningdistance.
- `get_world_day([world])` -> int (throws InvalidWorldException) [restricted] - Returns the current day number of the specified world. As of MC 26.1 dimensions without a world clock will return 0. (e.g. nether)
- `get_world_time([world])` -> int (throws InvalidWorldException) [restricted] - Returns the time of the specified world, as an integer in ticks from 0 to 23999. As of MC 26.1 dimensions without a world clock will return 0. (e.g. nether)
- `get_worlds()` -> array [restricted] - Returns a list of all currently loaded worlds.
- `get_yaw(location_from, location_to)` -> double (throws InvalidWorldException; FormatException) [restricted] - Calculate yaw from one location to another on the X-Z plane. The rotation is measured in degrees (0-359.99...) relative to the (x=0,z=1) vector, which points south.
- `is_slime_chunk(x, z, [world] / locationArray, [world])` -> boolean (throws CastException; FormatException; InvalidWorldException) [restricted] - Returns if the chunk is a slime spawning chunk. The current player's world is used if one is not provided.
- `load_chunk([world], x, z / [world], locationArray)` -> void (throws CastException; FormatException; InvalidWorldException) [restricted] - Loads a chunk for a world using the x and z coordinates. The current player's world is used if one isn't provided.
- `location_shift(origin, target, [distance], [clamp] / origin, direction, [distance])` -> array (throws InvalidWorldException; FormatException) [restricted] - Returns a location array that is the specified distance from the origin location along a vector. See more...
- `refresh_chunk([world], x, z / [world], locationArray)` -> void (throws CastException; FormatException; InvalidWorldException) [restricted] - This is not guaranteed to work reliably! Resends the chunk data to all clients, using the specified world or current player's world.
- `regen_chunk(x, z, [world] / locationArray, [world])` -> boolean (throws CastException; FormatException; InvalidWorldException) [restricted] - Regenerate the chunk for a world. The current player's world is used if one is not provided. Beware that this is destructive! Any data in this chunk will be lost! Returns true if the operation was suc...
- `save_world(world_name)` -> void (throws InvalidWorldException) [restricted] - Saves the specified world.
- `set_chunk_force_loaded([world], x, z, forced / locationArray, forced)` -> void (throws CastException; FormatException; InvalidWorldException) [restricted] - Sets a chunk to be persistently loaded.
- `set_difficulty([world], difficulty)` -> void (throws InvalidWorldException; FormatException) [restricted] - Sets the difficulty of the world with the given name, or all worlds if the name is not given. The difficulty can be PEACEFUL, EASY, NORMAL, or HARD.
- `set_gamerule([world], gameRule, value)` -> boolean (throws InvalidWorldException; FormatException; CastException) [restricted] - Sets the value of the gamerule for the specified world. If world is not given the value is set for all worlds. Returns true if successful. See more...
- `set_keep_spawn_loaded(world, boolean)` -> void (throws InvalidWorldException) [restricted] - Sets whether or not the spawn chunks in the given world should stay loaded. Spawn chunks are never kept loaded starting from MC 1.21.9.
- `set_pvp([world], boolean)` -> void (throws InvalidWorldException) [restricted] - Sets if PVP is allowed in the world with the given name, or all worlds if the name is not given. (uses gamerule in 1.21.9+)
- `set_spawn([world], locationArray / [world], x, y, z)` -> void (throws InvalidWorldException; CastException; FormatException) [restricted] - Sets the spawn of the world. Note that in some cases a plugin may override the spawn.
- `set_world_autosave([world_name], newState)` -> void [restricted] - Updates the world's auto-save state. If no world is specified, set the option for all worlds.
- `set_world_border(world_name, paramArray)` -> void (throws CastException; FormatException; InvalidWorldException; RangeException) [restricted] - Updates the world's border with the given values. In addition to the keys returned by get_world_border(), you can also specify the "seconds".
- `set_world_day([world], day)` -> void (throws InvalidWorldException) [restricted] - Set the current day number of a given world. As of MC 26.1 some dimensions may not have a world clock. (e.g. nether)
- `set_world_time([world], time)` -> void (throws InvalidWorldException; FormatException) [restricted] - Sets the time of a given world. As of MC 26.1 some dimensions may not have a world clock. (e.g. nether) The time should be a number in ticks from 0 to 23999. If not, it is modulo scaled.
- `spawn_falling_block(locationArray, blockName, [vectorArray])` -> string (throws FormatException) [restricted] - Spawns a falling block entity of the specified block type at the specified location, applying the vector array as a velocity if given.
- `unload_chunk([world], x, z / [world], locationArray)` -> void (throws CastException; FormatException; InvalidWorldException) [restricted] - Unloads a chunk for a world using the x and z coordinates. The current player's world is used if one is not provided.
- `unload_world(world, [save])` -> boolean (throws InvalidWorldException) [restricted] - Unloads a world, and saves it if save is true (defaults true), and returns whether or not the operation was successful.
- `world_info(world)` -> array (throws InvalidWorldException) [restricted] - Returns an associative array of immutable info about the world. The keys are name, uuid, seed, environment, generator, sealevel, minheight and maxheight. The worldtype key is deprecated as of 1.16.
