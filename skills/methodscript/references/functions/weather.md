# MethodScript Function Reference: Weather

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Provides functions to control the weather

5 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `has_storm([world])` -> boolean (throws InvalidWorldException) - Returns whether the world (defaults to player's world) has a storm.
- `has_thunder([world])` -> boolean (throws InvalidWorldException) - Returns whether the world (defaults to player's world) has thunder.
- `lightning(locationArray, [safe] / x, y, z, [safe])` -> string (throws CastException; LengthException; InvalidWorldException; FormatException) [restricted] - Makes lightning strike at the x y z coordinates specified in the array or arguments. Safe defaults to false, but if true, lightning striking a player will not hurt them.
- `set_thunder(boolean, [world], [int])` -> void (throws InvalidWorldException; CastException) [restricted] - Sets whether or not the weather can have thunder. The third argument can specify how long the thunder should last in server ticks.
- `storm(isStorming, [world], [int])` -> void (throws CastException; FormatException; InvalidWorldException) [restricted] - Creates a (rain) storm if isStorming is true, stops a storm if isStorming is false. The second argument can be a world name or the duration in ticks of the given weather setting.
