---
description: "Use when writing or editing Bash or shell scripts. Covers exception handling."
applyTo: "**/*.sh"
---
## Bash & Other UNIX Shells

### Safety
- Always add `set -euo pipefail` at the top of every non-interactive script. This causes the script to exit immediately on any error (`-e`), treats unset variables as errors (`-u`), and propagates failures through pipelines (`-o pipefail`).

### Error Handling
- Print error messages to stderr: `echo "[ERROR] Message goes here." >&2`.
