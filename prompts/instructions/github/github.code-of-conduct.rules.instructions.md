---
description: "Rules for creating or revising custom CODE_OF_CONDUCT.md files informed by established open-source community standards."
applyTo: "CODE_OF_CONDUCT.md"
---

Generate or revise `CODE_OF_CONDUCT.md` for this GitHub repository using the `github.code-of-conduct.template.instructions.md` template.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `CODE_OF_CONDUCT.md` creation or revision and overrides conflicting instructions. This means fidelity to the custom template below, not reproduction of any external code of conduct.

### Generation Contract

**MANDATORY INCLUSION RULE:** Every section in the template MUST be included in the final `CODE_OF_CONDUCT.md`. Remove only template instructions and replace only the marked placeholder.

1. Start from `github.code-of-conduct.template.instructions.md` and process it from top to bottom.
2. Preserve the custom template's wording, emoji-prefixed heading order, list markers, and line breaks exactly.
3. Replace only `[[REPORTING_CONTACT]]` with a verified project reporting address or channel.
4. Remove all template comments before writing the final document.
5. Do not replace the custom guidance with text copied from the Contributor Covenant or another external code of conduct.
6. Generate the Table of Contents after finalising the document, including every `##` heading except the Table of Contents heading itself.
7. Use heading text without emojis in Table of Contents link labels, and indent nested entries by two spaces.
8. If `CODE_OF_CONDUCT.md` exists or is being generated, update the entire corresponding `## 📜 Code of Conduct` section in `README.md` from the README template. A link to `CODE_OF_CONDUCT.md` alone is insufficient. Also ensure `CONTRIBUTING.md` links to it when that document exists or is being generated.
9. Use a repository-relative Markdown link for every repository file reference added to another document, and verify that the target exists.
10. Do not expose credentials, personal data, private endpoints, or unverified contact details.

### Placeholder Rules

- `[[REPORTING_CONTACT]]` must be replaced with the project's verified incident-reporting address or channel.
- Do not leave any `[[...]]` placeholder, HTML comment, or template instruction in the final document.
- Do not add external attribution that implies the final document reproduces the Contributor Covenant.

### Mandatory Validation Before Final Output

- All template sections are present and remain in order.
- The reporting contact is verified and actionable.
- The final document contains no unresolved placeholders or HTML comments.
- The custom template wording is unchanged apart from the reporting-contact placeholder.
- The final document contains no unsupported enforcement promises or project claims.
- All required headings have their specified emojis.
- The Table of Contents includes every applicable heading in order, uses emoji-free labels, and links to valid anchors.
- Markdown headings, lists, and links render correctly.
