---
description: "Enforces fixed prose fidelity for GitHub markdown templates. Prose must be copied exactly; only placeholders and comments may change."
applyTo: "**/*.md"
---

# GitHub Markdown Template Prose Fidelity

When generating or revising any GitHub markdown document from a template (`README.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `PRIVACY.md`, `ROADMAP.md`), the following rule is absolute:

## Fixed Prose Is Immutable

**All template prose outside of `[[PLACEHOLDER]]` tokens and `<!-- HTML comments -->` must be copied byte-for-byte into the output.** This includes:

- Headings (text, emoji, punctuation, capitalisation)
- Paragraphs and sentences
- List markers and bullet phrasing
- Table headers and fixed cell text
- Code fence annotations and fixed code lines
- Mermaid diagram directives and fixed labels
- Footnotes, blockquotes, and horizontal rules
- Whitespace and line breaks exactly as written in the template

## What May Change

Only these elements may be modified during generation:

1. **Scalar placeholders** — `[[UPPER_SNAKE_CASE]]` tokens replaced with single evidence-based values
2. **Content placeholders** — `[[CONTENT_PLACEHOLDER]]` tokens expanded into complete Markdown (paragraphs, lists, tables, code blocks)
3. **Block placeholders** — `[[[BLOCK_PLACEHOLDER]]]` tokens expanded into complete sections
4. **Repeatable examples** — Rows, bullets, or subsections duplicated only when the template explicitly says `Repeat` or `Repeat for each...`
5. **Conditional blocks** — Entire `<!-- Only if ... -->` blocks included or removed in their entirety based on evidence
6. **HTML comments** — All `<!-- ... -->` template comments stripped from final output

## What Must Never Change

- ❌ Rewording, paraphrasing, or "improving" any fixed template sentence
- ❌ Adding, removing, or reordering words in fixed prose
- ❌ Changing heading text, emoji, or punctuation
- ❌ Altering fixed list item phrasing
- ❌ Modifying table header text or fixed column content
- ❌ Adjusting whitespace or line breaks in fixed sections
- ❌ "Correcting" spelling, grammar, or style in template prose
- ❌ Normalising terminology used deliberately in the template

## Enforcement

This rule is validated by the `github-md-template-fidelity` skill. Any output that rephrases fixed template prose will be rejected and must be regenerated from the exact template source.

## Applicable Templates

| Template | Rules |
|----------|-------|
| `github.readme.template.instructions.md` | `github.readme.rules.instructions.md` |
| `github.architecture.template.instructions.md` | `github.architecture.rules.instructions.md` |
| `github.contributing.template.instructions.md` | `github.contributing.rules.instructions.md` |
| `github.code-of-conduct.template.instructions.md` | `github.code-of-conduct.rules.instructions.md` |
| `github.security.template.instructions.md` | `github.security.rules.instructions.md` |
| `github.privacy.template.instructions.md` | `github.privacy.rules.instructions.md` |
| `github.roadmap.template.instructions.md` | `github.roadmap.rules.instructions.md` |

When working with any of these files, read both the template and its rules file completely before generating output.