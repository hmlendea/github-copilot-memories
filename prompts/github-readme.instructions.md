---
description: "Use when the user asks to revise, create, or generate a README.md. Auto-invoked by requests such as 'revise the readme', 'create a readme', 'compose the readme', or 'generate the readme'. Fills in project-specific details and applies the standard structure, badges, and conditional sections."
agent: agent
---

Generate or revise the `README.md` for this GitHub repository using the template below.

If a `README.md` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `README.md` exists, create one from scratch.

Use the exact template wording for fixed sections. Do not reword, paraphrase, or alter `## License`, `## Contributing`, or `## Support`; only replace placeholder tokens such as `[[License Title]]`, `[[GITHUB_REPO_USERNAME]]`, and `[[GITHUB_REPO_NAME]]`.

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
- `## Support`: Always include with standard base template.

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

---

<!-- Only if `.github/FUNDING.yml` exists. -->
[![Donate](https://img.shields.io/badge/-%E2%99%A5%20Donate-%23ff69b4)](https://hmlendea.go.ro/funding)
<!-- Only if the repository has at least one published release. -->
[![Latest Release](https://img.shields.io/github/v/release/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]])](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/releases/latest)
<!-- Only if the repository has a configured Website URL or GitHub Pages is enabled. Use label 'GitHub Pages' for github.io URLs, otherwise 'Website'. -->
[![Website](https://img.shields.io/badge/Website-Visit-blue)](https://[[WEBSITE_URL]])
<!-- Only if `.github/workflows/[WORKFLOW_FILE]` exists. -->
[![Build Status](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/actions/workflows/[[WORKFLOW_FILE]].yml/badge.svg)](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/actions/workflows/[[WORKFLOW_FILE]].yml)
<!-- Only if code coverage reporting is configured (e.g. `.codecov.yml` or `coveralls.yml`). -->
[![Coverage](https://codecov.io/gh/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/branch/master/graph/badge.svg)](https://codecov.io/gh/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]])
<!-- Only if `LICENSE` exists. -->
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://gnu.org/licenses/gpl-3.0)

<!-- Human-friendly project title (not necessarily the repository name). Must come after the badges. -->
# [[Project Title]]

[[[Clear description of what this project does and why it is useful.]]]

<!-- Only if `preview.png` exists. -->
![Preview screenshot](preview.png)

## 📑 Table of Contents

<!-- Generate one entry per ##/###/#### heading present in the final output, in order. -->

<!-- Only if `screenshots/` directory exists with image files. -->
## 🖼️ Screenshots

![[[Screenshot 1 description]]](screenshots/[[screenshot1.png]])
![[[Screenshot 2 description]]](screenshots/[[screenshot2.png]])

## ✨ Features

- [[Feature 1]]
- [[Feature 2]]

## 🚀 Usage

<!-- Provide a minimal but realistic example showing how to use the project. For CLI tools, demonstrate with a shell command. For libraries, demonstrate with a code snippet. For web apps, describe the main workflow. -->
[[Usage example]]

<!-- Only if there are notable caveats, constraints, or missing features worth highlighting. -->
## ⚠️ Known Limitations

- [[Limitation 1]]

<!-- Only if `FAQ.md` exists. -->
## ❓ FAQ

See [FAQ.md](./FAQ.md) for answers to frequently asked questions.

<!-- Only if this is an end-user application with meaningful OS, hardware, or runtime prerequisites. -->
## 🖥️ System Requirements

- **OS:** [[Supported operating systems. Priority order: Linux, MacOS, Windows. Include versions if relevant.]]
- **RAM:** [[Minimum RAM]]
- [[Any other relevant prerequisites]]

<!-- Only if this is distributed in any form. -->
## 📦 Installation

<!-- Only if this is distributed as a Flatpak package. -->
[![Obtain it from FlatHub](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/flathub.png)](https://flathub.org/apps/details/[[FLATHUB_PACKAGE_ID]])
<!-- Only if this is distributed as a Snap package. -->
[![Obtain it from Snap Store](https://raw.githubusercontent.com/snapcore/snap-store-badges/master/EN/%5BEN%5D-snap-store-white.png)](https://snapcraft.io/[[SNAP_PACKAGE_ID]])
<!-- Only if this is distributed as an AUR package. -->
[![Obtain it from AUR](https://raw.githubusercontent.com/hmlendea/readme-assets/master/install_from_aur.png)](https://aur.archlinux.org/packages/[[AUR_PACKAGE_ID]])
<!-- Only if this is distributed as a NuGet package. -->
[![Obtain it from NuGet](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/nuget.png)](https://nuget.org/packages/[[NUGET_PACKAGE_ID]])
<!-- Only if this is distributed as a Steam Workshop mod. -->
[![Obtain it from Steam Workshop](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/steam-workshop.png)](https://steamcommunity.com/sharedfiles/filedetails/?id=[[STEAM_WORKSHOP_ID]])
<!-- Only if this is distributed as a Nexus Mods mod. -->
[![Obtain it from Nexus Mods](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/nexus.png)](https://nexusmods.com/[[NEXUS_MODS_GAME_ID]]/mods/[[NEXUS_MODS_ID]])
<!-- Only if this is distributed as a Paradox Mods mod. -->
[![Obtain it from Paradox Mods](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/paradox-mods.png)](https://mods.paradoxplaza.com/mods/[[PARADOX_MODS_ID]]/Any)
<!-- Only if this is distributed as a GitHub release. -->
[![Obtain it from GitHub](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/github.png)](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/releases)

### CLI Installation

<!-- Only if this is distributed as a Flatpak package. -->
```bash
flatpak install flathub [[FLATHUB_PACKAGE_ID]]
```
<!-- Only if this is distributed as a Snap package. -->
```bash
snap install [[SNAP_PACKAGE_ID]]
```
<!-- Only if this is distributed as an AUR package. -->
```bash
paru -S [[AUR_PACKAGE_ID]]
```
or, if you use `yay`:
```bash
yay -S [[AUR_PACKAGE_ID]]
```
<!-- Only if this is distributed as a NuGet package. -->
```bash
dotnet add package [[NUGET_PACKAGE_ID]]
```

Or, via the `Package Manager Console`:
```powershell
Install-Package [[NUGET_PACKAGE_ID]]
```
<!-- Only if this is distributed as an NPM package. -->
```bash
npm install [[NPM_PACKAGE_ID]]
```

<!-- Only if `appsettings.json`, `config.json`, `config.yaml`, `config.toml`, or `settings.py` exists and has at least one documented setting. Omit entirely rather than leaving an empty or filler table. -->
## ⚙️ Configuration

All settings are loaded from the configuration file. The subsequent keys are recognised:

| Section | Key | Description |
|---------|-----|-------------|
| [[Section]] | [[Key]] | [[Description]] |

<!-- Only if `.env.example` exists. -->
### Environment Variables

The subsequent environment variables can be set:

| Variable | Description | Default |
|----------|-------------|---------|
| `[[VARIABLE_NAME]]` | [[Description]] | `[[default value]]` |

<!-- Only if localisation signals are detected anywhere in the repository (directories like `locales/`, `i18n/`, `translations/`, `Localisation/`, `Localization/`; files like `LocalisationStrings.*`, `LocalizationStrings.*`, `LocaleService.*`, `LocalisationManager.*`; or language-code JSON files inside localisation-related directories). -->
## 🌍 Localisation

Translations are located in the project's localisation resources. The subsequent languages are currently supported:

| Language | Code | Status |
|----------|------|--------|
| [[Language]] | `[[code]]` | [[Complete / Partial]] |

## 🛠️ Development

### Requirements

<!-- Only if this is a .NET project. -->
- [.NET [[DOTNET_VERSION]] SDK](https://dotnet.microsoft.com/download/dotnet/[[DOTNET_VERSION]])
<!-- Only if other requirements exist. -->
- [[Additional requirement 1]]
- [[Additional requirement 2]]

### Setup

<!-- Only if this is a .NET project. -->
All NuGet dependencies are restored automatically by `dotnet restore`.

<!-- Only if this is an npm/Node.js project. -->
```bash
npm install
```

<!-- Only if this is a Python project. -->
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

<!-- Only if this is a Go project. -->
```bash
go mod tidy
```

<!-- Only if this is a Rust project. -->
```bash
cargo fetch
```

### Build

<!-- This is an example for .NET, use a different command for other frameworks. -->
```bash
dotnet build [[MAIN_PROJECT_NAME]]
```

### Run

<!-- This is an example for .NET, use a different command for other frameworks. -->
```bash
dotnet run --project [[MAIN_PROJECT_NAME]]
```

<!-- Only if tests exist. -->
### Test

<!-- This is an example for .NET, use a different command for other frameworks. -->
```bash
dotnet test [[SOLUTION_FILE]]
```

<!-- Only if a lint configuration file exists (e.g. `.eslintrc`, `.pylintrc`, `rubocop.yml`). -->
### Linting

<!-- This is an example; replace with the appropriate lint command for the project's language/framework. -->
```bash
[[lint command]]
```

<!-- Only if `Dockerfile` exists. -->
### Docker

```bash
docker build -t [[IMAGE_NAME]] .
docker run --rm [[IMAGE_NAME]]
```

<!-- Only if `docker-compose.yml` or `docker-compose.yaml` exists. -->
### Docker Compose

```bash
docker compose up
```

<!-- For NuGet packages only: include this Release sub-section. -->
### Release

```bash
dotnet pack [[MAIN_PROJECT_NAME]] -c Release
```

<!-- For NPM packages only, if they have the `dist` command configured: include this Release sub-section. -->
### Release

```bash
npm run dist
```

<!-- Only if `release.sh` exists. -->
### Release

The repository includes `release.sh`, which delegates to the upstream deployment script used by the project maintainer.

```bash
bash ./release.sh [[LATEST_RELEASE_VERSION_WITHOUT_V_PREFIX]]
```

This script downloads and executes an external release helper from `https://raw.githubusercontent.com/hmlendea/deployment-scripts/master/release/dotnet/[[DOTNET_VERSION]].sh`.

**Note:** Piping into `bash` is an intensely controversial topic. Please review any external scripts before running them in your environment!

<!-- Only if there are non-test runtime dependencies. -->
### Dependencies

| Package | Purpose |
|---------|---------|
| [[package]] | [[purpose]] |

<!-- Only if the solution has more than one project or the directory layout is non-obvious. -->
## 🗂️ Project Structure

The solution contains the subsequent projects:

- [[ProjectName]]: [[purpose]]

The key directories inside `[[MAIN_PROJECT_NAME]]/` are:

| Directory | Purpose |
|-----------|---------|
| [[dir]]   | [[purpose]] |


<!-- Only if `ROADMAP.md` exists. -->
## 🗺️ Roadmap

See [ROADMAP.md](./ROADMAP.md) for planned features and upcoming changes.

<!-- Only if docs/ directory, GitHub Pages, or GitHub Wiki exists. -->
## 📚 Documentation

Full documentation is available at [[DOCS_URL]].

<!-- Only if this is a library, SDK, or API project with auto-generated or hosted documentation. -->
## 🌐 API Reference

See the [API Reference]([[API_DOCS_URL]]) for the full type and method documentation.

<!-- Only if `ARCHITECTURE.md` exists or `docs/architecture/` directory exists. -->
## 🏗️ Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md) for an overview of the system design and component interactions.

<!-- Only if `MIGRATION.md` or `UPGRADING.md` exists. -->
## 🔄 Migration Guide

See [MIGRATION.md](./MIGRATION.md) for instructions on upgrading from previous versions.

## 🤝 Contributing

You are welcome to bring any suggestion, feedback or modification to this project.

When doing so, please:
<!-- Only if relevant (e.g. applications, libraries, mods, etc). -->
- Maintain cross-platform compatibility
<!-- Only if this is an API or library. -->
- Maintain the existing public contract intact unless a breaking change is intentional
- Maintain the pull requests as focused and consistent with the existing code style
- Maintain your branch up-to-date with `master`
<!-- Only if documentation and behaviour exists. -->
- Revise the documentation when behaviour changes
- Properly test all changes <!-- Only if tests exist, append: `, including edge cases and error conditions` -->
<!-- Only if tests exist. -->
- Add unit tests for any new or changed functionality

<!-- Only if `CONTRIBUTING.md` exists in this repository's root directory. -->
See [CONTRIBUTING.md](./CONTRIBUTING.md) for more details on contributing to this project.

<!-- Only if there are related projects. -->
## 🔗 Related Projects

- [[Related project 1 with link]]: [[description]]
- [[Related project 2 with link]]: [[description]]

<!-- Only if there are notable third-party works, data sources, or inspiration worth attributing. -->
## 🙏 Acknowledgements

- [[Acknowledgement 1]]

<!-- Only if `CHANGELOG.md` exists. -->
## 📋 Changelog

See [CHANGELOG.md](./CHANGELOG.md) for a full history of changes.

<!-- Only if `SECURITY.md` exists. -->
## 🔒 Security

For information on reporting security vulnerabilities, see [SECURITY.md](./SECURITY.md).

<!-- Always include this Support section -->
## 💝 Helping out

Discovered a problem or have a suggestion? [Open an issue](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/issues)!

<!-- Only if `.github/FUNDING.yml` exists. -->
If you find this project useful, consider [funding it](https://hmlendea.go.ro/funding) or starring ⭐️ it on GitHub!

<!-- Only if `.github/FUNDING.yml` exists. -->
[![Donate](https://raw.githubusercontent.com/hmlendea/readme-assets/master/donate_generic.png)](https://hmlendea.go.ro/funding)

<!-- Only if `./LICENSE` exists. Add this exactly as it is written here, do not modify it in any way. -->
## 📄 License

This project is being distributed under the `[[License Title]]`<!-- Only for GPL-family licences, append: " or later" -->.
See [LICENSE](./LICENSE) for details.
