---
description: "Use when creating or revising the GitHub Release workflow for a repository that hosts a NuGet package. Provides the canonical template for github-release.yml."
applyTo: ".github/workflows/github-release.yml"
---

Use the canonical template `skills/github-actions-workflow/templates/github-release-nuget.yml` for github-release.yml, and its rules `skills/github-actions-workflow/rules/github-release-nuget.md`.

Use this template only for repositories that host a NuGet package. For a compilable .NET project that builds release assets, use `prompts/instructions/github/actions/github.actions.workflows.dotnet.github-release.instructions.md` instead. For an Android project that builds an APK release artefact through Gradle, use `prompts/instructions/github/actions/github.actions.workflows.android.github-release.instructions.md` instead.

The `[[NUGET_PACKAGE_NAME]]` placeholder must be replaced with the NuGet package ID.

Apply the complete `github-actions-workflow` skill in `skills/github-actions-workflow/SKILL.md` for the cross-file procedure, documentation synchronisation, fidelity contract, and validation.
