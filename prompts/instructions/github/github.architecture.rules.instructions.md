---
description: "Use when the user requests revision, creation, or generation of an ARCHITECTURE.md. Auto-invoked by requests such as 'revise the architecture document', 'create an architecture document', 'document the architecture', or 'generate ARCHITECTURE.md'. Derives verified boundaries, runtime flows, ownership, dependencies, constraints, and extension points from repository evidence while applying the standard structure and conditional sections."
applyTo: "ARCHITECTURE.md"
---

Generate or revise the `ARCHITECTURE.md` for this GitHub repository using the `github.architecture.template.instructions.md` template.

## Strict Template Fidelity Mode (Default)

This mode applies automatically when the user requests any of the subsequent:
- Revise the architecture document
- Create the ARCHITECTURE.md file
- Create an architecture document
- Document the architecture
- Generate the architecture document
- Compose the architecture document

### Precedence

- These rules supersede all other ARCHITECTURE generation instructions.
- If another rule conflicts with strict fidelity, strict fidelity prevails.

### Current-State Evidence Contract

Unless the user explicitly requests a target architecture, document the verified current architecture rather than a proposed or idealised design.

- Inspect the principal entry points, composition roots, project manifests, configuration, public contracts, persistence adapters, integration boundaries, tests, and deployment artefacts relevant to the documented system.
- Ground every material statement in repository evidence. Do not infer a technology, boundary, dependency, lifetime, protocol, data flow, or operational guarantee solely from naming conventions.
- Distinguish implemented guarantees from intentions, recommendations, and absent coverage.
- Record consequential uncertainty as a constraint or verification gap rather than presenting speculation as fact.
- Never expose secrets, personal data, private endpoint credentials, or sensitive configuration values. Document the configuration contract and secret source instead.
- If both current and target architectures are requested, label them explicitly and include a migration section that separates present facts from proposed changes.

### Generation Contract

1. Commence from an exact copy of `github.architecture.template.instructions.md`, preserving the order of all included template-defined sections, headings, punctuation, and whitespace layout.
2. Replace scalar `[[PLACEHOLDER]]` tokens and block `[[[PLACEHOLDER]]]` tokens with repository-specific content.
3. Resolve template-marked conditional blocks in accordance with the Conditional Content Rules. Removing an inapplicable conditional block is permitted; removing a mandatory section is prohibited.
4. Duplicate or remove repeatable placeholder rows, bullets, subsections, and diagram elements in accordance with repository evidence.
5. Do not rephrase fixed template text outside placeholders, except when a conditional block is removed in its entirety.
6. Additional project-specific sections or subsections are permitted when they document material domain mechanics, ownership rules, caches, compatibility contracts, or operational concerns absent from the standard sections.
7. Preserve accurate, current project-specific content from an existing ARCHITECTURE.md. Position it beneath the nearest standard section or retain it as an additive section; do not discard it solely because the template lacks an identical heading.
8. Preserve deliberate architecture terminology used by the repository, including layer, component, module, service, adapter, facade, pipeline, host, and domain names.
9. Use repository-relative links for source references, and verify that every referenced path exists.
10. Remove all template comments and unresolved placeholders from the final document.

### Failure Conduct

- If the principal system boundary, runtime entry point, or requested current-versus-target scope remains indeterminate after focused repository inspection, cease generation and request one concise clarification.
- Do not produce a partial or speculative architecture document.

### Mandatory Validation Before Final Output

- Mandatory headings are present in template order.
- The title identifies the project and the document as architecture documentation.
- The system context defines the system boundary, actors, external systems, data stores, and trust boundaries that are material to the repository.
- Runtime flow, component ownership, and dependency direction are mutually consistent.
- At least one of `Components` or `Architectural Areas` is included.
- Every diagram agrees with the surrounding prose and uses valid Mermaid syntax.
- Conditional and additional sections are supported by repository evidence.
- Existing accurate project-specific material has not been omitted.
- Source paths and local document links resolve within the repository.
- Commands in `Testing and Verification` correspond to real project commands or scripts.
- No unsupported claims, template comments, example rows, or unresolved placeholders remain.
- The Table of Contents contains every final `##`, `###`, and `####` heading in order and links to the correct anchors.

If an `ARCHITECTURE.md` previously exists, preserve content that remains accurate and current, and revise only material that is obsolete, incomplete, or structurally inconsistent. If no `ARCHITECTURE.md` exists, derive it from repository evidence.

## Mandatory Editing Rules

When revising an existing ARCHITECTURE.md:
- Never delete ARCHITECTURE.md.
- Never use `*** Delete File`.
- Never recreate ARCHITECTURE.md with `create_file`.
- Modify the existing file only with `apply_patch` using `*** Update File`.
- A complete revision must still use `*** Update File`.
- Preserve the file path and file identity throughout the operation.
- If an in-place patch cannot be produced, cease and explain the impediment instead of deleting the file.

## Conditional Content Rules

### Sections

Include sections in accordance with the subsequent conditions:

| Section | Condition | Notes |
|---------|-----------|-------|
| Table of Contents | Always include. | Include all `##`, `###`, and `####` headings in order. |
| Purpose | Always include. | Define document scope, system responsibility, audience, and current or target status. |
| System Context | Always include. | Identify material actors, external systems, stores, outputs, and trust boundaries. |
| Architectural Style | Always include. | Name only styles demonstrated by the implementation and explain their consequences. |
| Runtime Flow | Always include. | Describe process startup and the principal ordered execution path. |
| Components | A finite catalogue of runtime services, modules, adapters, or collaborators clarifies responsibility. | Include responsibility, dependencies, and lifetime or ownership where verified. |
| Architectural Areas | Directory, layer, subsystem, or ownership boundaries provide more clarity than a component catalogue. | Include paths, responsibilities, and boundary rules. At least one of Components or Architectural Areas is mandatory. |
| Data Architecture | The system owns, transforms, caches, transmits, or persists meaningful state. | Describe models, mappings, stores, ownership, lifecycle, consistency, and migration where relevant. |
| Interfaces and Integrations | Public APIs, protocols, command interfaces, remote providers, devices, or external systems exist. | Record direction, contract, ownership, and failure semantics. |
| Key Flows | Multiple requests, commands, jobs, or domain workflows merit detail beyond Runtime Flow. | Use one subsection per flow and include sequence diagrams where they improve precision. |
| Domain-Specific Concerns | Material mechanics do not fit a standard section. | Examples include matching, rendering, caching, packet framing, authorisation, or compatibility facades. Use precise project terminology. |
| Cross-Cutting Concerns | Security, privacy, error handling, observability, configuration, localisation, concurrency, or resource management has architectural impact. | Include only relevant subsections and omit filler. |
| Dependency Direction and Rules | Always include. | State permitted dependency direction, ownership rules, and prohibited coupling. |
| External Dependencies | Third-party frameworks, packages, services, or data sources have architectural responsibility. | Include principal dependencies only, not a complete package inventory. |
| Deployment and Operations | Always include. | State process topology, deployment model, persistent state, scaling assumptions, and operational consequences. |
| Compatibility Contracts | Public APIs, serialised data, protocols, lifecycle order, assets, or legacy facades must remain compatible. | State the owner, invariant, verification method, and change policy. |
| Testing and Verification | Always include. | Record test boundaries, executable verification, manual checks, and material coverage gaps or prohibitions. |
| Design Constraints | Always include. | Describe current trade-offs, capacity limits, invariants, and deliberately excluded architecture. |
| Extension Points | Stable interfaces or composition boundaries intentionally support substitute implementations or additional capabilities. | Explain the required contract and registration or integration location. |
| Evolution and Migration | A target architecture, active transition, deprecated boundary, or migration sequence exists. | Separate current facts, target state, transition phases, and compatibility requirements. |
| Architecture Decisions | Architecture Decision Records or consequential design decisions exist. | Link ADRs when present; otherwise record only decisions that repository evidence can substantiate. |
| Source Map | The repository contains multiple projects, non-obvious directories, or dispersed architecture entry points. | Map areas to repository-relative paths without duplicating a complete directory tree. |
| Related Documentation | Complementary repository documentation defines security, migration, planning, protocols, operations, or detailed component design. | Link only documents that exist and state their distinct scope. |

### Architecture Profiles

Use the applicable profile to select conditional sections and project-specific detail. A repository may combine profiles:

| Profile | Emphasise | Usually Omit Unless Relevant |
|---------|-----------|------------------------------|
| HTTP service or modular monolith | system context, transport boundary, request flows, application services, persistence, authorisation, error translation, configuration, and observability | desktop lifecycle, rendering, and packet bytes |
| Console or scheduled batch pipeline | process lifecycle, pipeline stages, input and output data, matching or transformation, caching, concurrency, degradation, and exit semantics | API routes, request middleware, and interactive presentation |
| Desktop, game, or compatibility-sensitive client | lifecycle order, presentation, session state, protocol, loaders, renderers, compatibility facades, immutable contracts, and specialised verification | server scaling and REST request flows |
| Library or SDK | public contracts, internal modules, dependency direction, versioning, and extension points | process hosting and operator workflows |
| Plugin, mod, or extension | host boundary, lifecycle hooks, host APIs, owned state, compatibility range, and packaging | independent process topology and unrelated persistence |

Profiles guide emphasis only. They do not authorise unsupported claims or omission of mandatory sections.

### Content Rules

- Define the system boundary before describing internal components.
- Describe ownership and responsibility before implementation detail.
- State process and service lifetimes when they influence concurrency, state, disposal, or scaling.
- Identify synchronous, asynchronous, parallel, queued, and scheduled transitions precisely.
- Describe data at its architectural boundaries: origin, owner, representation, transformation, persistence, retention, and consistency.
- State trust boundaries, authorisation, secret injection, and sensitive-data handling when relevant.
- Describe failure translation, degradation, retries, fallbacks, and process-level termination at the boundary that owns them.
- State permitted dependency direction and consequential prohibited dependencies explicitly.
- Treat reflection conventions, numeric identifiers, serialised bytes, route shapes, event order, and public facade signatures as contracts when the implementation depends upon them.
- Explain trade-offs and limitations without presenting hypothetical replacements as implemented architecture.
- Prefer diagrams for topology and interaction; prefer tables for catalogues and contracts; prefer prose for rationale and constraints.
- Keep diagrams focused. Split a dense diagram by concern rather than creating an unreadable complete-system graph.
- Do not duplicate installation, usage, or contribution guidance from README.md unless it has direct architectural significance.
- Do not describe every class or file. Concentrate upon boundaries, ownership, interactions, and change-sensitive contracts.

### Always Include

- A concise scope statement beneath the title.
- `## 🎯 Purpose`.
- `## 🌐 System Context` with a Mermaid context diagram.
- `## 🏗️ Architectural Style`.
- `## 🔄 Runtime Flow` with a Mermaid flow or sequence diagram.
- At least one of `## 🧩 Components` or `## 🗂️ Architectural Areas`.
- `## 🧭 Dependency Direction and Rules`.
- `## 🚀 Deployment and Operations`.
- `## ✅ Testing and Verification`.
- `## ⚠️ Design Constraints`.

## Styling and Format Rules

- Respect the active language instructions for all ARCHITECTURE text, including spelling and phrasing conventions.
- Prefix every `##` heading with the emoji demonstrated in the template. Prefix additive project-specific `##` headings with one semantically appropriate emoji.
- Do not include heading emojis in Table of Contents labels, anchors, or links.
- Use title case for every heading.
- Use Mermaid for architecture diagrams; do not use ASCII art when Mermaid can express the relationship more precisely.
- Label diagram edges when the transported data, command, protocol, or direction is not self-evident.
- Use repository-relative Markdown links for files and directories.
- Remove all HTML comments from the final output.
- Replace every placeholder with verified project detail, and remove example rows or subsections that do not apply.
- Maintain concise prose, but include sufficient detail for a contributor to locate ownership, follow a runtime flow, and evaluate the impact of a change.