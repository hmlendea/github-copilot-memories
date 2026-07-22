---
description: "Use when the user asks to revise, create, or generate a README.md. Auto-invoked by requests such as 'revise the readme', 'create a readme', 'compose the readme', or 'generate the readme'. Fills in project-specific details and applies the standard structure, badges, and conditional sections."
agent: agent
---

Generate or revise the `README.md` for this GitHub repository using the template below.

If a `README.md` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `README.md` exists, create one from scratch.

Fill in all `[[PLACEHOLDER]]` values from the actual project. Remove any section or comment that does not apply (see the inline guidance). Do not leave any placeholder text, template comments, or example rows in the final output.

Rules:
- Include the `Build Status` badge only if a GitHub Actions workflow file exists in `.github/workflows/`.
- Include the `Latest Release` badge only if the repository has at least one published release.
- Include the `Website` badge only if the repository has a configured Website URL in its GitHub About section, or if GitHub Pages is enabled (i.e. a `gh-pages` branch or a `docs/` folder is published). Use the label `GitHub Pages` if the URL is a `github.io` domain, otherwise use `Website`.
- Include `## Installation` (NuGet section) only if this is a NuGet package, not an executable app. Place it directly above `## Development`.
- Include `### Release` using the appropriate variant: `dotnet pack` for NuGet packages; `npm run dist` for npm packages with a `dist` script configured; `bash ./release.sh` if `release.sh` exists; omit the section entirely for executables with no dedicated release process.
- Include `### Dependencies` only if there are non-test runtime dependencies. For .NET, omit test-only packages. For other project types, list only non-trivial runtime packages.
- Include the preview screenshot line only if `preview.png` exists in the repository root.
- Include `## Screenshots` only if a `screenshots/` directory exists in the repository root containing image files. Place it directly after the description paragraph.
- Include `## Known Limitations` only if there are real, notable caveats or missing features worth warning users about. Omit it otherwise.
- Include `## Configuration` if any of the following exist and contain at least one recognisable setting: `appsettings.json`, `config.json`, `config.yaml`, `config.toml`, or `settings.py`. If none has documented keys, omit the section entirely rather than leaving an empty or filler table.
- Include `### Environment Variables` within `## Configuration` only if `.env.example` exists.
- Include `## Roadmap` only if `ROADMAP.md` exists in the repository root.
- Include `## Project Structure` only if the solution has more than one project or the directory layout is non-obvious and genuinely helps orientation. Omit it for single-project solutions with a standard layout.
- Include `## Changelog` only if `CHANGELOG.md` exists in the repository root.
- Include `## Security` only if `SECURITY.md` exists in the repository root.
- Include `## Acknowledgements` only if the project builds on notable third-party work, data sources, or inspiration that warrants attribution.
- Include `### Docker` only if a `Dockerfile` exists in the repository root.
- Include `### Docker Compose` only if `docker-compose.yml` or `docker-compose.yaml` exists in the repository root.
- Always include `## Usage`. Even for trivial projects, at minimum show one example command or snippet.
- In `## License`, include "or later" only for GPL-family licences. Omit it for MIT, Apache, and other non-copyleft licences.
- Prefix each `##` heading with its emoji as shown in the template. Omit the emoji only if the existing README uses no emojis and the project's tone is formal (e.g. an enterprise SDK or internal tooling).
- For npm/Node.js projects, replace the .NET SDK requirement with the Node.js version, and replace dotnet commands with: `npm install` for the initial configuration, `npm run build` for building, `npm start` or `npm run dev` for running, and `npm test` for testing.
- For Python projects, replace the .NET SDK requirement with the Python version, and replace dotnet commands with: `python -m venv .venv && source .venv/bin/activate` and `pip install -r requirements.txt` for the initial configuration, `python [[entrypoint]]` or `python -m [[module]]` for running, and `pytest` for testing.
- For Go projects, replace the .NET SDK requirement with the Go version, and replace dotnet commands with: `go mod tidy` for the initial configuration, `go build ./...` for building, `go run ./cmd/[[entrypoint]]` for running, and `go test ./...` for testing.
- For Rust projects, replace the .NET SDK requirement with the Rust toolchain version, and replace dotnet commands with: `cargo build` for building, `cargo run` for running, and `cargo test` for testing.
- For Java projects, replace the .NET SDK requirement with the Java/JDK version and build tool (Maven or Gradle), and replace dotnet commands with the appropriate Maven or Gradle equivalents (`mvn install` / `gradle build`, `mvn test` / `gradle test`).
- Include `## 📚 Documentation` only if a `docs/` directory exists in the repository root, GitHub Pages is enabled, or the repository has a GitHub Wiki. Place it directly after `## 🗺️ Roadmap`.
- Include `## 🌐 API Reference` only if this is a library, SDK, or API project with auto-generated or hosted API documentation. Place it directly after `## 📚 Documentation` when that section is present, otherwise directly after `## 🗺️ Roadmap`.
- Always include `## 📑 Table of Contents` after the description paragraph and the `preview.png` image (if present), and before the first `##` section. Generate its entries dynamically: include one entry per `##`, `###`, and `####` heading that is actually present in the final output, in the order they appear, using the heading title stripped of its leading emoji as the link text, and a lowercased, emoji-stripped, space-to-hyphen anchor as the target. Indent `###` entries by two spaces and `####` entries by four spaces relative to the `##` entries. Omit entries for any sections that have been conditionally excluded.
- Remove all HTML comments from the final output.

---

[![Donate](https://img.shields.io/badge/-%E2%99%A5%20Donate-%23ff69b4)](https://hmlendea.go.ro/funding)
<!-- Only if the repository has at least one published release. -->
[![Latest Release](https://img.shields.io/github/v/release/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]])](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/releases/latest)
<!-- Only if the repository has a configured Website URL or GitHub Pages is enabled. Use label 'GitHub Pages' for github.io URLs, otherwise 'Website'. -->
[![Website](https://img.shields.io/badge/Website-Visit-blue)](https://[[WEBSITE_URL]])
<!-- Only if `.github/workflows/[WORKFLOW_FILE]` exists. -->
[![Build Status](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/actions/workflows/[[WORKFLOW_FILE]].yml/badge.svg)](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/actions/workflows/[[WORKFLOW_FILE]].yml)
<!-- Only if `LICENSE` exists. -->
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://gnu.org/licenses/gpl-3.0)

# [[Project Title]]

[[[Clear description of what this project does and why it is useful.]]]

<!-- Only if `preview.png` exists. -->
![Preview screenshot](preview.png)

## 📑 Table of Contents

<!-- Generate one entry per ## section present in the final output, in order. -->
- [[Section 1]]
  - [[Subsection 1.1]]
  - [[Subsection 1.2]]
- [[Section 2]]

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

<!-- Only if this is distributed as a Flatpak package. -->
### Flatpak CLI

```bash
flatpak install flathub [[FLATHUB_PACKAGE_ID]]
```

<!-- Only if this is distributed as a Snap package. -->
### Snap CLI

```bash
snap install [[SNAP_PACKAGE_ID]]
```

<!-- Only if this is distributed as an AUR package. -->
### AUR CLI

```bash
paru -S [[AUR_PACKAGE_ID]]
```
or, if you use `yay`:
```bash
yay -S [[AUR_PACKAGE_ID]]
```

<!-- Only if this is distributed as a NuGet package. -->
### .NET CLI

```bash
dotnet add package [[NUGET_PACKAGE_ID]]
```

<!-- Only if this is a NuGet package. -->
### Package Manager Console

```powershell
Install-Package [[NUGET_PACKAGE_ID]]
```

<!-- Only if this is an npm package. -->
### npm

```bash
npm install [[NPM_PACKAGE_ID]]
```

<!-- Only if `appsettings.json`, `config.json`, `config.yaml`, `config.toml`, or `settings.py` exists and has at least one documented setting. Omit entirely rather than leaving an empty or filler table. -->
## ⚙️ Configuration

All settings are loaded from `appsettings.json`. The subsequent keys are recognised:

| Section | Key | Description |
|---------|-----|-------------|
| [[Section]] | [[Key]] | [[Description]] |

<!-- Only if `.env.example` exists. -->
### Environment Variables

The subsequent environment variables can be set:

| Variable | Description | Default |
|----------|-------------|---------|
| `[[VARIABLE_NAME]]` | [[Description]] | `[[default value]]` |

## 🛠️ Development

### Requirements

<!-- Only if this is a .NET project. -->
- [.NET [[DOTNET_VERSION]] SDK](https://dotnet.microsoft.com/download/dotnet/[[DOTNET_VERSION]])
<!-- Only if other requirements exist. -->
- [[Additional requirement 1]]
- [[Additional requirement 2]]

<!-- Only if this is a .NET project. -->
All NuGet dependencies are restored automatically by `dotnet restore`.

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

## 🤝 Contributing

You are welcome to bring any suggestion, feedback or modification to this project.

When doing so, please:
<!-- Only if relevant (e.g. applications, libraries, mods, etc). -->
- Maintain cross-platform compatibility
<!-- Only if this is an API or library. -->
- Maintain the existing public contract intact unless a breaking change is intentional
- Maintain the pull requests as focused and consistent with the existing code style
<!-- Only if documentation and behaviour exists. -->
- Revise the documentation when behaviour changes
- Properly test all changes <!-- Only if tests exist, append: `, including edge cases and error conditions` -->
<!-- Only if tests exist. -->
- Add unit tests for any new or changed functionality

<!-- Only if `CONTRIBUTING.md` exists. -->
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
## 💝 Support

Discovered a bug or have a suggestion? [Open an issue](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/issues)!

If you find this project useful, consider [funding it](https://hmlendea.go.ro/funding) or starring ⭐️ it on GitHub!

[![Donate](https://raw.githubusercontent.com/hmlendea/readme-assets/master/donate_generic.png)](https://hmlendea.go.ro/funding)

<!-- Only if `LICENSE` exists. Add this exactly as it is written here, do not modify it in any way. -->
## 📄 License

Licensed under the `[[License Title]]`<!-- only for GPL-family licences, append: " or later" -->.
See [LICENSE](./LICENSE) for details.
