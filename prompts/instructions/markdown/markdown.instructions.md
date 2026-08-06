---
description: "Use when writing or editing Markdown files. Covers Markdown list formatting conventions."
applyTo: "**/*.md"
---

## Markdown

### Intendation
- Use two spaces for each indentation level.
- Do not use tabs for indentation.

### Lists

- When a list is introduced by a sentence ending with a colon, place the first list item on the immediately following line. Do not insert a blank line.

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
