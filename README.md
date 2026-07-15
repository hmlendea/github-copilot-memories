[![Donate](https://img.shields.io/badge/-%E2%99%A5%20Donate-%23ff69b4)](https://hmlendea.go.ro/funding)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://gnu.org/licenses/gpl-3.0)

# GitHub Copilot Memories

A curated collection of GitHub Copilot instruction files and prompt templates that encode personal coding standards, style conventions, and domain-specific rules. These files are loaded automatically by VS Code's Copilot Chat, ensuring consistent, high-quality code generation across all projects.

## ✨ Features

- **Language-specific instruction files** for C#, Python, TypeScript/JavaScript, and Bash, each covering naming, style, error handling, and best practices for that language.
- **General coding rules** applied to all files: clean code, single responsibility, British English, magic number elimination, dead code removal, and line-length limits.
- **MonoGame / NuciXNA rules** covering GUI control lifecycle, texture management, and NuciXNA-specific APIs.
- **Language preference rules** for both English (British spelling) and Romanian (word replacement lists).
- **Standard test values** providing a consistent set of funny, reusable test data (names, cities, domains, video game titles, etc.) used across all test suites.
- **README prompt template** for generating standardised, well-structured `README.md` files.
- **Patterns memory file** stored under `globalStorage/` so Copilot Chat's memory tool can reference the index at runtime.
- **Symlink-friendly layout**: the `prompts/` folder is designed to be symlinked directly into the VS Code user profile so rule updates are reflected immediately without copying files.

## 🚀 Usage

Once the `prompts/` folder is symlinked (see [Development](#-development)), Copilot Chat picks up all `.instructions.md` files automatically based on their `applyTo` patterns. No further configuration is necessary - just use Copilot Chat as normal and the rules will be applied.

To generate a `README.md` for any repository, open Copilot Chat and type:

```
Update the readme
```

The `github-readme.prompt.md` template will be invoked automatically.

## 🛠️ Development

### Requirements

- [VS Code](https://code.visualstudio.com/) with the GitHub Copilot Chat extension installed.

### Setup

Clone the repository and symlink the `prompts/` and `memories/` directories into your VS Code user profile:

```bash
# Linux
ln -s "$(pwd)/prompts" ~/.config/Code/User/prompts
mkdir -p ~/.config/Code/User/globalStorage/github.copilot-chat/memory-tool
ln -s "$(pwd)/globalStorage/github.copilot-chat/memory-tool/memories" ~/.config/Code/User/globalStorage/github.copilot-chat/memory-tool/memories

# macOS
ln -s "$(pwd)/prompts" ~/Library/Application\ Support/Code/User/prompts
mkdir -p ~/Library/Application\ Support/Code/User/globalStorage/github.copilot-chat/memory-tool
ln -s "$(pwd)/globalStorage/github.copilot-chat/memory-tool/memories" ~/Library/Application\ Support/Code/User/globalStorage/github.copilot-chat/memory-tool/memories

# Windows (run as Administrator)
mklink /D "%APPDATA%\Code\User\prompts" "%CD%\prompts"
mkdir "%APPDATA%\Code\User\globalStorage\github.copilot-chat\memory-tool"
mklink /D "%APPDATA%\Code\User\globalStorage\github.copilot-chat\memory-tool\memories" "%CD%\globalStorage\github.copilot-chat\memory-tool\memories"
```

VS Code picks up all `.instructions.md` and `.prompt.md` files automatically via the `chat.promptFilesLocations` setting (or the default user-profile scan).

## 🗂️ Project Structure

Key directories and files:

| Path | Purpose |
|------|---------|
| `prompts/` | Instruction and prompt files loaded by VS Code Copilot Chat |
| `globalStorage/github.copilot-chat/memory-tool/memories/` | Memory files used by the Copilot Chat memory tool |

Key files inside `prompts/`:

| File | `applyTo` | Purpose |
|------|-----------|---------|
| `general.instructions.md` | `**` | General coding rules and source control conventions |
| `language.instructions.md` | `**` | British English spelling and Romanian word replacements |
| `csharp.instructions.md` | `**/*.cs`, `**/*.csproj`, `**/*.slnx` | C# project structure, code style, and unit test rules |
| `bash.instructions.md` | `**/*.sh` | Bash/shell scripting conventions |
| `python.instructions.md` | `**/*.py` | Python coding conventions |
| `typescript.instructions.md` | `**/*.ts`, `**/*.tsx` | TypeScript/JavaScript coding conventions |
| `monogame.instructions.md` | description-based | XNA / MonoGame / NuciXNA-specific rules |
| `test-values.instructions.md` | description-based | Standard reusable test data values |
| `github-readme.prompt.md` | prompt | Template for generating `README.md` files |

## 🤝 Contributing

Contributions are welcome. Please:
- Keep changes cross-platform
- Keep pull requests focused and consistent with the existing code style
- Update documentation when behaviour changes

## 💝 Support

Found a bug or have a suggestion? [Open an issue](https://github.com/hmlendea/github-copilot-memories/issues)!

If you find this project useful, consider [funding it](https://hmlendea.go.ro/funding) or giving a ⭐️ on GitHub!

## 📄 License

Licensed under the `GNU General Public License v3.0` or later.
See [LICENSE](./LICENSE) for details.
