---
description: "Use when the user asks to revise, create, or generate a README.md. Auto-invoked by requests such as 'revise the readme', 'create a readme', 'compose the readme', or 'generate the readme'. Fills in project-specific details and applies the standard structure, badges, and conditional sections."
applyTo: "README.md"
---
This is the `README.md` template that must be used.
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

[[[Clear description of what this project provides and why it is valuable.]]]

<!-- Only if `preview.png` exists. -->
![Preview screenshot](preview.png)

## 📑 Table of Contents

<!-- Generate one entry per ##/###/#### heading present in the final output, in order. -->

<!-- Only if `screenshots/` directory exists with image files. -->
## 🖼️ Screenshots

![[[Screenshot 1 description]]](screenshots/[[screenshot1.png]])
![[[Screenshot 2 description]]](screenshots/[[screenshot2.png]])

## ✨ Capabilities

- [[Capability 1]]
- [[Capability 2]]

## 🚀 Usage

<!-- Provide a minimal but realistic example showing how to use the project. For CLI tools, demonstrate with a shell command. For libraries, demonstrate with a code snippet. For web apps, describe the main workflow. -->
[[Usage example]]

<!-- Only if there are notable caveats, constraints, or missing capabilities worth emphasising. -->
## ⚠️ Known Limitations

- [[Limitation 1]]

<!-- Only if `FAQ.md` exists. -->
## ❓ FAQ

See [FAQ.md](./FAQ.md) for responses to frequently raised inquiries.

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

See [ROADMAP.md](./ROADMAP.md) for planned work and forthcoming changes.

<!-- Only if docs/ directory, GitHub Pages, or GitHub Wiki exists. -->
## 📚 Documentation

Full documentation is available at [[DOCS_URL]].

<!-- Only if this is a library, SDK, or API project with auto-generated or hosted documentation. -->
## 🌐 API Reference

See the [API Reference]([[API_DOCS_URL]]) for the full type and method documentation.

<!-- Only if `ARCHITECTURE.md` exists or `docs/architecture/` directory exists. -->
## 🏗️ Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md) for a structural synopsis and component interactions.

<!-- Only if `MIGRATION.md` or `UPGRADING.md` exists. -->
## 🔄 Migration Guide

See [MIGRATION.md](./MIGRATION.md) for instructions on upgrading from previous versions.

## 🤝 Contributing

You are welcome to submit any suggestion, feedback, or modification to this project.

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
See [CONTRIBUTING.md](./CONTRIBUTING.md) for further information on contributing to this project.

<!-- Only if `ROADMAP.md` exists. -->
See [ROADMAP.md](./ROADMAP.md) for planned work and forthcoming changes.

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
## 💝 Helping outellput

Discovered a problemroble or have a suggestion? [Open an issue](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/issues)!

<!-- Only if `.github/FUNDING.yml` exists. -->
If you findonsiind this project useful, consider [funding it](https://hmlendea.go.ro/funding) or starring ⭐️ it on GitHub!

<!-- Only if `.github/FUNDING.yml` exists. -->
[![Donate](https://raw.githubusercontent.com/hmlendea/readme-assets/master/donate_generic.png)](https://hmlendea.go.ro/funding)

<!-- Only if `./LICENSE` exists. Add this exactly as it is written here, do not modify it in any way. -->
## 📄 License

This project is being distributed under the `[[License Title]]`<!-- Only for GPL-family licences, append: " or later" -->.
See [LICENSE](./LICENSE) for further information.
