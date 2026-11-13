# MethodScript Function Reference: Minecraft

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

These functions provide a hook into game functionality.

18 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `all_materials()` -> array - Returns an array of all material names.
- `convert_legacy_item(itemArray)` -> array (throws CastException; FormatException; RangeException; NotFoundException) - Converts old pre-1.13 item arrays to new item arrays. Almost all item arrays will be converted successfully when passing them to a function that accepts item arrays.
- `data_name(item)` -> string (throws CastException; FormatException) - Returns a modern material for the a legacy item id, name, notation, or array. If an invalid argument is passed in, null is returned. Given 1 or '1:0', returns 'STONE'.
- `data_values(var1)` -> int - Does a lookup to return the legacy data value of a name. For instance, returns 1 for 'stone'. If the data value cannot be found, null is returned.
- `get_banned_players()` -> array - An array of players banned on the server.
- `get_ip_bans()` -> array [restricted] - Returns an array of entries from banned-ips.txt.
- `get_server_info([value])` -> mixed (throws CastException; RangeException; NotFoundException) - Returns various information about server.If value is set, it should be an integer of one of the following indexes, and only that information for that index will be returned. See more...
- `get_spawner_type(locationArray)` -> string (throws FormatException) [restricted] - Gets the entity type that will spawn from the specified mob spawner. May be null.
- `get_whitelisted_players()` -> array - An array of players whitelisted on the server.
- `make_effect(locationArray, effect, [radius])` -> void (throws CastException; FormatException) [restricted] - Plays the specified effect at the given location for all players within the radius (or 64 by default). See more...
- `material_info(material, [trait])` -> mixed (throws CastException; FormatException; IllegalArgumentException) - Returns an array of info about the material. If a trait is specified, it returns only that trait. Available traits: hasGravity, isBlock, isItem, isBurnable, isEdible, isFlammable, isOccluding, isRecor...
- `max_stack_size(itemArray)` -> integer (throws CastException; FormatException; RangeException; NotFoundException) - Given an item array, returns the maximum allowed stack size. This method will accept an item array like is returned from pinv().
- `monitor_redstone(location, [isMonitored])` -> void (throws CastException; FormatException) [restricted] - Sets up a location to be monitored for redstone changes. If a location is monitored, it will cause redstone_changed events to be triggered.
- `select_entities([player], selector)` -> array (throws FormatException; LengthException; PlayerOfflineException) [restricted] - Returns an array of all matching entities for a Minecraft target selector. The selector will use the current command sender context unless a player is specified.
- `send_resourcepack(player, url)` -> void (throws PlayerOfflineException) [restricted] - Sends a resourcepack URL to the player's client. If the client has not been requested to change resources in the past, they will receive a confirmation dialog before downloading and switching to the n...
- `set_ip_banned(address, banned)` -> void [restricted] - If banned is true, address is added to banned-ips.txt, if false, the address is removed.
- `set_spawner_type(locationArray, type)` -> void (throws FormatException) [restricted] - Sets the mob spawner's entity type at the location specified. If the location is not a mob spawner, a FormatException is thrown. Entity type may be set to null.
- `shutdown_server()` -> void [restricted] - Shuts down the minecraft server instance.
