---
description: "Rules for creating or revising SECURITY.md files."
applyTo: "SECURITY.md"
---

Generate or revise the `SECURITY.md` for this GitHub repository using the `github.security.template.instructions.md` template.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `SECURITY.md` creation or revision and overrides conflicting instructions.

### Generation Contract

1. Use an exact copy of `github.security.template.instructions.md`; preserve every mandatory template section, subsection, table, bullet structure, heading order, punctuation, and whitespace layout.
2. Replace only `[[PLACEHOLDER]]` tokens. Apply language rules only to inserted values; never rephrase, normalise, correct, or improve fixed text.
3. Add only genuinely relevant sections that neither replace, rename, reorder, nor omit template content.
4. Resolve template-marked conditional blocks exactly as written; core sections and headings remain mandatory.
5. Ensure `README.md` contains an accurate Security section or link.

### Failure Behaviour

- Unknown required placeholder: cease generation and request one concise clarification. Never produce a partial security policy.

### Mandatory Validation Before Final Output

- Headings match the template exactly in text and order.
- No template-defined section is absent.
- Any added section or subsection is repository-relevant and purely additive.
- No fixed template line was rephrased.
- All resolvable placeholders were replaced.

If a `SECURITY.md` previously exists, preserve any content that is accurate and current, and revise only what has changed or is absent. If no `SECURITY.md` exists, create one from commencement.

Use the exact template wording for fixed sections. Do not reword, paraphrase, or alter `## 🛡️ Supported Versions`, `## 🚨 Reporting a Vulnerability`, or `## 📢 Disclosure Policy`; only replace placeholder tokens such as `[[Latest version or branch, e.g. 2.x]]`, `[[Distribution method, e.g. GitHub Releases]]`, and `[[In-scope category 1]]`.

Fill in all `[[PLACEHOLDER]]` values from the real project. Remove any section or comment that is not applicable (refer to inline guidance). Do not leave placeholder text, template comments, or example rows in the final output.

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
