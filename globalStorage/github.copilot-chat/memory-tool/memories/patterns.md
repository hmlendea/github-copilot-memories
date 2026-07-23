# Coding Patterns Index

This file is a reference index only. The actual coding rules are maintained as `.instructions.md` files in the VS Code user profile `prompts/` folder and are automatically applied by GitHub Copilot via `applyTo` glob patterns.

The `prompts/` folder location varies by OS:

| OS | Path |
|---|---|
| Linux | `~/.config/Code/User/prompts/` |
| macOS | `~/Library/Application Support/Code/User/prompts/` |
| Windows | `%APPDATA%\Code\User\prompts\` |

On this machine the folder is symlinked to `prompts/` in this repository.

## Instruction Files

| File | `applyTo` | Contents |
|---|---|---|
| `general.instructions.md` | `**` | General rules, source control |
| `bash.instructions.md` | `**/*.sh` | Bash/shell scripting |
| `csharp.instructions.md` | `**/*.cs`, `**/*.csproj`, `**/*.slnx` | C# (all sections) |
| `monogame.instructions.md` | description-based | XNA / MonoGame / NuciXNA |
| `python.instructions.md` | `**/*.py` | Python |
| `typescript.instructions.md` | `**/*.ts`, `**/*.tsx` | TypeScript |
| `test-values.instructions.md` | description-based | Standard test values (names, cities, etc.) |

## Prompt Files

| File | Trigger | Purpose |
|---|---|---|
| `github-readme.instructions.md` | `/github-readme` or "generate/update README" | Generate or update a `README.md` for a GitHub repository |

See also: [test-values.md](test-values.md) for the raw test values reference.
