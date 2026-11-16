Generate or revise the `CONTRIBUTING.md` for this GitHub repository using the `templates/contributing.md` template.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `CONTRIBUTING.md` creation or revision and overrides conflicting instructions. Strict fidelity applies **only to personal repositories owned by the current git user** (GitHub owner type `User` and owner matching the current git user); organization-owned repositories and repositories owned by another user are out of strict-fidelity scope. If the user explicitly requests the templates, strict fidelity applies regardless of repository ownership.

### Generation Contract

**MANDATORY INCLUSION RULE:** Every section marked with `<!-- Only if ... -->` in the template MUST be included in the final CONTRIBUTING.md when its condition is satisfied. Do not omit conditional sections whose conditions are met. Remove the entire conditional block (including heading, body, and directive comment) only when the condition is NOT met.

1. Start from `templates/contributing.md` and process it from top to bottom.
2. Resolve every `Always include` and `Only if` directive from repository evidence before composing content.
3. When `CODE_OF_CONDUCT.md`, `SECURITY.md`, `ROADMAP.md`, or similar policy documents exist or are being generated, ensure that every affected corresponding section in `CONTRIBUTING.md` is fully updated to match the template-defined content, including all conditional sections, placeholders, and fixed prose. If the section is missing, add it as per the template. Preserve the complete template-defined section; a link alone is insufficient when the template defines a dedicated section.
4. When CONTRIBUTING.md is created or updated, update the entire corresponding `## 🤝 Contributing` section in `README.md` from the README template. Preserve its template-defined heading and fixed prose; a link to `CONTRIBUTING.md` alone is insufficient.
5. When `CODE_OF_CONDUCT.md`, `SECURITY.md`, or `LICENSE` is created or updated, update the complete corresponding `## 📜 Code of Conduct`, `## 🔒 Security`, or `## 📄 License` section in `CONTRIBUTING.md` from this template. Preserve the section heading and fixed prose; a link alone is insufficient.
6. The `## 💝 Donations` section is included, together with the Donate badge before the `# Contributing to` title, only when `.github/FUNDING.yml` exists. Remove the section, its heading, body, badge, and directive comment in their entirety when it does not. Resolve `[[FUNDING_URL]]` as described in the placeholder rules; the section heading and fixed prose are immutable.
7. Remove each inapplicable conditional block in its entirety, including its heading, body, example rows, associated badge, and directive comment.
8. For every included block, preserve the template-defined heading, relative order, and fixed prose. Replace only placeholders, repeatable examples, and content explicitly designated by comments.
9. Replace scalar placeholders such as `[[PROJECT_TITLE]]` with one evidence-based value.
10. Expand content placeholders such as `[[DEVELOPMENT_SETUP]]`, `[[TESTING_INSTRUCTIONS]]`, and `[[RELEASE_INSTRUCTIONS]]` into the complete Markdown required by that block, including paragraphs, lists, tables, or fenced code blocks.
11. Duplicate rows, list items, or other examples only when an adjacent template comment says `Repeat` or otherwise expressly permits repetition. When adjacent directives define mutually exclusive variants with identical headings, include exactly one matching variant.
12. Remove an optional placeholder together with its containing conditional block when no evidenced content applies. Never preserve an empty heading, table, list, or code block.
13. Additional sections are permitted only when genuinely material repository information has no suitable template section. Position each addition after the nearest related template section without reordering template-defined sections.
14. Apply language, spelling, and phrasing rules to placeholder values and additive content. Do not rephrase fixed template prose while generating a CONTRIBUTING.
15. Use project-native commands from scripts, manifests, task definitions, CI workflows, or existing documentation. The strict template does not impose a framework or toolchain.
16. Remove all template comments and unused examples from the final CONTRIBUTING.

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
- `[[FUNDING_URL]]` must expand to the author's donation link. When the user or repository explicitly provides one, use it verbatim. Otherwise take it from `.github/FUNDING.yml`: use the `custom` field value verbatim; when `custom` is missing or empty, use the `github` field as `https://github.com/sponsors/<github>`. Never invent a donation link.
- `[[CODE_OF_CONDUCT_DOCUMENT_LINK]]` must expand to a Markdown link labelled `Code of Conduct` whose target is the verified repository-relative document path.
- `[[SECURITY_DOCUMENT_LINK]]` must expand to a Markdown link labelled `Security Policy` whose target is the verified repository-relative document path.
- `[[LICENSE_TITLE]]` must reflect the repository licence without inference.
- Badge placeholders must expand to complete linked badge Markdown from a configured provider.
- Generic placeholders such as `[[ADDITIONAL_SECTIONS]]` are removed when no additional evidenced records exist.

## Conditional Content Rules

### Badges

Include badges only when their state and destination can be verified:

| Badge | Condition | Notes |
|-------|-----------|-------|
| Donate | `.github/FUNDING.yml` exists. | Place before the document title and resolve `[[FUNDING_URL]]` from `.github/FUNDING.yml`. |

### Sections

Process the subsequent sections in table order. This order is canonical after conditional omissions.

**MANDATORY:** When a section's condition is met, the section MUST be included in the CONTRIBUTING.md. Do not omit sections whose conditions are satisfied.

| Section | Condition | Required Content or Placement |
|---------|-----------|-------------------------------|
| `# Contributing to [[PROJECT_TITLE]]` | Always. | Expand `[[PROJECT_TITLE]]` with the evidence-based project title. |
| `## 📑 Table of Contents` | Always. | Include every final `##`, `###`, and `####`; indent nested levels by two spaces and omit heading emojis from labels and anchors. |
| `## 🤝 Contributing` | Always. | Preserve the fixed base text and resolve conditional bullets. |
| `### Reporting Issues` | The repository uses GitHub Issues. | Preserve the fixed bullets. |
| `### Suggesting Enhancements` | The repository accepts feature requests. | Resolve the nested ROADMAP condition only. |
| `### Code Contributions` | Always. | Preserve its `####` subsections and resolve only their conditionals and placeholders. |
| `### Code Style` | A style guide or linter configuration exists. | Resolve `[[CODE_STYLE_GUIDE]]` and `[[FORMAT_COMMAND]]`. |
| `### Testing` | Tests exist. | Resolve `[[TEST_COMMAND]]` and `[[TEST_SPECIFIC_COMMAND]]`. |
| `### Documentation` | Documentation exists or is generated. | Resolve the dependency-package bullet conditional. |
| `## 📜 Code of Conduct` | `CODE_OF_CONDUCT.md` exists. | Preserve its fixed sentence and resolve only `[[CODE_OF_CONDUCT_DOCUMENT_LINK]]`. |
| `## 🔒 Security` | `SECURITY.md` exists. | Preserve its fixed sentence and resolve only `[[SECURITY_DOCUMENT_LINK]]`. |
| `## 💝 Donations` | `.github/FUNDING.yml` exists. | Preserve the fixed prose and resolve only `[[FUNDING_URL]]`. |
| `## 📄 License` | `LICENSE` exists. | Preserve the fixed sentence and resolve only `[[LICENSE_TITLE]]`. |
| `## 🙏 Recognition` | A contributors list or recognition mechanism exists. | Resolve `[[RECOGNITION_LOCATION]]`. |
| `## ❓ Getting Assistance` | Support channels exist. | Resolve `[[SUPPORT_CHANNELS]]`. |

### Mandatory Validation Before Final Output

- Every included heading matches the template exactly and follows template order after conditional omissions.
- Every included badge corresponds to an evidenced funding configuration.
- Every mandatory section is present.
- Every conditional section has evidence, substantive content, and no filler rows.
- Every additional section is repository-relevant, substantive, and purely additive.
- Fixed template prose has not been rephrased, including `## 💝 Donations` and `## 📄 License`.
- No `[[PLACEHOLDER]]`, template comment, unused example, empty heading, empty table, or empty code block remains.
- The Table of Contents includes every final `##`, `###`, and `####` heading in order, with two-space indentation per level and no heading emoji in labels or anchors.
- Commands, paths, versions, links, defaults, and compatibility statements agree with repository evidence.
- No secret, credential, personal datum, private endpoint, or unsafe remote-script instruction is exposed.
