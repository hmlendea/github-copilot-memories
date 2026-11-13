# MethodScript Function Reference: Trades

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Functions related to the management of trades and merchants. A trade is a special kind of recipe accessed through the merchant interface. A merchant is a provider of trades, which may or may not be attached to a Villager or Wandering Trader.

7 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `create_virtual_merchant(ID, title)` -> void (throws IllegalArgumentException) [restricted] - Creates a merchant that can be traded with by players but is not attached to a physical entity. The ID given should not be a UUID.
- `delete_virtual_merchant(string)` -> boolean [restricted] - Deletes a virtual merchant if one by the given ID exists. Returns true if one was removed, or false if there was no match for the ID.
- `get_merchant_trades(specifier)` -> array (throws IllegalArgumentException; FormatException; BadEntityException) [restricted] - Returns a list of trades used by the specified merchant. Specifier can be the UUID of an entity or a virtual merchant ID.
- `get_virtual_merchants()` -> array [restricted] - Returns an array where the keys are currently registered merchant IDs and the values are the corresponding window titles of those merchants.
- `merchant_trader(specifier)` -> UUID (throws BadEntityException; FormatException; FormatException; IllegalArgumentException; LengthException) [restricted] - Returns the UUID of the user trading with the merchant, or null if no one is.
- `popen_trading(specifier, [player], [force])` -> boolean (throws PlayerOfflineException; LengthException; IllegalArgumentException; BadEntityException; FormatException) [restricted] - Opens a trading interface for the current player, or the one specified. Only one player can trade with a merchant at a time.
- `set_merchant_trades(specifier, array)` -> void (throws IllegalArgumentException; FormatException; CastException; BadEntityException; NotFoundException) [restricted] - Sets the list of trades the specified merchant can use to the provided array of TradeArrays. The specifier can be the UUID of a physical entity or the ID of a user-created virtual merchant.
