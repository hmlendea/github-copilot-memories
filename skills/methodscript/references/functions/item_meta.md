# MethodScript Function Reference: ItemMeta

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

These functions manipulate an item's meta data. The items are modified in a player's inventory.

5 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `get_armor_color([player], inventorySlot)` -> colorArray (throws CastException; PlayerOfflineException) [restricted] - Returns a color array for the color of the leather armor at the given slot. A CastException is thrown if this is not leather armor at that slot.
- `get_itemmeta([player,] slot)` -> array (throws PlayerOfflineException; CastException) [restricted] - Returns an associative array of known item data in the slot given, or null if there isn't any. See more...
- `is_leather_armor([player], itemSlot)` -> boolean (throws CastException; PlayerOfflineException) [restricted] - Returns true if the item at the given slot is a piece of leather armor, that is, if dying it is allowed.
- `set_armor_color([player], slot, colorArray)` -> void (throws CastException; PlayerOfflineException; FormatException) [restricted] - Sets the color of the leather armor at the given slot. colorArray should be an array that matches one of the formats: array(r: 0, g: 0, b: 0) array(red: 0, green: 0, blue: 0) array(0, 0, 0)
- `set_itemmeta([player,] slot, itemMetaArray)` -> void (throws PlayerOfflineException; FormatException; CastException; NotFoundException) [restricted] - Applies the data from the given array to the item at the specified slot. Unused fields will use defaults. If null or an empty array is supplied, or if none of the given fields are applicable, the item...
