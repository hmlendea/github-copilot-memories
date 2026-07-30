---
description: "Use when writing or editing Bash or shell scripts. Covers naming conventions."
applyTo: "**/*.sh"
---
## Bash & Other UNIX Shells

### Variables & Constants

- Variable naming: all uppercase, always referenced with surrounding curly braces: `${VAR_NAME}`, never `$var_name`.
- Always use environment variables for paths instead of hardcoded values, e.g. `${HOME}`, `${XDG_CONFIG_HOME}`, `${XDG_DATA_HOME}`, `${XDG_CACHE_HOME}`. Never hardcode paths like `/home/user/` or `/etc/`.

### Functions

- Function naming: all lowercase, words separated by underscores: `my_function`, never `myFunction` or `MY_FUNCTION`.
