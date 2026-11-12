---
description: "Use when creating or revising GitHub Actions workflow files. Defines canonical workflow file names for specific delivery targets."
applyTo: ".github/workflows/*.{yml,yaml}"
---

## Workflow File Naming Standard

When creating or revising workflow files, use these canonical file names:

- .NET Security workflows: `security.yml`
- .NET workflows: `dotnet.yml`
- Bash workflows: `bash.yml`
- GitHub Release workflows: `github-release.yml`
- Nexus Mods workflows: `nexus-mods-release.yml`
- NuGet.org release workflows: `nuget-release.yml`
- Release asset upload workflows: `release-assets.yml`
- Steam Workshop workflows: `steam-workshop-release.yml`

Do not use alternative names for these workflow categories unless the user explicitly requests an exception.

## Documentation Updates

When creating or revising GitHub Actions workflows, update all relevant documentation, repository Markdown files, README badges, and any other affected documentation to reflect the changes.

This is a cross-file procedure. Apply the complete `github-actions-workflow` skill in `skills/github-actions-workflow/SKILL.md`, which holds the canonical workflow templates under `skills/github-actions-workflow/templates/`, their rules under `skills/github-actions-workflow/rules/`, the fidelity contract, and the validator. Workflow work is incomplete until every affected document has been synchronised and validated. A workflow-only change is never sufficient.
