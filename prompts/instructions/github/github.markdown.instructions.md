---
description: "Use for Markdown edits in GitHub repositories. Covers verified repository-relative links."
applyTo: "**/*.md"
---

## Markdown

### GitHub Repository File Links

- Link every repository file referenced by a Markdown document using a verified repository-relative Markdown link, and confirm that the referenced path exists.
- Link reference repository directories using verified repository-relative Markdown links, and confirm that the referenced path exists. Same-document heading links may remain fragment-only links.
- When creating or revising a referenced document, inspect every repository Markdown document that contains a corresponding template-defined section and synchronise the entire section from that document's template. Preserve the heading and fixed prose; a link alone is insufficient.

### HTML Comments

- After creating or revising GitHub repository Markdown files, check that no `<!-- ... -->` elements exist.
- Address the text within these elements and then remove them.
