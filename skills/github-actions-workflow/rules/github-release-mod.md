Generate or revise `.github/workflows/github-release.yml` using `templates/github-release-mod.yml`.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `github-release.yml` creation or revision and overrides conflicting instructions. Strict fidelity applies **only to personal repositories owned by the current git user** (GitHub owner type `User` and owner matching the current git user); organization-owned repositories and repositories owned by another user are out of strict-fidelity scope. If the user explicitly requests the templates, strict fidelity applies regardless of repository ownership.

### Generation Contract

1. Use this template only for content-only or packaged repositories — game mods, asset packs, and similar repositories whose distributable content is committed rather than compiled. For a compilable .NET project, use `rules/github-release-dotnet.md` instead. For a repository that hosts a NuGet package, use `rules/github-release-nuget.md` instead. For an Android project that builds an APK release artefact through Gradle, use `rules/github-release-android.md` instead. For an Electron project that builds release artefacts through `electron-builder`, use `rules/github-release-electron.md` instead.
2. Use an exact copy of `templates/github-release-mod.yml`; preserve the workflow `name`, triggers, permissions, job, steps, action versions, indentation, and whitespace layout.
3. The template must remain exactly as written, with only the placeholders replaced.
4. The `contents: write` permission is required to publish the release asset and must remain.
5. The archive is built from the checked-out release tag, so the archive name carries the release version with the leading `v` stripped.
6. Do not compute, append, or publish a checksum. The release body is left exactly as the maintainer wrote it.

### Placeholders

| Placeholder | Replacement |
|-------------|-------------|
| `[[RELEASE_ASSET_LABEL]]` | The release archive label, equal to the packaged directory name and the mod descriptor base name (for example `ui-deposit-blockers`). |
| `[[RELEASE_ASSETS_LIST]]` | The assets to archive, as a double-quoted, space-separated list of paths in the checked-out tag (for example `"my-mod/" "my-mod.mod"`). |

### Failure Behaviour

- If the release asset label or the asset list cannot be determined from evidence, cease generation and ask one concise clarification question. Never invent paths or labels.

### Mandatory Validation Before Final Output

- The output file is named `github-release.yml`.
- The workflow `name` is `GitHub Release` and triggers on published releases.
- Top-level `permissions` sets `contents: write`.
- The `release` job runs on `ubuntu-latest`, extracts the version from the release tag, builds `[[RELEASE_ASSET_LABEL]]_<version>.zip` from `[[RELEASE_ASSETS_LIST]]`, and publishes it with `softprops/action-gh-release@v2`.
- Every fixed template line is present verbatim; no placeholder or reformatted line remains.
- No secret value, credential, or personal datum is exposed.

If a `github-release.yml` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `github-release.yml` exists, create one from scratch.

## Migrating a Non-Canonical Release Workflow

A repository that predates this template commonly holds an equivalent workflow under a non-canonical name, such as `release.yml`, triggered by tag pushes. Replace it with the canonical `github-release.yml`:

- Migrate to the canonical file name and to the `release: types: [ published ]` trigger, which publishes only after the maintainer has created the release.
- Retain the archive label and asset list, and let the template build and upload the archive, so that the release asset set is declared explicitly.
- Remove any checksum computation, checksum line appended to the release body, downloadable GitHub release asset retrieval, and any other workflow that consumes the release archive as though it were externally produced.
- Remove the superseded workflow file in the same change, and update every document that references it.
