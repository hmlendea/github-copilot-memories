# GitHub Copilot Memories Architecture

This document describes the current architecture of the GitHub Copilot Memories repository. It covers the repository's content organisation, activation model, and integration boundaries with GitHub Copilot Chat and OpenAI Codex.

## 📑 Table of Contents

- [Purpose](#purpose)
- [System Context](#system-context)
- [Architectural Style](#architectural-style)
- [Runtime Process](#runtime-process)
- [Architectural Areas](#architectural-areas)
  - [Instruction Files](#instruction-files)
  - [Skills](#skills)
  - [Agents](#agents)
  - [Hooks](#hooks)
  - [Codex Entry Point](#codex-entry-point)
- [Dependency Direction and Rules](#dependency-direction-and-rules)
- [Deployment and Operations](#deployment-and-operations)
- [Testing and Verification](#testing-and-verification)
- [Design Constraints](#design-constraints)
- [Related Documentation](#related-documentation)

## 🎯 Purpose

The repository provides a curated collection of instruction files, skills, and agents that encode reusable coding standards, documentation templates, language conventions, and domain-specific guidance for GitHub Copilot Chat and OpenAI Codex. The architectural scope covers the repository's content organisation, activation model, and integration boundaries with the host AI assistants. The intended audience is contributors who maintain or extend the instruction library.

## 🌐 System Context

The repository is a content-only repository. It does not host services, execute code, or process user data. The repository content is consumed by two external systems:

```mermaid
flowchart LR
    subgraph "GitHub Copilot Memories Repository"
        A["Instruction Files<br/>instructions/"]
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

## 🔄 Runtime Process

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
- `instructions/common/`
- `instructions/csharp/`
- `instructions/gh-actions/`
- `instructions/git/`
- `instructions/github/`
- `instructions/html/`
- `instructions/java/`
- `instructions/javascript/`
- `instructions/kotlin/`
- `instructions/language/`
- `instructions/markdown/`
- `instructions/methodscript/`
- `instructions/polyglot/`
- `instructions/python/`
- `instructions/shell/`
- `instructions/typescript/`
- `instructions/xml/`

Responsibilities:
- Encode reusable coding standards, naming conventions, error-handling patterns, and language preferences.
- Provide language-specific and framework-specific guidance.
- Define activation contracts through `applyTo` globs and semantic descriptions.
- Require reading the agent home `Locations.md` registry (`~/.copilot/Locations.md`, `~/.codex/Locations.md`, or the platform equivalent) before resolving any path or address, so a recorded value is preferred over search, probe, or inference.
- Require, through the always-on `instructions/common/common.instructions.md`, that an item inserted into an alphabetically ordered list, enumeration, table, or key set in any text takes its alphabetical position, so the existing order is preserved.
- Require, through the always-on `instructions/common/common.work-directory.instructions.md`, that every repository task consults the Git-excluded `.work/` directory when present, places temporary data and utilities there, records reusable progress, decisions, context, and data there for later sessions, and never mentions the directory in any tracked artefact.
- Keep secrets, personal data, system-specific details, and agent configuration details (names, paths, or invocations of skills, instructions, prompts, agents, or memories that the working repository does not track) out of every tracked file, commit, publication, third-party request, and agent memory through the always-on `instructions/common/common.security.instructions.md`, which defines the protected categories, the Git-ignored exception, the required substitutes, and the mandatory `leak-prevention` scan.
- Cover GitHub Actions workflow naming and documentation rules, and Markdown link conventions, under `instructions/github/`; GitHub document templates and rules live in the `github-md-template-fidelity` skill, GitHub Actions workflow templates and rules live in the `github-actions-workflow` skill, shared test fixture values live in the `test-values` skill, English and Romanian vocabulary preferences live in the `english-language` and `romanian-language` skills, MethodScript architecture, style rules, built-in function reference, and bindable event reference live in the `methodscript` skill, and Imperator: Rome mod packaging, scripting, setup, localisation, GUI, map, and debugging references live in the `imperator-rome-modding` skill; Stellaris mod packaging, merge semantics, scripting, dynamic scripting, events and on actions, economy and planets, empires and content, localisation, interface, map, defines, and debugging references live in the `stellaris-modding` skill; Crusader Kings II mod packaging, override semantics, scripting, events, on actions and decisions, history and setup, common definitions, localisation, interface, graphics, portraits, coats of arms, map, music, and debugging references live in the `ck2-modding` skill; Crusader Kings III mod packaging, override and load-order semantics, scripting, events and on actions, decisions and interactions, history and characters, common definitions, localisation, interface, graphics, coat of arms, map and terrain, audio, and debugging references live in the `ck3-modding` skill; Civilization IV mod packaging and modular loading, XML table and schema handling, text and art-define conventions, content definitions, Python scripting, interface and font art, WorldBuilder and map scripts, SDK and C++ changes, and debugging references live in the `civ4-modding` skill; Civilization V mod packaging, VFS and action wiring, XML/SQL database updates, content definitions, Lua scripting, UI contexts, art atlases, localisation, and debugging references live in the `civ5-modding` skill; Civilization VI ModBuddy action, criteria, and load-order wiring, SQL and GameData updates, content definitions, modifier and requirement composition, Lua scripting, UI, icon and art handling, localisation, and debugging references live in the `civ6-modding` skill; Civilization: Beyond Earth mod packaging, VFS and action wiring, XML/SQL database updates, sponsor, colonist, cargo, spacecraft, unit, technology, affinity, virtue, quest, artifact, marvel, covert operation, orbital unit, biome, improvement, and resource content definitions, Lua scripting, UI contexts and art, localisation, and debugging references live in the `civbe-modding` skill; Victoria 3 mod packaging, metadata and override semantics, scripting, events and on actions, politics and diplomacy content, buildings, production methods, goods and pops, history and map, localisation, interface, graphics and audio, and debugging references live in the `vic3-modding` skill; Europa Universalis V mod packaging, top-folder and override semantics, scripting, events and on actions, actions and interactions, setup and history, map and terrain, countries and politics, economy and pops, content definitions, interface, localisation and graphics, and debugging references live in the `eu5-modding` skill; Old World mod directory and profile, Infos XML add/change/append semantics, event stories and text, custom units and assets, DLL entry points, mod.io publishing, and console and debugging references live in the `old-world-modding` skill; Total War: Rome Remastered mod packaging, manifest and override semantics, scripting, units and models, buildings and factions, campaign data and map, interface, audio and localisation, and debugging references live in the `tw-rome-remastered-modding` skill. C# enumeration-class conventions live in the `csharp-enumerations` skill, C# architecture and fitness test conventions live in the `csharp-architecture-testing` skill, and C# NuGet package usage and versioned package-documentation lookup live in the `csharp-nuget-usage` skill. Java security rules live in `instructions/java/java.security.instructions.md`, and the remaining Java rules live in the `java-code-quality` skill. JavaScript security rules live in `instructions/javascript/javascript.security.instructions.md`, and the remaining JavaScript rules live in the `javascript-code-quality` skill. Kotlin security rules live in `instructions/kotlin/kotlin.security.instructions.md`, and the remaining Kotlin rules live in the `kotlin-code-quality` skill. Python security rules live in `instructions/python/python.security.instructions.md`, and the remaining Python rules live in the `python-code-quality` skill. GitHub Actions security rules live in `instructions/gh-actions/gh-actions.security.instructions.md`, and the remaining GitHub Actions rules live in the `gh-actions-code-quality` skill. Shell security rules live in `instructions/shell/shell.security.instructions.md`, and the remaining Shell rules live in the `shell-code-quality` skill. XML security rules live in `instructions/xml/xml.security.instructions.md`, and the remaining XML rules live in the `xml-code-quality` skill. HTML security rules live in `instructions/html/html.security.instructions.md`, and the remaining HTML rules live in the `html-code-quality` skill.

Boundary rules:
- Each instruction file must define a narrow `applyTo` glob and a semantic description; only always-on safeguards (instruction sources, alphabetical order, privacy and security, evidence and documentation principles, Git safety, response style, test values, and the local work directory) and the language instructions may use a global `applyTo` pattern, because they govern every file type. Instruction files that govern skill authoring, such as `instructions/common/common.skills.instructions.md`, apply to skill files.
- Instruction files must not reference external services or expose secrets, personal data, or system-specific details such as absolute home paths, usernames, hostnames, private addresses, or internal names; they use placeholders, environment variables, and reserved example values instead.

### Skills

Paths:
- `skills/`

Responsibilities:
- Provide on-demand procedures for context, baseline checks, failure triage, review, instruction audits, investigation, phase separation for non-trivial work, data pre-aggregation, structured data, secrets management assessment, leak prevention, secure code review, prompt injection assessment, agent security assessment, API security assessment, pipeline security assessment, supply chain security assessment, user interface design review, MethodScript conventions and API references, Imperator: Rome modding conventions and references, Stellaris modding conventions and references, Crusader Kings II modding conventions and references, Crusader Kings III modding conventions and references, Civilization IV modding conventions and references, Civilization V modding conventions and references, Civilization VI modding conventions and references, Civilization: Beyond Earth modding conventions and references, Victoria 3 modding conventions and references, Europa Universalis V modding conventions and references, test suite auditing, manual QA acceptance criteria, project-local verification skill generation, agent instruction coaching, commit-series composition, agent regression evaluation, migration planning, performance profiling, interface localisation, memory-store engineering, skill security auditing, validation, GitHub Actions workflow templates, GitHub markdown template fidelity, Steam Workshop page description templates, repository documentation generation, and token-efficient workflows. C# enumeration-class conventions, C# architecture and fitness test conventions, C# NuGet package usage, Java code quality, JavaScript code quality, Kotlin code quality, Python code quality, GitHub Actions code quality, Shell code quality, XML code quality, and HTML code quality are likewise provided on demand.
- Support task-based discovery through concise descriptions.
- Bundle the GitHub document templates, rules, fidelity contract, and validator under `skills/github-md-template-fidelity/` so they load only for document generation tasks.
- Bundle the canonical GitHub Actions workflow templates, rules, fidelity contract, and validator under `skills/github-actions-workflow/` so they load only for workflow tasks.
- Bundle the Steam Workshop description BBCode template, rules, fidelity contract, and validator under `skills/steam-workshop-page/` so they load only for Workshop page description tasks. The template fixes the header and donate-banner blocks, holds the mandatory About, Capabilities, Installation with a manual sub-section, Support, Project Engagement, and License prose directly so that only placeholders, repeatable lines, and conditional blocks change, and carries the conditional Contributing and Related Mods blocks, with FAQ and troubleshooting folded into Support and the language list and game name and version folded into Compatibility, and the store-badge block with at most three badges per line, balanced evenly across lines; the generated description is written to `description/steam-workshop.bbcode`.
- Bundle the shared test fixture values under `skills/test-values/` so they load only for test and test-data work, while the always-on `common.test-values.instructions.md` requires the skill for every language and technology.
- Bundle the test suite gardening procedure under `skills/test-audit/` so it loads only for test audits, test pruning, duplicate coverage, and continuous-integration test cost work, complementing the authoring guidance held by `test-design`.
- Bundle the manual QA acceptance criteria and validation plan procedure under `skills/qa-acceptance/` so it loads only for feature-level acceptance, release candidate smoke passes, and incident regression verification work.
- Bundle the project-local verification skill generator under `skills/create-verification-skill/` so it loads only when a repository lacks a scripted way to drive its application and capture behavioural evidence.
- Bundle the evidence-backed agent instruction coaching procedure under `skills/agent-instruction-coaching/` so it loads only when a proposal must refine another agent's instructions, skills, or tool descriptions behind a reviewed-diff gate.
- Bundle the English and Romanian vocabulary preferences under `skills/english-language/` and `skills/romanian-language/` so they load only for language, terminology, and localisation work, while the `instructions/language/` instruction files require the corresponding skill, apply automatically to every file through a global `applyTo` pattern, mandate complete rather than partial application of the dictionary, and extend it to identifiers, literals, comments, messages, and test data inside code.
- Bundle the MethodScript architecture and style rules, plus a reference for every built-in function and bindable event, under `skills/methodscript/` so they load only for CommandHelper script work, while the `instructions/methodscript/` instruction files require the skill.
- Bundle the C# enumeration-class placement, selection, and canonical template procedure under `skills/csharp-enumerations/` so it loads only for enumeration work, while `instructions/csharp/csharp.enumerations.instructions.md` requires the skill.
- The [C# coding instructions](instructions/csharp/csharp.coding.instructions.md) retain universal invariants and explicit activation conditions for [csharp-code-quality](skills/csharp-code-quality/SKILL.md). Its specialised allocation, numeric-contract, binding, and diagnostic rules apply even without analyser warnings; direct file reading supports hosts without skill invocation. The [C# architecture-testing skill](skills/csharp-architecture-testing/SKILL.md) references both sources, preserving their conditions and compatibility exceptions. One directive per C# rule resides in topic references under `skills/csharp-code-quality/references/` and, for security rules, in `instructions/csharp/csharp.security.instructions.md`, so the rule catalogue loads by topic rather than on every C# edit.
- Bundle one directive per Java quality and reliability rule in topic references under `skills/java-code-quality/references/`, indexed by [java-code-quality](skills/java-code-quality/SKILL.md) with its precedence notes and thresholds, while one directive per Java security rule resides in `instructions/java/java.security.instructions.md`, which applies to every Java source file, so the rule catalogue loads by topic rather than on every Java edit.
- Bundle one directive per JavaScript quality and reliability rule in topic references under `skills/javascript-code-quality/references/`, indexed by [javascript-code-quality](skills/javascript-code-quality/SKILL.md) with its precedence notes and thresholds, while one directive per JavaScript security rule resides in `instructions/javascript/javascript.security.instructions.md`, which applies to every JavaScript source file, so the rule catalogue loads by topic rather than on every JavaScript edit.
- Bundle one directive per Kotlin quality and reliability rule in topic references under `skills/kotlin-code-quality/references/`, indexed by [kotlin-code-quality](skills/kotlin-code-quality/SKILL.md) with its precedence notes and thresholds, while one directive per Kotlin security rule resides in `instructions/kotlin/kotlin.security.instructions.md`, which applies to every Kotlin source and script file, so the rule catalogue loads by topic rather than on every Kotlin edit.
- Bundle one directive per Python quality and reliability rule in topic references under `skills/python-code-quality/references/`, indexed by [python-code-quality](skills/python-code-quality/SKILL.md) with its precedence notes and thresholds, while one directive per Python security rule resides in `instructions/python/python.security.instructions.md`, which applies to every Python source file, so the rule catalogue loads by topic rather than on every Python edit; `instructions/python/python.coding.instructions.md` requires the skill.
- Bundle one directive per GitHub Actions quality and reliability rule in topic references under `skills/gh-actions-code-quality/references/`, indexed by [gh-actions-code-quality](skills/gh-actions-code-quality/SKILL.md) with its precedence notes and thresholds, while one directive per GitHub Actions security rule resides in `instructions/gh-actions/gh-actions.security.instructions.md`, which applies to every workflow and action metadata file, so the rule catalogue loads by topic rather than on every workflow edit.
- Bundle one directive per Shell quality and reliability rule in topic references under `skills/shell-code-quality/references/`, indexed by [shell-code-quality](skills/shell-code-quality/SKILL.md) with its precedence notes and thresholds, while one directive per Shell security rule resides in `instructions/shell/shell.security.instructions.md`, which applies to every shell script, so the rule catalogue loads by topic rather than on every shell script edit; `instructions/shell/shell.coding.instructions.md` requires the skill.
- Bundle one directive per XML quality and reliability rule in topic references under `skills/xml-code-quality/references/`, indexed by [xml-code-quality](skills/xml-code-quality/SKILL.md) with its precedence notes and thresholds, while one directive per XML security rule resides in `instructions/xml/xml.security.instructions.md`, which applies to every XML file, so the rule catalogue loads by topic rather than on every XML edit.
- Bundle one directive per HTML quality and reliability rule in topic references under `skills/html-code-quality/references/`, indexed by [html-code-quality](skills/html-code-quality/SKILL.md) with its precedence notes and thresholds, while one directive per HTML security rule resides in `instructions/html/html.security.instructions.md`, which applies to every HTML file, so the rule catalogue loads by topic rather than on every HTML edit.
- Bundle the C# architecture and fitness test procedure, including the ArchUnit.NET dependency rules, the Roslyn source and semantic convention checks, the layer dependency matrix, and the per-instruction enforcement catalogue, under `skills/csharp-architecture-testing/` so it loads only for architecture and fitness test work, while `instructions/csharp/testing/csharp.testing.architecture.instructions.md` requires the skill.
- Bundle the `hmlendea` NuGet package versioned documentation lookup procedure, the prohibition on investigating by decompilation, and the `NuciWeb.HTTP` networking requirements under `skills/csharp-nuget-usage/` so it loads only when such a package is used, while `instructions/csharp/csharp.nuget.usage.instructions.md` requires the skill.
- Bundle the Imperator: Rome mod packaging, scripting, event and decision, setup and entity, localisation, GUI, map and world, and console and debugging procedures under `skills/imperator-rome-modding/` so they load only for Imperator: Rome mod work.
- Bundle the Stellaris mod packaging, merge and load-order semantics, scripting, dynamic scripting, event and on action, economy and planet, empire and content, localisation, interface, map and defines, and console and debugging procedures under `skills/stellaris-modding/` so they load only for Stellaris mod work.
- Bundle the Crusader Kings II mod packaging, override and load-order semantics, scripting, event, on action and decision, history and setup, common definition, localisation, interface, graphics, portrait, coat of arms, map, music, and console and debugging procedures under `skills/ck2-modding/` so they load only for Crusader Kings II mod work.
- Bundle the Crusader Kings III mod packaging, override and load-order semantics, scripting, event and on action, decision and interaction, history and character, common definition, localisation, interface, graphics, coat of arms, map and terrain, audio, and console and debugging procedures under `skills/ck3-modding/` so they load only for Crusader Kings III mod work.
- Bundle the Civilization IV mod folder and ini configuration, modular loading, XML table and schema, content definition, Python scripting, interface and font art, WorldBuilder and map script, SDK and C++, and debugging procedures under `skills/civ4-modding/` so they load only for Civilization IV mod work.
- Bundle the Civilization V ModBuddy action and VFS wiring, XML/SQL database update, content definition, Lua scripting, UI and art, localisation, and console and debugging procedures under `skills/civ5-modding/` so they load only for Civilization V mod work.
- Bundle the Civilization VI ModBuddy action and criteria wiring, SQL and GameData update, content definition, modifier and requirement composition, Lua scripting, UI, icon and art handling, localisation, and debugging procedures under `skills/civ6-modding/` so they load only for Civilization VI mod work.
- Bundle the Civilization: Beyond Earth ModBuddy action and VFS wiring, XML/SQL database update, sponsor, colonist, cargo, spacecraft, unit, technology, affinity, virtue, quest, artifact, marvel, covert operation, orbital unit, biome, improvement, and resource content definition, Lua scripting, UI and art, localisation, and console and debugging procedures under `skills/civbe-modding/` so they load only for Civilization: Beyond Earth mod work.
- Bundle the Victoria 3 metadata and override semantics, scripting, event and on action, politics and diplomacy, building and production method, goods and pop, history and map, localisation, interface, graphics and audio, and console and debugging procedures under `skills/vic3-modding/` so they load only for Victoria 3 mod work.
- Bundle the Europa Universalis V metadata and override semantics, scripting, event and on action, action and interaction, setup and history, map and terrain, country and politics, economy and pop, content definition, interface, localisation and graphics, and console and debugging procedures under `skills/eu5-modding/` so they load only for Europa Universalis V mod work.
- Bundle the Old World mod directory and profile, Infos XML add/change/append semantics, event stories and text, custom units and assets, DLL entry points, mod.io publishing, and console and debugging procedures under `skills/old-world-modding/` so they load only for Old World mod work.
- Bundle the Total War: Rome Remastered mod descriptor and manifest, override semantics, scripting, unit and model, building and faction, campaign and map, interface, audio and localisation, and console and debugging procedures under `skills/tw-rome-remastered-modding/` so they load only for Rome Remastered mod work.
- Bundle the OWASP and NIST SP 800-57 secrets management assessment procedure under `skills/secrets-management/` so it loads only for secret handling, credential exposure, and rotation policy work.
- Bundle the leak-prevention procedure, covering local-identity scanning, detection patterns, agent configuration scanning, false-positive classification, remediation by exposure stage, and redacted reporting, under `skills/leak-prevention/` so it loads before a file-changing task finishes and before any commit or publication, while `instructions/common/common.security.instructions.md` requires it.
- Bundle the OWASP ASVS 4.0.3 and CWE Top 25 secure code review procedure under `skills/secure-code-review/` so it loads only for security-focused reviews of code, pull requests, diffs, and modules.
- Bundle the OWASP LLM01:2025 and MITRE ATLAS AML.T0051 prompt injection assessment procedure under `skills/prompt-injection/` so it loads only for LLM interaction surface, injection vector, and defence review work.
- Bundle the OWASP Agentic AI threat and NIST AI RMF 1.0 agent architecture security assessment procedure under `skills/agent-security/` so it loads only for agent permission model, human-in-the-loop gate, blast radius, audit trail, rollback, and multi-agent trust review work.
- Bundle the OWASP API Security Top 10:2023 API review procedure, its per-category checklist, and its C# and .NET supplement under `skills/api-security/` so they load only for REST, GraphQL, gRPC, and hybrid API specification, endpoint, and gateway review work.
- Bundle the SLSA v1.0 build level and OWASP Top 10 CI/CD Security Risks pipeline assessment procedure under `skills/pipeline-security/` so it loads only for CI/CD configuration, build provenance, and supply chain security work.
- Bundle the dependency inventory, SBOM and VEX validation, licence compliance, typosquatting, and CVSS 4.0, EPSS, SSVC 2.1, and CISA KEV triage procedure under `skills/supply-chain-security/` so it loads only for dependency, SBOM, VEX, licence, and CVE remediation work.
- Bundle the prioritised interface rule set, the native and mobile pre-delivery checklist, and the Playwright audit script under `skills/ui-design-review/` so they load only for interface design, review, and repair work; the audit script is the only skill asset that executes a browser, and it mutates nothing outside its output directory.
- Bundle the three-phase investigation, planning, and implementation workflow under `skills/research-plan-implement/` so it loads only for non-trivial capabilities and changes, and so each phase consumes a durable `PLAN.md` artefact in a fresh session rather than accumulated transcript context.
- Bundle the data pre-aggregation procedure under `skills/pre-aggregate-data/` so it loads only when an assignment necessitates API, repository, or command data, and so trimmed results are retrieved into `.work/data/` files during a preliminary step rather than round-tripping unprocessed payloads through the model.
- Bundle the local work directory procedure, covering consultation of existing entries at task start, Git exclusion through `.git/info/exclude` rather than a tracked ignore file, the directory layout and entry format with recorded sources, freshness verification, and the check that no tracked artefact mentions the directory, under `skills/work-directory/`, while the always-on `instructions/common/common.work-directory.instructions.md` requires it; the `session-handoff` and `pre-aggregate-data` procedures store their artefacts there.
- Bundle the exhaustive repository-documentation procedure and the `docs/` structure contract under `skills/repository-documentation/` so deep reverse-engineering guidance loads only when repository documentation is requested.
- Bundle the pull request observation procedure under `skills/pr-babysit/` so it loads only for monitoring a pull request or review cycle to merge readiness, verifying each finding before correction and resolving a review thread only after the code addresses it.
- Bundle the commit-series composition procedure and its staged-secret gate under `skills/commit-craft/` so they load only when a mixed working tree must become reviewable commits or a series must be verified before pushing.
- Bundle the agent, prompt, model, and tool regression evaluation procedure under `skills/agent-regression-evals/` so it loads only when a modification requires repeated trials, trajectory grading, flake quarantine, and paired comparison against a baseline.
- Bundle the phased migration planning, compatibility determination, and per-phase rollback procedure under `skills/migration-architect/` so it loads only when a live schema, database, service, or host requires modification or cut-over.
- Bundle the measured-baseline performance profiling procedure under `skills/performance-profiler/` so it loads only for a slow endpoint, memory growth, elevated processor usage, an oversized bundle, or a performance budget.
- Bundle the interface localisation verification procedure under `skills/i18n-localization/` so it loads only when interface text is added, a locale is added or shipped, translation files are reviewed, or localisation must be built into an application.
- Bundle the memory-system selection, pricing, and forgetting-policy procedure under `skills/memory-engineering/` so it loads only prior to adding memory to an agent or when a memory store grows without eviction.

- Bundle the untrusted skill, plug-in, hook, and agent-definition security audit procedure under `skills/skill-security-auditor/` so it loads only when content from an untrusted source requires inspection prior to installation.
- Bundle the post-release verification procedure under `skills/release-verification/` so it loads only after a release, publication, or deployment, covering release identity, per-surface artefact evidence, finding classification, observation cadence, and partial-verification reporting.
- When skills modify code, dependencies, or project structure, they must trigger documentation updates for relevant repository files (README.md, SECURITY.md, ARCHITECTURE.md, docs/, or any other project-specific documentation files).

Boundary rules:
- Each skill must be self-contained with a clear procedure.
- Skills must not execute arbitrary code outside the repository context.
- The `name` in a skill's YAML frontmatter must equal its directory name, and the single-line double-quoted `description` must be at most 1024 characters, which is the host's hard load limit; `instructions/common/common.skills.instructions.md` holds the contract, the measurement procedure, and the enforcement step in `verification.yml`.

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
| Continuous verification | `verification.yml` workflow | The repository's own content contracts are re-checked on every push and pull request rather than asserted |

## ✅ Testing and Verification

The repository contains no executable tests. The `hooks/` directory includes a test file (`litellm-instruction-gate.test.cjs`) that validates the instruction-gate hook. The `skills/github-md-template-fidelity/` directory includes a validation script (`validate_github_md.py`) that checks template fidelity for generated GitHub markdown files in personal repositories owned by the current git user; `--force` asserts an explicit template request and bypasses the ownership scope. The `skills/github-actions-workflow/` directory includes a validation script (`validate_github_actions.py`) that checks template fidelity for generated GitHub Actions workflows under the same ownership scope, with `--force` asserting an explicit template request. The `skills/steam-workshop-page/` directory includes a validation script (`validate_steam_workshop_page.py`) that checks the fixed header and donate-banner blocks, the Steam link-filter wrapper, the BBCode-only constraint, placeholder clearance, and BBCode tag balance for generated Workshop page descriptions. The `.github/workflows/verification.yml` workflow executes the hook tests, checks the hook and validator scripts for syntax errors, validates every governed GitHub document against its template, and parses every workflow file; it sets the `--force` environment equivalents because the repository is a personal repository owned by the current git user. The `skills/ui-design-review/` directory includes a heuristic audit script (`design-audit.mjs`) that requires Playwright and exits with status 2 when high-severity findings exist.

Execute the principal automated verification with:

```bash
python3 skills/github-md-template-fidelity/validate_github_md.py . README.md README.md
python3 skills/github-actions-workflow/validate_github_actions.py . dotnet.yml .github/workflows/dotnet.yml
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
