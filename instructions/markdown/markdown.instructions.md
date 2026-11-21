---
description: "Use when writing or editing Markdown files. Covers Markdown list formatting conventions."
applyTo: "**/*.md"
---

## Markdown

### Indentation
- Use two spaces for each indentation level.
- Do not use tabs for indentation.

### Lists

- If a sentence ends with a colon and is followed by a list, the first list item MUST be on the next line immediately.
- NEVER insert a blank line between the introducing line and the first list item.
- This applies to unordered lists (`-`, `*`, `+`), ordered lists (`1.`), and task lists (`- [ ]`).

Incorrect:
```markdown
Roman designs eventually improve:

- medical instruments
- electromechanical communication
- archive indexing
- legal and technical standardisation
  - distances
  - weights
  - currencies
  - etc.
```

Correct:
```markdown
Roman designs eventually improve:
- medical instruments
- electromechanical communication
- archive indexing
  - legal and technical standardisation
  - distances
  - weights
  - currencies
  - etc.
```

### Headings

- Headings must use title case.

Example:
```markdown
## The Dawn of Man
```
