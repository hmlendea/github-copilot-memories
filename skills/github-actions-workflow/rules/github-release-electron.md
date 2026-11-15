Generate or revise `.github/workflows/github-release.yml` using `templates/github-release-electron.yml`.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `github-release.yml` creation or revision and overrides conflicting instructions. Strict fidelity applies **only to personal repositories owned by the current git user** (GitHub owner type `User` and owner matching the current git user); organization-owned repositories and repositories owned by another user are out of strict-fidelity scope. If the user explicitly requests the templates, strict fidelity applies regardless of repository ownership.

### Generation Contract

1. Use this template only for Electron projects that build release artefacts through `electron-builder`. For a compilable .NET project that builds release assets, use `rules/github-release-dotnet.md` instead. For a repository that hosts a NuGet package, use `rules/github-release-nuget.md` instead. For an Android project that builds an APK release artefact through Gradle, use `rules/github-release-android.md` instead.
2. Use an exact copy of `templates/github-release-electron.yml`; preserve the workflow `name`, triggers, permissions, job, steps, action versions, indentation, and whitespace layout.
3. The template must remain exactly as written, with only the placeholders replaced.
4. The `contents: write` permission is required to publish release assets and must remain.
5. `npm ci` is required rather than `npm install`, so that the locked dependency tree is installed.
6. The release script must not publish independently; `npm run build` runs with publishing disabled by the repository's `build` script, and the template publishes the assets itself.
7. `[[RELEASE_ASSET_GLOB]]` must not embed the release version. `electron-builder` derives artefact names from the `package.json` version, which can diverge from the release tag, so a version-bearing glob can silently match nothing and publish an empty release.
8. When the repository uses `electron-updater`, include the channel metadata files (`latest-linux*.yml`) in the published assets, otherwise the updater cannot resolve releases.

### Placeholders

| Placeholder | Replacement |
|-------------|-------------|
| `[[NODE_VERSION]]` | The Node.js major version used in the repository (for example `20` or `22`), consistent with `.nvmrc`, the `engines` field, and the continuous-integration workflow. The template appends `.x`, so the replacement is the major version only. |
| `[[RELEASE_ASSET_GLOB]]` | The repository-relative glob of the release assets produced by `npm run build` (for example `dist/geforcenow-electron_*`) and of the updater metadata when the repository uses `electron-updater` (for example `dist/latest-linux*.yml`). The globs must be version-independent, because `electron-builder` names artefacts from the `package.json` version rather than from the release tag. When several patterns are required, expand the placeholder into a YAML block scalar containing one pattern per line. |

### Failure Behaviour

- If the Node.js version or the release asset glob cannot be determined from evidence, cease generation and ask one concise clarification question. Never invent a version or glob.

### Mandatory Validation Before Final Output

- The output file is named `github-release.yml`.
- The workflow `name` is `GitHub Release` and triggers on published releases.
- Top-level `permissions` sets `contents: write`.
- The `release` job runs on `ubuntu-latest`, sets up Node.js at the evidenced major version with npm caching, installs locked dependencies with `npm ci`, builds with `npm run build`, and publishes `[[RELEASE_ASSET_GLOB]]` with `softprops/action-gh-release@v2`.
- Every fixed template line is present verbatim; no placeholder or reformatted line remains.
- No secret value, credential, or personal datum is exposed.

If a `github-release.yml` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `github-release.yml` exists, create one from scratch.

## Migrating a Non-Canonical Release Workflow

A repository that predates this template commonly holds an equivalent workflow under a non-canonical name, such as `release.yml`, triggered by tag pushes and publishing through `npm run build -- --publish always`. Replace it with the canonical `github-release.yml`:

- Migrate to the canonical file name and to the `release: types: [ published ]` trigger, which publishes only after the maintainer has created the release.
- Retain `npm run build` with the repository's publishing disabled, and let the template upload the produced assets, so that the release asset set is declared explicitly.
- Remove the superseded workflow file in the same change, and update every document that references it.
