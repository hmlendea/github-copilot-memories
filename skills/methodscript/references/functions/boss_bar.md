# MethodScript Function Reference: BossBar

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Functions to create and manage boss bars in Minecraft.

8 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `bar_add_player(id, player)` -> void (throws NotFoundException; PlayerOfflineException; LengthException) [restricted] - Adds a player to the specified boss bar.
- `bar_remove_player(id, player)` -> void (throws NotFoundException; PlayerOfflineException; LengthException) [restricted] - Removes a player from the specified boss bar.
- `create_bar(id, [optionsArray])` -> void (throws IllegalArgumentException; CastException; FormatException; RangeException; Exception) [restricted] - Creates a new boss bar with a reference id. An optional array can be given with the keys: title, color, style, visible, percent. Title displays above the boss bar.
- `get_bar(id)` -> array (throws NotFoundException) [restricted] - Gets an array of current options for the specified boss bar.
- `get_bar_players(id)` -> array (throws NotFoundException) [restricted] - Returns an array of players that can see this boss bar.
- `get_bars()` -> array [restricted] - Gets an array of boss bar ids currently in use.
- `remove_bar(id)` -> void (throws NotFoundException) [restricted] - Removes the boss bar for all players.
- `update_bar(id, optionsArray / id, percent / id, title)` -> void (throws IllegalArgumentException; CastException; FormatException; NotFoundException; RangeException) [restricted] - Updates the state for the specified boss bar. See create_bar() for available option keys and values for the optionsArray. If the second argument is a string, it'll use it to update the title.
