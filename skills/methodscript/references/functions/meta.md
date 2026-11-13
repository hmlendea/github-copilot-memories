# MethodScript Function Reference: Meta

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

These functions provide a way to run other commands, and otherwise interact with the system in a meta way.

24 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `build_date()` -> int [restricted] - Returns the compile date of the current script, as a unix time stamp in milliseconds.
- `call_alias(cmd)` -> boolean - Allows a CommandHelper alias to be called from within another alias. Typically this is not possible, as a script that runs "/jail = /jail" for instance, would simply be calling whatever plugin that ac...
- `capture_runas(player, command)` -> string (throws PlayerOfflineException; FormatException; PluginInternalException) [restricted] - Works like runas, except any messages sent to the command sender during command execution are attempted to be intercepted, and are then returned as a string, instead of being sent to the command sende...
- `engine_build_date()` -> int [restricted] - Returns the compile date, in a millisecond unit time stamp, of when MethodScript was compiled, or null, if that can't be computed for various reasons.
- `engine_location()` -> string [restricted] - Returns the location of the currently running engine binary.
- `get_cmd()` -> string - Gets the command (as a string) that ended up triggering this script, exactly how it was entered by the player. This could be null, if for instance it is called from within an event.
- `get_cmd_completions([player], command, args)` -> array (throws FormatException; PluginInternalException; NotFoundException) [restricted] - Runs a plugin command's tab completer and returns an array of possible completions for the final argument. See more...
- `get_command_block()` -> locationArray - If this command was being run from a command block block or minecart, this will return the location of the block or minecart.
- `get_compiler_options()` -> array - Returns a list of all defined compiler options, which can be set using the compilerOptions file option
- `get_compiler_warnings()` -> array - Returns a list of all defined compiler warnings, which can be suppressed using the suppressWarnings file option
- `get_locales()` -> array - Returns a list of locales on this system.
- `get_script_environment()` -> Resource [restricted] - Returns a copy of the underlying engine's environment object. This is only useful to embedded scripting engines that are attempting to call back into MethodScript. The object returned is a CResource.
- `has_runtime_setting(name)` -> boolean (throws CastException) [restricted] - Returns true if the runtime setting is set. This will also return true if the value of the setting is null.
- `is_alias(cmd)` -> boolean (throws IOException) [restricted] - Returns true if using call_alias with this cmd would trigger an alias.
- `nameof(component)` -> string (throws CastException) - Returns the name of the item. For now, only works with variables. For instance, nameof(@var) returns the string "@var".
- `noop([...])` -> void - An operation that does nothing. Any arguments passed in are ignored entirely, though they will be evaluated first.
- `psetop([player], status)` -> string (throws PlayerOfflineException) [restricted] - Sets whether or not a player has operator status. If no player is specified the player running the script is given.
- `remove_runtime_setting(name)` -> void (throws CastException) [restricted] - Removes the previously set runtime setting. If the setting wasn't already set, then a warning is issued, unless 'function.remove_runtime_setting.no_warn_on_removing_blank' is set to true.
- `run(string command)` -> void (throws FormatException; PluginInternalException) - Runs a command as the current player. Useful for running commands in a loop. Note that this accepts commands like from the chat; with a forward slash in front.
- `run_cmd(cmd)` -> void (throws FormatException) - Runs a command regardless of whether or not it is an alias or a builtin command. Essentially, this works like checking if(is_alias(@cmd)){ call_alias(@cmd) } else { run(@cmd) }.
- `runas(player, command)` -> void (throws FormatException; PlayerOfflineException) [restricted] - Runs a command as a particular online player. The special name '~console' can be used to run it as console. If you want to run the command as if the player was op, use sudo instead.
- `scriptas(sender, [label], script)` -> void (throws PlayerOfflineException) [restricted] - Runs the specified script in the context of a given player or ~console. A script that runs player(), for instance, would return the specified player's name, not the player running the command.
- `set_runtime_setting(name, setting)` -> void (throws CastException) [restricted] - Sets the value of a particular runtime setting. Various system components can define these differently, so see the documentation for a particular component to see if it has a runtime setting that can...
- `sudo([player], command)` -> void (throws FormatException) [restricted] - Runs a single command for the current or provided player, as op. See more...
