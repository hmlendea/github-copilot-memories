---
description: "Use when creating or revising the GitHub Release workflow for an Android project. Provides the canonical template for github-release.yml."
applyTo: ".github/workflows/github-release.yml"
---

Use the canonical template `skills/github-actions-workflow/templates/github-release-android.yml` for `.github/workflows/github-release.yml`, and its rules `skills/github-actions-workflow/rules/github-release-android.md`.

Use this template only for Android projects that build an APK release artefact through Gradle. For a compilable .NET project that builds release assets, use `instructions/github/actions/github.actions.workflows.dotnet.github-release.instructions.md` instead. For a repository that hosts a NuGet package, use `instructions/github/actions/github.actions.workflows.nuget.github-release.instructions.md` instead.

The template must remain exactly as written, with only the placeholders replaced:

- `[[REPOSITORY_JAVA_VERSION]]` must be replaced with the Java (JDK) version used in the repository, consistent with `sourceCompatibility`, `targetCompatibility`, and `jvmTarget` in the Gradle build.
- `[[RELEASE_APK_PATH]]` must be replaced with the repository-relative path of the signed release APK produced by `./gradlew clean assembleRelease`.
- `[[DEBUG_APK_PATH]]` must be replaced with the repository-relative path of the debug APK produced by `./gradlew assembleDebug`.
- `[[KEYSTORE_FILE_NAME]]` must be replaced with the keystore file name written by the signing-restore step.
- `[[RELEASE_ASSET_LABEL]]` must be replaced with the release asset label used to name the published APKs.

The workflow is incomplete until the release signing material is bootstrapped. Generate the keystore and the git-ignored `keystore.properties` at the repository root, then present the four `gh secret set` commands to the user, instructing the user to run them from the repository root and stating that the values are read locally and are not printed. After the user confirms that the secrets are registered, delete the local keystore file and confirm the deletion.

Apply the complete `github-actions-workflow` skill in `skills/github-actions-workflow/SKILL.md` for the cross-file procedure, documentation synchronisation, fidelity contract, and validation.
