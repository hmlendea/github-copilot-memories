---
description: "Use when creating or editing any skill file. Covers the frontmatter contract and the hard 1024-character description limit."
applyTo: "**/SKILL.md"
---

## Skill Frontmatter Contract

- Every `SKILL.md` starts with YAML frontmatter delimited by `---` lines and containing `name` and `description`.
- `name` must equal the containing directory name.
- `description: ` value must be at most **1024 characters**, counted on the raw value as written between the quotes. This is a hard host limit; a longer description is a load error and makes the skill undiscoverable. Verify by measurement, never by estimation.
- Quote the description as a single-line double-quoted scalar and escape nothing unnecessarily. Never use a multi-line or folded scalar.
- An unquoted description fails to parse as soon as it contains `: ` or starts with a reserved YAML indicator, so quoting is mandatory, not stylistic. Verify that the frontmatter parses as YAML before finishing.
- Put discovery keywords in the description and all procedure, examples, tables, and detail in the body or in `references/` files loaded on demand.
- Prefer a uniform frontmatter shape across a family of related skills, so every file in that family is written and reviewed the same way.

## Verification

Measure the description value and parse the frontmatter before finishing:

```bash
python3 - <<'PY'
import re, sys, yaml, pathlib
failed = False
for path in sorted(pathlib.Path('skills').glob('*/SKILL.md')):
    head = re.match(r'^---\n(.*?)\n---\n', path.read_text(encoding='utf-8'), re.S).group(1)
    try:
        data = yaml.safe_load(head)
    except yaml.YAMLError as error:
        print(f'{path}: unparsable frontmatter: {error}')
        failed = True
        continue
    description = str(data.get('description', ''))
    if len(description) > 1024:
        print(f'{path}: description is {len(description)} characters')
        failed = True
    if data.get('name') != path.parent.name:
        print(f"{path}: name does not match directory")
        failed = True
sys.exit(1 if failed else 0)
PY
```

Report the measured length; an unmeasured claim that a description fits is not evidence.
