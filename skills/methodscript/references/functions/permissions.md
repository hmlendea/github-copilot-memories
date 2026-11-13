# MethodScript Function Reference: Permissions

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Provides access to the server's underlying permissions system. Permissions functionality is only as good as the management system in place, however, and so not all functions may be supported on a given system.

1 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `has_permission([player], permissionName)` -> boolean (throws InsufficientPermissionException; PlayerOfflineException) - Using the built in permissions system, checks to see if the player has a particular permission. This is simply passed through to the permissions system.
