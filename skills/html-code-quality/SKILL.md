---
name: html-code-quality
description: "Use when editing or reviewing HTML pages or templates for TODO and FIXME comments, commented-out markup, doctype, title, and lang declarations, unique id values, nested scripts, ARIA roles and properties, keyboard focus, tabindex, accesskey, event attributes, text alternatives, labels, autocomplete tokens, captions, autoplay, list and table structure, obsolete elements and attributes, meta refresh, viewport zoom, or analyser diagnostics, and to apply the complete HTML rule catalogue: naming, layout, and comments, ARIA roles and properties, events, keyboard, and focus, text alternatives, forms, and media, lists and tables, and platform APIs. Preserves access for screen reader, keyboard, and voice control users, standards-mode parsing, and valid document structure even without analyser diagnostics."
---

# HTML Code Quality

Apply each relevant section prior to editing and verify it prior to completion. These are preventive requirements, not merely responses to analyser diagnostics. Do not refactor unrelated code or install analysers solely for this checklist.

Use the [HTML security instructions](../../instructions/html/html.security.instructions.md) for security guidance. Load them if absent from context. Required external contracts, including server-side template syntax, framework conventions, and generated files, take precedence; report exceptions rather than silently weakening a rule.

## Rule Catalogue

The `references/rules-*.md` files contain one directive per HTML quality and reliability rule (50 rules); the [security instructions](../../instructions/html/html.security.instructions.md) contain the 3 security rules. Load every reference whose topic the change touches, and the security instructions for any security-relevant change.

- Precedence: explicit local instructions and required external contracts prevail over a catalogue directive. Report each conflict instead of silently selecting a policy.
- Markers: **Local precedence** records a local deviation.
- Known deviations: none. No local instruction conflicts with a catalogue directive; the common coding and naming instructions, including their `TODO` comment format, do not apply to HTML files.

| Concern | Threshold |
| --- | --- |
| Redundant ARIA roles | Only `navigation` on `<nav>` is permitted |

| Topic | Reference |
| --- | --- |
| `TODO` and `FIXME` comments, commented-out markup, `<!DOCTYPE>`, `<title>`, `lang`, unique `id` values, nested `<script>` | [rules-naming-and-layout.md](references/rules-naming-and-layout.md) |
| `aria-*` values and support, required properties, valid, redundant, interactive, and non-interactive roles, landmark labels, accessible names | [rules-aria-roles-and-properties.md](references/rules-aria-roles-and-properties.md) |
| `aria-activedescendant`, anchors as buttons, `tabindex`, `accesskey`, event attributes, keyboard equivalents of mouse events | [rules-events-and-focus.md](references/rules-events-and-focus.md) |
| `alt` text, frame titles, `<object>` fallbacks, anchor and heading content, labels, `autocomplete`, captions, `autoplay` | [rules-text-alternatives-and-media.md](references/rules-text-alternatives-and-media.md) |
| List containers, data table headers, layout tables, `headers`, `scope`, and `id` on header cells | [rules-lists-and-tables.md](references/rules-lists-and-tables.md) |
| Obsolete elements and attributes, `<meta>` refresh, viewport zoom, Flash embedding | [rules-platform-apis.md](references/rules-platform-apis.md) |

## Verification

- Review every applicable section and rule reference, not solely the reported diagnostic.
- Execute existing focused checks for the changed files, for example HTML validation, accessibility audits, or end-to-end tests that the repository employs.
- Verify keyboard operation, focus order, accessible names, and text alternatives where affected. Report unexecuted checks and unresolved diagnostics; do not present static inspection as runtime verification.
