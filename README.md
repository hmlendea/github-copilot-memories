[![Donate](https://img.shields.io/badge/-%E2%99%A5%20Donate-%23ff69b4)](https://hmlendea.go.ro/funding)
[![Build Status](https://github.com/hmlendea/github-copilot-memories/actions/workflows/verification.yml/badge.svg)](https://github.com/hmlendea/github-copilot-memories/actions/workflows/verification.yml)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://gnu.org/licenses/gpl-3.0)

# GitHub Copilot Memories

A curated collection of instruction files and skills that encode reusable coding standards, documentation templates, language conventions, and domain-specific guidance for GitHub Copilot Chat and OpenAI Codex.

## 📑 Table of Contents

- [Table of Contents](#table-of-contents)
- [Capabilities](#capabilities)
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
- Assesses secret handling, credential exposure, rotation policy, and vault integration against the OWASP Secrets Management Cheat Sheet and NIST SP 800-57 Part 1 Rev 5, without reproducing secret values.
- Reviews code, pull requests, and diffs against OWASP ASVS 4.0.3 requirements and the CWE Top 25 (2024), producing findings mapped to ASVS controls and CWE identifiers with severity ratings and remediation guidance.
- Reviews REST, GraphQL, and gRPC APIs against the OWASP API Security Top 10:2023, covering object-level and function-level authorisation, authentication, property-level authorisation, resource consumption, sensitive business processes, server-side request forgery, security misconfiguration, inventory management, and unsafe consumption of APIs, and supplies C# and .NET patterns for ASP.NET Core, HotChocolate, and gRPC.
- Assesses LLM-integrated applications for prompt injection against OWASP LLM01:2025 and MITRE ATLAS AML.T0051, mapping the model interaction surface, enumerating direct and indirect injection vectors, and evaluating layered defences.
- Reviews AI agent architectures against OWASP Agentic AI threats and NIST AI RMF 1.0, covering permission models, least-privilege design, human-in-the-loop gates, blast radius containment, audit trails, rollback capability, and multi-agent trust boundaries.
- Reviews and repairs user interfaces against a ten-category rule set ordered by user impact, covering accessibility, touch and interaction, performance, style selection, layout and responsiveness, typography and colour, animation, forms and feedback, navigation, and charts, with a native and mobile pre-delivery checklist and a Playwright-driven audit that reports evidence-ranked findings and fails a pipeline on high-severity defects.
- Maintains British English and Romanian language preferences through contextual terminology rules supplied by the on-demand `english-language` and `romanian-language` skills, applied to prose, documentation, and all human-readable text in code, including identifiers, string literals, comments, messages, and test data.
- Defines systematic test design and edge-case coverage requirements, including failure-side assertions that a failure does not produce a later, unrequested effect, supplies consistent test values through the on-demand `test-values` skill, and provides an optional coding-pattern memory index.
- Observes a pull request until it is genuinely mergeable through the `pr-babysit` skill, verifying each finding prior to correction and resolving a review thread only after the code addresses it.
- Verifies a release after merge, publication, or deployment through the `release-verification` skill, confirming the delivered artefact per surface, classifying findings, and reporting partial verification with its coverage gap rather than claiming unverified health.
- Verifies its own content in continuous integration by executing the instruction-gate hook tests, validating every governed GitHub document against its template, and parsing every workflow file.
- Uses narrowly scoped `applyTo` globs and semantic descriptions so Copilot receives relevant guidance for each file.
- Resolves installed software, repository clones, documentation, configuration, data directories, and URLs from the agent home `Locations.md` registry before searching, probing, or inferring a location.
- Provides a Codex `AGENTS.md` entry point for selecting relevant files from the shared instruction library.
- Provides an opt-in Token Saver agent with restricted tools, targeted context, and terse reporting.
- Provides an opt-in LiteLLM agent with automatic pre-execution instruction gating, staged semantic instruction audits, complete applicable skill procedures, and bounded corrective retries.
- Provides on-demand skills for AI-credit routing, repository orientation, scoped research, baseline checks, failure triage, diff review, instruction-budget audits, symbol navigation, structured-data queries, signal-preserving output, phased investigation and implementation, English language conventions, Romanian language conventions, test design, test suite auditing, test values, manual QA acceptance criteria, project-local verification skill generation, agent instruction coaching, commit-series composition, agent regression evaluation, migration planning, performance profiling, interface localisation, memory-store engineering, skill security auditing, validation, secrets management assessment, secure code review against OWASP ASVS 4.0.3 and the CWE Top 25, prompt injection assessment against OWASP LLM01:2025 and MITRE ATLAS AML.T0051, agent security assessment against OWASP Agentic AI threats and NIST AI RMF 1.0, API security assessment against the OWASP API Security Top 10:2023 with a C# and .NET supplement, pipeline security assessment against the SLSA v1.0 build track and the OWASP Top 10 CI/CD Security Risks, MethodScript conventions with a reference for its 897 built-in functions and 104 bindable events, Imperator: Rome modding conventions with references for scripting, events, setup data, localisation, GUI, map data, and debugging, Stellaris modding conventions with references for merge semantics, scripting, dynamic scripting, events and on actions, economy and planets, empires and content, localisation, interface, map data and defines, and debugging, Crusader Kings II modding conventions with references for override semantics, scripting, events, on actions and decisions, history and setup data, common definitions, localisation, interface, graphics, portraits, coats of arms, map data, music, and debugging, Crusader Kings III modding conventions with references for override and load-order semantics, scripting, events and on actions, decisions and interactions, history and characters, common definitions, localisation, interface, graphics, coat of arms, map and terrain, audio, and debugging, Civilization V modding conventions with references for ModBuddy actions and VFS, XML/SQL database updates, content definitions, Lua scripting, UI and art, localisation, and debugging, GitHub Actions workflow documentation, repository documentation generation, NuGet package updates, logical commit-series composition with staged-secret gating, agent regression evaluation against a measured baseline, migration planning with per-phase rollback, performance profiling from a measured baseline, interface localisation verification, memory-store engineering with a mandatory forgetting policy, skill and plug-in security auditing, and session handoff.
- Skills that modify code or dependencies (e.g., NuGet package updates) automatically trigger documentation updates for relevant repository files (README.md, CONTRIBUTING.md, ARCHITECTURE.md, or project-specific documentation). The `github-actions-workflow` skill holds each canonical workflow template, its rules, the fidelity contract, and the validation script, and synchronises every affected Markdown document whenever a GitHub Actions workflow is created or revised. The `github-md-template-fidelity` skill holds each GitHub document template, its rules, the fidelity contract, and the validation script, so they load only for document generation tasks. The `repository-documentation` skill performs exhaustive evidence-based reverse engineering and generates the structured `docs/` knowledge base when repository documentation is requested.

## 🚀 Usage

After installation, access a project in VS Code and submit a normal Copilot Chat request. Matching instruction files are selected through their `applyTo` globs and descriptions.

For example, to revise a repository README, submit:

```text
Update the README
```

The README rules inspect repository evidence, select applicable template sections, and revise the existing `README.md` in place.

For cost-sensitive coding work, select **Token Saver** from the agent picker. It limits operations to reading, searching, editing, and terminal execution; it neither delegates to subagents nor permits implicit model invocation.

For explicit instruction-compliance checks, select **LiteLLM** from the agent selector. The [agent definition](agents/litellm.agent.md) retains default tools and the selected model, requires complete contextual reading of applicable instructions and skills, and adds pre-action, post-action, and final semantic audits. Tools may retrieve sources and validate results, but never substitute for LLM comprehension. Corrective retries are limited to two per issue and three recovery cycles per assignment, subject to stricter applicable limits. The Local agent hook injects path-scoped common, language, and detected programming-language instructions at session start, preserving that state across prompts and request recovery; complete semantic applicability remains an agent audit requirement.

Skill descriptions remain available for discovery, while full skill procedures load only for relevant tasks.

For Codex, start a new session in your project after installation. The global `AGENTS.md` directs Codex to read relevant shared instructions. Invoke a skill explicitly with its name, such as `$repository-orientation`, or let Codex select it from its description.

## 📦 Installation

### Installation from Source

#### GitHub Copilot

Install [Git](https://git-scm.com/) and [VS Code](https://code.visualstudio.com/) with the [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat). The destination `prompts`, `skills`, `agents`, `hooks`, and `memories` paths must not exist before creating the links, so preserve or relocate any existing content first.

On Linux:

```bash
git clone https://github.com/hmlendea/github-copilot-memories.git
cd github-copilot-memories
ln -s "$PWD/prompts" "$HOME/.config/Code/User/prompts"
mkdir -p "$HOME/.copilot"
ln -s "$PWD/skills" "$HOME/.copilot/skills"
ln -s "$PWD/agents" "$HOME/.copilot/agents"
ln -s "$PWD/hooks" "$HOME/.copilot/hooks"
mkdir -p "$HOME/.config/Code/User/globalStorage/github.copilot-chat/memory-tool"
ln -s "$PWD/globalStorage/github.copilot-chat/memory-tool/memories" "$HOME/.config/Code/User/globalStorage/github.copilot-chat/memory-tool/memories"
```

On macOS:

```bash
git clone https://github.com/hmlendea/github-copilot-memories.git
cd github-copilot-memories
ln -s "$PWD/prompts" "$HOME/Library/Application Support/Code/User/prompts"
mkdir -p "$HOME/.copilot"
ln -s "$PWD/skills" "$HOME/.copilot/skills"
ln -s "$PWD/agents" "$HOME/.copilot/agents"
ln -s "$PWD/hooks" "$HOME/.copilot/hooks"
mkdir -p "$HOME/Library/Application Support/Code/User/globalStorage/github.copilot-chat/memory-tool"
ln -s "$PWD/globalStorage/github.copilot-chat/memory-tool/memories" "$HOME/Library/Application Support/Code/User/globalStorage/github.copilot-chat/memory-tool/memories"
```

On Windows, use an Administrator Command Prompt:

```batch
git clone https://github.com/hmlendea/github-copilot-memories.git
cd github-copilot-memories
mklink /D "%APPDATA%\Code\User\prompts" "%CD%\prompts"
if not exist "%USERPROFILE%\.copilot" mkdir "%USERPROFILE%\.copilot"
mklink /D "%USERPROFILE%\.copilot\skills" "%CD%\skills"
mklink /D "%USERPROFILE%\.copilot\agents" "%CD%\agents"
mklink /D "%USERPROFILE%\.copilot\hooks" "%CD%\hooks"
if not exist "%APPDATA%\Code\User\globalStorage\github.copilot-chat\memory-tool" mkdir "%APPDATA%\Code\User\globalStorage\github.copilot-chat\memory-tool"
mklink /D "%APPDATA%\Code\User\globalStorage\github.copilot-chat\memory-tool\memories" "%CD%\globalStorage\github.copilot-chat\memory-tool\memories"
```

The skill and memory links are optional when only instruction files and custom agents are required. The [hooks directory](hooks/) link is required by the LiteLLM agent.

#### OpenAI Codex

Install [Git](https://git-scm.com/) and [Codex](https://developers.openai.com/codex/quickstart/). Use an existing clone or clone this repository, then run the link commands from its root. Keep the clone in place because the links point to it.

The commands install [user-level skills](https://learn.chatgpt.com/docs/build-skills) in `~/.codex/skills` and [global instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md) in `~/.codex/AGENTS.md`. If `CODEX_HOME` is set, all three links use that directory instead of `~/.codex`. The linked [codex/AGENTS.md](codex/AGENTS.md) directs Codex to the `instructions` link; it uses `applyTo` and `description` to select relevant files.

The destination `skills`, `AGENTS.md`, and `instructions` paths must not already exist. Preserve existing content first: merge the supplied guidance into an existing `AGENTS.md`, and link individual skill folders if you already have a skills directory. If `AGENTS.override.md` exists in your Codex home, merge the guidance there instead because it takes precedence over `AGENTS.md`.

On Linux or macOS:

```bash
git clone https://github.com/hmlendea/github-copilot-memories.git
cd github-copilot-memories
codex_config_dir="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$codex_config_dir"
ln -s "$PWD/skills" "$codex_config_dir/skills"
ln -s "$PWD/codex/AGENTS.md" "$codex_config_dir/AGENTS.md"
ln -s "$PWD/prompts/instructions" "$codex_config_dir/instructions"
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
mklink /D "%codex_config_dir%\instructions" "%CD%\prompts\instructions"
```

Start a new Codex session and ask it to summarise its active instructions and locate `$repository-orientation` to check discovery.

## ⚙️ Configuration

Instruction files reside under `prompts/instructions/`. Each file starts with YAML frontmatter in which `description` identifies the relevant context and `applyTo`, when present, limits automatic application to matching paths.

The always-on common instructions additionally direct each agent to read the `Locations.md` registry in its own home directory (`~/.copilot/Locations.md` for GitHub Copilot, `~/.codex/Locations.md` or `$CODEX_HOME/Locations.md` for Codex, with the macOS and Windows equivalents) before resolving any path or address, so a recorded location is used instead of being searched for or inferred.

Language dictionaries use semantic discovery rather than automatic path activation. Their compact `source [context] -> replacements/replacements` records live in the `english-language` and `romanian-language` skills and load only for relevant language and terminology work.

Custom agents reside under [agents/](agents/). Token Saver and LiteLLM are opt-in and do not pin a model; select the desired model and reasoning effort prior to starting a session.

Skills reside under `skills/`. Their concise descriptions support task-based discovery; complete procedures load on demand. The `ai-credit-routing` skill selects economical modes, models, reasoning effort, sessions, and tool sets, gates model and effort escalation behind a stated condition, attributes spend by tokens and by cost, and judges savings by cost per completed task; `repository-orientation` limits repository discovery to relevant sources; `github-md-template-fidelity` supplies the GitHub document templates, rules, fidelity contract, and validator; `github-actions-workflow` supplies the GitHub Actions workflow templates, rules, fidelity contract, validator, and cross-file documentation procedure; `repository-documentation` supplies the exhaustive reverse-engineering procedure and `docs/` structure contract; `secrets-management` supplies the OWASP and NIST SP 800-57 secrets management assessment procedure; `secure-code-review` supplies the OWASP ASVS 4.0.3 and CWE Top 25 secure code review procedure; `prompt-injection` supplies the OWASP LLM01:2025 and MITRE ATLAS AML.T0051 prompt injection assessment procedure; `agent-security` supplies the OWASP Agentic AI and NIST AI RMF 1.0 agent architecture security assessment procedure; `api-security` supplies the OWASP API Security Top 10:2023 API review procedure with a per-category checklist and a C# and .NET supplement; `pipeline-security` supplies the SLSA v1.0 build level and OWASP Top 10 CI/CD Security Risks pipeline assessment procedure; `supply-chain-security` supplies the dependency inventory, SBOM and VEX validation, licence compliance, and multi-signal CVE triage procedure; `ui-design-review` supplies the prioritised interface rule set, the native and mobile pre-delivery checklist, and the browser-driven audit script; `research-plan-implement` separates non-trivial work into an investigation phase, a planning phase, and an implementation phase, each in a fresh session, and hands off between them with `session-handoff`; `pr-babysit` observes a pull request or review cycle to merge readiness, verifying each finding before correction and resolving a review thread only after the code addresses it; `imperator-rome-modding` supplies Imperator: Rome mod packaging, scripting, event, decision, setup, localisation, GUI, map, unit, and debugging procedures; `stellaris-modding` supplies Stellaris mod packaging, merge and load-order semantics, scripting, dynamic scripting, events and on actions, economy and planet content, empire and content definitions, localisation, interface, map and defines, and debugging procedures; `ck2-modding` supplies Crusader Kings II mod packaging, override and load-order semantics, scripting: event, on action and decision, history and setup, common definition, localisation, interface, graphics, portrait, coat of arms, map, music, and debugging procedures; `ck3-modding` supplies Crusader Kings III mod packaging, override and load-order semantics, scripting, events and on actions, decisions and interactions, history and characters, common definitions, localisation, interface, graphics, coat of arms, map and terrain, sound, and debugging procedures; `civ5-modding` supplies Civilization V ModBuddy action and VFS wiring, XML/SQL database update, content definition, Lua scripting, UI and art, localisation, and debugging procedures; `vic3-modding` supplies Victoria 3 metadata and override semantics, scripting, event and on action, politics and diplomacy, building and production method, goods and pop, history and map, localisation, interface, graphics and audio, and debugging procedures; `release-verification` verifies the delivered artefact per surface after a release, publication, or deployment, classifies findings, and reports partial verification with its coverage gap; `pre-aggregate-data` moves data collection out of the token-billed loop by retrieving trimmed results into `.work` files during a preliminary step; `methodscript` supplies the MethodScript architecture and style rules together with a reference for every built-in function and bindable event; `test-audit` gardens test suites by detecting and eliminating redundant, vacuous, or implementation-coupled tests while preserving regression proof; `qa-acceptance` produces Given-When-Then acceptance criteria and a manual validation plan for feature changes; `create-verification-skill` generates a project-local verification skill that drives the application the way a user does and captures evidence; `agent-instruction-coaching` proposes evidence-backed modifications to another agent's instructions, skills, or tool descriptions behind a reviewed-diff gate; `commit-craft` composes a mixed working tree into logical commits with a staged-secret gate and message discipline; `agent-regression-evals` adjudicates an agent, prompt, model, or tool modification through repeated trials and paired comparison against a baseline; `migration-architect` plans a schema, database, service, or host migration in phases, each with a compatibility determination and a rollback procedure; `performance-profiler` establishes a measured baseline, profiles processor, memory, data, and distribution constrictions, and substantiates each modification with a measured difference; `i18n-localization` verifies keys, placeholders, ICU syntax, and CLDR plural categories, detects untranslated text, and reviews a pseudo-locale; `memory-engineering` prices and selects a memory family and demands an explicit forgetting policy; `skill-security-auditor` inspects an untrusted skill, plug-in, hook, or agent definition for execution, instruction, dependency, and structure risks and returns a redacted verdict; the Token Saver agent handles execution with restricted tools.

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
| GitHub Copilot Chat memory tool | `memory-tool/memories/` storage layout | Exposes the coding-pattern reference index | No |

## 🛡️ Privacy and Data

GitHub Copilot Memories does not collect, process, transmit, or persist user data, analytics, diagnostics, or telemetry.

For the detailed description of how the application handles privacy and personal data, see [PRIVACY.md](./PRIVACY.md).

## 🛠️ Development

### Requirements

- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/), required by the instruction-gate hook tests
- [Python 3](https://www.python.org/downloads/), required by the template validators
- [PyYAML](https://pypi.org/project/PyYAML/), required only to parse workflow files during verification

### Setup

Clone the repository and create the user-profile links described under [Installation](#installation). The instruction content requires no dependency installation; only the verification commands below need the listed requirements.

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

Validate the hook and validator scripts for syntax errors:

```bash
node --check hooks/litellm-instruction-gate.cjs
python3 -m py_compile skills/github-md-template-fidelity/validate_github_md.py skills/github-actions-workflow/validate_github_actions.py
```

### Continuous Integration

The [Verification workflow](.github/workflows/verification.yml) executes these checks, and parses every workflow file, on every push and pull request targeting `master`. Reproduce it locally with the commands above before opening a pull request.

## ⚙️ GitHub Actions

| Workflow | Purpose | What it does |
|----------|---------|--------------|
| [Verification](https://github.com/hmlendea/github-copilot-memories/blob/master/.github/workflows/verification.yml) | Continuous verification | Executes the instruction-gate hook tests, checks the hook and validator scripts for syntax errors, validates every governed GitHub document against its template, and parses every workflow file to confirm it remains valid YAML with a name and job definitions |

## 🗂️ Project Structure

The tracked project is content-focused. Instruction families are separated by language and concern so each file can define a narrow activation contract.

### Directories

| Directory | Purpose |
|-----------|---------|
| `codex/` | Global Codex instructions that select relevant files from the shared library |
| [agents/](agents/) | Opt-in custom agents for restricted-tool execution and semantic instruction-compliance audits |
| [hooks/](hooks/) | Runtime instruction-read enforcement used by the LiteLLM agent |
| `prompts/instructions/common/` | Shared coding, naming, error-handling, test-design, and documentation principles |
| `prompts/instructions/csharp/` | C# language, project, testing, mapping, logging, MonoGame, and NuciXNA guidance |
| `prompts/instructions/github/` | GitHub Actions workflow naming and documentation rules |
| `prompts/instructions/language/` | British English and Romanian terminology preferences; require the `english-language` and `romanian-language` skills |
| `prompts/instructions/markdown/` | Markdown structure and formatting conventions |
| `prompts/instructions/methodscript/` | MethodScript coding and style conventions; require the `methodscript` skill |
| `prompts/instructions/polyglot/` | PolyGlot dictionary conventions |
| `prompts/instructions/python/` | Python coding and error-handling conventions |
| `prompts/instructions/shell/` | Shell coding, naming, and error-handling conventions |
| `prompts/instructions/typescript/` | TypeScript coding, naming, and style conventions |
| `skills/` | On-demand procedures for context, baseline checks, failure triage, review, instruction audits, research, phased investigation and implementation, structured data, English and Romanian language conventions, secrets management assessment, secure code review, prompt injection assessment, agent security assessment, API security assessment, pipeline security assessment, supply chain security assessment, user interface design review, MethodScript conventions and API references, Imperator: Rome modding conventions and references, Stellaris modding conventions and references, Crusader Kings II modding conventions and references, Crusader Kings III modding conventions and references, Civilization V modding conventions and references, Victoria 3 modding conventions and references, test design, test suite auditing, test values, manual QA acceptance criteria, project-local verification skill generation, agent instruction coaching, validation, commit-series composition, agent regression evaluation, migration planning, performance profiling, interface localisation, memory-store engineering, skill security auditing, GitHub Actions workflow templates, GitHub markdown template fidelity, repository documentation generation, NuGet package updates, data pre-aggregation, and token-efficient workflows |
| `globalStorage/github.copilot-chat/memory-tool/memories/` | Optional Copilot Chat memory index |

## 🏗️ Architecture

GitHub Copilot Memories is a content-only repository of instruction files, skills, and agents.

See the [architecture documentation](./ARCHITECTURE.md) for the system context, principal components, runtime flows, ownership boundaries, dependencies, constraints, and extension points.

## 🗺️ Roadmap

See [ROADMAP.md](./ROADMAP.md) for planned work and forthcoming changes.

## 🤝 Contributing

You are welcome to submit any suggestion, feedback, or modification to this project.

When doing so, please:
- Maintain cross-platform compatibility
- Submit focused pull requests that conform to the existing code style
- Maintain your branch synchronised with `master`

## 📜 Code of Conduct

See the [Code of Conduct](./CODE_OF_CONDUCT.md) for the standards of conduct expected in all project spaces.

## 🔒 Security

GitHub Copilot Memories does not host services, execute code, or process user data.

For information on reporting security vulnerabilities, see [SECURITY.md](./SECURITY.md).

## 💬 Support

For support, please [open an issue](https://github.com/hmlendea/github-copilot-memories/issues).

## 💝 Project Engagement

Discovered a problem or have a suggestion? [Open an issue](https://github.com/hmlendea/github-copilot-memories/issues)!

If you find this project useful, consider [funding it](https://hmlendea.go.ro/funding) or giving a ⭐️ on GitHub!

## 📄 License

This project is being distributed under the `GNU General Public License v3.0`.
See [LICENSE](./LICENSE) for further information.
