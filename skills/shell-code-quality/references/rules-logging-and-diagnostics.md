# Shell Rules: Logging And Diagnostics

One directive per Shell rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Print error messages to stderr with `>&2` (`echo "[ERROR] Message goes here." >&2`), never to stdout.
