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
- Remove all HTML comments from the final output.

---

[![Donate](https://img.shields.io/badge/-%E2%99%A5%20Donate-%23ff69b4)](https://hmlendea.go.ro/funding)
[![Latest Release](https://img.shields.io/github/v/release/[[GITHUB_USERNAME]]/[[REPO_NAME]])](https://github.com/[[GITHUB_USERNAME]]/[[REPO_NAME]]/releases/latest)
<!-- Only if `.github/workflows/[WORKFLOW_FILE]` exists. -->
[![Build Status](https://github.com/[[GITHUB_USERNAME]]/[[REPO_NAME]]/actions/workflows/[[WORKFLOW_FILE]].yml/badge.svg)](https://github.com/[[GITHUB_USERNAME]]/[[REPO_NAME]]/actions/workflows/[[WORKFLOW_FILE]].yml)
<!-- Only if `LICENSE` exists. -->
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://gnu.org/licenses/gpl-3.0)

# [[Project Title]]

[[[Clear description of what this project does and why it is useful.]]]

<!-- Only if `preview.png` exists. -->
![Preview screenshot](preview.png)

## Features

- [[Feature 1]]
- [[Feature 2]]

<!-- For NuGet packages only: include this Installation section. -->
## Installation

[![Get it from NuGet](https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/nuget.png)](https://nuget.org/packages/[[PACKAGE_ID]])

### .NET CLI

```bash
dotnet add package [[PACKAGE_ID]]
```

### Package Manager Console

```powershell
Install-Package [[PACKAGE_ID]]
```

<!-- Only if `appsettings.json` exists. -->
## Configuration

All settings are loaded from `appsettings.json`. The following keys are recognised:

| Section | Key | Description |
|---------|-----|-------------|
| ....... | ... | ........... |

## Development

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

<!-- Only if `release.sh` exists. -->
### Release

The repository includes `release.sh`, which delegates to the upstream deployment script used by the project maintainer.

```bash
bash ./release.sh 1.0.0
```

This script downloads and executes an external release helper from `https://raw.githubusercontent.com/hmlendea/deployment-scripts/master/release/dotnet/[[DOTNET_VERSION]].sh`.

**Note:** Piping into `bash` is an intensely controversial topic. Please review any external scripts before running them in your environment!

## Project Structure

The solution contains the following projects:

- [[ProjectName]]: [[purpose]]

Key directories inside `[[MAIN_PROJECT_NAME]]/`:

| Directory | Purpose |
|-----------|---------|
| [[dir]]   | [[purpose]] |

<!-- Include the Dependencies section only if there are non-test runtime NuGet dependencies. -->
### Dependencies

| Package | Purpose |
|---------|---------|
| [[package]] | [[purpose]] |

## Contributing

Contributions are welcome. Please:
- Keep changes cross-platform
- Keep the existing public API intact unless a breaking change is intentional
- Keep pull requests focused and consistent with the existing code style
- Update documentation when behaviour changes

<!-- Only if `CONTRIBUTING.md` exists. -->
See [CONTRIBUTING.md](./CONTRIBUTING.md) for more details on contributing to this project.

## Support

If you find this project useful, consider [funding it](https://hmlendea.go.ro/funding) or giving a ⭐️ on GitHub!

<!-- Only if `LICENSE` exists. -->
## License

Licensed under the **[[License Title]]** or later.
See [LICENSE](./LICENSE) for details.
