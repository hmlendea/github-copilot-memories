---
description: "Use when the user asks to revise, create, or generate a README.md. Auto-invoked by requests such as 'revise the readme', 'create a readme', 'compose the readme', or 'generate the readme'. Fills in project-specific details and applies the standard structure, badges, and conditional sections."
applyTo: "README.md"
---

Generate or revise the `README.md` for this GitHub repository using the `github.readme.template.instructions.md` template.

## Strict Template Fidelity Mode (Default)

This mode applies automatically when the user requests any of the following:
- Update the README
- Create the README.md file
- Revise the README
- Create a README
- Generate the README
- Compose the README

### Precedence

- These rules supersede all other README generation instructions.
- If any other rule conflicts with strict fidelity, strict fidelity prevails.

### Generation Contract

1. Start from an exact copy of `github.readme.template.instructions.md`, preserving all template-defined section order, badge order, headings, punctuation, and whitespace layout.
2. Replace only `[[PLACEHOLDER]]` tokens.
3. Do not rephrase fixed template text.
4. Do not remove any template section, badge, table, or subsection.
5. Additional sections or subsections may be added when they are genuinely relevant to the repository, but they must be purely additive and must not replace, rename, reorder, or omit any template-defined section, badge, table, or subsection.
6. Do not normalise, correct, or improve fixed template wording.
7. Language, spelling, and phrasing rules apply only to values inserted into placeholders, not to fixed template literals.
8. Framework-specific command replacements are disabled in strict mode.
9. Resolve template-marked conditional blocks exactly as written in template comments (for example, lines marked with `Only if ...`). Template-defined core sections and headings remain mandatory and must not be removed.

### Failure Behaviour

- If any required placeholder value is unknown, cease generation and ask one concise clarification question.
- Do not output a partial README.

### Mandatory Validation Before Final Output

- Headings match the template exactly in text and order.
- Badge lines match the template exactly in text and order.
- No template section is missing.
- Any added section or subsection is repository-relevant and purely additive.
- No fixed template line was rephrased.
- All resolvable placeholders were replaced.

If a `README.md` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `README.md` exists, create one from scratch.

Use the exact template wording for fixed sections. Do not reword, paraphrase, or alter `## License`, `## Contributing`, or `## Supporting the Project`; only replace placeholder tokens such as `[[License Title]]`, `[[GITHUB_REPO_USERNAME]]`, and `[[GITHUB_REPO_NAME]]`.

Fill in all `[[PLACEHOLDER]]` values from the actual project. Remove any section or comment that does not apply (see the inline guidance). Do not leave any placeholder text, template comments, or example rows in the final output.

## Mandatory editing rules

When updating an existing README.md:

- Never delete README.md.
- Never use `*** Delete File`.
- Never recreate README.md with `create_file`.
- Modify the existing file only with `apply_patch` using `*** Update File`.
- A complete rewrite must still use `*** Update File`.
- Preserve the file path and file identity throughout the operation.
- If an in-place patch cannot be produced, stop and explain the problem instead of deleting the file.

## Conditional Content Rules

### Badges
- Include `Donate` if `.github/FUNDING.yml` exists.
- Include `Latest Release` if the repository has at least one published release.
- Include `Website` if the repository has a configured Website URL in its GitHub About section, or if GitHub Pages is enabled. Use `GitHub Pages` label for `github.io` domains, otherwise `Website`.
- Include `Build Status` if a GitHub Actions workflow file exists in `.github/workflows/`.
- Include code coverage badge if `.codecov.yml`, `coveralls.yml`, or a Codecov/Coveralls configuration block exists. Place after `Build Status` badge.
- Include `License` if `./LICENSE` exists.

### sections

Include these sections only when the specified conditions are met:

| Section | Condition | Notes |
|---------|-----------|-------|
| Preview screenshot | `preview.png` exists in root. | Place before Table of Contents. |
| Table of Contents | Always include. | After preview image (if present), before first `##` section. Include all `##`, `###`, `####` headings. Indent `###` by 2 spaces, `####` by 4 spaces. Do not include any emoji in entries, anchors, or links; strip emojis from anchors and links. |
| Screenshots | `screenshots/` directory exists with image files. | Place directly after Table of Contents. |
| Known Limitations | Real, notable caveats or missing features exist. | Omit if none exist. Place after Usage. |
| FAQ | `FAQ.md` exists. | Place directly after Known Limitations. |
| System Requirements | End-user application (not library or NuGet package) with meaningful OS, hardware, or runtime prerequisites. | Place directly before Installation. |
| Installation | Project distributed via Flatpak, Snap, AUR, NuGet, npm, Steam Workshop, Nexus Mods, Paradox Mods, or GitHub release. | Place directly above System Requirements section (if present), or directly above Development. |
| Configuration | Any of `appsettings.json`, `config.json`, `config.yaml`, `config.toml`, `settings.py` exist and contain recognised settings. | Include only sections with documented keys. Omit entirely if none have documented settings. |
| Environment Variables (subsection) | `.env.example` exists. | Placed within Configuration section. |
| Localisation | Directories: `locales/`, `i18n/`, `translations/`, `Localisation/`, `Localization/`; or files: `LocalisationStrings.*`, `LocalizationStrings.*`, `LocaleService.*`, `LocalisationManager.*`; or language-code files (e.g. `en.json`, `ro.json`) in localisation directory. | Place after Configuration. |
| Linting (subsection) | Lint config exists (`.eslintrc`, `.pylintrc`, `rubocop.yml`, `.editorconfig` with lint rules, similar). | Within Development, placed after Test subsection. |
| Docker (subsection) | `Dockerfile` exists. | Within Development. |
| Docker Compose (subsection) | `docker-compose.yml` or `docker-compose.yaml` exists. | Within Development. |
| Release (subsection) | Appropriate variant exists: `dotnet pack` (NuGet), `npm run dist` (npm with dist script), `release.sh` file; omit for executables without dedicated release process. | Within Development. |
| Dependencies (subsection) | Non-test runtime dependencies exist. For .NET, omit test-only packages; for other types, list only non-trivial packages. | Within Development. |
| Project Structure | Solution has multiple projects or non-obvious layout that aids orientation. | Omit for single-project solutions with standard layout. |
| Roadmap | `ROADMAP.md` exists. | |
| Documentation | `docs/` directory, GitHub Pages, or GitHub Wiki exists. | Place after Roadmap. |
| API Reference | Library, SDK, or API project with auto-generated or hosted documentation. | Place after Documentation (if present), otherwise after Roadmap. |
| Architecture | `ARCHITECTURE.md` exists or `docs/architecture/` directory exists. | Place directly after Project Structure. |
| Migration Guide | `MIGRATION.md` or `UPGRADING.md` exists. | Place before Contributing. |
| Related Projects | Related projects exist. | Include only if genuinely relevant. |
| Acknowledgements | Project builds on notable third-party work, data sources, or inspiration. | Include only if warranting attribution. |
| Changelog | `CHANGELOG.md` exists. | |
| Security | `SECURITY.md` exists. | |

### Always Include
- `## Usage`: Provide minimal but realistic example (shell command for CLI, code snippet for libraries, workflow description for web apps).
- `## Contributing`: Base template provided; extend as needed.
- `## License`: Specify licence title. For GPL-family licences only, append "or later". Omit for MIT, Apache, non-copyleft.
- `## Supporting the Project`: Always include with standard base template.

## Styling & Format Rules

- Respect the instructions in `language.instructions.md` for all README text, including spelling, phrasing, and language conventions.
- Prefix `##` headings with their emoji as shown in template (omit only if existing README uses no emojis and project tone is formal).
- Remove all HTML comments from final output.
- Always fill `[[PLACEHOLDER]]` values with actual project details; omit any template comments or example rows.
- In `## License`, include "or later" only for GPL-family licences; omit for MIT, Apache, and other non-copyleft licences.

## Framework-Specific replacements

Replace .NET commands when project uses different stack:

| Framework | SDK/Runtime | Setup | Build | Run | Test |
|-----------|-------------|-------|-------|-----|------|
| npm/Node.js | `Node.js [[VERSION]]` | `npm install` | `npm run build` | `npm start` or `npm run dev` | `npm test` |
| Python | `Python [[VERSION]]` | `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` | `python -m pip install -e .` (if package) or skip | `python [[entrypoint]]` or `python -m [[module]]` | `pytest` |
| Go | `Go [[VERSION]]` | `go mod tidy` | `go build ./...` | `go run ./cmd/[[entrypoint]]` | `go test ./...` |
| Rust | `Rust toolchain [[VERSION]]` | `cargo fetch` | `cargo build` | `cargo run` | `cargo test` |
| Java | `Java/JDK [[VERSION]]` and `Maven`/`Gradle` | `mvn install` or `gradle build` | `mvn compile` or `gradle build` | N/A | `mvn test` or `gradle test` |
