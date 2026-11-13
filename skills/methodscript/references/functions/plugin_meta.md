# MethodScript Function Reference: PluginMeta

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

6 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `fake_incoming_plugin_message([player,] channel, message)` -> void (throws CastException; PlayerOfflineException; IllegalArgumentException) [restricted] - Fakes an incoming plugin message from the player. Channel should be a string (the channel name) and message should be a byte_array primitive. Depending on the plugin, these parameters will vary.
- `get_registered_channels()` -> array (throws NotFoundException; IllegalArgumentException) [restricted] - Returns an array of strings containing the channels CommandHelper is listening on.
- `is_channel_registered(channel)` -> boolean (throws NotFoundException; IllegalArgumentException) [restricted] - Returns true if commandhelper is listening to the given plugin channel.
- `register_channel(channel)` -> void (throws PluginChannelException; NotFoundException; IllegalArgumentException) [restricted] - Registers a plugin channel for CommandHelper to listen on. Channel name should be a string that is all lower-case, no longer than 32 characters, and contain a colon, or it will throw an IllegalArgumen...
- `send_plugin_message([player,] channel, message)` -> void (throws CastException; PlayerOfflineException; IllegalArgumentException) [restricted] - Sends a plugin message to the player. Channel name should be a string that is all lower-case, no longer than 32 characters, and contain a colon, or it will throw an IllegalArgumentException.
- `unregister_channel(channel)` -> void (throws PluginChannelException; NotFoundException; IllegalArgumentException) [restricted] - Unregisters a plugin channel CommandHelper is listening on, if any.
