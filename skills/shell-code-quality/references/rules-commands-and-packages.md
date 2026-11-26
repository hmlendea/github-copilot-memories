# Shell Rules: Commands And Packages

One directive per Shell rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Prefix glob expansions with `./` or precede them with `--` so that expanded filenames never become command options: use `rm ./*` or `rm -- *`, never `rm *`.
- Execute package installations, upgrades, and uninstallations non-interactively with an explicit consent flag: `apt-get -y`, `apt -y` (or `--yes`/`--assume-yes`), `aptitude -y` (or `--assume-yes`), and `gdebi --n`; commands that never prompt, for example `apt --simulate`, are exempt.
- Use `$(command)` for command substitution, never `` `command` ``.
