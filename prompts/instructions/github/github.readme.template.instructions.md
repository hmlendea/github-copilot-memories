---
description: "Use when the user asks to revise, create, or generate a README.md. Auto-invoked by requests such as 'revise the readme', 'create a readme', 'compose the readme', or 'generate the readme'. Fills in project-specific details and applies the standard structure, badges, and conditional sections."
applyTo: "README.md"
---
This is the `README.md` template that must be used.
---

<!-- BEGIN README TEMPLATE IMMUTABLE -->

<!-- Only if `.github/FUNDING.yml` exists. -->
[![Donate](https://img.shields.io/badge/-%E2%99%A5%20Donate-%23ff69b4)](https://hmlendea.go.ro/funding)
<!-- Only if the repository is public and it has at least one published release. -->
[![Latest Release](https://img.shields.io/github/v/release/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]])](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/releases/latest)
<!-- Only if the repository has a configured Website URL or GitHub Pages is enabled. Use label 'GitHub Pages' for github.io URLs, otherwise 'Website'. -->
[![Website](https://img.shields.io/badge/Website-Visit-blue)](https://[[WEBSITE_URL]])
<!-- Only if a primary GitHub Actions workflow exists. `[[WORKFLOW_FILE]]` includes its `.yml` or `.yaml` extension. -->
[![Build Status](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/actions/workflows/[[WORKFLOW_FILE]]/badge.svg)](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/actions/workflows/[[WORKFLOW_FILE]])
<!-- Only if code coverage reporting is configured. Use the provider's canonical badge and report URLs. -->
[[COVERAGE_BADGE]]
<!-- Only if an external code-quality or analysis service is configured. -->
[[CODE_QUALITY_BADGE]]
<!-- Only if the project is published to NuGet. -->
[![NuGet](https://img.shields.io/nuget/v/[[NUGET_PACKAGE_ID]])](https://nuget.org/packages/[[NUGET_PACKAGE_ID]])
<!-- Only if the project is published to npm. -->
[![npm](https://img.shields.io/npm/v/[[NPM_PACKAGE_ID]])](https://npmjs.com/package/[[NPM_PACKAGE_ID]])
<!-- Only if the project is published to PyPI. -->
[![PyPI](https://img.shields.io/pypi/v/[[PYPI_PACKAGE_ID]])](https://pypi.org/project/[[PYPI_PACKAGE_ID]])
<!-- Only if the project is published to crates.io. -->
[![Crates.io](https://img.shields.io/crates/v/[[CRATES_PACKAGE_ID]])](https://crates.io/crates/[[CRATES_PACKAGE_ID]])
<!-- Only if a public container image is published. -->
[[CONTAINER_BADGE]]
<!-- Only if `LICENSE` exists. -->
[![License](https://img.shields.io/github/license/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]])](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/blob/[[DEFAULT_BRANCH]]/LICENSE)
<!-- Only if other repository-evidenced status badges provide distinct, useful information. Omit vanity counters and redundant badges. -->
[[ADDITIONAL_STATUS_BADGES]]

<!-- Human-friendly project title (not necessarily the repository name). Must come after the badges. -->
# [[PROJECT_TITLE]]

[[PROJECT_DESCRIPTION]]

<!-- Only if project maturity, maintenance status, deprecation, archival, or a material stability warning merits prominent disclosure. -->
> **Project status:** [[PROJECT_STATUS]]

<!-- Only if `preview.png` exists. -->
![Preview screenshot](preview.png)

## 📑 Table of Contents

<!-- Generate one entry per `##`, `###`, and `####` heading present in the final output, in order. Indent each level by two spaces. Use the text and anchor without heading emojis. -->

<!-- Only if `screenshots/` directory exists with image files. -->
## 🖼️ Screenshots

<!-- Repeat for each useful screenshot; omit redundant or obsolete images. -->
![[[SCREENSHOT_DESCRIPTION]]](screenshots/[[SCREENSHOT_FILE]])

<!-- Only if a public interactive demonstration, sample instance, recorded demonstration, or representative media asset exists. -->
## 🎬 Demo

[[DEMO_CONTENT]]

## ✨ Capabilities

<!-- Repeat for each principal, evidenced capability. Prioritise user outcomes over implementation details. -->
- [[CAPABILITY]]

<!-- Only if the project supports multiple distinct audiences or workflows that benefit from concise orientation. -->
## 🎯 Use Cases

<!-- Repeat for each evidenced use case. -->
- **[[USE_CASE_NAME]]:** [[USE_CASE_DESCRIPTION]]

## 🚀 Usage

<!-- Provide a minimal but realistic example showing how to use the project. For CLI tools, demonstrate with a shell command. For libraries, demonstrate with a code snippet. For web apps, describe the main workflow. -->
[[USAGE_EXAMPLE]]

<!-- Only if an `examples/`, `samples/`, or equivalent directory exists, or multiple non-trivial examples are documented. -->
### Examples

[[EXAMPLES_DESCRIPTION]]

<!-- Only if a CLI, command system, task runner, or interactive console exposes multiple user-facing commands. Repeat rows as required. -->
## ⌨️ Command Reference

| Command | Description |
|---------|-------------|
| `[[COMMAND]]` | [[COMMAND_DESCRIPTION]] |

<!-- Only if a graphical or terminal interface exposes documented keyboard shortcuts. Repeat rows as required and state platform-specific variants. -->
## ⌨️ Keyboard Shortcuts

| Shortcut | Action | Context |
|----------|--------|---------|
| [[KEYBOARD_SHORTCUT]] | [[KEYBOARD_SHORTCUT_ACTION]] | [[KEYBOARD_SHORTCUT_CONTEXT]] |

<!-- Only if there are notable caveats, constraints, or missing capabilities worth emphasising. -->
## ⚠️ Known Limitations

<!-- Repeat for each material, evidenced limitation. -->
- [[LIMITATION]]

<!-- Only if this is an end-user application with meaningful OS, hardware, or runtime prerequisites. -->
## 🖥️ System Requirements

<!-- Repeat only for evidenced requirements. List operating systems in the priority order Linux, macOS, then Windows. Use `N/A` when no recommendation exists. -->
| Component | Minimum | Recommended |
|-----------|---------|-------------|
| [[REQUIREMENT_COMPONENT]] | [[MINIMUM_REQUIREMENT]] | [[RECOMMENDED_REQUIREMENT]] |

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
<!-- Only if the project uses another evidenced distribution channel. Include a canonical package or store link and repeat as required. -->
[[ADDITIONAL_DISTRIBUTION_BADGES]]

<!-- Only if at least one package-manager command applies. Include each applicable command and omit the rest. -->
### Package Manager Installation

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
<!-- Only if this is distributed as a Homebrew formula or cask. -->
```bash
brew install [[HOMEBREW_INSTALL_TARGET]]
```
<!-- Only if this is distributed through WinGet. -->
```powershell
winget install --id [[WINGET_PACKAGE_ID]] --exact
```
<!-- Only if this is distributed through Chocolatey. -->
```powershell
choco install [[CHOCO_PACKAGE_ID]]
```
<!-- Only if this is distributed through Scoop. Include `scoop bucket add` first only when a custom bucket is necessary. -->
```powershell
[[SCOOP_INSTALL_COMMANDS]]
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
<!-- Only if this is distributed as a PyPI package. -->
```bash
python -m pip install [[PYPI_PACKAGE_ID]]
```
<!-- Only if this is distributed through conda-forge. -->
```bash
conda install --channel conda-forge [[CONDA_PACKAGE_ID]]
```
<!-- Only if this is a Rust library distributed through crates.io. -->
```bash
cargo add [[CRATES_PACKAGE_ID]]
```
<!-- Only if this is a Rust executable distributed through crates.io. -->
```bash
cargo install [[CRATES_PACKAGE_ID]]
```
<!-- Only if this is distributed through RubyGems. -->
```bash
gem install [[RUBYGEMS_PACKAGE_ID]]
```
<!-- Only if this is distributed through Packagist. -->
```bash
composer require [[PACKAGIST_PACKAGE_ID]]
```
<!-- Only if this is a Go executable intended for installation with `go install`. -->
```bash
go install [[GO_INSTALL_PATH]]@[[GO_INSTALL_VERSION]]
```
<!-- Only for additional evidenced package managers not represented above. -->
[[ADDITIONAL_PACKAGE_MANAGER_INSTRUCTIONS]]

<!-- Only if this is a Maven-compatible library distributed through Maven Central. -->
#### Maven

```xml
<dependency>
	<groupId>[[MAVEN_GROUP_ID]]</groupId>
	<artifactId>[[MAVEN_ARTIFACT_ID]]</artifactId>
	<version>[[MAVEN_VERSION]]</version>
</dependency>
```

<!-- Only if this is a Gradle-compatible library distributed through Maven Central. -->
#### Gradle

```kotlin
dependencies {
	implementation("[[MAVEN_GROUP_ID]]:[[MAVEN_ARTIFACT_ID]]:[[MAVEN_VERSION]]")
}
```

<!-- Only if a public OCI container image is distributed. Use the repository's documented Docker-, Podman-, or registry-specific command. -->
### Container Image

```bash
[[CONTAINER_PULL_COMMAND]]
```

<!-- Only if users install downloadable archives, executables, installers, extensions, plug-ins, or other manually distributed artefacts. -->
### Manual Installation

[[MANUAL_INSTALLATION_STEPS]]

<!-- Only if source installation is supported for end users rather than solely for contributors. -->
### Installation from Source

```bash
[[SOURCE_INSTALLATION_COMMANDS]]
```

<!-- Only if there is a concise command or observable result that confirms a correct installation. -->
### Verification

```bash
[[INSTALLATION_VERIFICATION_COMMAND]]
```

<!-- Only if the upgrade process requires more than repeating the installation command. -->
### Upgrading

[[UPGRADE_INSTRUCTIONS]]

<!-- Only if uninstallation leaves data, services, configuration, or other resources, or requires a non-obvious command. -->
### Uninstallation

[[UNINSTALLATION_INSTRUCTIONS]]

<!-- Only if the repository evidences user-configurable settings through configuration files, `.env.example`, command-line options, or public configuration APIs. Include only evidenced settings and never expose secret values. -->
## ⚙️ Configuration

[[CONFIGURATION_OVERVIEW]]

<!-- Only if one or more configuration files contain public settings. -->
### Configuration Files

| File | Scope | Purpose |
|------|-------|---------|
| `[[CONFIGURATION_FILE]]` | [[CONFIGURATION_SCOPE]] | [[CONFIGURATION_FILE_PURPOSE]] |

<!-- Only if one or more public settings are documented or directly evidenced. Use `—` where a section, default, or applicable value does not exist. -->
### Settings

The subsequent settings are recognised:
| Section | Key | Type | Default | Required | Description |
|---------|-----|------|---------|----------|-------------|
| [[CONFIGURATION_SECTION]] | `[[CONFIGURATION_KEY]]` | `[[CONFIGURATION_TYPE]]` | `[[CONFIGURATION_DEFAULT]]` | [[CONFIGURATION_REQUIRED]] | [[CONFIGURATION_DESCRIPTION]] |

<!-- Only if `.env.example` exists. -->
### Environment Variables

The subsequent environment variables can be set:
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `[[ENVIRONMENT_VARIABLE]]` | [[ENVIRONMENT_VARIABLE_REQUIRED]] | `[[ENVIRONMENT_VARIABLE_DEFAULT]]` | [[ENVIRONMENT_VARIABLE_DESCRIPTION]] |

<!-- Only if an executable exposes documented command-line options beyond standard help and version options. -->
### Command-Line Options

| Option | Value | Default | Description |
|--------|-------|---------|-------------|
| `[[COMMAND_LINE_OPTION]]` | `[[COMMAND_LINE_VALUE]]` | `[[COMMAND_LINE_DEFAULT]]` | [[COMMAND_LINE_DESCRIPTION]] |

<!-- Only if multiple configuration sources have a defined precedence. List sources from highest to lowest precedence. -->
### Precedence

[[CONFIGURATION_PRECEDENCE]]

<!-- Only if configuration changes require a reload, restart, or explicit command, or if hot reload is supported. -->
### Reload Behaviour

[[CONFIGURATION_RELOAD_BEHAVIOUR]]

<!-- Only if named profiles, environments, layered files, or per-user and system-wide scopes exist. -->
### Profiles and Scopes

[[CONFIGURATION_PROFILES_AND_SCOPES]]

<!-- Only if secret references, credential stores, secret files, or external secret providers are configured. Document names and sources, never values. -->
### Secret Management

[[SECRET_MANAGEMENT_INSTRUCTIONS]]

<!-- Only if the application binds, exposes, or requires documented network ports. Repeat rows as required. -->
### Network Ports

| Port | Protocol | Direction | Purpose | Required |
|------|----------|-----------|---------|----------|
| `[[NETWORK_PORT]]` | [[NETWORK_PROTOCOL]] | [[NETWORK_DIRECTION]] | [[NETWORK_PURPOSE]] | [[NETWORK_PORT_REQUIRED]] |

<!-- Only if a command, endpoint, or observable result validates the effective configuration. -->
### Validation

[[CONFIGURATION_VALIDATION_INSTRUCTIONS]]

<!-- Only if localisation signals are detected anywhere in the repository (directories like `locales/`, `i18n/`, `translations/`, `Localisation/`, `Localization/`; files like `LocalisationStrings.*`, `LocalizationStrings.*`, `LocaleService.*`, `LocalisationManager.*`; or language-code JSON files inside localisation-related directories). -->
## 🌍 Localisation

[[LOCALISATION_OVERVIEW]]

<!-- Repeat for each evidenced locale. Use standards-compliant locale identifiers where available. -->
| Language | Locale | Status |
|----------|--------|--------|
| [[LANGUAGE]] | `[[LOCALE_CODE]]` | [[TRANSLATION_STATUS]] |

<!-- Only if a documented translation contribution process exists. -->
### Contributing Translations

[[TRANSLATION_CONTRIBUTION_INSTRUCTIONS]]

<!-- Only if compatibility with runtimes, browsers, operating systems, game versions, protocols, file formats, or host applications is material to users. -->
## 🧩 Compatibility

<!-- Repeat for each compatibility boundary. State unsupported versions explicitly when evidenced. -->
| Component | Supported Versions | Notes |
|-----------|--------------------|-------|
| [[COMPATIBILITY_COMPONENT]] | [[SUPPORTED_VERSIONS]] | [[COMPATIBILITY_NOTES]] |

<!-- Only if the project integrates with external services, platforms, plug-ins, extensions, or optional providers. -->
## 🔌 Integrations

<!-- Repeat for each evidenced integration. -->
| Integration | Compatibility | Purpose | Required |
|-------------|---------------|---------|----------|
| [[INTEGRATION_NAME]] | [[INTEGRATION_COMPATIBILITY]] | [[INTEGRATION_PURPOSE]] | [[INTEGRATION_REQUIRED]] |

<!-- Only if users or API clients must authenticate, or if roles, scopes, or access-control boundaries are public and material. Do not include credentials, tokens, private endpoints, or unsafe examples. -->
## 🔐 Authentication and Authorisation

[[AUTHENTICATION_OVERVIEW]]

<!-- Only if public roles, scopes, or permissions are evidenced. Repeat rows as required. -->
| Role or Scope | Access | Intended Audience |
|---------------|--------|-------------------|
| `[[ROLE_OR_SCOPE]]` | [[ACCESS_DESCRIPTION]] | [[ACCESS_AUDIENCE]] |

<!-- Only if the project exposes a public plug-in, extension, hook, provider, middleware, theme, or scripting system. -->
## 🧱 Extensibility

[[EXTENSIBILITY_OVERVIEW]]

<!-- Repeat for each public extension point when a concise inventory aids users. -->
| Extension Point | Contract | Purpose |
|-----------------|----------|---------|
| [[EXTENSION_POINT]] | [[EXTENSION_CONTRACT]] | [[EXTENSION_PURPOSE]] |

<!-- Only if the application requests operating-system, browser, mobile, game-server, or cloud permissions that users must grant. -->
## 🔑 Permissions

<!-- Repeat for each requested permission. Distinguish mandatory permissions from optional ones. -->
| Permission | Required | Purpose |
|------------|----------|---------|
| [[PERMISSION]] | [[PERMISSION_REQUIRED]] | [[PERMISSION_PURPOSE]] |

<!-- Only if the project collects, processes, transmits, or persists user data, analytics, diagnostics, or telemetry. Document only repository-evidenced conduct. -->
## 🛡️ Privacy and Data

<!-- Repeat for each data category. Never include genuine personal data, credentials, or secret values. -->
| Data | Purpose | Storage | Retention | Optional |
|------|---------|---------|-----------|----------|
| [[DATA_CATEGORY]] | [[DATA_PURPOSE]] | [[DATA_STORAGE]] | [[DATA_RETENTION]] | [[DATA_OPTIONAL]] |

<!-- Only if users must locate, transfer, inspect, reset, or delete application data. Repeat rows for platform-specific locations. -->
### Data Locations

| Platform or Scope | Location | Contents |
|-------------------|----------|----------|
| [[DATA_PLATFORM_OR_SCOPE]] | `[[DATA_LOCATION]]` | [[DATA_LOCATION_CONTENTS]] |

<!-- Only if analytics, diagnostics, or telemetry can be configured or deactivated. -->
### Telemetry Controls

[[TELEMETRY_CONTROL_INSTRUCTIONS]]

<!-- Only if a user-facing application or interface has documented accessibility support, constraints, or conformance. -->
## ♿ Accessibility

[[ACCESSIBILITY_INFORMATION]]

<!-- Only if the repository provides a local development workflow. Omit in content-only repositories without executable development steps. -->
## 🛠️ Development

<!-- Include every required SDK, runtime, tool, service, and version constraint. Link to canonical installation sources where useful. -->
### Requirements

<!-- Only if this is a .NET project. -->
- [.NET [[DOTNET_VERSION]] SDK](https://dotnet.microsoft.com/download/dotnet/[[DOTNET_VERSION]])
<!-- Only if other requirements exist. -->
- [[Additional requirement 1]]
- [[Additional requirement 2]]

<!-- Include source checkout, submodules or Git LFS when applicable, dependency restoration, local configuration, and required service initialisation. -->
### Setup

[[DEVELOPMENT_SETUP]]

<!-- Only if compilation, bundling, packaging, or asset generation is required. Include the canonical development command. -->
### Build

[[BUILD_INSTRUCTIONS]]

<!-- Only if the project can be executed locally. Include required services, working directory, arguments, and local URL where relevant. -->
### Run

[[RUN_INSTRUCTIONS]]

<!-- Only if tests exist. -->
### Test

[[TEST_INSTRUCTIONS]]

<!-- Only if coverage can be generated locally. Include the report location. -->
### Coverage

[[COVERAGE_INSTRUCTIONS]]

<!-- Only if integration tests have prerequisites or commands distinct from the principal test command. -->
### Integration Tests

[[INTEGRATION_TEST_INSTRUCTIONS]]

<!-- Only if end-to-end tests have prerequisites or commands distinct from the principal test command. -->
### End-to-End Tests

[[END_TO_END_TEST_INSTRUCTIONS]]

<!-- Only if a lint configuration or canonical lint command exists. -->
### Linting

[[LINT_INSTRUCTIONS]]

<!-- Only if a formatter or formatting check is configured. -->
### Formatting

[[FORMATTING_INSTRUCTIONS]]

<!-- Only if a separate static type-checking command exists. -->
### Type Checking

[[TYPE_CHECK_INSTRUCTIONS]]

<!-- Only if additional static analysis, dependency auditing, or security scanning is configured and useful locally. -->
### Static Analysis

[[STATIC_ANALYSIS_INSTRUCTIONS]]

<!-- Only if generated source, schemas, clients, assets, or localisation files must be refreshed. State whether generated files are committed. -->
### Code Generation

[[CODE_GENERATION_INSTRUCTIONS]]

<!-- Only if local development requires database creation, seeding, emulation, or migrations. Never include genuine credentials or production data. -->
### Database Setup

[[DATABASE_SETUP_INSTRUCTIONS]]

<!-- Only if project documentation can be generated or previewed locally. -->
### Documentation

[[DOCUMENTATION_DEVELOPMENT_INSTRUCTIONS]]

<!-- Only if a benchmark suite exists. Include any release-mode or hardware considerations necessary for representative results. -->
### Benchmarks

[[BENCHMARK_INSTRUCTIONS]]

<!-- Only if the repository documents a non-obvious debugging or profiling workflow. -->
### Debugging and Profiling

[[DEBUGGING_AND_PROFILING_INSTRUCTIONS]]

<!-- Only if `Dockerfile` exists. -->
### Docker

[[DOCKER_DEVELOPMENT_INSTRUCTIONS]]

<!-- Only if `compose.yml`, `compose.yaml`, `docker-compose.yml`, or `docker-compose.yaml` exists. -->
### Docker Compose

[[COMPOSE_DEVELOPMENT_INSTRUCTIONS]]

<!-- Only if continuous-integration checks or workflows merit contributor guidance. Summarise required checks and how to reproduce them locally. -->
### Continuous Integration

[[CONTINUOUS_INTEGRATION_INSTRUCTIONS]]

<!-- Only if maintainers have an evidenced packaging or release process and the exact .NET `release.sh` variant below does not apply. Include versioning, artefact, signing, and publication steps that are safe to disclose. Identify every remotely executed script and prominently instruct readers to inspect it first. -->
### Release

[[RELEASE_INSTRUCTIONS]]

<!-- Only if `release.sh` exists. -->
### Release

The repository includes `release.sh`, which delegates to the upstream deployment script used by the project maintainer.

```bash
bash ./release.sh [[LATEST_RELEASE_VERSION_WITHOUT_V_PREFIX]]
```

This script downloads and executes an external release helper from `https://raw.githubusercontent.com/hmlendea/deployment-scripts/master/release/dotnet/[[DOTNET_VERSION]].sh`.

**Note:** Piping into `bash` is an intensely controversial topic. Please review any external scripts before running them in your environment!

<!-- Only if direct, non-trivial dependencies merit explanation. Repeat rows as required and classify their scope, such as runtime, development, build, or optional. -->
### Dependencies

| Package | Version | Scope | Purpose |
|---------|---------|-------|---------|
| [[DEPENDENCY]] | [[DEPENDENCY_VERSION]] | [[DEPENDENCY_SCOPE]] | [[DEPENDENCY_PURPOSE]] |

<!-- Only if the solution has more than one project or the directory layout is non-obvious. -->
## 🗂️ Project Structure

[[PROJECT_STRUCTURE_OVERVIEW]]

<!-- Only if the repository contains multiple projects, packages, applications, services, or modules. Repeat rows as required. -->
### Projects and Packages

| Project | Type | Purpose |
|---------|------|---------|
| `[[PROJECT_PATH]]` | [[PROJECT_TYPE]] | [[PROJECT_PURPOSE]] |

<!-- Repeat for each principal, non-obvious directory. -->
### Directories

| Directory | Purpose |
|-----------|---------|
| `[[DIRECTORY_PATH]]` | [[DIRECTORY_PURPOSE]] |

<!-- Only if `ARCHITECTURE.md` exists or a `docs/architecture/` directory contains substantive documentation. -->
## 🏗️ Architecture

See the [[ARCHITECTURE_DOCUMENT_LINK]] for the system context, principal components, runtime flows, ownership boundaries, dependencies, constraints, and extension points.

<!-- Only if the project is deployed as an application, service, website, infrastructure component, or self-hosted system. Include only evidenced procedures and never include secret values or private production endpoints. -->
## 🚢 Deployment

[[DEPLOYMENT_OVERVIEW]]

<!-- Only if multiple deployment environments or targets are documented. Repeat rows as required. -->
### Environments

| Environment | Purpose | Deployment Method |
|-------------|---------|-------------------|
| [[DEPLOYMENT_ENVIRONMENT]] | [[DEPLOYMENT_PURPOSE]] | [[DEPLOYMENT_METHOD]] |

<!-- Only if deployment configuration or secret provisioning requires explanation beyond the Configuration section. Document secret names and sources, never their values. -->
### Configuration and Secrets

[[DEPLOYMENT_CONFIGURATION_INSTRUCTIONS]]

<!-- Only if deployment requires database or state migrations. Include ordering and rollback constraints. -->
### Database Migrations

[[DEPLOYMENT_MIGRATION_INSTRUCTIONS]]

<!-- Only if the deployed system exposes health, readiness, or liveness checks. -->
### Health Checks

[[HEALTH_CHECK_INFORMATION]]

<!-- Only if logs, metrics, traces, alerts, or dashboards are documented for operators. Do not expose private observability endpoints. -->
### Observability

[[OBSERVABILITY_INFORMATION]]

<!-- Only if the system persists state that operators must back up or recover. -->
### Backup and Restore

[[BACKUP_AND_RESTORE_INSTRUCTIONS]]

<!-- Only if a documented rollback or disaster-recovery procedure exists. -->
### Rollback and Recovery

[[ROLLBACK_AND_RECOVERY_INSTRUCTIONS]]

<!-- Only if `ROADMAP.md` exists. -->
## 🗺️ Roadmap

See [ROADMAP.md](./ROADMAP.md) for planned work and forthcoming changes.

<!-- Only if docs/ directory, GitHub Pages, or GitHub Wiki exists. -->
## 📚 Documentation

[[DOCUMENTATION_OVERVIEW]]

<!-- Repeat for each principal documentation resource. -->
| Resource | Description |
|----------|-------------|
| [[DOCUMENTATION_RESOURCE]] | [[DOCUMENTATION_DESCRIPTION]] |

<!-- Only if this is a library, SDK, or API project with auto-generated or hosted documentation. -->
## 🌐 API Reference

[[API_REFERENCE]]

<!-- Only if the project exposes public file formats, schemas, network protocols, import/export contracts, or serialisation formats that users implement directly. -->
## 🧾 Data Formats and Protocols

<!-- Repeat for each public contract. -->
| Format or Protocol | Specification | Purpose |
|--------------------|---------------|---------|
| [[FORMAT_OR_PROTOCOL]] | [[SPECIFICATION_REFERENCE]] | [[FORMAT_OR_PROTOCOL_PURPOSE]] |

<!-- Only if a documented versioning scheme, stability guarantee, support window, or deprecation policy exists. -->
## 🏷️ Versioning

[[VERSIONING_POLICY]]

<!-- Only if `MIGRATION.md` or `UPGRADING.md` exists. -->
## 🔄 Migration Guide

[[MIGRATION_GUIDE_REFERENCE]]

<!-- Only if recurring, evidenced problems have concise diagnostic procedures or resolutions. Do not invent speculative problems. -->
## 🩺 Troubleshooting

<!-- Repeat for each evidenced problem. -->
| Symptom | Probable Cause | Resolution |
|---------|----------------|------------|
| [[TROUBLESHOOTING_SYMPTOM]] | [[TROUBLESHOOTING_CAUSE]] | [[TROUBLESHOOTING_RESOLUTION]] |

<!-- Only if `FAQ.md` exists. -->
## ❓ FAQ

See [FAQ.md](./FAQ.md) for responses to frequently raised inquiries.

<!-- Always include. -->
## 🤝 Contributing

You are welcome to submit any suggestion, feedback, or modification to this project.

When doing so, please:
- Maintain cross-platform compatibility <!-- Only if relevant to the project. -->
- Preserve the existing public contract unless a breaking change is intentional <!-- Only if this is a library, SDK, API, plug-in platform, or other project with a public contract. -->
- Submit focused pull requests that conform to the existing code style
- Maintain your branch synchronised with `[[DEFAULT_BRANCH]]`
- Revise the documentation when functionality changes <!-- Only if documentation and executable functionality exist. -->
- Properly test all modifications, including edge cases and error conditions <!-- Only if tests exist. -->
- Add tests for additional or modified functionality <!-- Only if tests exist. -->

<!-- Only if `CONTRIBUTING.md` exists in this repository's root directory. -->
Consult [CONTRIBUTING.md](./CONTRIBUTING.md) for further information on contributing to this project.

<!-- Only if `CODE_OF_CONDUCT.md` exists in the repository root or `.github/` directory. -->
## 📜 Code of Conduct

See the [[CODE_OF_CONDUCT_DOCUMENT_LINK]] for the standards of conduct expected in all project spaces.

<!-- Only if `GOVERNANCE.md`, `MAINTAINERS.md`, `OWNERS`, or another public governance document exists, or if project decision-making and stewardship are otherwise documented. -->
## 🧭 Governance

[[GOVERNANCE_INFORMATION]]

<!-- Only if there are related projects. -->
## 🔗 Related Projects

<!-- Repeat for each directly related project. -->
- [[RELATED_PROJECT]]: [[RELATED_PROJECT_DESCRIPTION]]

<!-- Only if there are notable third-party works, data sources, or inspiration worth attributing. -->
## 🙏 Acknowledgements

<!-- Repeat for each warranted acknowledgement. -->
- [[ACKNOWLEDGEMENT]]

<!-- Only if `CITATION.cff`, `CITATION.bib`, or equivalent citation metadata exists, or the project is an academic or research artefact. -->
## 📝 Citation

[[CITATION_INFORMATION]]

<!-- Only if `CHANGELOG.md` exists. -->
## 📋 Changelog

See [CHANGELOG.md](./CHANGELOG.md) for a full history of changes.

<!-- Only if `SECURITY.md` exists. -->
## 🔒 Security

For information on reporting security vulnerabilities, see [SECURITY.md](./SECURITY.md).

<!-- Only if `SUPPORT.md`, a public discussion forum, community channel, or another documented support route exists. Distinguish support inquiries from security disclosures. -->
## 💬 Support

[[SUPPORT_INFORMATION]]

<!-- Always include. -->
## 💝 Project Engagement

Discovered a problem or have a suggestion? [Open an issue](https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/issues)!

<!-- Set `[[FUNDING_PREFIX]]` to `[funding it](https://hmlendea.go.ro/funding) or ` only if `.github/FUNDING.yml` exists; otherwise set it to an empty value. -->
If you find this project useful, consider [[FUNDING_PREFIX]]starring ⭐️ it on GitHub!

<!-- Only if `.github/FUNDING.yml` exists. -->
[![Donate](https://raw.githubusercontent.com/hmlendea/readme-assets/master/donate_generic.png)](https://hmlendea.go.ro/funding)

<!-- Only if `./LICENSE` exists. Add this exactly as it is written here, do not modify it in any way. -->
## 📄 License

This project is being distributed under the `[[License Title]]`<!-- Only for GPL-family licences, append: " or later" -->.
See [LICENSE](./LICENSE) for further information.

<!-- END README TEMPLATE IMMUTABLE -->
