# GitHub Actions Rules: Commands And Containers

One directive per GitHub Actions rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Execute package installations, upgrades, and uninstallations non-interactively with an explicit consent flag: `apt-get -y`, `apt -y` (or `--yes`/`--assume-yes`), `aptitude -y` (or `--assume-yes`), and `gdebi --n`; commands that never prompt, for example `apt --simulate`, are exempt. **Local precedence:** the canonical .NET workflow template installs MonoGame fonts with `sudo apt install` and no consent flag; retain that fixed template content within template-fidelity scope and report the occurrence.
- Prefix glob expansions with `./` or precede them with `--` so that expanded filenames never become command options: use `rm ./*` or `rm -- *`, never `rm *`.
- Reference every container image (`container:` or its `image:` key) by a specific version tag or an `@sha256:` digest; never omit the tag or use `latest`.
