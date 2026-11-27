# Debugging and Tools

Use a test build and enable debug mode. After activation, inspect the game's `Logs/output.txt`; resolve the first error and repeat. A new game is the default validation target because saves do not refresh every definition.

The documented console opens with `Shift` + tilde. `dumpconsolecommands` prints available commands, and `reloadmods` reloads mods where supported by the installed build. Useful documented categories include event testing (`testEvents`, `doeventstory`), economy (`addmoney`, `addyield`), units and improvements (`addunit`, `addimprovement`), map visibility (`revealmap`, `fullrevealmap`), characters (`newcharacter`, `addtrait`, `setrating`), and profiling (`dumpprofilerdata`, `memoryprofilersnapshot`). Confirm command syntax with `dumpconsolecommands` because commands and arguments can change.

The documented hotkey list includes camera movement, overlays, selection cycling, undo/redo, city navigation, and UI toggles. Use `dumphotkeyscommands` in-game when available rather than depending on an old list.

For difficult XML errors, compare against the installed `Reference/XML/` files, inspect the Event Browser or Wizard, reduce to one changed file, and retest from a new game.
