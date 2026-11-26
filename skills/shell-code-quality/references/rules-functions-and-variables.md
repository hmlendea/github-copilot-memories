# Shell Rules: Functions And Variables

One directive per Shell rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- At the start of each function, assign positional parameters (`$1`, `$2`, …) to `local` variables with descriptive names (`local SOURCE_FILE="${1}"`), and reference those variables instead of the positional parameters.
- Conclude every function with an explicit `return` (`return 0` on success, a non-zero status on error) instead of relying on the status of the final command.
- Delete unused local variables; variables passed by name to a function whose name contains `by_ref` count as used.
