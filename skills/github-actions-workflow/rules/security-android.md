Generate or revise `.github/workflows/security.yml` using `templates/security-android.yml`.

## Repository Visibility Precondition (Blocking)

Before creating or revising any `security.yml` workflow, determine the repository visibility:

```bash
gh api repos/<owner>/<repo> --jq .visibility   # must return "public"
```

GitHub Code Scanning requires a public repository (or GitHub Enterprise Cloud with GitHub Advanced Security). CodeQL `analyze` uploads SARIF results to the code-scanning endpoint, which returns `Resource not accessible by integration` and fails the run on a private repository under a free or Pro plan.

- Visibility `public` → proceed.
- Visibility `private` or `internal` → **REFUSE** to create or revise `security.yml`. Do not create a partial workflow, do not weaken the permissions, and do not silently drop the `analyze` step. State that CodeQL code scanning requires the repository to be public and that `security.yml` cannot be added until the repository visibility changes.
- Visibility cannot be determined → do not proceed silently; report that visibility must be confirmed before the workflow is added.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `security.yml` creation or revision and overrides conflicting instructions. Strict fidelity applies **only to personal repositories owned by the current git user** (GitHub owner type `User` and owner matching the current git user); organization-owned repositories and repositories owned by another user are out of strict-fidelity scope. If the user explicitly requests the templates, strict fidelity applies regardless of repository ownership.

### Generation Contract

1. Use this template only for Android projects that build an APK through Gradle. For a .NET repository, use `rules/security-dotnet.md` instead.
2. Use an exact copy of `templates/security-android.yml`; preserve the workflow `name`, triggers, job, permissions, steps, action versions, indentation, and whitespace layout.
3. The template must remain exactly as written, with only this exception:
   - `[[REPOSITORY_JAVA_VERSION]]` is replaced with the actual Java (JDK) version used in the repository.
4. Keep the `temurin` distribution, the `gradle/actions/setup-gradle` step, and the `--no-daemon` flag exactly as written.
5. The `security-events` permission must be `write`. The CodeQL `analyze` action uploads SARIF results to GitHub Code Scanning, and that upload requires the `security-events: write` scope. With `security-events: read`, the upload fails on `push` and `schedule` runs with `Resource not accessible by integration`, while `pull_request` runs still complete. GitHub's own CodeQL workflow therefore grants `security-events: write`.
6. The `contents: write` permission is required by the `gradle/actions/dependency-submission` step to submit the dependency graph and must remain.

### Placeholders

| Placeholder | Replacement |
|-------------|-------------|
| `[[REPOSITORY_JAVA_VERSION]]` | The Java (JDK) version used in the repository (for example `17` or `21`), consistent with `sourceCompatibility`, `targetCompatibility`, and `jvmTarget` in the Gradle build. |

### Failure Behaviour

- Private or internal repository → refuse, explain that CodeQL requires the repository to be public, and create nothing.
- If the repository Java version cannot be determined from evidence, cease generation and ask one concise clarification question. Never downgrade the `security-events` permission below `write`.

### Mandatory Validation Before Final Output

- The output file is named `security.yml`.
- The repository visibility was confirmed as `public` before generation.
- The workflow `name` is `Security`.
- Triggers are `push`, `pull_request` on `master`, and a weekly `schedule`.
- The `security-scan` job grants `security-events: write` and `contents: write`, and runs on `ubuntu-latest`.
- Steps set up Temurin Java at the evidenced version, set up Gradle, submit vulnerable dependencies through `gradle/actions/dependency-submission@v6`, run CodeQL `init@v4` for `java-kotlin`, build, and run CodeQL `analyze@v4`.
- Every fixed template line is present verbatim; no placeholder or reformatted line remains.
- No secret, credential, or personal datum is exposed.

If a `security.yml` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `security.yml` exists, create one from scratch.
