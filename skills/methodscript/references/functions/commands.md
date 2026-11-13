# MethodScript Function Reference: Commands

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

A series of functions for creating and managing custom commands.

7 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `clear_commands()` -> void [restricted] - Attempts to clear all registered commands on the server. Vanilla and default Spigot functions are not affected, but all plugins commands are.
- `get_commands()` -> array [restricted] - Returns an array of command arrays in the format register_command expects or null if no commands could be found. The command arrays will not include executors or tabcompleters.
- `get_tabcomplete_prototype(prototypes...)` -> closure (throws CastException) - Returns a closure which can be provided to tabcompleters or run manually, which provides an easy to use syntax for simple to moderately complex tab completion scenarios.
- `register_command(commandname, optionsArray)` -> boolean (throws FormatException; NotFoundException) [restricted] - Registers a command to the server's command list, or updates an existing one. Options is an associative array that can have the following keys: description, usage, permission, noPermMsg, aliases, tabc...
- `set_executor(commandname, closure)` -> void (throws FormatException; NotFoundException) [restricted] - Sets the code that will be run when a user attempts to execute a command. The closure can return true false (treated as true by default). Returning false will display The usage message if it is set.
- `set_tabcompleter(commandname, closure)` -> void (throws FormatException; NotFoundException) [restricted] - Sets the code that will be run when a user attempts to tabcomplete a command. The closure is expected to return an array of completions, otherwise the tab_complete_command event will be fired and used...
- `unregister_command(commandname)` -> boolean (throws NotFoundException) [restricted] - Unregisters a command from the server's command list. Commands from other plugins can be unregistered using this function.
