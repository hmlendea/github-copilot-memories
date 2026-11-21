---
description: "Use when creating or revising the GitHub Release workflow for a content-only or packaged repository, such as a game mod or asset pack. Provides the canonical template for github-release.yml."
applyTo: ".github/workflows/github-release.yml"
---

Use the canonical template `skills/github-actions-workflow/templates/github-release-mod.yml` for `.github/workflows/github-release.yml`, and its rules `skills/github-actions-workflow/rules/github-release-mod.md`.

Use this template only for content-only or packaged repositories whose distributable content is committed rather than compiled — game mods, asset packs, and the like. For a compilable .NET project that builds release assets, use `instructions/github/actions/github.actions.workflows.dotnet.github-release.instructions.md` instead. For a repository that hosts a NuGet package, use `instructions/github/actions/github.actions.workflows.nuget.github-release.instructions.md` instead. For an Android project that builds an APK release artefact through Gradle, use `instructions/github/actions/github.actions.workflows.android.github-release.instructions.md` instead. For an Electron project, use `instructions/github/actions/github.actions.workflows.electron.github-release.instructions.md` instead.

The template must remain exactly as written, with only the placeholders replaced:

- `[[RELEASE_ASSET_LABEL]]` must be replaced with the release archive label, equal to the packaged directory name and the mod descriptor base name (for example `ui-deposit-blockers`).
- `[[RELEASE_ASSETS_LIST]]` must be replaced with the assets to archive, as a double-quoted, space-separated list of paths in the checked-out tag (for example `"my-mod/" "my-mod.mod"`).

Do not compute, append, or publish a checksum; the release body is left exactly as the maintainer wrote it.

Apply the complete `github-actions-workflow` skill in `skills/github-actions-workflow/SKILL.md` for the cross-file procedure, documentation synchronisation, fidelity contract, and validation.
