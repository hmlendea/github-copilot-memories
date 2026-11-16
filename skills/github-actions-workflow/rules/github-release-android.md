Generate or revise `.github/workflows/github-release.yml` using `templates/github-release-android.yml`.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `github-release.yml` creation or revision and overrides conflicting instructions. Strict fidelity applies **only to personal repositories owned by the current git user** (GitHub owner type `User` and owner matching the current git user); organization-owned repositories and repositories owned by another user are out of strict-fidelity scope. If the user explicitly requests the templates, strict fidelity applies regardless of repository ownership.

### Generation Contract

1. Use this template only for Android projects that build an APK release artefact through Gradle. For a compilable .NET project that builds release assets, use `rules/github-release-dotnet.md` instead. For a repository that hosts a NuGet package, use `rules/github-release-nuget.md` instead.
2. Use an exact copy of `templates/github-release-android.yml`; preserve the workflow `name`, triggers, permissions, job, steps, action versions, indentation, and whitespace layout.
3. The template must remain exactly as written, with only the placeholders replaced.
4. Keep the `temurin` distribution, the `gradle/actions/setup-gradle` step, and the `--no-daemon` flag exactly as written.
5. The `contents: write` permission is required to publish release assets and must remain.
6. Keep the `Restore release signing configuration` step, its four secret references, its emptiness guards, and its `chmod 600` exactly as written. The secret names are fixed, because they are the names the bootstrap procedure below registers.
7. Keep the separate release and debug build, naming, and publishing steps, because a release publishes both APKs.

### Placeholders

| Placeholder | Replacement |
|-------------|-------------|
| `[[REPOSITORY_JAVA_VERSION]]` | The Java (JDK) version used in the repository (for example `17` or `21`), consistent with `sourceCompatibility`, `targetCompatibility`, and `jvmTarget` in the Gradle build. |
| `[[RELEASE_APK_PATH]]` | The repository-relative path of the signed release APK produced by `./gradlew clean assembleRelease` (for example `app/build/outputs/apk/release/app-release.apk`). |
| `[[DEBUG_APK_PATH]]` | The repository-relative path of the debug APK produced by `./gradlew assembleDebug` (for example `app/build/outputs/apk/debug/app-debug.apk`). |
| `[[KEYSTORE_FILE_NAME]]` | The keystore file name written by the signing-restore step and referenced from `keystore.properties` (for example `profi-bot.jks`). |
| `[[RELEASE_ASSET_LABEL]]` | The release asset label used to name the published APKs (for example `ProfiBotAndroid`). |

### Release Signing Bootstrap

The signed release build requires four repository secrets before the workflow can succeed. When they are absent, the agent prepares the signing material and hands the registration to the user:

1. Generate the keystore at the repository root with `keytool -genkeypair -v -keystore <keystore-file-name> -alias <key-alias> -keyalg RSA -keysize 4096 -validity 10000`, using the resolved keystore file name.
2. Create the git-ignored `keystore.properties` in the repository root with the `storeFile`, `storePassword`, `keyAlias`, and `keyPassword` values that were used.
3. Present the following commands to the user with the resolved keystore file name substituted, instructing the user to run them from the repository root, and state that the values are read locally and are not printed:

```bash
gh secret set ANDROID_KEYSTORE_BASE64 --body "$(base64 --wrap=0 <keystore-file-name>)"
gh secret set ANDROID_KEY_ALIAS --body "$(grep '^keyAlias=' keystore.properties | cut -d= -f2-)"
gh secret set ANDROID_KEYSTORE_PASSWORD --body "$(grep '^storePassword=' keystore.properties | cut -d= -f2-)"
gh secret set ANDROID_KEY_PASSWORD --body "$(grep '^keyPassword=' keystore.properties | cut -d= -f2-)"
```

4. After the user confirms registration, delete the local keystore file and confirm the deletion, because the keystore is preserved as `ANDROID_KEYSTORE_BASE64` and must not be retained on disk.

Never invent a password. Never print, log, transmit, or commit a password, the keystore, or `keystore.properties`; both paths are git-ignored and must remain so. Never delete the keystore before the user confirms that the secrets are registered, because Android only accepts an update signed with the same key as the installed application.

### Failure Behaviour

- If the Java version, the release APK path, the debug APK path, the keystore file name, or the release asset label cannot be determined from evidence, cease generation and ask one concise clarification question. Never invent a value.
- If a signing password cannot be obtained from the user, cease and ask; never invent, echo, or display a password.

### Mandatory Validation Before Final Output

- The output file is named `github-release.yml`.
- The workflow `name` is `GitHub Release` and triggers on published releases.
- Top-level `permissions` sets `contents: write`.
- The `release` job runs on `ubuntu-latest`, sets up Temurin Java at the evidenced version, sets up Gradle, and extracts the version from the tag.
- The `Restore release signing configuration` step reads `ANDROID_KEYSTORE_BASE64`, `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_ALIAS`, and `ANDROID_KEY_PASSWORD` from secrets, guards each with `test -n`, decodes the keystore, writes `keystore.properties`, and restricts both files with `chmod 600`.
- The job builds with `./gradlew clean assembleRelease --no-daemon` and `./gradlew assembleDebug --no-daemon`, names both artefacts with the resolved release asset label, and publishes both with `softprops/action-gh-release@v2`.
- The release-signing bootstrap was completed: the keystore was generated, the four registration commands were presented to the user, the user confirmed registration, and the local keystore was deleted.
- Every fixed template line is present verbatim; no placeholder or reformatted line remains.
- No secret value, credential, or personal datum is exposed.

If a `github-release.yml` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `github-release.yml` exists, create one from scratch.
