---
description: "Use when the user asks to update, create, or generate a README.md. Auto-invoked by requests such as 'update the readme', 'create a readme', 'write the readme', or 'generate the readme'. Fills in project-specific details and applies the standard structure, badges, and conditional sections."
mode: generate
---

Generate or update the `README.md` for this GitHub repository using the template below.

If a `README.md` already exists, preserve any content that is correct and up to date, and update only what has changed or is missing. If no `README.md` exists, create one from scratch.

Fill in all `[[PLACEHOLDER]]` values from the actual project. Remove any section or comment that does not apply (see the inline guidance). Do not leave any placeholder text, template comments, or example rows in the final output.

Rules:
- Include the `Build Status` badge only if a GitHub Actions workflow file exists in `.github/workflows/`.
- Include `## Installation` (NuGet section) only if this is a NuGet package, not an executable app. Place it directly above `## Development`.
- Include `### Release` only if the project produces an executable output (i.e. it is not a NuGet package).
- Include `### Dependencies` only if there are non-test runtime NuGet dependencies. Do not list test-only packages.
- Include the preview screenshot line only if `preview.png` exists in the repository root.
- Include `## Known Limitations` only if there are real, notable caveats or missing features worth warning users about. Omit it otherwise.
- Include `## Configuration` only if `appsettings.json` exists and contains at least one recognisable setting. If it exists but has no documented keys, omit the section entirely rather than leaving an empty or filler table.
- Include `## Project Structure` only if the solution has more than one project or the directory layout is non-obvious and genuinely helps orientation. Omit it for single-project solutions with a standard layout.
- Include `## Changelog` only if `CHANGELOG.md` exists in the repository root.
- Include `## Security` only if `SECURITY.md` exists in the repository root.
- Include `## Acknowledgements` only if the project builds on notable third-party work, data sources, or inspiration that warrants attribution.
- Include `### Docker` only if a `Dockerfile` exists in the repository root.
- Always include `## Usage`. Even for trivial projects, at minimum show one example command or snippet.
- In `## License`, include "or later" only for GPL-family licences. Omit it for MIT, Apache, and other non-copyleft licences.
- Prefix each `##` heading with its emoji as shown in the template. Omit the emoji only if the existing README uses no emojis and the project's tone is formal (e.g. an enterprise SDK or internal tooling).
- Remove all HTML comments from the final output.

---

[![Donate](https://img.shields.io/badge/-%E2%99%A5%20Donate-%23ff69b4)](https://hmlendea.go.ro/funding)
[![Latest Release](https://img.shields.io/github/v/release/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]])](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/releases/latest)
<!-- Only if `.github/workflows/[WORKFLOW_FILE]` exists. -->
[![Build Status](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/actions/workflows/[[WORKFLOW_FILE]].yml/badge.svg)](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/actions/workflows/[[WORKFLOW_FILE]].yml)
<!-- Only if `LICENSE` exists. -->
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://gnu.org/licenses/gpl-3.0)

# [[Project Title]]

[[[Clear description of what this project does and why it is useful.]]]

<!-- Only if `preview.png` exists. -->
![Preview screenshot](preview.png)

## ✨ Features

- [[Feature 1]]
- [[Feature 2]]

## 🚀 Usage

<!-- Provide a minimal but realistic example showing how to use the project. For CLI tools, show a shell command. For libraries, show a code snippet. For web apps, describe the main workflow. -->
[[Usage example]]

<!-- Only if there are notable caveats, constraints, or missing features worth highlighting. -->
## ⚠️ Known Limitations

- [[Limitation 1]]

<!-- For NuGet packages only: include this Installation section. -->
## 📦 Installation

[![Get it from NuGet](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/nuget.png)](https://nuget.org/packages/[[PACKAGE_ID]])

### .NET CLI

```bash
dotnet add package [[PACKAGE_ID]]
```

### Package Manager Console

```powershell
Install-Package [[PACKAGE_ID]]
```

<!-- Only if `appsettings.json` exists and has at least one documented setting. Omit entirely rather than leaving an empty or filler table. -->
## ⚙️ Configuration

All settings are loaded from `appsettings.json`. The following keys are recognised:

| Section | Key | Description |
|---------|-----|-------------|
| [[Section]] | [[Key]] | [[Description]] |

## 🛠️ Development

### Requirements

<!-- Only if this is a .NET project. -->
- [.NET [[DOTNET_VERSION]] SDK](https://dotnet.microsoft.com/download)
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

<!-- Only if there are non-test runtime NuGet dependencies. -->
### Dependencies

| Package | Purpose |
|---------|--------|
| [[package]] | [[purpose]] |

<!-- Only if `release.sh` exists. -->
### Release

The repository includes `release.sh`, which delegates to the upstream deployment script used by the project maintainer.

```bash
bash ./release.sh 1.0.0
```

This script downloads and executes an external release helper from `https://raw.githubusercontent.com/hmlendea/deployment-scripts/master/release/dotnet/[[DOTNET_VERSION]].sh`.

**Note:** Piping into `bash` is an intensely controversial topic. Please review any external scripts before running them in your environment!

<!-- Only if the solution has more than one project or the directory layout is non-obvious. -->
## 🗂️ Project Structure

The solution contains the following projects:

- [[ProjectName]]: [[purpose]]

Key directories inside `[[MAIN_PROJECT_NAME]]/`:

| Directory | Purpose |
|-----------|---------|
| [[dir]]   | [[purpose]] |


## 🤝 Contributing

Contributions are welcome. Please:
- Keep changes cross-platform
<!-- Only if this is an API or library. -->
- Keep the existing public contract intact unless a breaking change is intentional
- Keep pull requests focused and consistent with the existing code style
- Update documentation when behaviour changes
<!-- Only if tests exist. -->
- Add unit tests for any new or changed functionality

<!-- Only if `CONTRIBUTING.md` exists. -->
See [CONTRIBUTING.md](./CONTRIBUTING.md) for more details on contributing to this project.

<!-- Only if there are notable third-party works, data sources, or inspiration worth attributing. -->
## 🙏 Acknowledgements

- [[Acknowledgement 1]]

<!-- Only if `CHANGELOG.md` exists. -->
## 📋 Changelog

See [CHANGELOG.md](./CHANGELOG.md) for a full history of changes.

<!-- Only if `SECURITY.md` exists. -->
## 🔒 Security

For information on reporting security vulnerabilities, see [SECURITY.md](./SECURITY.md).

## 💬 Support

Found a bug or have a suggestion? [Open an issue](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/issues)!

If you find this project useful, consider [funding it](https://hmlendea.go.ro/funding) or giving a ⭐️ on GitHub!

<!-- Only if `LICENSE` exists. -->
## 📄 License

Licensed under the `[[License Title]]`<!-- only for GPL-family licences, append: " or later" -->.
See [LICENSE](./LICENSE) for details.
