# GitHub Copilot Memories Architecture

This document describes the current architecture of the GitHub Copilot Memories repository. It covers the repository's content organisation, activation model, and integration boundaries with GitHub Copilot Chat and OpenAI Codex.

## 📑 Table of Contents

- [Purpose](#purpose)
- [System Context](#system-context)
- [Architectural Style](#architectural-style)
- [Runtime Flow](#runtime-flow)
- [Architectural Areas](#architectural-areas)
- [Dependency Direction and Rules](#dependency-direction-and-rules)
- [Deployment and Operations](#deployment-and-operations)
- [Testing and Verification](#testing-and-verification)
- [Design Constraints](#design-constraints)
- [Related Documentation](#related-documentation)

## 🎯 Purpose

This repository provides a curated collection of instruction files, skills, and agents that encode reusable coding standards, documentation templates, language conventions, and domain-specific guidance for GitHub Copilot Chat and OpenAI Codex. The architectural scope covers the repository's content organisation, activation model, and integration boundaries with the host AI assistants. The intended audience is contributors who maintain or extend the instruction library.

## 🌐 System Context

The repository is a content-only repository. It does not host services, execute code, or process user data. The repository content is consumed by two external systems:

```mermaid
flowchart LR
    subgraph "GitHub Copilot Memories Repository"
        A["Instruction Files<br/>prompts/instructions/"]
        B["Skills<br/>skills/"]
        C["Agents<br/>agents/"]
        D["Hooks<br/>hooks/"]
        E["Codex AGENTS.md<br/>codex/AGENTS.md"]
    end
    F["GitHub Copilot Chat"]
    G["OpenAI Codex"]
    F -->|"reads via applyTo globs"| A
    F -->|"discovers and loads"| B
    F -->|"selects from agent picker"| C
    F -->|"executes at session start"| D
    G -->|"reads via AGENTS.md"| E
    G -->|"discovers and loads"| B
end
```

The principal external boundaries are:
- **GitHub Copilot Chat:** Consumes instruction files through `applyTo` globs and descriptions, loads skills on demand, selects custom agents from the agent picker, and executes hooks at session start.
- **OpenAI Codex:** Reads the global `AGENTS.md` and user-level skills directory to discover and apply relevant instructions.

## 🏗️ Architectural Style

The repository follows a content-library architectural style. Instruction files are organised by concern (common, language, framework) and activated through narrowly scoped `applyTo` globs and semantic descriptions. Skills are self-contained procedures discovered by name or description. Agents are opt-in execution modes with restricted or extended tool sets. Hooks enforce pre-execution instruction gating.

```mermaid
flowchart LR
    A["Instruction Files<br/>by language/concern"]
    B["Skills<br/>on-demand procedures"]
    C["Agents<br/>execution modes"]
    D["Hooks<br/>runtime enforcement"]
    E["Codex AGENTS.md<br/>entry point"]
    A -->|"applyTo globs"| F["Copilot Chat"]
    B -->|"skill discovery"| F
    C -->|"agent picker"| F
    D -->|"session start"| F
    E -->|"global instructions"| G["OpenAI Codex"]
    B -->|"skill discovery"| G
end
```

The principal architecture boundaries are:
- **Instruction Files:** Content-scoped guidance activated by `applyTo` globs; no runtime execution.
- **Skills:** Self-contained procedures with concise descriptions for discovery; full procedures load on demand.
- **Agents:** Opt-in execution modes with defined tool restrictions and reporting styles.
- **Hooks:** Runtime scripts that enforce instruction gating before model invocation.

## 🔄 Runtime Flow

The repository content is consumed at session start and on demand. There is no persistent runtime process.

```mermaid
flowchart TD
    A["User opens project in VS Code or Codex"] --> B{"Copilot Chat or Codex?"}
    B -->|"Copilot Chat"| C["Load instruction files via applyTo globs"]
    B -->|"Codex"| D["Read global AGENTS.md"]
    C --> E["Execute hooks at session start"]
    D --> F["Read linked instructions directory"]
    E --> G["Inject path-scoped instructions"]
    F --> G
    G --> H["User submits request"]
    H --> I["Match instructions by applyTo/description"]
    H --> J["Discover skills by description"]
    H --> K["Select agent from picker"]
    I --> L["Apply matched instructions"]
    J --> L
    K --> L
    L --> M["Generate response"]
end
```

The principal runtime sequence is:
1. User opens a project in VS Code with Copilot Chat or starts a Codex session.
2. Instruction files are loaded via `applyTo` globs (Copilot) or the global `AGENTS.md` (Codex); hooks execute at session start to inject path-scoped instructions.
3. User submits a request; matching instructions, skills, and agents are selected and applied to generate a response.

## 🗂️ Architectural Areas

### Instruction Files

Paths:
- `prompts/instructions/common/`
- `prompts/instructions/csharp/`
- `prompts/instructions/github/`
- `prompts/instructions/language/`
- `prompts/instructions/markdown/`
- `prompts/instructions/methodscript/`
- `prompts/instructions/polyglot/`
- `prompts/instructions/python/`
- `prompts/instructions/shell/`
- `prompts/instructions/typescript/`

Responsibilities:
- Encode reusable coding standards, naming conventions, error-handling patterns, and documentation templates.
- Provide language-specific and framework-specific guidance.
- Define activation contracts through `applyTo` globs and semantic descriptions.

Boundary rules:
- Each instruction file must define a narrow `applyTo` glob and a semantic description.
- Instruction files must not reference external services or expose secrets.

### Skills

Paths:
- `skills/`

Responsibilities:
- Provide on-demand procedures for context, baseline checks, failure triage, review, instruction audits, research, structured data, validation, and token-efficient workflows.
- Support task-based discovery through concise descriptions.

Boundary rules:
- Each skill must be self-contained with a clear procedure.
- Skills must not execute arbitrary code outside the repository context.

### Agents

Paths:
- `agents/`

Responsibilities:
- Provide opt-in execution modes with restricted or extended tool sets.
- Define reporting styles and operational constraints.

Boundary rules:
- Agents must not pin a model; the user selects the model and reasoning effort.
- Agents must declare their tool restrictions explicitly.

### Hooks

Paths:
- `hooks/`

Responsibilities:
- Enforce pre-execution instruction gating for the LiteLLM agent.
- Inject path-scoped common, language, and detected programming-language instructions at session start.

Boundary rules:
- Hooks must not modify repository content.
- Hooks must preserve state across prompts and request recovery.

### Codex Entry Point

Paths:
- `codex/AGENTS.md`

Responsibilities:
- Direct Codex to read relevant shared instructions from the linked `instructions` directory.
- Use `applyTo` and `description` to select relevant files.

Boundary rules:
- The `AGENTS.md` must not duplicate instruction content; it must reference the linked directory.

## 🧭 Dependency Direction and Rules

The repository has no internal runtime dependencies. It depends on external systems for consumption:

```mermaid
flowchart LR
    A["GitHub Copilot Memories"] -->|"consumed by"| B["GitHub Copilot Chat"]
    A -->|"consumed by"| C["OpenAI Codex"]
    A -->|"references"| D["GitHub"]
    A -->|"references"| E["VS Code"]
end
```

The principal dependency rules are:
- Instruction files must not depend on external services at runtime.
- Skills must not depend on external services beyond repository evidence.
- Agents must not pin a model; the user selects the model and reasoning effort.
- Hooks must not modify repository content.

## 🚀 Deployment and Operations

The repository is deployed through GitHub. Users install it by cloning the repository and creating symbolic links to their user-profile directories. There is no build step, no persistent state, and no operational deployment.

| Concern | Current Design | Architectural Consequence |
|---------|----------------|---------------------------|
| Distribution | Git clone and symbolic links | Users must keep the clone in place because links point to it |
| Activation | `applyTo` globs and descriptions | Instructions are selected automatically by file path and context |
| Skill discovery | Skill descriptions | Full procedures load only for relevant tasks |
| Agent selection | Agent picker | Agents are opt-in and do not pin a model |

## ✅ Testing and Verification

The repository contains no executable tests. The `hooks/` directory includes a test file (`litellm-instruction-gate.test.cjs`) that validates the instruction-gate hook. The `skills/github-md-template-fidelity/` directory includes a validation script (`validate_github_md.py`) that checks template fidelity for generated GitHub markdown files.

Execute the principal automated verification with:

```bash
python3 skills/github-md-template-fidelity/validate_github_md.py /home/horatiu/Proiecte/ai/github-copilot-memories README.md README.md
```

## ⚠️ Design Constraints

- **Content-only repository:** The repository does not host services, execute code, or process user data.
- **No model pinning:** Agents must not pin a model; the user selects the model and reasoning effort.
- **No secrets:** Instruction files must not reference external services or expose secrets.
- **Symbolic links:** Users must keep the clone in place because links point to it.

## 📚 Related Documentation

- [README.md](./README.md) — Project overview, capabilities, usage, installation, and configuration.
- [CONTRIBUTING.md](./CONTRIBUTING.md) — Guidelines for contributing to the project.
- [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) — Standards of conduct expected in all project spaces.
- [SECURITY.md](./SECURITY.md) — Security policy and vulnerability reporting.
- [PRIVACY.md](./PRIVACY.md) — Data-handling practices.
- [ROADMAP.md](./ROADMAP.md) — Planned work and forthcoming changes.