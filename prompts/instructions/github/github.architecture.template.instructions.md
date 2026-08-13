---
description: "Use when the user requests revision, creation, or generation of an ARCHITECTURE.md. Auto-invoked by requests such as 'revise the architecture document', 'create an architecture document', 'document the architecture', or 'generate ARCHITECTURE.md'. Provides the standard evidence-based structure for system context, runtime flows, ownership, dependencies, constraints, and extension points."
applyTo: "ARCHITECTURE.md"
---
This is the `ARCHITECTURE.md` template that shall be utilised.
---

<!-- BEGIN ARCHITECTURE TEMPLATE IMMUTABLE -->

# [[Project Title]] Architecture

[[[State what this document covers, whether it describes the current or target architecture, and any relevant scope boundary.]]]

## 📑 Table of Contents

<!-- Generate one entry per ##/###/#### heading present in the final output, in order. Do not include emojis here. -->

## 🎯 Purpose

[[[Describe the system's principal responsibility, architectural scope, intended audience, and the value of recording these boundaries.]]]

## 🌐 System Context

[[[Describe the system boundary, initiating actors, external systems, persistent stores, outputs, and material trust boundaries.]]]

```mermaid
[[[Define a focused context flowchart with the documented system as one boundary and every material external interaction labelled.]]]
```

The principal external boundaries are:
- **[[Boundary Name]]:** [[Interaction, exchanged information, and ownership]]
<!-- Repeat the preceding item for each material boundary. -->

## 🏗️ Architectural Style

[[[Name the verified architectural style or combination of styles, explain how the repository implements it, and state the principal consequences for ownership and change.]]]

```mermaid
[[[Define a component, container, layer, or pipeline diagram that demonstrates the principal internal relationships.]]]
```

The principal architecture boundaries are:
- **[[Boundary or Layer Name]]:** [[Responsibility and permitted dependencies]]
<!-- Repeat the preceding item for each principal boundary. -->

## 🔄 Runtime Flow

```mermaid
[[[Define a flowchart or sequence diagram for startup and the principal execution path.]]]
```

The principal runtime sequence is:
1. [[Initialisation or initiating event]]
2. [[Principal orchestration step]]
3. [[Result, persistence, response, or shutdown step]]
<!-- Add, combine, or remove numbered steps in accordance with the verified runtime. -->

<!-- Include when a finite component catalogue clarifies runtime responsibility. -->
## 🧩 Components

| Component | Responsibility | Principal Dependencies | Lifetime or Ownership |
|-----------|----------------|------------------------|-----------------------|
| `[[Component Name]]` | [[Responsibility]] | [[Principal dependencies]] | [[Lifetime or owner]] |
<!-- Repeat the preceding row for each principal component. -->

<!-- Include when directory, layer, subsystem, or ownership boundaries provide more clarity than a component catalogue. -->
## 🗂️ Architectural Areas

### [[Area Name]]

Paths:
- `[[repository/relative/path]]`
<!-- Repeat the preceding item for each path owned by this area. -->

Responsibilities:
- [[Responsibility]]
<!-- Repeat the preceding item for each responsibility. -->

Boundary rules:
- [[Permitted dependency, prohibited dependency, invariant, or ownership rule]]
<!-- Repeat the preceding item for each rule. Repeat the complete subsection for each area. -->

<!-- Include when the system owns, transforms, caches, transmits, or persists meaningful state. -->
## 💾 Data Architecture

[[[Describe data ownership, representations, transformations, persistence, cache policy, consistency, retention, and migrations that are relevant to the architecture.]]]

```mermaid
[[[Define a data-flow or state-ownership diagram from source through transformation to persistence or output.]]]
```

| Data or Store | Owner | Representation and Storage | Lifecycle or Consistency |
|---------------|-------|----------------------------|--------------------------|
| `[[Data Model or Store]]` | [[Owning component]] | [[Representation and location]] | [[Creation, mutation, retention, consistency, or expiry]] |
<!-- Repeat the preceding row for each principal model, store, or cache. -->

<!-- Include when public APIs, protocols, command interfaces, remote providers, devices, or other integrations exist. -->
## 🔌 Interfaces and Integrations

| Interface or Integration | Direction | Contract | Owner | Failure Semantics |
|--------------------------|-----------|----------|-------|-------------------|
| `[[Interface Name]]` | [[Inbound / Outbound / Bidirectional]] | [[Protocol, route, command, format, or version]] | [[Owning component]] | [[Translation, retry, fallback, or termination]] |
<!-- Repeat the preceding row for each material interface or integration. -->

<!-- Include when multiple requests, commands, jobs, or domain workflows merit detail beyond Runtime Flow. -->
## 🔀 Key Flows

### [[Flow Name]]

```mermaid
[[[Define a sequence diagram for this flow, including boundary validation, state mutation, persistence, and failure translation where relevant.]]]
```

[[[Explain ordering, ownership, invariants, and consequential alternatives or failure paths for this flow.]]]

<!-- Repeat the complete subsection for each principal flow. -->

<!-- Include repeatable project-specific sections when material domain mechanics do not fit a standard section. -->
## ⚙️ [[Domain-Specific Concern]]

[[[Describe the concern's algorithm, policy, ownership, invariants, state transitions, and architectural consequences.]]]

<!-- Include when one or more cross-cutting concerns have architectural impact. Include only relevant subsections. -->
## 🧵 Cross-Cutting Concerns

<!-- Include when authentication, authorisation, trust boundaries, secrets, untrusted input, or sensitive data are relevant. -->
### Security and Privacy

[[[Describe trust boundaries, authentication, authorisation, input validation, secret injection, sensitive-data handling, and security ownership.]]]

<!-- Include when exceptions, degradation, retries, fallbacks, or process termination have defined ownership. -->
### Error Handling

[[[Describe where failures originate, how they are translated or recorded, which failures permit degradation, and which terminate the operation or process.]]]

<!-- Include when logs, metrics, traces, health checks, diagnostics, or audit events exist. -->
### Observability

[[[Describe emitted signals, their owners, destinations, correlation context, and material diagnostic gaps without exposing sensitive values.]]]

<!-- Include when configuration sources or override precedence influence composition or runtime conduct. -->
### Configuration

| Configuration Area | Source | Responsibility | Override or Secret Policy |
|--------------------|--------|----------------|---------------------------|
| `[[Configuration Area]]` | [[File, environment, command line, service, or device]] | [[Controlled conduct]] | [[Precedence or secret source]] |
<!-- Repeat the preceding row for each principal configuration area. -->

<!-- Include when parallelism, asynchronous execution, shared state, disposal, or resource limits influence the architecture. -->
### Concurrency and Resource Use

[[[Describe concurrency boundaries, shared-state protection, lifetime constraints, resource reuse, backpressure or boundedness, and practical capacity limits.]]]

## 🧭 Dependency Direction and Rules

[[[Describe the permitted dependency direction and identify the abstractions that protect stable boundaries.]]]

```mermaid
[[[Define a dependency diagram when it communicates direction more precisely than prose.]]]
```

The principal dependency rules are:
- [[Permitted dependency or ownership rule]]
- [[Prohibited dependency or coupling]]
<!-- Repeat, combine, or remove rules in accordance with the verified architecture. -->

<!-- Include when third-party frameworks, packages, services, or data sources have architectural responsibility. -->
## 📦 External Dependencies

| Dependency | Responsibility | Integration Boundary | Architectural Consequence |
|------------|----------------|----------------------|---------------------------|
| `[[Dependency Name]]` | [[Responsibility supplied to the system]] | [[Owning adapter or component]] | [[Constraint, coupling, replacement boundary, or operational consequence]] |
<!-- Repeat the preceding row for each principal external dependency. -->

## 🚀 Deployment and Operations

[[[Describe the process or service topology, deployment unit, persistent state, filesystem or network requirements, scaling assumptions, startup and shutdown responsibilities, and operator-visible outputs.]]]

| Concern | Current Design | Architectural Consequence |
|---------|----------------|---------------------------|
| [[Process topology, state, scaling, availability, recovery, or resource concern]] | [[Verified design]] | [[Consequence or operator responsibility]] |
<!-- Repeat the preceding row for each material operational concern. -->

<!-- Include when public APIs, serialised data, protocols, lifecycle order, assets, or legacy facades must remain compatible. -->
## 🛡️ Compatibility Contracts

| Contract | Owner | Invariant | Verification | Change Policy |
|----------|-------|-----------|--------------|---------------|
| `[[Contract Name]]` | [[Owning component]] | [[Value, order, shape, format, or semantics that must remain stable]] | [[Automated or manual verification]] | [[Compatibility requirement or migration policy]] |
<!-- Repeat the preceding row for each compatibility-sensitive contract. -->

## ✅ Testing and Verification

[[[Describe the test projects and levels, the architecture boundaries each verifies, manual or specialised verification, and material coverage gaps or explicit test constraints.]]]

<!-- Include when executable verification commands or repository scripts exist. -->
Execute the principal automated verification with:

```bash
[[verification command]]
```

<!-- Add further commands only when each command verifies a distinct architecture-sensitive contract. -->

## ⚠️ Design Constraints

- **[[Constraint Name]]:** [[Current trade-off, limit, invariant, rationale, and consequence]]
<!-- Repeat the preceding item for each material constraint. -->

<!-- Include when stable interfaces or composition boundaries intentionally support substitute implementations or additional capabilities. -->
## 🔧 Extension Points

### [[Extension Point]]

1. [[Implement or revise the owning contract.]]
2. [[Register or integrate the implementation at the verified composition boundary.]]
3. [[Add the verification required to preserve neighbouring contracts.]]

[[[State any naming, lifetime, protocol, ordering, or compatibility convention that the extension must preserve.]]]

<!-- Repeat the complete subsection for each intentional extension point. -->

<!-- Include when a target architecture, active transition, deprecated boundary, or migration sequence exists. -->
## 🌱 Evolution and Migration

### Current State

[[[Describe only verified present architecture relevant to the transition.]]]

### Target State

[[[Describe the explicitly requested or documented target architecture without presenting it as implemented.]]]

### Transition

1. [[Migration phase, dependency, and validation gate]]
<!-- Repeat the preceding item for each ordered phase. -->

Compatibility requirements:
- [[Contract that must remain stable during migration]]
<!-- Repeat the preceding item for each requirement. -->

<!-- Include when Architecture Decision Records or substantiated consequential design decisions exist. -->
## 📝 Architecture Decisions

| Decision | Rationale | Consequence | Record |
|----------|-----------|-------------|--------|
| [[Decision]] | [[Verified rationale]] | [[Trade-off or constraint]] | [[Repository-relative ADR link, issue, or `Documented here`]] |
<!-- Repeat the preceding row for each consequential decision. -->

<!-- Include when multiple projects, non-obvious directories, or dispersed architecture entry points merit a navigation aid. -->
## 🗺️ Source Map

| Area | Path |
|------|------|
| [[Architecture Area]] | `[[repository/relative/path]]` |
<!-- Repeat the preceding row for each principal source area. -->

<!-- Include when complementary repository documentation defines security, migration, planning, protocols, operations, or detailed component design. -->
## 📚 Related Documentation

[[[List existing complementary documents using repository-relative Markdown links and describe the distinct scope of each document.]]]

<!-- END ARCHITECTURE TEMPLATE IMMUTABLE -->