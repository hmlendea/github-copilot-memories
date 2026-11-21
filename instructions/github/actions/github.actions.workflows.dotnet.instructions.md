---
description: "Use when creating or revising the .NET GitHub Actions workflow file. Provides the canonical template for dotnet.yml."
applyTo: ".github/workflows/dotnet.yml"
---

Use the canonical template `skills/github-actions-workflow/templates/dotnet.yml` for `dotnet.yml`, and its rules `skills/github-actions-workflow/rules/dotnet.md`.

The template must remain exactly as written, with only these exceptions:

- `[[DOTNET_PROJECT_PATH]]` must be replaced with the repository-relative path of the primary project file whose `TargetFramework` determines the .NET version; the `Determine the .NET version` step derives `dotnet-version` from that file.
- If the project uses MonoGame, add the MonoGame setup steps exactly as shown in the template, immediately before `Restore dependencies`.

Apply the complete `github-actions-workflow` skill in `skills/github-actions-workflow/SKILL.md` for the cross-file procedure, documentation synchronisation, fidelity contract, and validation.
