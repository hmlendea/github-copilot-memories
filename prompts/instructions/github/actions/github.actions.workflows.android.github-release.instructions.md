---
description: "Use when creating or revising the GitHub Release workflow for an Android project. Provides the canonical template for github-release.yml."
applyTo: ".github/workflows/github-release.yml"
---

Use the canonical template `skills/github-actions-workflow/templates/github-release-android.yml` for `.github/workflows/github-release.yml`, and its rules `skills/github-actions-workflow/rules/github-release-android.md`.

Use this template only for Android projects that build an APK release artefact through Gradle. For a compilable .NET project that builds release assets, use `prompts/instructions/github/actions/github.actions.workflows.dotnet.github-release.instructions.md` instead. For a repository that hosts a NuGet package, use `prompts/instructions/github/actions/github.actions.workflows.nuget.github-release.instructions.md` instead.

The template must remain exactly as written, with only the placeholders replaced:

- `[[REPOSITORY_JAVA_VERSION]]` must be replaced with the Java (JDK) version used in the repository, consistent with `sourceCompatibility`, `targetCompatibility`, and `jvmTarget` in the Gradle build.
- `[[RELEASE_APK_PATH]]` must be replaced with the repository-relative path of the release APK produced by `./gradlew clean assembleRelease`.
- `[[RELEASE_ASSET_LABEL]]` must be replaced with the release asset label used to name the published APK.

Apply the complete `github-actions-workflow` skill in `skills/github-actions-workflow/SKILL.md` for the cross-file procedure, documentation synchronisation, fidelity contract, and validation.
