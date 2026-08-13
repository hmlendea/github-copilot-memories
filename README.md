[![Donate](https://img.shields.io/badge/-%E2%99%A5%20Donate-%23ff69b4)](https://hmlendea.go.ro/funding)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://gnu.org/licenses/gpl-3.0)

# GitHub Copilot Memories

A curated collection of GitHub Copilot instruction files that encode reusable coding standards, documentation templates, language conventions, and domain-specific guidance for VS Code and GitHub Copilot Chat.

## 📑 Table of Contents

- [Table of Contents](#table-of-contents)
- [Capabilities](#capabilities)
- [Usage](#usage)
- [Installation](#installation)
  - [Installation from Source](#installation-from-source)
- [Configuration](#configuration)
- [Integrations](#integrations)
- [Project Structure](#project-structure)
  - [Directories](#directories)
- [Contributing](#contributing)
- [Project Engagement](#project-engagement)
- [License](#license)

## ✨ Capabilities

- Applies shared coding, naming, error-handling, security, and documentation principles across supported file types.
- Provides specialised guidance for C#, Python, TypeScript, shell scripts, MethodScript, PolyGlot dictionaries, Markdown, MonoGame, and NuciXNA.
- Generates evidence-based README, architecture, roadmap, security, and GitHub Actions documents from strict templates.
- Maintains British English and Romanian language preferences through contextual terminology rules.
- Supplies consistent test values and an optional coding-pattern memory index.
- Uses narrowly scoped `applyTo` globs and semantic descriptions so Copilot receives relevant guidance for each file.

## 🚀 Usage

After installation, access a project in VS Code and submit a normal Copilot Chat request. Matching instruction files are selected through their `applyTo` globs and descriptions.

For example, to revise a repository README, submit:

```text
Update the README
```

The README rules inspect repository evidence, select applicable template sections, and revise the existing `README.md` in place.

## 📦 Installation

### Installation from Source

Install [Git](https://git-scm.com/) and [VS Code](https://code.visualstudio.com/) with the [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat). The destination `prompts` and `memories` paths must not exist before creating the links, so preserve or relocate any existing content first.

On Linux:

```bash
git clone https://github.com/hmlendea/github-copilot-memories.git
cd github-copilot-memories
ln -s "$PWD/prompts" "$HOME/.config/Code/User/prompts"
mkdir -p "$HOME/.config/Code/User/globalStorage/github.copilot-chat/memory-tool"
ln -s "$PWD/globalStorage/github.copilot-chat/memory-tool/memories" "$HOME/.config/Code/User/globalStorage/github.copilot-chat/memory-tool/memories"
```

On macOS:

```bash
git clone https://github.com/hmlendea/github-copilot-memories.git
cd github-copilot-memories
ln -s "$PWD/prompts" "$HOME/Library/Application Support/Code/User/prompts"
mkdir -p "$HOME/Library/Application Support/Code/User/globalStorage/github.copilot-chat/memory-tool"
ln -s "$PWD/globalStorage/github.copilot-chat/memory-tool/memories" "$HOME/Library/Application Support/Code/User/globalStorage/github.copilot-chat/memory-tool/memories"
```

On Windows, use an Administrator Command Prompt:

```batch
git clone https://github.com/hmlendea/github-copilot-memories.git
cd github-copilot-memories
mklink /D "%APPDATA%\Code\User\prompts" "%CD%\prompts"
if not exist "%APPDATA%\Code\User\globalStorage\github.copilot-chat\memory-tool" mkdir "%APPDATA%\Code\User\globalStorage\github.copilot-chat\memory-tool"
mklink /D "%APPDATA%\Code\User\globalStorage\github.copilot-chat\memory-tool\memories" "%CD%\globalStorage\github.copilot-chat\memory-tool\memories"
```

The memory link is optional; omit its `mkdir` and `ln` or `mklink` commands when only the instruction files are required.

## ⚙️ Configuration

Instruction files reside under `prompts/instructions/`. Each file starts with YAML frontmatter in which `description` identifies the relevant context and `applyTo`, when present, limits automatic application to matching paths.

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
| VS Code with GitHub Copilot Chat | User-profile `prompts/` discovery | Applies the instruction files during Copilot interactions | Yes |
| GitHub Copilot Chat memory tool | `memory-tool/memories/` storage layout | Exposes the coding-pattern reference index | No |

## 🗂️ Project Structure

The tracked project is content-focused. Instruction families are separated by language and concern so each file can define a narrow activation contract.

### Directories

| Directory | Purpose |
|-----------|---------|
| `prompts/instructions/common/` | Shared coding, naming, error-handling, test-data, security, and documentation principles |
| `prompts/instructions/csharp/` | C# language, project, testing, mapping, logging, MonoGame, and NuciXNA guidance |
| `prompts/instructions/github/` | Repository document and GitHub Actions rules and templates |
| `prompts/instructions/language/` | British English and Romanian terminology preferences |
| `prompts/instructions/markdown/` | Markdown structure and formatting conventions |
| `prompts/instructions/methodscript/` | MethodScript coding and style conventions |
| `prompts/instructions/polyglot/` | PolyGlot dictionary conventions |
| `prompts/instructions/python/` | Python coding and error-handling conventions |
| `prompts/instructions/shell/` | Shell coding, naming, and error-handling conventions |
| `prompts/instructions/typescript/` | TypeScript coding, naming, and style conventions |
| `globalStorage/github.copilot-chat/memory-tool/memories/` | Optional Copilot Chat memory index |

## 🤝 Contributing

You are welcome to submit any suggestion, feedback, or modification to this project.

When doing so, please:
- Maintain cross-platform compatibility
- Submit focused pull requests that conform to the existing code style
- Maintain your branch synchronised with `master`

## 💝 Project Engagement

Discovered a problem or have a suggestion? [Open an issue](https://github.com/hmlendea/github-copilot-memories/issues)!

If you find this project useful, consider [funding it](https://hmlendea.go.ro/funding) or giving a ⭐️ on GitHub!

## 📄 License

This project is being distributed under the `GNU General Public License v3.0`.
See [LICENSE](./LICENSE) for further information.
