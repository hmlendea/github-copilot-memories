---
description: "Use when writing or editing Bash or shell scripts. Covers variable declarations, quoting rules, portability, and distro-agnostic practices."
applyTo: "**/*.sh"
---
## Bash & Other UNIX Shells

### Variables & Constants

- Variables inside functions must be declared with `local` whenever possible.
- Always use environment variables for paths instead of hardcoded values, e.g. `${HOME}`, `${XDG_CONFIG_HOME}`, `${XDG_DATA_HOME}`, `${XDG_CACHE_HOME}`. Never hardcode paths like `/home/user/` or `/etc/`.
- Declare constants with `readonly`: `readonly MY_CONSTANT='value'`.

### Strings & Quoting

- Constant strings (no variable references or command substitutions) must use single quotes: `'constant string'`. Strings that reference variables or call commands must use double quotes: `"Value is: ${VAR}"` / `"Today is: $(date)"`.
- Use `$(command)` for command substitution; never use backticks.

### Conditionals

- Always use `[[ ]]` over `[ ]` for all conditional tests.

### Portability

- Always write distro-agnostic code: use only POSIX-standard or universally available commands, and avoid paths or tools specific to any particular Linux distribution.
- Never embed Python in shell scripts unless explicitly asked.
