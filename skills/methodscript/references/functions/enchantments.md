# MethodScript Function Reference: Enchantments

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Provides methods for dealing with enchanted items

8 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `can_enchant_item(name, item)` -> boolean (throws EnchantmentException; FormatException; CastException; RangeException; NotFoundException) - Given an enchantment name and an item array, returns whether or not that item can be enchanted with that enchantment. Throws an EnchantmentException if the name is not a valid enchantment type.
- `enchant_item([player], slot, type, level / player, slot, enchantsArray)` -> void (throws CastException; EnchantmentException; PlayerOfflineException) [restricted] - Adds enchantments to an item in the player's inventory. A single enchantment type and level can be specified or an enchantment array may be given.
- `enchantment_list()` -> array - Returns an informational list of all valid enchantment names. Note that this will simply cover all enchantment types, but may not be a comprehensive list of names that can be accepted, there may be mo...
- `get_enchant_max(name)` -> int (throws EnchantmentException) - Given an enchantment name, returns the max level it can be. If name is not a valid enchantment, an EnchantException is thrown.
- `get_enchants(item)` -> array (throws FormatException; CastException; RangeException; NotFoundException) - Given an item array, returns the enchantments that can be validly added to this item. This may return an empty array.
- `get_item_enchants([player], slot)` -> array (throws PlayerOfflineException; CastException) [restricted] - Returns an array of arrays of the enchantments and their levels on the given item. For example: array('sharpness': 1, 'unbreaking': 3).
- `is_enchantment(name)` -> boolean - Returns true if this name is a valid enchantment type.
- `remove_item_enchant([player], slot, type)` -> void (throws CastException; EnchantmentException; PlayerOfflineException) [restricted] - Removes an enchantment from an item. The type may be a valid enchantment, or an array of enchantment names. It can also be null, and all enchantments will be removed.
