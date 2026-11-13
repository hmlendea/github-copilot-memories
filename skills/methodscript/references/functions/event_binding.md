# MethodScript Function Reference: EventBinding

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

13 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `bind(event_name, options, prefilter, event_obj, [custom_params], <code>)` -> string (throws BindException) [restricted] - Binds some functionality to an event, so that when said event occurs, the event handler will fire. Returns the id of this event, so it can be unregistered later, if need be.
- `cancel([state])` -> void (throws BindException) [restricted] - Cancels the event (if applicable). If the event is not cancellable, or is already set to the specified cancelled state, nothing happens.
- `consume()` -> void (throws BindException) [restricted] - Consumes an event, so that lower priority handlers don't even receive the event. Monitor level handlers will still receive it, however, and they can check to see if the event was consumed.
- `dump_events()` -> array [restricted] - Returns an array of all the events currently registered on the server. Mostly meant for debugging, however it would be possible to parse this response to cherry pick events to unregister.
- `event_meta()` -> array (throws BindException) [restricted] - Returns meta information about the activity in regards to this event. This is meant as a debug tool.
- `has_bind(id)` -> boolean [restricted] - Returns true if a bind with the specified id exists and is currently bound. False is returned otherwise. This can be used to pre-emptively avoid a BindException if duplicate ids are used.
- `is_cancelled()` -> boolean (throws BindException) [restricted] - Returns whether or not the underlying event is cancelled or not. If the event is not cancellable in the first place, false is returned. If called from outside an event, a BindException is thrown
- `is_consumed()` -> boolean (throws BindException) [restricted] - Returns whether or not this event has been consumed. Usually only useful for Monitor level handlers, it could also be used for highly robust code, as an equal priority handler could have consumed the...
- `is_locked(parameter)` -> boolean (throws BindException) [restricted] - Returns whether or not a call to modify_event() would fail, based on the parameter being locked by a higher priority handler.
- `lock(<none> / parameterArray / parameter, [parameter...])` -> void (throws BindException) [restricted] - Locks the specified event parameter(s), or all of them, if specified with no arguments. Locked parameters become read only for lower priority event handlers.
- `modify_event(parameter, value, [throwOnFailure])` -> boolean (throws CastException; BindException) [restricted] - Modifies the underlying event object, if applicable. The documentation for each event will explain what parameters can be modified, and what their expected values are. See more...
- `trigger(eventName, eventObject, [serverWide])` -> void (throws CastException; BindException) [restricted] - Manually triggers bound events. The event object passed to this function is sent directly as-is to the bound events. Check the documentation for each event to see what is required.
- `unbind([eventID])` -> void (throws BindException) [restricted] - Unbinds an event, which causes it to not run anymore. If called from within an event handler, eventID is optional, and defaults to the current event id.
