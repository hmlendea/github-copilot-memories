---
description: "Use when the user inquires regarding revising, creating, or generating a ROADMAP.md. Auto-invoked by requests such as 'revise the roadmap', 'create a roadmap', 'compose the roadmap', or 'generate the roadmap'. Populates project-specific priorities and applies the standard structure and conditional sections."
applyTo: "ROADMAP.md"
---

Generate or revise the `ROADMAP.md` for this GitHub repository using the `github.roadmap.template.instructions.md` template.

If a `ROADMAP.md` previously exists, preserve any content that is accurate and current, and revise only what has changed or is absent. If no `ROADMAP.md` exists, create one from commencement.

Use the exact template wording for fixed sections. Do not reword, paraphrase, or alter `## Support` or `## Contribution`; only replace placeholder tokens such as `[[Project Title]]`, `[[GITHUB_REPO_USERNAME]]`, and `[[GITHUB_REPO_NAME]]`.

Fill in all `[[PLACEHOLDER]]` values from the actual project. Remove any section or comment that is not applicable (refer to inline guidance). Do not leave placeholder text, template comments, or example rows in the final output.

## Mandatory editing rules

When updating an existing ROADMAP.md:
- Never delete ROADMAP.md.
- Never use `*** Delete File`.
- Never recreate ROADMAP.md with `create_file`.
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
