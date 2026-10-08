---
description: "Rules for creating or revising CONTRIBUTING.md files."
applyTo: "CONTRIBUTING.md"
---

Generate or revise the `CONTRIBUTING.md` for this GitHub repository using the `github.contributing.template.instructions.md` template.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `CONTRIBUTING.md` creation or revision and overrides conflicting instructions.

### Generation Contract

1. Start from `github.contributing.template.instructions.md` and process it from top to bottom.
2. Resolve every `Always include` and `Only if` directive from repository evidence before composing content.
3. When `CODE_OF_CONDUCT.md`, `SECURITY.md`, `ROADMAP.md`, or similar policy documents exist or are being generated, ensure the CONTRIBUTING contains the corresponding section or link unless that section already exists and remains accurate.
4. Remove each inapplicable conditional block in its entirety, including its heading, body, example rows, associated badge, and directive comment.
5. For every included block, preserve the template-defined heading, relative order, and fixed prose. Replace only placeholders, repeatable examples, and content explicitly designated by comments.
6. Replace scalar placeholders such as `[[PROJECT_TITLE]]` with one evidence-based value.
6. Expand content placeholders such as `[[DEVELOPMENT_SETUP]]`, `[[TESTING_INSTRUCTIONS]]`, and `[[RELEASE_INSTRUCTIONS]]` into the complete Markdown required by that block, including paragraphs, lists, tables, or fenced code blocks.
7. Duplicate rows, list items, or other examples only when an adjacent template comment says `Repeat` or otherwise expressly permits repetition. When adjacent directives define mutually exclusive variants with identical headings, include exactly one matching variant.
8. Remove an optional placeholder together with its containing conditional block when no evidenced content applies. Never preserve an empty heading, table, list, or code block.
9. Additional sections are permitted only when genuinely material repository information has no suitable template section. Position each addition after the nearest related template section without reordering template-defined sections.
10. Apply language, spelling, and phrasing rules to placeholder values and additive content. Do not rephrase fixed template prose while generating a CONTRIBUTING.
11. Use project-native commands from scripts, manifests, task definitions, CI workflows, or existing documentation. The strict template does not impose a framework or toolchain.
12. Remove all template comments and unused examples from the final CONTRIBUTING.

### Evidence Requirements

Use the subsequent evidence priority:
1. Repository source, documentation, manifests, configuration examples, scripts, workflows, and policy files
2. Git metadata, release tags, package metadata, and configured repository remotes
3. Public repository metadata, package registries, hosted documentation, and deployment metadata when accessible
4. One concise user clarification when a mandatory value remains indeterminate

Do not infer unsupported capabilities, compatibility, guarantees, package availability, support channels, security conduct, or project status. Never expose credentials, secret values, personal data, private endpoints, or internal operational details.

### Placeholder Rules

- Placeholder names use uppercase snake case enclosed by double brackets.
- A content placeholder may expand to multiple Markdown lines.
- Repeatable examples must be duplicated once per evidenced record and then have their placeholder row or item removed.
- `[[DEFAULT_BRANCH]]` must reflect repository metadata; do not presume `master` or `main`.
- `[[CODE_OF_CONDUCT_DOCUMENT_LINK]]` must expand to a Markdown link labelled `Code of Conduct` whose target is the verified repository-relative document path.
- `[[SECURITY_DOCUMENT_LINK]]` must expand to a Markdown link labelled `Security Policy` whose target is the verified repository-relative document path.
- `[[LICENSE_TITLE]]` must reflect the repository licence without inference.
- Badge placeholders must expand to complete linked badge Markdown from a configured provider.
- Generic placeholders such as `[[ADDITIONAL_SECTIONS]]` are removed when no additional evidenced records exist.