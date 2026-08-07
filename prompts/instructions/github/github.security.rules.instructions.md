---
description: "Use when the user inquires regarding revising, creating, or generating a SECURITY.md. Auto-invoked by requests such as 'revise the security policy', 'create a security policy', 'compose the security policy', or 'generate SECURITY.md'. Populates project-specific disclosure scope and supported-version details while applying the standard structure."
applyTo: "SECURITY.md"
---

Generate or revise the `SECURITY.md` for this GitHub repository using the `github.security.template.instructions.md` template.

## Strict Template Fidelity Mode (Default)

This mode applies automatically when the user requests any of the subsequent:
- Revise the security policy
- Create the SECURITY.md file
- Revise the security policy
- Create a security policy
- Generate the security policy
- Compose the security policy

### Precedence

- These rules supersede all other SECURITY generation instructions.
- If any other rule conflicts with strict fidelity, strict fidelity prevails.

### Generation Contract

1. Commence from an exact copy of `github.security.template.instructions.md`, preserving all template-defined section order, heading order, punctuation, and whitespace layout.
2. Replace only `[[PLACEHOLDER]]` tokens.
3. Do not rephrase fixed template text.
4. Do not remove any template-defined section, table, bullet structure, or subsection.
5. Additional sections or subsections may be added when they are genuinely relevant to the repository, but they must be purely additive and must not replace, rename, reorder, or omit any template-defined section, table, or subsection.
6. Do not normalise, correct, or improve fixed template wording.
7. Language, spelling, and phrasing rules apply only to values inserted into placeholders, not to fixed template literals.
8. Resolve template-marked conditional blocks exactly as written in template comments (for example, lines marked with `Only if ...`). Template-defined core sections and headings remain mandatory and must not be removed.

### Failure Behaviour

- If any required placeholder value is unknown, cease generation and inquire one concise clarification question.
- Do not produce a partial security policy.

### Mandatory Validation Before Final Output

- Headings match the template exactly in text and order.
- No template-defined section is absent.
- Any added section or subsection is repository-relevant and purely additive.
- No fixed template line was rephrased.
- All resolvable placeholders were replaced.

If a `SECURITY.md` previously exists, preserve any content that is accurate and current, and revise only what has changed or is absent. If no `SECURITY.md` exists, create one from commencement.

Use the exact template wording for fixed sections. Do not reword, paraphrase, or alter `## 🛡️ Supported Versions`, `## 🚨 Reporting a Vulnerability`, or `## 📢 Disclosure Policy`; only replace placeholder tokens such as `[[Latest version or branch, e.g. 2.x]]`, `[[Distribution method, e.g. GitHub Releases]]`, and `[[In-scope category 1]]`.

Fill in all `[[PLACEHOLDER]]` values from the real project. Remove any section or comment that is not applicable (refer to inline guidance). Do not leave placeholder text, template comments, or example rows in the final output.

## Mandatory editing rules

When updating an existing SECURITY.md:

- Never delete SECURITY.md.
- Never use `*** Delete File`.
- Never recreate SECURITY.md with `create_file`.
- Modify the existing file only with `apply_patch` using `*** Update File`.
- A complete revision must still use `*** Update File`.
- Preserve the file path and file identity throughout the operation.
- If an in-place patch cannot be produced, cease and explain the problem instead of deleting the file.

## Conditional Content Rules

### Sections

Include these sections only when the specified conditions are met:

| Section | Condition | Notes |
|---------|-----------|-------|
| Table of Contents | Always include. | Include all `##`, `###`, and `####` headings in order. |
| Scope | Always include. | Distinguish in-scope and out-of-scope report categories. |
| Disclosure Policy | Always include. | State coordinated disclosure expectations. |
| Safe Harbour | A good-faith testing statement exists or is required by maintainers. | Omit when unavailable. |
| Recognition | The project publicly acknowledges reporters. | Omit when unavailable. |

### Content Rules

- Provide an explicit instruction not to disclose vulnerabilities publicly before maintainers validate and remediate them.
- Ensure supported versions reflect genuine maintenance status.
- By default, indicate only the latest maintained version or branch as supported.
- Add additional rows only when maintainers explicitly support or deprecate other versions.
- Ensure each supported-version row includes the distribution method column.
- If no supported versions are maintained, state this transparently and include a migration recommendation.

### Always Include

- Introductory summary describing scope and objective of the policy.
- `## 🚨 Reporting a Vulnerability` with direct maintainer contact guidance.
- `## 📢 Disclosure Policy` with coordinated disclosure expectations.

## Styling & Format Rules

- Respect the instructions in `language.instructions.md` for all SECURITY text, including spelling, phrasing, and language conventions.
- Prefix `##` headings with their emoji as demonstrated in the template (omit only if existing SECURITY.md uses no emojis and repository tone is formal).
- Remove all HTML comments from final output.
- Always fill `[[PLACEHOLDER]]` values with real project details; omit template comments and example rows.
- Maintain concise, explicit, and actionable security guidance.
