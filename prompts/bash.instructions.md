---
description: "Use when writing or editing Bash or shell scripts. Covers variable declarations, quoting rules, naming conventions, portability, and distro-agnostic practices."
applyTo: "**/*.sh"
---
## Bash & Other UNIX Shells

- Variables inside functions must be declared with `local` whenever possible.
- Never embed Python in shell scripts unless explicitly asked.
- Always write distro-agnostic code: use only POSIX-standard or universally available commands, and avoid paths or tools specific to any particular Linux distribution.
- Always use environment variables for paths instead of hardcoded values — e.g. `${HOME}`, `${XDG_CONFIG_HOME}`, `${XDG_DATA_HOME}`, `${XDG_CACHE_HOME}`. Never hardcode paths like `/home/user/` or `/etc/`.
- Constant strings (no variable references or command substitutions) must use single quotes: `'constant string'`. Strings that reference variables or call commands must use double quotes: `"Value is: ${VAR}"` / `"Today is: $(date)"`.
- Variable naming: all uppercase, always referenced with surrounding curly braces — `${VAR_NAME}`, never `$var_name`.
- Function naming: all lowercase, words separated by underscores — `my_function`, never `myFunction` or `MY_FUNCTION`.
