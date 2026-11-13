---
description: "Use when creating or revising the GitHub Release workflow for a compilable .NET project. Provides the canonical template for github-release.yml."
applyTo: ".github/workflows/github-release.yml"
---

Use the canonical template `skills/github-actions-workflow/templates/github-release-dotnet.yml` for `.github/workflows/github-release.yml`, and its rules `skills/github-actions-workflow/rules/github-release-dotnet.md`.

Use this template only for compilable .NET projects, that is, projects that build to release assets. Do not use it for NuGet packages. For a repository that hosts a NuGet package, use `prompts/instructions/github/actions/github.actions.workflows.nuget.github-release.instructions.md` instead. For an Android project that builds an APK release artefact through Gradle, use `prompts/instructions/github/actions/github.actions.workflows.android.github-release.instructions.md` instead.

The template must remain exactly as written, with only the placeholders replaced:

- `[[DOTNET_PROJECT_PATH]]` must be replaced with the repository-relative path of the primary project file whose `TargetFramework` determines the .NET version (for example `NuciCraft.API/NuciCraft.API.csproj`).
- `[[RELEASE_ASSET_GLOB]]` must be replaced with the repository-relative glob of the release assets produced by the release script (for example `NuciCraft.API/bin/Release/nucicraft-api_*`).

Apply the complete `github-actions-workflow` skill in `skills/github-actions-workflow/SKILL.md` for the cross-file procedure, documentation synchronisation, fidelity contract, and validation.
