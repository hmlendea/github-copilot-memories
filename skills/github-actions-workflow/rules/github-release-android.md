Generate or revise `.github/workflows/github-release.yml` using `templates/github-release-android.yml`.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `github-release.yml` creation or revision and overrides conflicting instructions. Strict fidelity applies **only to personal repositories owned by the current git user** (GitHub owner type `User` and owner matching the current git user); organization-owned repositories and repositories owned by another user are out of strict-fidelity scope. If the user explicitly requests the templates, strict fidelity applies regardless of repository ownership.

### Generation Contract

1. Use this template only for Android projects that build an APK release artefact through Gradle. For a compilable .NET project that builds release assets, use `rules/github-release-dotnet.md` instead. For a repository that hosts a NuGet package, use `rules/github-release-nuget.md` instead.
2. Use an exact copy of `templates/github-release-android.yml`; preserve the workflow `name`, triggers, permissions, job, steps, action versions, indentation, and whitespace layout.
3. The template must remain exactly as written, with only the placeholders replaced.
4. Keep the `temurin` distribution, the `gradle/actions/setup-gradle` step, and the `--no-daemon` flag exactly as written.
5. The `contents: write` permission is required to publish release assets and must remain.

### Placeholders

| Placeholder | Replacement |
|-------------|-------------|
| `[[REPOSITORY_JAVA_VERSION]]` | The Java (JDK) version used in the repository (for example `17` or `21`), consistent with `sourceCompatibility`, `targetCompatibility`, and `jvmTarget` in the Gradle build. |
| `[[RELEASE_APK_PATH]]` | The repository-relative path of the release APK produced by `./gradlew clean assembleRelease` (for example `app/build/outputs/apk/release/app-release-unsigned.apk`). |
| `[[RELEASE_ASSET_LABEL]]` | The release asset label used to name the published APK (for example `ProfiBotAndroid`). |

### Failure Behaviour

- If the Java version, the release APK path, or the release asset label cannot be determined from evidence, cease generation and ask one concise clarification question. Never invent a value.

### Mandatory Validation Before Final Output

- The output file is named `github-release.yml`.
- The workflow `name` is `GitHub Release` and triggers on published releases.
- Top-level `permissions` sets `contents: write`.
- The `release` job runs on `ubuntu-latest`, sets up Temurin Java at the evidenced version, sets up Gradle, extracts the version from the tag, builds with `./gradlew clean assembleRelease --no-daemon`, names the artefact with `[[RELEASE_ASSET_LABEL]]`, and publishes it with `softprops/action-gh-release@v2`.
- Every fixed template line is present verbatim; no placeholder or reformatted line remains.
- No secret value, credential, or personal datum is exposed.

If a `github-release.yml` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `github-release.yml` exists, create one from scratch.
