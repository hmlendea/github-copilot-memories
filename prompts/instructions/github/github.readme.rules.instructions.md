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

1. Start from `github.readme.template.instructions.md` and process it from top to bottom.
2. Resolve every `Always include` and `Only if` directive from repository evidence before composing content.
3. Remove each inapplicable conditional block in its entirety, including its heading, body, example rows, associated badge, and directive comment.
4. For every included block, preserve the template-defined heading, relative order, and fixed prose. Replace only placeholders, repeatable examples, and content explicitly designated by comments.
5. Replace scalar placeholders such as `[[PROJECT_TITLE]]` with one evidence-based value.
6. Expand content placeholders such as `[[USAGE_EXAMPLE]]`, `[[DEVELOPMENT_SETUP]]`, and `[[RELEASE_INSTRUCTIONS]]` into the complete Markdown required by that block, including paragraphs, lists, tables, or fenced code blocks.
7. Duplicate rows, list items, screenshots, badges, or other examples only when an adjacent template comment says `Repeat` or otherwise expressly permits repetition. When adjacent directives define mutually exclusive variants with identical headings, include exactly one matching variant.
8. Remove an optional placeholder together with its containing conditional block when no evidenced content applies. Never preserve an empty heading, table, list, or code block.
9. Additional sections are permitted only when genuinely material repository information has no suitable template section. Position each addition after the nearest related template section without reordering template-defined sections.
10. Apply language, spelling, and phrasing rules to placeholder values and additive content. Do not rephrase fixed template prose while generating a README.
11. Use project-native commands from scripts, manifests, task definitions, CI workflows, or existing documentation. The strict template does not impose a framework or toolchain.
12. Remove all template comments and unused examples from the final README.

### Evidence Requirements

Use the subsequent evidence priority:
1. Repository source, documentation, manifests, configuration examples, scripts, workflows, and policy files
2. Git metadata, release tags, package metadata, and configured repository remotes
3. Public repository metadata, package registries, hosted documentation, and deployment metadata when accessible
4. One concise user clarification when a mandatory value remains indeterminate

Do not infer unsupported capabilities, compatibility, guarantees, package availability, support channels, security conduct, or project status. Never expose credentials, secret values, personal data, private endpoints, or internal operational details.

### Placeholder Rules

- Placeholder names use uppercase snake case enclosed by double brackets.
- A content placeholder may expand to multiple Markdown lines.
- Repeatable examples must be duplicated once per evidenced record and then have their placeholder row or item removed.
- `[[DEFAULT_BRANCH]]` must reflect repository metadata; do not presume `master` or `main`.
- `[[ARCHITECTURE_DOCUMENT_LINK]]` must expand to a Markdown link labelled `architecture documentation` whose target is the verified repository-relative document path.
- `[[CODE_OF_CONDUCT_DOCUMENT_LINK]]` must expand to a Markdown link labelled `Code of Conduct` whose target is the verified repository-relative document path.
- `[[LICENSE_TITLE]]` must reflect the repository licence without inference.
- `[[LICENSE_SUFFIX]]` is ` or later` only when the licence text or SPDX expression explicitly grants later versions; otherwise it is empty.
- Badge placeholders such as `[[COVERAGE_BADGE]]` must expand to complete linked badge Markdown from a configured provider.
- Generic placeholders such as `[[ADDITIONAL_STATUS_BADGES]]` and `[[ADDITIONAL_DISTRIBUTION_BADGES]]` are removed when no additional evidenced records exist.

### Failure Behaviour

- If a mandatory core value remains indeterminate after evidence collection, cease generation and ask one concise clarification question.
- Do not output a partial README.

### Mandatory Validation Before Final Output

- Every included heading matches the template exactly and follows template order after conditional omissions.
- Every included badge corresponds to an evidenced service, package, workflow, distribution channel, or licence.
- Every mandatory core section is present.
- Every conditional section has evidence, substantive content, and no filler rows.
- Every additional section is repository-relevant, substantive, and purely additive.
- Fixed template prose has not been rephrased.
- No `[[PLACEHOLDER]]`, template comment, unused example, empty heading, empty table, or empty code block remains.
- The Table of Contents includes every final `##`, `###`, and `####` heading in order, with two-space indentation per level and no heading emoji in labels or anchors.
- Commands, paths, versions, links, defaults, and compatibility statements agree with repository evidence.
- Exactly one `### Release` subsection remains when release guidance applies. A .NET project with the template-defined `release.sh` workflow uses that fixed subsection verbatim instead of `[[RELEASE_INSTRUCTIONS]]`.
- No secret, credential, personal datum, private endpoint, or unsafe remote-script instruction is exposed.

If a `README.md` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `README.md` exists, create one from scratch.

Use the exact template wording for fixed sections. Do not reword, paraphrase, or alter `## 🏗️ Architecture`, `## 🤝 Contributing`, `## 📜 Code of Conduct`, `## 💝 Project Engagement`, or `## 📄 License`; resolve only their conditional lines and placeholders.

## Mandatory Editing Rules

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

Include badges only when their state and destination can be verified:
| Badge | Condition | Notes |
|-------|-----------|-------|
| Donate | `.github/FUNDING.yml` exists. | Use the fixed funding URL from the template. |
| Latest Release | At least one published release exists. | Do not include for tags without published releases. |
| Website or GitHub Pages | A public repository website is configured or GitHub Pages is enabled. | Use `GitHub Pages` for `github.io` URLs; otherwise use `Website`. |
| Build Status | A primary GitHub Actions workflow exists. | `[[WORKFLOW_FILE]]` includes its `.yml` or `.yaml` extension. Select the principal validation workflow rather than every workflow. |
| Coverage | A coverage provider and public report are configured. | Use the provider's canonical linked badge; do not presume Codecov, a branch, or a report URL. |
| Code Quality | An external analysis service is configured and has a useful public report. | Omit local-only linters and redundant quality badges. |
| NuGet, npm, PyPI, or crates.io | The corresponding package is publicly published. | Confirm the package identifier from manifests and registry metadata. |
| Container Image | A public OCI image is published. | Link to the canonical registry page. |
| License | `LICENSE` exists. | Use the repository's detected default branch. |
| Additional Status Badges | Another configured service provides distinct, material information. | Omit vanity counters, social counters, stale badges, and duplicates. |

### Mandatory Core Content

Always include:
- Project title and concise description
- `## 📑 Table of Contents`
- `## ✨ Capabilities`
- `## 🚀 Usage`
- `## 🤝 Contributing`
- `## 💝 Project Engagement`

Include `## 📄 License` only when `LICENSE` exists. Never infer or invent a licence.

### Sections

Process the subsequent sections in table order. This order is canonical after conditional omissions:
| Section | Condition | Required Content or Placement |
|---------|-----------|-------------------------------|
| Project status callout | Maturity, maintenance, deprecation, archival, or stability status requires prominent disclosure. | Place directly after the project description. |
| Preview screenshot | `preview.png` exists in the repository root. | Place before Table of Contents. |
| `## 📑 Table of Contents` | Always. | Include every final `##`, `###`, and `####`; indent nested levels by two spaces and omit heading emojis from labels and anchors. |
| `## 🖼️ Screenshots` | `screenshots/` contains useful image files. | Include representative current images only. |
| `## 🎬 Demo` | A public interactive demonstration, sample instance, recorded demonstration, or representative media asset exists. | Link or embed the canonical public resource. |
| `## ✨ Capabilities` | Always. | Describe evidenced user outcomes rather than implementation details. |
| `## 🎯 Use Cases` | Multiple distinct audiences or workflows benefit from concise orientation. | Include only evidenced use cases. |
| `## 🚀 Usage` | Always. | Provide a minimal realistic command, code example, or workflow. |
| `## ⌨️ Command Reference` | A CLI, command system, task runner, or console exposes multiple user-facing commands. | Document public commands, not contributor-only scripts. |
| `## ⌨️ Keyboard Shortcuts` | A graphical or terminal interface exposes documented shortcuts. | State platform-specific variants where relevant. |
| `## ⚠️ Known Limitations` | Material caveats, unsupported scenarios, or missing capabilities are evidenced. | Omit generic disclaimers and speculative limitations. |
| `## 🖥️ System Requirements` | An end-user application has material OS, hardware, runtime, host, or service prerequisites. | Place directly before Installation. |
| `## 📦 Installation` | Any package, store, container, downloadable artefact, source-installation, or mod-distribution route exists. | Include only published or supported routes. |
| `## ⚙️ Configuration` | Public settings are evidenced by files, examples, command-line options, APIs, source, or documentation. | Omit secret values and internal-only settings. |
| `## 🌍 Localisation` | Localisation resources, locale files, translation services, or localisation managers exist. | Report only evidenced locales and status. |
| `## 🧩 Compatibility` | Runtime, browser, OS, game, protocol, format, or host compatibility is material. | Distinguish supported and unsupported versions when evidenced. |
| `## 🔌 Integrations` | External services, platforms, plug-ins, providers, or optional adapters are supported. | Distinguish required and optional integrations. |
| `## 🔐 Authentication and Authorisation` | Users or clients authenticate, or public roles and scopes are material. | Never include credentials, tokens, or unsafe examples. |
| `## 🧱 Extensibility` | A public plug-in, extension, hook, provider, middleware, theme, or scripting contract exists. | Document public extension points only. |
| `## 🔑 Permissions` | Users must grant OS, browser, mobile, server, cloud, or host permissions. | Explain purpose and whether each permission is mandatory. |
| `## 🛡️ Privacy and Data` | The project collects, processes, transmits, or persists user data, analytics, diagnostics, or telemetry. | Document evidenced data conduct and controls without exposing personal data. |
| `## ♿ Accessibility` | A user-facing interface has documented accessibility support, constraints, or conformance. | Do not assert standards conformance without evidence. |
| `## 🛠️ Development` | A local development workflow exists. | Use canonical project-native commands. Omit for content-only repositories without executable steps. |
| `## 🗂️ Project Structure` | Multiple projects exist or the directory layout is non-obvious. | Include principal projects and directories only. |
| `## 🏗️ Architecture` | `ARCHITECTURE.md` exists or `docs/architecture/` contains substantive documentation. | Place directly after Project Structure, preserve its fixed sentence, and resolve only `[[ARCHITECTURE_DOCUMENT_LINK]]`. |
| `## 🚢 Deployment` | The project is deployed as an application, service, website, infrastructure component, or self-hosted system. | Include only public, safe operational procedures. |
| `## 🗺️ Roadmap` | `ROADMAP.md` exists. | Link to the root document. |
| `## 📚 Documentation` | A substantive `docs/` directory, GitHub Pages site, Wiki, or hosted manual exists. | List principal resources without duplicating the README. |
| `## 🌐 API Reference` | A library, SDK, or API exposes generated, hosted, or substantive reference documentation. | Link the canonical reference. |
| `## 🧾 Data Formats and Protocols` | Users implement public formats, schemas, protocols, or import/export contracts directly. | Link specifications and avoid duplicating generated schemas. |
| `## 🏷️ Versioning` | A versioning scheme, stability guarantee, support window, or deprecation policy is documented. | Do not infer Semantic Versioning from version-shaped tags alone. |
| `## 🔄 Migration Guide` | `MIGRATION.md`, `UPGRADING.md`, or an equivalent migration resource exists. | Link the evidenced resource. |
| `## 🩺 Troubleshooting` | Recurring evidenced problems have diagnostic procedures or resolutions. | Do not invent speculative failures. |
| `## ❓ FAQ` | `FAQ.md` exists. | Place after Troubleshooting. |
| `## 🤝 Contributing` | Always. | Preserve the fixed base text and resolve conditional bullets. |
| `## 📜 Code of Conduct` | `CODE_OF_CONDUCT.md` exists in the root or `.github/`. | Preserve its fixed sentence and resolve only `[[CODE_OF_CONDUCT_DOCUMENT_LINK]]`. |
| `## 🧭 Governance` | Public governance, maintainer, owner, or decision-making documentation exists. | Link or summarise the canonical source. |
| `## 🔗 Related Projects` | Directly related projects exist. | Explain each relationship. |
| `## 🙏 Acknowledgements` | Notable third-party works, data sources, contributors, or inspiration merit attribution. | Do not duplicate licence notices. |
| `## 📝 Citation` | Citation metadata exists or the project is an academic or research artefact. | Prefer `CITATION.cff`, `CITATION.bib`, DOI, or canonical publication metadata. |
| `## 📋 Changelog` | `CHANGELOG.md` exists. | Link to the root document. |
| `## 🔒 Security` | `SECURITY.md` exists. | Direct vulnerability reports to the policy, not the public issue tracker. |
| `## 💬 Support` | `SUPPORT.md` or a public support route exists. | Distinguish general support from security disclosure. |
| `## 💝 Project Engagement` | Always. | Preserve the fixed issue, suggestion, funding, and starring text while resolving funding conditionals. |
| `## 📄 License` | `LICENSE` exists. | Preserve the fixed base text and resolve title and suffix from licence evidence. |

### Distribution Channels

Resolve each installation channel independently:
| Channel | Evidence | Required Pairing |
|---------|----------|------------------|
| Flatpak or Flathub | Manifest, packaging metadata, or a published Flathub application. | Store badge and `flatpak install` command. |
| Snap | `snapcraft.yaml` or a published Snap Store package. | Store badge and `snap install` command. |
| AUR | Packaging metadata or a published AUR package. | AUR badge and at least one supported helper command. |
| Homebrew | Formula, cask, tap, or published Homebrew package. | Homebrew badge and canonical `brew install` target. |
| WinGet | Manifest or published WinGet package. | WinGet badge and exact package identifier. |
| Chocolatey | Package specification or published Chocolatey package. | Chocolatey badge and install command. |
| Scoop | Manifest, bucket, or supported Scoop installation instructions. | Public manifest badge when available and complete install commands. |
| NuGet | Package metadata and a published NuGet package. | NuGet badge and appropriate CLI or Package Manager Console command. |
| npm | Package manifest and a published npm package. | npm badge and install command. |
| PyPI | Python package metadata and a published PyPI project. | PyPI badge and `python -m pip install` command. |
| conda-forge | Recipe or published conda-forge package. | conda-forge badge and install command. |
| Maven Central | Maven or Gradle metadata and a published artefact. | Maven Central badge and applicable dependency snippets. |
| crates.io | Cargo metadata and a published crate. | crates.io badge and `cargo add` for libraries or `cargo install` for executables. |
| RubyGems | Gemspec and a published gem. | RubyGems badge and install command. |
| Packagist | Composer metadata and a published package. | Packagist badge and `composer require` command. |
| Go install | A supported installable Go command path. | `go install` command with the documented version selector; no store badge is required. |
| OCI registry | Container definition and a published public image. | Registry badge, canonical package link, and pull command. |
| Steam Workshop, Nexus Mods, or Paradox Mods | Published mod identifier and repository evidence. | Corresponding store badge; add manual steps only when necessary. |
| GitHub Releases | At least one published release with installable artefacts. | GitHub badge and any necessary manual installation instructions. |
| Other channel | Verifiable publication metadata or supported repository instructions. | Canonical badge or link plus complete installation instructions through the additional placeholders. |

Do not include an installation badge without the corresponding supported installation path. Do not represent a package as published merely because a manifest exists.

### Conditional Subsections

Include each subsection only when its template directive is satisfied:
| Parent | Subsection | Condition |
|--------|------------|-----------|
| Usage | Examples | An examples or samples directory exists, or multiple substantive examples are documented. |
| Installation | Package Manager Installation | At least one evidenced package-manager command applies. |
| Installation | Maven or Gradle | A published Maven-compatible library supports the corresponding consumer tool. |
| Installation | Container Image | A public OCI image is published. |
| Installation | Manual Installation | Users install downloadable or manually distributed artefacts. |
| Installation | Installation from Source | Source installation is supported for end users, not solely contributors. |
| Installation | Verification | A concise command or observable result verifies installation. |
| Installation | Upgrading | Upgrading requires more than repeating the install command. |
| Installation | Uninstallation | Removal is non-obvious or leaves services, state, configuration, or data. |
| Configuration | Configuration Files | Public settings exist in one or more configuration files. |
| Configuration | Settings | Public keys, types, defaults, and requirements are evidenced. |
| Configuration | Environment Variables | `.env.example` or equivalent public environment-variable documentation exists. |
| Configuration | Command-Line Options | Documented options exist beyond ordinary help and version switches. |
| Configuration | Precedence | Multiple sources have a defined precedence. |
| Configuration | Reload Behaviour | Configuration reload, restart, or hot-reload semantics are material. |
| Configuration | Profiles and Scopes | Named profiles, environments, layered files, or per-user and system scopes exist. |
| Configuration | Secret Management | Public secret names, sources, credential stores, or providers require explanation. |
| Configuration | Network Ports | Documented ports are bound, exposed, or required. |
| Configuration | Validation | A command, endpoint, or observable result validates effective configuration. |
| Localisation | Contributing Translations | A documented translation contribution process exists. |
| Privacy and Data | Data Locations | Users may locate, transfer, inspect, reset, or delete application data. |
| Privacy and Data | Telemetry Controls | Analytics, diagnostics, or telemetry can be configured or deactivated. |
| Development | Requirements and Setup | Include both whenever Development is present. Cover tools, source checkout, dependencies, local configuration, and services as applicable. |
| Development | Build | Compilation, bundling, packaging, or asset generation is required. |
| Development | Run | The project can be executed locally. |
| Development | Test | Tests exist. |
| Development | Coverage | A local coverage command and report exist. |
| Development | Integration Tests or End-to-End Tests | Distinct prerequisites or commands exist for the corresponding test category. |
| Development | Linting, Formatting, Type Checking, or Static Analysis | The corresponding configured local command exists. Resolve each independently. |
| Development | Code Generation | Generated sources, schemas, clients, assets, or locales must be refreshed. |
| Development | Database Setup | Local development requires database creation, seeding, emulation, or migrations. |
| Development | Documentation | Documentation can be generated or previewed locally. |
| Development | Benchmarks | A benchmark suite exists. |
| Development | Debugging and Profiling | A non-obvious documented workflow exists. |
| Development | Docker | `Dockerfile` or `Containerfile` exists for development. |
| Development | Docker Compose | `compose.yml`, `compose.yaml`, `docker-compose.yml`, or `docker-compose.yaml` exists. |
| Development | Continuous Integration | Contributor-relevant checks merit local reproduction guidance. |
| Development | Release | For a .NET project with the template-defined `release.sh` workflow, include the exact fixed release variant and omit the generic variant. For every other evidenced maintainer release process, include the generic variant. |
| Development | Dependencies | Direct, non-trivial dependencies merit explanation. Classify runtime, development, build, and optional scope. |
| Project Structure | Projects and Packages | Multiple projects, packages, applications, services, or modules exist. |
| Project Structure | Directories | Principal non-obvious directories aid orientation. |
| Deployment | Environments | Multiple deployment targets or environments are documented. |
| Deployment | Configuration and Secrets | Deployment provisioning requires explanation beyond Configuration. |
| Deployment | Database Migrations | Deployment requires state or database migrations. |
| Deployment | Health Checks | Health, readiness, or liveness checks exist. |
| Deployment | Observability | Public operator guidance exists for logs, metrics, traces, alerts, or dashboards. |
| Deployment | Backup and Restore | Persistent state requires operator backup or recovery. |
| Deployment | Rollback and Recovery | A documented rollback or disaster-recovery procedure exists. |

## Styling & Format Rules

- Respect the instructions in `language.instructions.md` for all README text, including spelling, phrasing, and language conventions.
- Preserve every included template heading and emoji exactly.
- Generate the Table of Contents only after all conditional and additive content is final.
- Remove every HTML directive comment, unresolved placeholder, unused example, and empty block from the final output.
- Use valid repository-relative links for repository files and canonical HTTPS links for external resources.
- Provide concise, descriptive alternative text for every image.
- Use fenced code blocks with the correct language identifier and no shell prompt characters that impede direct reuse.
- Use tables only for genuinely tabular information. Omit inapplicable rows rather than filling them with speculative values.
- Use `N/A` only when a required table row has no applicable value; do not use it as filler for optional content.
- Keep the README concise by linking detailed documentation rather than duplicating it.
- Maintain command examples non-destructive unless the documented operation inherently modifies state and the consequence is explicit.
- In `## 📄 License`, set `[[LICENSE_SUFFIX]]` to ` or later` only when the actual licence explicitly grants later versions.

## Project-Native Command Resolution

Resolve setup, compilation, execution, test, quality, packaging, and release content from the repository rather than a framework lookup table:
1. Prefer canonical commands from maintained documentation and task entry points such as `Makefile`, `Justfile`, package scripts, solution files, project manifests, workspace manifests, and executable scripts.
2. Confirm commands with CI workflows when CI represents the supported contributor path.
3. Respect the repository's selected package manager, lockfile, workspace layout, tool versions, and required working directory.
4. Distinguish end-user installation from contributor setup and maintainer release procedures.
5. Include prerequisites, environment preparation, dependent services, and generated artefacts only when required.
6. Do not invent a compilation, execution, test, lint, package, or release command when none is evidenced.
7. When a command downloads or executes remote content, identify the source and prominently instruct readers to inspect it before execution.
