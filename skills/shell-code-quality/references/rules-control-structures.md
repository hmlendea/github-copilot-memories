# Shell Rules: Control Structures

One directive per Shell rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Merge an `if` that is the sole command of an outer `if` into one condition when no `else` branch exists on either (`if [[ -f "${FILE}" && -r "${FILE}" ]]; then`).
- Conclude every `case` construct with a `*)` clause that manages unexpected values or contains a comment explaining why no action is required.
- Use `[[ ]]` instead of `[ ]` or `test` for conditional tests; scripts that explicitly require POSIX compatibility are exempt. **Local precedence:** the coding instructions require `[[ ]]` for all conditional tests, so the POSIX exemption does not apply; report each script that explicitly requires POSIX compatibility.
- Never assign a variable to itself (`NAME="${NAME}"`); correct the intended value or delete the redundant assignment.
- Never use identical expressions as both operands of a binary operator: `==`, `!=`, `=`, `-eq`, `-ne`, `-lt`, `-le`, `-gt`, `-ge`, `<`, `>`, `&&`, `||`, `=~`, and, within `$(( ))`, `-`, `/`, `%`, `|`, `&`, and `^`. Exempt: `*`, `**`, `+`, assignment `=`, `<<`, and `>>`.
