Generate or revise `.github/workflows/android.yml` using `templates/android.yml`.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `android.yml` creation or revision and overrides conflicting instructions. Strict fidelity applies **only to personal repositories owned by the current git user** (GitHub owner type `User` and owner matching the current git user); organization-owned repositories and repositories owned by another user are out of strict-fidelity scope. If the user explicitly requests the templates, strict fidelity applies regardless of repository ownership.

### Generation Contract

1. Use an exact copy of `templates/android.yml`; preserve the workflow `name`, triggers, job, steps, action versions, indentation, and whitespace layout.
2. The template must remain exactly as written, with only this exception:
   - `[[REPOSITORY_JAVA_VERSION]]` is replaced with the Java (JDK) version used in the repository.
3. Keep the `temurin` distribution, the `gradle/actions/setup-gradle` step, and the `--no-daemon` flag exactly as written.

### Placeholders

| Placeholder | Replacement |
|-------------|-------------|
| `[[REPOSITORY_JAVA_VERSION]]` | The Java (JDK) version used in the repository (for example `17` or `21`), consistent with `sourceCompatibility`, `targetCompatibility`, and `jvmTarget` in the Gradle build. |

### Failure Behaviour

- If the repository Java version cannot be determined from evidence, cease generation and ask one concise clarification question. Never produce a partial workflow.

### Mandatory Validation Before Final Output

- The output file is named `android.yml`.
- The workflow `name` is `Android`.
- Triggers are `push` and `pull_request` on `master`.
- The `build` job runs on `ubuntu-latest`, sets up Temurin Java at the evidenced version, sets up Gradle, builds with `./gradlew assembleDebug --no-daemon`, and tests with `./gradlew test --no-daemon`.
- The `gradle/actions/setup-gradle` step remains in place.
- Every fixed template line is present verbatim; no placeholder or reformatted line remains.
- No secret, credential, or personal datum is exposed.

If an `android.yml` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `android.yml` exists, create one from scratch.
