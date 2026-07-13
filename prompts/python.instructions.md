---
description: "Use when writing or editing Python code. Covers imports, naming, string literals, comments, error handling, HTTP/requests, function structure, type hints, module structure, and blank line rules."
applyTo: "**/*.py"
---
## Python

### Imports

- Standard library imports first, one name per line (`import random`, `import re`, etc.).
- `from … import` for stdlib submodules grouped on one line (`from urllib.parse import urlencode, parse_qs, urlparse, urlsplit`).
- Local imports last, grouped by module; use a `from module import (name, name, …)` multi-line form with each name on its own line when there are many names.

### Naming

- `snake_case` for all functions, variables, and parameters. `SCREAMING_SNAKE_CASE` for all module-level constants.
- Clear, explicit names with no abbreviations or shortenings — same full-name rule as for other languages. This applies everywhere: local variables, parameters, loop variables, lambda variables, etc. Single-letter names and abbreviated prefixes are forbidden.
- Boolean variables and functions must use a meaningful boolean-semantic prefix: `is_`, `has_`, `does_`, `are_`, or contextual tense-embedded forms (`..._was_...`, `..._were_...`) — e.g. `is_enabled`, `has_permission`, `request_was_handled`. Never use vague names like `flag`, `check`, or `result` for booleans.

### String Literals

- Single quotes for plain string literals: `'grant_type'`, `'code'`.
- f-strings for all interpolation — never `%` formatting or `.format()`.

### Comments

- Keep code self-explanatory and avoid comments unless they are exceptional and genuinely useful.
- Always place at least one space after `#`: `# text`, never `#text`.
- Inline and block comments must always begin with an uppercase letter and end with a period: `# Calculates the wall distance.`
- TODO comments must always use the exact format `# TODO: Description.` (uppercase TODO, colon, space, sentence ending with period).
- Section dividers use `# --- Section Name ---` with dashes on both sides and a blank line above and below.

### Error Handling

- Guard clauses at top of functions for missing configuration or preconditions.
- `try/except Exception as exception:` wrapping all external I/O calls (HTTP, file, socket).
- Check response status code before parsing the body: `if response.status_code == 200:`.
- Use `.get("key", default)` for safe dict access on JSON responses.

### HTTP / Requests

- `requests.Session()` used as a context manager.
- URL query parameters extracted with `parse_qs(urlsplit(url).query).get('key', [''])[0]`.

### Function Structure

- Variables initialised to `None` before conditional assignment; returned at the end.
- `for _ in range(n):` for counted loops with a throwaway variable.
- `or` chaining for fallback values: `obj.get('emailAddress') or obj.get('phoneNumber') or DEFAULT`.

### Type Hints

- Used selectively on public-facing or complex functions; not required everywhere.
- When used, annotate parameters and return type: `def build_headers(fields: dict, key: str) -> dict:`.

### Module Structure

- All configuration constants extracted to a dedicated `config.py` and imported explicitly by name.
- Module-level constants defined at the top of each file, before any function definitions.
- `if __name__ == "__main__": main()` at the very end of the entry-point file.

### Blank Lines

- One blank line between top-level functions.
- `if`, `for`, `while`, `continue`, and `break` statements must always be separated from adjacent assignments or other statements by a blank line above and below.
- `return` statements must always be separated from other lines of code by a blank line above (unless they are the only statement in the function body or the first line after an opening block).
- Never use two or more consecutive blank lines anywhere.
