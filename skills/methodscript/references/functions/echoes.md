# MethodScript Function Reference: Echoes

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

These functions allow you to echo information to the screen

12 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `action_msg([player], message)` -> void (throws PlayerOfflineException; LengthException) [restricted] - Sends a message to the action bar above the hot bar.
- `broadcast(message, [permission] / message, [recipients])` -> void (throws FormatException) [restricted] - Broadcasts a message to all or some players and/or console. If permission is given, only players with that permission and console will see the broadcast.
- `chat(string)` -> void (throws PlayerOfflineException) [restricted] - Echoes string to the chat, as if the user simply typed something into the chat bar. This function cannot be run from console, a PlayerOfflineException is thrown if attempted. Use broadcast() instead.
- `chatas(player, msg)` -> void (throws PlayerOfflineException; LengthException) [restricted] - Sends a chat message to the server, as the given player. Otherwise the same as the chat() function
- `color(name)` -> string - Returns the color (or style) code modifier for a given value. If the value isn't valid, white is used instead. The list of valid color names is: BLACK, DARK_BLUE, DARK_GREEN, DARK_AQUA, DARK_RED, DARK...
- `colorize(text, [symbol])` -> mixed - Replaces all the colorizable character codes in the string. For instance, colorize('&aText') would be equivalent to (color('a').'Text').
- `console(message, [prefix])` -> void (throws CastException) [restricted] - Logs a message to the console. If prefix is true, prepends "CommandHelper:" to the message. Default is true. If you wish to set the default value of prefix to false, use set_runtime_setting('function...
- `msg(var1, [var2...])` -> void (throws PlayerOfflineException) - Echoes a message to the player running the command
- `strip_colors(toStrip)` -> string - Strips all the color codes from a given string
- `tellraw([string selector], array raw)` -> void (throws CastException; FormatException; IOException) [restricted] - A thin wrapper around the tellraw command from console context, this simply passes the input to the command. The raw is passed in as an array and json encoded.
- `title([player], title, subtitle, [fadein, stay, fadeout])` -> void (throws PlayerOfflineException; CastException; RangeException; LengthException) [restricted] - Shows a title and/or subtitle to a player. The title and subtitle parameters can be null. The integers fadein, stay, and fadeout define the time in ticks that the title will be displayed.
- `tmsg(player, msg, [...])` -> void (throws PlayerOfflineException; InsufficientArgumentsException; LengthException) [restricted] - Displays a message on the specified players screen, similar to msg, but targets a specific user.
