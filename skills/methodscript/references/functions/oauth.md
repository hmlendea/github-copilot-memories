# MethodScript Function Reference: OAuth

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

2 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `clear_oauth_tokens([clientId])` -> void [restricted] - Clears the oauth tokens (refresh token and access token) for the given client ID. If the client ID is not specified, all tokens are deleted.
- `x_get_oauth_token()` -> void [restricted] - 
