---
description: "Rules for creating or revising ROADMAP.md files."
applyTo: "ROADMAP.md"
---

Generate or revise the `ROADMAP.md` for this GitHub repository using the `github.roadmap.template.instructions.md` template.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `ROADMAP.md` creation or revision and overrides conflicting instructions.

### Generation Contract

1. Use an exact copy of `github.roadmap.template.instructions.md`; preserve every template section, subsection, table, bullet structure, heading order, punctuation, and whitespace layout.
2. Replace only `[[PLACEHOLDER]]` tokens. Apply language rules only to inserted values; never rephrase, normalise, correct, or improve fixed text.
3. Add only genuinely relevant sections that neither replace, rename, reorder, nor omit template content.
4. Include every template-defined section; conditional inclusion and omission are disabled.
5. Ensure `README.md` contains an accurate Roadmap section or link.

### Failure Behaviour

- Unknown required placeholder: cease generation and ask one concise clarification. Never output a partial roadmap.

### Mandatory Validation Before Final Output

- Headings match the template exactly in text and order.
- No template-defined section is missing.
- Any added section or subsection is repository-relevant and purely additive.
- No fixed template line was rephrased.
- All resolvable placeholders were replaced.

If a `ROADMAP.md` previously exists, preserve any content that is accurate and current, and revise only what has changed or is absent. If no `ROADMAP.md` exists, create one from commencement.

Use the exact template wording for fixed sections. Do not reword, paraphrase, or alter `## Support` or `## Contribution`; only replace placeholder tokens such as `[[Project Title]]`, `[[GITHUB_REPO_USERNAME]]`, and `[[GITHUB_REPO_NAME]]`.

Fill in all `[[PLACEHOLDER]]` values from the actual project. Remove any section or comment that is not applicable (refer to inline guidance). Do not leave placeholder text, template comments, or example rows in the final output.

## Conditional Content Rules

### Sections

Include these sections only when the specified conditions are met:

| Section | Condition | Notes |
|---------|-----------|-------|
| Table of Contents | Always include. | Include all `##`, `###`, and `####` headings in order. |
| Current Focus | There are actively prioritised initiatives. | Use concise bullets with status and target period. |
| Planned Labour | There is meaningful forward planning beyond current focus. | Use grouped horizons such as short-term and medium-term. |
| Milestones | Date-based goals exist (quarterly, monthly, or release-based). | Include target period and measurable outcome. |
| Dependencies and Risks | External constraints or notable risks exist. | Omit when no material risk is known. |
| Change History Link | `CHANGELOG.md` exists. | Link to changelog for delivered labour. |
| Related Planning Documents | `ARCHITECTURE.md`, `MIGRATION.md`, `UPGRADING.md`, or `docs/` planning artefacts exist. | Include only relevant links. |
| Contribution | Repository accepts external contributions. | Maintain concise and actionable guidance. |
| Support | Always include. | Use issue tracker link with repository placeholders. |

### Content Rules

- Ensure each roadmap item contains a status indicator and a concise outcome statement.
- Prefer time windows (for example, `Q4 2026`, `Next 30 days`) over exact dates unless exact dates are committed.
- Avoid over-promising; mark uncertain labour as tentative.
- Maintain repository-agnostic wording so it applies to code, assets, books, and documentation.
- Use checklists only for concrete commitments; use bullets for tentative labour.

### Always Include

- Introductory summary describing scope and planning horizon.
- `## Support` with issue link.
- At least one planning section (`Current Focus` or `Planned Labour`).

## Styling & Format Rules

- Respect the instructions in `language.instructions.md` for all ROADMAP text, including spelling, phrasing, and language conventions.
- Prefix `##` headings with their emoji as demonstrated in the template (omit only if existing ROADMAP uses no emojis and repository tone is formal).
- Remove all HTML comments from final output.
- Always fill `[[PLACEHOLDER]]` values with actual project details; omit template comments and example rows.
- Maintain concise and outcome-oriented entries.
