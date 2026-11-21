---
description: "Use when creating or revising the NuGet.org release workflow for a repository that hosts a NuGet package. Provides the canonical template for nuget-release.yml."
applyTo: ".github/workflows/nuget-release.yml"
---

Use the canonical template `skills/github-actions-workflow/templates/nuget-release.yml` for `nuget-release.yml`, and its rules `skills/github-actions-workflow/rules/nuget-release.md`.

The `[[NUGET_PACKAGE_NAME]]` placeholder must be replaced with the NuGet package ID.

The repository must define the `NUGET_USER` secret with the NuGet.org account name associated with the package. NuGet trusted publishing must be configured for the repository so `NuGet/login` can exchange the GitHub Actions OIDC token for a temporary API key.

Apply the complete `github-actions-workflow` skill in `skills/github-actions-workflow/SKILL.md` for the cross-file procedure, documentation synchronisation, fidelity contract, and validation.