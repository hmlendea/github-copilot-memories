[![Donate](https://img.shields.io/badge/-%E2%99%A5%20Donate-%23ff69b4)](https://hmlendea.go.ro/funding)
[![Build Status](https://github.com/hmlendea/github-copilot-memories/actions/workflows/verification.yml/badge.svg)](https://github.com/hmlendea/github-copilot-memories/actions/workflows/verification.yml)
[![License](https://img.shields.io/github/license/hmlendea/github-copilot-memories)](https://github.com/hmlendea/github-copilot-memories/blob/master/LICENSE)

# GitHub Copilot Memories

A curated collection of instruction files and skills that encode reusable coding standards, documentation templates, language conventions, and domain-specific guidance for GitHub Copilot Chat and OpenAI Codex.

## 📑 Table of Contents

- [Capabilities](#capabilities)
- [Use Cases](#use-cases)
- [Usage](#usage)
- [Installation](#installation)
  - [Installation from Source](#installation-from-source)
    - [GitHub Copilot](#github-copilot)
    - [OpenAI Codex](#openai-codex)
- [Configuration](#configuration)
- [Integrations](#integrations)
- [Privacy and Data](#privacy-and-data)
- [Development](#development)
  - [Requirements](#requirements)
  - [Setup](#setup)
  - [Test](#test)
  - [Continuous Integration](#continuous-integration)
- [GitHub Actions](#github-actions)
- [Project Structure](#project-structure)
  - [Directories](#directories)
- [Architecture](#architecture)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Code of Conduct](#code-of-conduct)
- [Security](#security)
- [Support](#support)
- [Project Engagement](#project-engagement)
- [License](#license)

## ✨ Capabilities

- Applies shared coding, naming, error-handling, security, and documentation principles across supported file types.
- Provides specialised guidance for C#, Python, TypeScript, shell scripts, MethodScript, PolyGlot dictionaries, Markdown, MonoGame, and NuciXNA.
- Generates evidence-based README, architecture, roadmap, privacy, security, and GitHub Actions documents from strict templates.
- Assesses secrets handling, credential exposure, rotation, and vault integration against OWASP and NIST guidance.
- Reviews code, pull requests, and diffs against OWASP ASVS 4.0.3 and the CWE Top 25 (2024), reporting severity-rated findings and remediation.
- Reviews REST, GraphQL, gRPC, and hybrid APIs against the OWASP API Security Top 10:2023, with C# and .NET guidance.
- Assesses prompt injection risk in LLM-integrated applications against OWASP LLM01:2025 and MITRE ATLAS AML.T0051.
- Reviews AI agent architectures against OWASP Agentic AI threats and NIST AI RMF 1.0, covering permissions, trust boundaries, and rollback.
- Reviews and repairs user interfaces against a prioritised rule set covering accessibility, interaction, performance, layout, typography, animation, forms, and navigation, with a browser-driven audit.
- Maintains British English and Romanian language preferences through the mandatory `english-language` and `romanian-language` skills, applied to every file.
- Defines test design, edge-case coverage, test suite auditing, shared test values, and manual QA acceptance criteria.
- Observes a pull request to merge readiness through the `pr-babysit` skill, verifying each finding before correction.
- Verifies a release after publication or deployment through the `release-verification` skill, per surface and with explicit coverage gaps.
- Verifies its own content in continuous integration by executing the instruction-gate hook tests, validating every governed GitHub document against its template, and parsing every workflow file.
- Uses narrowly scoped `applyTo` globs and semantic descriptions so Copilot receives relevant guidance for each file, except for the language instructions, which deliberately apply to every file.
- Resolves paths and addresses from the agent home `Locations.md` registry before searching or inferring them.
- Provides a Codex `AGENTS.md` entry point for selecting relevant files from the shared instruction library.
- Provides the opt-in **Token Saver** (restricted tools, terse reporting) and **LiteLLM** (pre-execution instruction gating, semantic audits) agents.
- Provides game-modding conventions for MethodScript, Imperator: Rome, Stellaris, Crusader Kings II and III, Civilization IV, V, VI, and Beyond Earth, Victoria 3, Europa Universalis V, and Total War: Rome Remastered.
- Provides on-demand procedures for context, research, review, migration, profiling, localisation, memory, documentation, release, and workflow automation.
- Holds each document and workflow template, its rules, the fidelity contract, and the validation script in the corresponding skill, so they load only for generation tasks.
- Triggers documentation updates for affected repository files whenever a skill modifies code or dependencies.

## 🎯 Use Cases

- **GitHub Copilot Chat users:** Apply reusable coding standards, documentation templates, and domain-specific guidance to their projects.
- **OpenAI Codex users:** Read the shared instruction library through a global `AGENTS.md` entry point and invoke skills on demand.
- **Repository maintainers:** Generate and validate template-governed GitHub documents and Actions workflows against a fixed fidelity contract.
- **Application and game-mod developers:** Apply framework, language, and game-specific conventions from the on-demand skills.

## 🚀 Usage

After installation, access a project in VS Code and submit a normal Copilot Chat request. Matching instruction files are selected through their `applyTo` globs and descriptions.

For example, to revise a repository README, submit:

```text
Update the README
```

The README rules inspect repository evidence, select applicable template sections, and revise the existing `README.md` in place.

For cost-sensitive coding work, select **Token Saver** from the agent picker. It limits operations to reading, searching, editing, and terminal execution; it neither delegates to subagents nor permits implicit model invocation.

For instruction-compliance audits, select **LiteLLM**. The [agent definition](agents/litellm.agent.md) keeps default tools and the selected model, reads applicable instructions and skills in full, and adds pre-action, post-action, and final semantic audits. The local agent hook injects path-scoped common, language, and detected programming-language instructions at session start; complete semantic applicability remains an agent audit requirement.

Skill descriptions remain available for discovery, while full skill procedures load only for relevant tasks.

For Codex, start a new session in your project after installation. The global `AGENTS.md` directs Codex to read relevant shared instructions. Invoke a skill explicitly with its name, such as `$repository-orientation`, or let Codex select it from its description.

## 📦 Installation

### Installation from Source

#### GitHub Copilot

Install [Git](https://git-scm.com/) and [VS Code](https://code.visualstudio.com/) with the [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat). The commands link the shared library into the GitHub Copilot home (`~/.copilot`, which holds `skills`, `agents`, and `hooks`) and into the user profile of every installed VS Code flavour (`Code`, `Code - OSS`, and `Code - Insiders`). The user profile holds `prompts` and `agents`, and its `prompts/instructions` path receives the repository `instructions` directory, because VS Code expects instruction files beneath `prompts/instructions`.

| Destination | Content | Consumed by |
|-------------|---------|-------------|
| `<profile>/prompts` | `prompts` | Prompt files, discovered from `*.prompt.md` |
| `<profile>/prompts/instructions` | `instructions` | Instruction files, selected through `applyTo` and `description` |
| `<profile>/prompts/github-md-generator.prompt.md` | `prompts/github-md-generator.prompt.md` | The GitHub MD Generator slash command |
| `<profile>/agents` | `agents` | Custom agents, discovered from `*.agent.md` |
| `~/.copilot/skills` | `skills` | On-demand skill procedures |
| `~/.copilot/agents` | `agents` | Custom agent discovery through the GitHub Copilot home |
| `~/.copilot/hooks` | `hooks` | Instruction-gate script referenced by the LiteLLM agent |

The repository keeps the GitHub MD Generator prompt under `prompts/` and the instruction files under `instructions/`. The commands create `<profile>/prompts` as a real directory rather than a link, then link the prompt file and the `instructions` directory into it, so the prompt resolves to `<profile>/prompts/github-md-generator.prompt.md` and the instructions resolve to `<profile>/prompts/instructions`.

Each command is idempotent: it creates the parent directories first and replaces any existing link at the destination, so the commands can be re-run after moving the clone. A destination that is a regular file or directory rather than a link must be moved or removed manually, because the link commands do not overwrite it. When a destination already holds a link, the commands replace it in place rather than creating a link inside the target, so re-running them never nests `skills/skills`, `agents/agents`, or `hooks/hooks` inside the clone.

Create the links with an absolute, existing source path. A relative or non-existent source such as `$PWD/instructions` evaluated outside the clone root resolves to the wrong location and produces `No such file or directory`.

On Linux:

```bash
git clone https://github.com/hmlendea/github-copilot-memories.git
cd github-copilot-memories

# GitHub Copilot home: skills, custom agents, and hooks
mkdir -p "${HOME}/.copilot"
ln -sfn "${PWD}/skills" "${HOME}/.copilot/skills"
ln -sfn "${PWD}/agents" "${HOME}/.copilot/agents"
ln -sfn "${PWD}/hooks" "${HOME}/.copilot/hooks"

# VS Code user profile: instruction files, prompt files, and custom agents
for VS_CODE_FLAVOUR in 'Code' 'Code - OSS' 'Code - Insiders'; do
  VS_CODE_PROFILE="${HOME}/.config/${VS_CODE_FLAVOUR}/User"
  if [ -d "${VS_CODE_PROFILE}" ]; then
    mkdir -p "${VS_CODE_PROFILE}/prompts"
    ln -sfn "${PWD}/instructions" "${VS_CODE_PROFILE}/prompts/instructions"
    ln -sfn "${PWD}/prompts/github-md-generator.prompt.md" "${VS_CODE_PROFILE}/prompts/github-md-generator.prompt.md"
    ln -sfn "${PWD}/agents" "${VS_CODE_PROFILE}/agents"
  fi
done
```

On macOS:

```bash
git clone https://github.com/hmlendea/github-copilot-memories.git
cd github-copilot-memories

# GitHub Copilot home: skills, custom agents, and hooks
mkdir -p "${HOME}/.copilot"
ln -sfn "${PWD}/skills" "${HOME}/.copilot/skills"
ln -sfn "${PWD}/agents" "${HOME}/.copilot/agents"
ln -sfn "${PWD}/hooks" "${HOME}/.copilot/hooks"

# VS Code user profile: instruction files, prompt files, and custom agents
for VS_CODE_FLAVOUR in 'Code' 'Code - OSS' 'Code - Insiders'; do
  VS_CODE_PROFILE="${HOME}/Library/Application Support/${VS_CODE_FLAVOUR}/User"
  if [ -d "${VS_CODE_PROFILE}" ]; then
    mkdir -p "${VS_CODE_PROFILE}/prompts"
    ln -sfn "${PWD}/instructions" "${VS_CODE_PROFILE}/prompts/instructions"
    ln -sfn "${PWD}/prompts/github-md-generator.prompt.md" "${VS_CODE_PROFILE}/prompts/github-md-generator.prompt.md"
    ln -sfn "${PWD}/agents" "${VS_CODE_PROFILE}/agents"
  fi
done
```

On Windows, use an Administrator Command Prompt:

```batch
git clone https://github.com/hmlendea/github-copilot-memories.git
cd github-copilot-memories

rem GitHub Copilot home: skills, custom agents, and hooks
if not exist "%USERPROFILE%\.copilot" mkdir "%USERPROFILE%\.copilot"
if exist "%USERPROFILE%\.copilot\skills" rmdir "%USERPROFILE%\.copilot\skills"
if exist "%USERPROFILE%\.copilot\agents" rmdir "%USERPROFILE%\.copilot\agents"
if exist "%USERPROFILE%\.copilot\hooks" rmdir "%USERPROFILE%\.copilot\hooks"
mklink /D "%USERPROFILE%\.copilot\skills" "%CD%\skills"
mklink /D "%USERPROFILE%\.copilot\agents" "%CD%\agents"
mklink /D "%USERPROFILE%\.copilot\hooks" "%CD%\hooks"

rem VS Code user profile: instruction files, prompt files, and custom agents
if exist "%APPDATA%\Code\User" (
  if not exist "%APPDATA%\Code\User\prompts" mkdir "%APPDATA%\Code\User\prompts"
  if exist "%APPDATA%\Code\User\prompts\instructions" rmdir "%APPDATA%\Code\User\prompts\instructions"
  if exist "%APPDATA%\Code\User\prompts\github-md-generator.prompt.md" del "%APPDATA%\Code\User\prompts\github-md-generator.prompt.md"
  if exist "%APPDATA%\Code\User\agents" rmdir "%APPDATA%\Code\User\agents"
  mklink /D "%APPDATA%\Code\User\prompts\instructions" "%CD%\instructions"
  mklink "%APPDATA%\Code\User\prompts\github-md-generator.prompt.md" "%CD%\prompts\github-md-generator.prompt.md"
  mklink /D "%APPDATA%\Code\User\agents" "%CD%\agents"
)
if exist "%APPDATA%\Code - OSS\User" (
  if not exist "%APPDATA%\Code - OSS\User\prompts" mkdir "%APPDATA%\Code - OSS\User\prompts"
  if exist "%APPDATA%\Code - OSS\User\prompts\instructions" rmdir "%APPDATA%\Code - OSS\User\prompts\instructions"
  if exist "%APPDATA%\Code - OSS\User\prompts\github-md-generator.prompt.md" del "%APPDATA%\Code - OSS\User\prompts\github-md-generator.prompt.md"
  if exist "%APPDATA%\Code - OSS\User\agents" rmdir "%APPDATA%\Code - OSS\User\agents"
  mklink /D "%APPDATA%\Code - OSS\User\prompts\instructions" "%CD%\instructions"
  mklink "%APPDATA%\Code - OSS\User\prompts\github-md-generator.prompt.md" "%CD%\prompts\github-md-generator.prompt.md"
  mklink /D "%APPDATA%\Code - OSS\User\agents" "%CD%\agents"
)
if exist "%APPDATA%\Code - Insiders\User" (
  if not exist "%APPDATA%\Code - Insiders\User\prompts" mkdir "%APPDATA%\Code - Insiders\User\prompts"
  if exist "%APPDATA%\Code - Insiders\User\prompts\instructions" rmdir "%APPDATA%\Code - Insiders\User\prompts\instructions"
  if exist "%APPDATA%\Code - Insiders\User\prompts\github-md-generator.prompt.md" del "%APPDATA%\Code - Insiders\User\prompts\github-md-generator.prompt.md"
  if exist "%APPDATA%\Code - Insiders\User\agents" rmdir "%APPDATA%\Code - Insiders\User\agents"
  mklink /D "%APPDATA%\Code - Insiders\User\prompts\instructions" "%CD%\instructions"
  mklink "%APPDATA%\Code - Insiders\User\prompts\github-md-generator.prompt.md" "%CD%\prompts\github-md-generator.prompt.md"
  mklink /D "%APPDATA%\Code - Insiders\User\agents" "%CD%\agents"
)
```

The `instructions` link must resolve to `<profile>/prompts/instructions`, which is the location VS Code expects for user-level instruction files, while the repository keeps them at the top level as `instructions`. Custom agents are discovered from the `agents` directory of the VS Code user profile, which is why the profile loop links it alongside `prompts`. The `~/.copilot/agents` link covers agent discovery through the GitHub Copilot home, and the `skills` link is optional when only instruction files and custom agents are required. The [hooks directory](hooks/) link is required by the LiteLLM agent, whose definition invokes `~/.copilot/hooks/litellm-instruction-gate.cjs`. The profile loop links only VS Code flavours whose user profile already exists, so installing a single flavour is sufficient.

After installation, reload the VS Code window and confirm the installation:

- Open the agent picker and locate **Token Saver** and **LiteLLM**, then confirm that the GitHub MD Generator prompt appears as a slash command.
- Confirm that `Code/User/agents`, `Code/User/prompts/instructions`, and `Code/User/prompts/github-md-generator.prompt.md` resolve to the clone, for example with `readlink -f "${HOME}/.config/Code/User/prompts/instructions"`.

If no agent appears, the profile `agents` link is missing or points to a non-existent path; recreate it with the commands above. If a link instead resolves to a nested path such as `skills/skills`, an earlier run created a link inside the target directory, and that stray link must be removed before the correct link is created.

#### OpenAI Codex

Install [Git](https://git-scm.com/) and [Codex](https://developers.openai.com/codex/quickstart/). Use an existing clone or clone this repository, then run the link commands from its root. Keep the clone in place because the links point to it.

The commands install [user-level skills](https://learn.chatgpt.com/docs/build-skills) in `~/.codex/skills` and [global instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md) in `~/.codex/AGENTS.md`, or in `$CODEX_HOME` when set. The linked [codex/AGENTS.md](codex/AGENTS.md) selects relevant instruction files through `applyTo` and `description`.

The destination `skills`, `AGENTS.md`, and `instructions` paths must not already exist. Merge the supplied guidance into an existing `AGENTS.md` or `AGENTS.override.md`, and link individual skill folders if a skills directory already exists.

On Linux or macOS:

```bash
git clone https://github.com/hmlendea/github-copilot-memories.git
cd github-copilot-memories
codex_config_dir="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$codex_config_dir"
ln -s "$PWD/skills" "$codex_config_dir/skills"
ln -s "$PWD/codex/AGENTS.md" "$codex_config_dir/AGENTS.md"
ln -s "$PWD/instructions" "$codex_config_dir/instructions"
```

On Windows, use an Administrator Command Prompt:

```batch
git clone https://github.com/hmlendea/github-copilot-memories.git
cd github-copilot-memories
set "codex_config_dir=%USERPROFILE%\.codex"
if defined CODEX_HOME set "codex_config_dir=%CODEX_HOME%"
if not exist "%codex_config_dir%" mkdir "%codex_config_dir%"
mklink /D "%codex_config_dir%\skills" "%CD%\skills"
mklink "%codex_config_dir%\AGENTS.md" "%CD%\codex\AGENTS.md"
mklink /D "%codex_config_dir%\instructions" "%CD%\instructions"
```

Start a new Codex session and ask it to summarise its active instructions and locate `$repository-orientation` to check discovery.

## ⚙️ Configuration

Instruction files reside under `instructions/`. Each file starts with YAML frontmatter in which `description` identifies the relevant context and `applyTo`, when present, limits automatic application to matching paths.

The always-on common instructions direct each agent to read the `Locations.md` registry in its own home directory (`~/.copilot/Locations.md` for GitHub Copilot, `~/.codex/Locations.md` for Codex) before resolving any path or address.

The language instruction files activate for every file and require the `english-language` and `romanian-language` skills, whose compact dictionaries must be applied in full.

Every skill file resides under `skills/<name>/SKILL.md` and begins with YAML frontmatter whose `name` equals the directory name and whose single-line double-quoted `description` is at most 1024 characters, the host's hard load limit.

Custom agents reside under [agents/](agents/). Token Saver and LiteLLM are opt-in and do not pin a model; select the desired model and reasoning effort prior to starting a session.

Skills reside under `skills/`. Their concise descriptions support task-based discovery; complete procedures load on demand. Each skill is self-contained: it holds its procedure, and where relevant its templates, rules, fidelity contract, validators, and references.

For example:

```yaml
---
description: "Use when writing or editing Python code. Covers imports, naming, string literals, comments, HTTP/requests, function structure, type hints, module structure, and blank line rules."
applyTo: "**/*.py"
---
```

Edit the Markdown body to personalise the guidance. Because the user-profile directories are linked to the repository, file revisions remain available without maintaining duplicate copies.

## 🔌 Integrations

| Integration | Compatibility | Purpose | Required |
|-------------|---------------|---------|----------|
| VS Code with GitHub Copilot Chat | User-profile prompt, custom-agent, hook, and skill discovery | Applies instructions, enforces the LiteLLM pre-execution gate, and exposes custom agents and on-demand skills | For Copilot |
| OpenAI Codex | Global `AGENTS.md` and user-level skill discovery | Reads the shared instruction library and exposes on-demand skills | For Codex |

## 🛡️ Privacy and Data

GitHub Copilot Memories does not collect, process, transmit, or persist user data, analytics, diagnostics, or telemetry.

For the detailed description of how the application handles privacy and personal data, see the [Privacy Statement](./PRIVACY.md).

## 🛠️ Development

### Requirements

- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/), required by the instruction-gate hook tests
- [Python 3](https://www.python.org/downloads/), required by the template validators
- [PyYAML](https://pypi.org/project/PyYAML/), required only to parse workflow files during verification

### Setup

Clone the repository and create the user-profile links described under [Installation](#installation). Only the verification commands below need the listed requirements.

### Test

Execute the instruction-gate hook tests:

```bash
node --test hooks/
```

Validate every governed GitHub document against its template:

```bash
for document in README.md ARCHITECTURE.md CONTRIBUTING.md CODE_OF_CONDUCT.md SECURITY.md PRIVACY.md ROADMAP.md; do
  python3 skills/github-md-template-fidelity/validate_github_md.py --force . "$document" "$document"
done
```

Validate a generated Steam Workshop page description against its template:

```bash
python3 skills/steam-workshop-page/validate_steam_workshop_page.py --force . path/to/workshop-description.bbcode
```

Validate the hook and validator scripts for syntax errors:

```bash
node --check hooks/litellm-instruction-gate.cjs
python3 -m py_compile skills/github-md-template-fidelity/validate_github_md.py skills/github-actions-workflow/validate_github_actions.py skills/steam-workshop-page/validate_steam_workshop_page.py
```

### Continuous Integration

The [Verification workflow](.github/workflows/verification.yml) runs these checks on every push and pull request targeting `master`. Reproduce it locally with the commands above before opening a pull request.

## ⚙️ GitHub Actions

| Workflow | Purpose | What it does |
|----------|---------|--------------|
| [Verification](https://github.com/hmlendea/github-copilot-memories/blob/master/.github/workflows/verification.yml) | Continuous verification | Runs the hook tests, checks script syntax, validates every governed GitHub document and workflow file, and verifies skill frontmatter |

## 🗂️ Project Structure

The tracked project is content-focused. Instruction families are separated by language and concern so each file can define a narrow activation contract.

### Directories

| Directory | Purpose |
|-----------|---------|
| `codex/` | Global Codex instructions that select relevant files from the shared library |
| [agents/](agents/) | Opt-in custom agents for restricted-tool execution and semantic instruction-compliance audits |
| [hooks/](hooks/) | Runtime instruction-read enforcement used by the LiteLLM agent |
| `instructions/common/` | Shared coding, naming, error-handling, test-design, documentation, and skill-frontmatter principles |
| `instructions/csharp/` | C# language, project, testing, mapping, logging, MonoGame, and NuciXNA guidance |
| `instructions/git/` | Git safety rules that prevent autonomous state changes and destructive operations |
| `instructions/github/` | GitHub Actions workflow naming and documentation rules |
| `instructions/language/` | British English and Romanian terminology preferences for every file type |
| `instructions/markdown/` | Markdown structure and formatting conventions |
| `instructions/methodscript/` | MethodScript coding and style conventions; require the `methodscript` skill |
| `instructions/polyglot/` | PolyGlot dictionary conventions |
| `instructions/python/` | Python coding and error-handling conventions |
| `instructions/shell/` | Shell coding, naming, and error-handling conventions |
| `instructions/typescript/` | TypeScript coding, naming, and style conventions |
| `prompts/` | The GitHub MD Generator prompt, discovered from the user-profile `prompts` directory once linked |
| `skills/` | On-demand procedures, templates, validators, and references |

## 🏗️ Architecture

GitHub Copilot Memories is a content-only repository of instruction files, skills, and agents.

See the [Architecture Documentation](./ARCHITECTURE.md) for the system context, principal components, runtime processes, ownership boundaries, dependencies, constraints, and extension points.

## 🗺️ Roadmap

See [ROADMAP.md](./ROADMAP.md) for planned work and forthcoming changes.

## 🤝 Contributing

You are welcome to submit any suggestion, feedback, or modification to this project.

When doing so, please:
- Maintain cross-platform compatibility
- Preserve the existing public contract unless a breaking change is intentional
- Submit focused pull requests that conform to the existing code style
- Maintain your branch synchronised with `master`
- Revise the documentation when functionality changes
- Properly test all modifications, including edge cases and error conditions
- Include tests for additional or modified functionality
- Raise a new [issue](https://github.com/hmlendea/github-copilot-memories/issues) for problems or suggestions

See the [Contributing Guidelines](./CONTRIBUTING.md) for details on how to report issues, suggest enhancements, and submit changes.

## 📜 Code of Conduct

See the [Code of Conduct](./CODE_OF_CONDUCT.md) for the standards of conduct expected in all project spaces.

## 🔒 Security

GitHub Copilot Memories does not host services, execute code, or process user data.

For information on reporting security vulnerabilities, see the [Security Policy](./SECURITY.md).

## 💬 Support

For support, please [open an issue](https://github.com/hmlendea/github-copilot-memories/issues).

## 💝 Project Engagement

Discovered a problem with GitHub Copilot Memories or have a suggestion for it? [Open an issue](https://github.com/hmlendea/github-copilot-memories/issues)!

If you find this project useful, consider [funding it](https://hmlendea.go.ro/funding) or starring ⭐️ it on GitHub!

[![Donate](https://raw.githubusercontent.com/hmlendea/readme-assets/master/donate_generic.png)](https://hmlendea.go.ro/funding)

## 📄 License

This project is being distributed under the `GNU General Public License v3.0`.
See [LICENSE](./LICENSE) for additional information.
