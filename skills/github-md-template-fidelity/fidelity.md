# GitHub Markdown Template Prose Fidelity

This rule applies **only to personal repositories owned by the current git user** — repositories whose GitHub owner is a personal account (`owner.type == "User"`) and whose owner matches the current git user. Organization-owned repositories and repositories owned by another user are out of strict-fidelity scope; fixed template prose fidelity is not enforced for them. Confirm repository ownership before generating or revising any target document:

```bash
git -C <repo_root> remote get-url origin
gh api repos/<owner>/<repo> --jq .owner.type   # must return "User"
gh api user --jq .login                        # current git user; fallback: git config github.user
```

When the user explicitly requests the templates, this rule applies regardless of who owns the repository or whether it is personal.

When generating or revising any GitHub markdown document from a template (`README.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `PRIVACY.md`, `ROADMAP.md`), the following rule is absolute.

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

## Cross-Document README Synchronisation

When creating or revising a document that is referenced by another template-generated document, update every affected corresponding section in each referencing document from that document's template. Preserve each template-defined heading, fixed prose, order, and whitespace, and replace only permitted placeholders or conditional content. A link to the separate document is not a substitute for synchronising a complete dedicated section. This includes the README sections corresponding to `ARCHITECTURE.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `PRIVACY.md`, `ROADMAP.md`, and `SECURITY.md`, plus the `CONTRIBUTING.md` sections corresponding to `CODE_OF_CONDUCT.md`, `SECURITY.md`, and `LICENSE`.

## Enforcement

This rule is validated by the `github-md-template-fidelity` skill. Any output that rephrases fixed template prose will be rejected and must be regenerated from the exact template source.
