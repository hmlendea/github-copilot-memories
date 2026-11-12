---
name: repository-documentation
description: "Use when asked to generate, create, write, or refresh the repository documentation or docs/ knowledge base (for example \"Generate the repository documentation\", \"Document this repository\", \"Create the docs\"), or to reconstruct deep repository comprehension for future agents. Performs exhaustive evidence-based reverse engineering and produces the structured docs/ tree (api-reference, behaviour, components, flows, and topic files) defined by this skill."
---

# Repository Documentation Generation

Trigger: any request to generate, create, write, refresh, or complete the repository's documentation, or to build/expand the `docs/` knowledge base. Execute the full procedure below exactly as specified, as though it had been supplied verbatim as the user's instruction.

Companion skill: for the root GitHub documents (`README.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `PRIVACY.md`, `ROADMAP.md`), use the `github-md-template-fidelity` skill. This skill governs the `docs/` tree only.

---

# Do Not Substitute Search For Reasoning

Repository search, symbol search, references, call hierarchies, test discovery, static analysis, and similar facilities are essential investigative instruments.

They do not substitute for reasoning.

Discovering that:

```text
A -> B -> C
```

is insufficient.

Determine:

- why A invokes B;
- why B requires C;
- what contract exists between them;
- what information crosses each boundary;
- what transformations occur;
- what assumptions each component makes;
- what happens when C fails;
- whether alternative paths exist;
- what tests demonstrate those semantics;
- what invariant the complete interaction preserves;
- and what other functionality depends upon the result.

Use tools to acquire evidence.

Use advanced reasoning to convert that evidence into repository comprehension.

------------------------------------------------------------------------

# Do Not Substitute Context Size For Comprehension

Having many files available in context does not mean they have been understood.

Do not perform a broad repository scan, recognise familiar architectural patterns, and generate documentation based principally upon those patterns.

Repository-specific evidence takes precedence over generic software expectations.

For example, do not presume that a class named `Repository` behaves like a conventional repository abstraction.

Inspect it.

Do not presume that an interface represents the genuine architectural boundary.

Trace its implementations and consumers.

Do not presume that tests accurately describe all production behaviour.

Compare them with implementation.

Do not presume that configuration is used merely because it exists.

Trace its consumers.

Do not presume that a method's name completely describes its effects.

Inspect its implementation and downstream calls.

------------------------------------------------------------------------

# Maintain Global And Local Models Simultaneously

During investigation, maintain both:

## Global Repository Model

Understand:

- repository purpose;
- architectural decomposition;
- principal capabilities;
- component relationships;
- dependency direction;
- runtime topology;
- major state;
- major integrations;
- system-wide invariants.

## Local Implementation Model

For the area currently under investigation, understand:

- exact source locations;
- exact symbols;
- call sequences;
- branch conditions;
- data transformations;
- side effects;
- error paths;
- tests;
- configuration;
- state changes.

Continuously reconcile the two.

A local implementation discovery may invalidate an architectural interpretation.

An architectural discovery may reveal that another local process must be investigated.

Revise previous conclusions when necessary.

------------------------------------------------------------------------

# Reason Across Abstraction Boundaries

Do not stop investigation merely because execution crosses:

- an interface;
- dependency injection;
- a repository abstraction;
- an HTTP client;
- middleware;
- a serializer;
- an event;
- a queue;
- a persistence layer;
- a factory;
- a mapper;
- a framework callback;
- a scheduled process;
- or another abstraction boundary.

Follow the behaviour until its meaningful effect is understood.

The documentation exists specifically so future agents do not have to repeat this tracing.

------------------------------------------------------------------------

# Perform Causal Analysis, Not Merely Structural Analysis

For important functionality, determine not merely **what components exist**, but **what causes what**.

The documentation should make relationships such as this comprehensible:

```text
Input
-> validation
-> decision
-> transformation
-> state access
-> external interaction
-> persistence
-> response construction
-> observable result
```

including alternate branches and failures.

When behaviour depends upon previous state, configuration, external responses, ordering, or environmental conditions, document those causal dependencies.

------------------------------------------------------------------------

# Challenge Your Own Interpretation

Do not settle upon the first plausible interpretation of unfamiliar code.

For important architectural or behavioural conclusions:

1. form an interpretation from initial evidence;
2. inspect callers;
3. inspect callees;
4. inspect relevant models;
5. inspect configuration;
6. inspect tests;
7. inspect alternate implementations;
8. inspect related processes;
9. search for contradictory evidence;
10. revise the interpretation if necessary.

Use corroborating evidence where practical.

This is particularly important for:

- business rules;
- implicit invariants;
- lifecycle assumptions;
- error semantics;
- persistence semantics;
- security behaviour;
- concurrency;
- algorithms;
- compatibility requirements.

------------------------------------------------------------------------

# Spend Compute Now To Save Compute Later

The economics of this task are intentionally unusual.

This documentation will be consumed by future coding agents.

Every architectural relationship accurately reconstructed now may prevent repeated repository exploration in numerous future sessions.

Every execution flow accurately documented now may prevent future agents from tracing the same call graph repeatedly.

Every implementation and test location indexed now may eliminate future repository searches.

Every invariant recorded now may prevent an erroneous modification.

Therefore:

**A large one-time reasoning investment is desirable.**

Do not optimise this task for minimum immediate token consumption.

Optimise it for minimum **lifetime repository comprehension cost across future agent sessions**.

Spending considerably more inference resources now is rational if it produces a materially superior persistent knowledge base.

------------------------------------------------------------------------

# Escalate Rather Than Simplify

If the task becomes difficult because:

- the repository is large;
- architecture is unclear;
- execution is highly distributed;
- abstractions obscure implementation;
- tests contradict apparent behaviour;
- multiple implementations exist;
- state transitions are complex;
- configuration materially changes behaviour;

do not respond by simplifying the documentation objective.

Increase analytical depth.

Perform additional repository investigation.

Use additional reasoning.

Divide the problem into coherent areas.

Persist established findings.

Continue systematically.

Complexity is a reason for **more capable reasoning**, not for shallower documentation.

------------------------------------------------------------------------

# Long-Horizon Task Discipline

Treat this as a long-horizon engineering investigation.

Do not optimise for producing an impressive result during the first few operations.

Progress should instead resemble:

```text
Inspect
-> reason
-> verify
-> persist findings
-> inspect related implementation
-> reason
-> verify
-> refine persisted findings
-> continue
```

Repeat this process until repository coverage is genuinely comprehensive.

The quality of the final repository knowledge base matters considerably more than how rapidly the first documentation files appear.

At the same time, persist useful findings frequently so progress survives interruption.

------------------------------------------------------------------------

# Quality Gate Before Declaring Comprehension

For each substantial area, do not consider it comprehended merely because its files have been inspected.

Consider it sufficiently comprehended only when you can explain, from repository evidence:

1. **Purpose:** Why does it exist?
2. **Scope:** What does it own?
3. **Boundary:** What does it deliberately not own?
4. **Location:** Where is it implemented?
5. **Entry:** How is it invoked?
6. **Execution:** What precisely happens?
7. **Data:** What information enters, changes, and exits?
8. **State:** What state does it read or mutate?
9. **Dependencies:** What does it depend upon?
10. **Dependants:** What depends upon it?
11. **Configuration:** What modifies its behaviour?
12. **Failures:** What can fail and what happens then?
13. **Invariants:** What must remain true?
14. **Tests:** Where and how is its behaviour verified?
15. **Integration:** How does it contribute to larger processes?
16. **Modification impact:** What else may require modification if it changes?

If several of these questions remain unanswered for a significant component, feature, algorithm, or process, continue investigating before considering that area complete.

------------------------------------------------------------------------

# Existing Root Architecture Documentation

If `ARCHITECTURE.md` exists at the repository root, treat it as an input source for repository comprehension, but do not duplicate it under `docs/`.

Its contents may be inspected, verified against the implementation, and used to inform, synthesise, or expand the documentation generated under `docs/`. However, do not create `docs/ARCHITECTURE.md` or any other document whose principal content duplicates or substantially reproduces the root `ARCHITECTURE.md`.

Generated documentation may reference or incorporate specific architectural information from the root `ARCHITECTURE.md` where that information is necessary to explain a broader component, capability, execution process, dependency, or implementation detail. Such incorporation must be contextual and selective rather than a near-duplicate reproduction.

The documentation under `docs/` must complement the root `ARCHITECTURE.md`, not create a second copy of it.

------------------------------------------------------------------------

# Documentation Location Constraints

Do not generate the following inside `docs/`:

- **Roadmap** — belongs at repository root as `ROADMAP.md`
- **Privacy policy** — belongs at repository root as `PRIVACY.md`
- **Security notice** — belongs at repository root as `SECURITY.md`
- **License** — belongs at repository root as `LICENSE`

These files must reside at the repository root, not under `docs/`.

------------------------------------------------------------------------

# Documentation Structure

Generate documentation under `docs/` with the following structure. Create as many files as needed to properly separate concerns.

## Directory Layout

```
docs/
├── api-reference/                    # API reference (one file per controller)
│   ├── INDEX.md                      # API reference index, endpoint summary table
│   ├── controller-a.md               # One file per controller
│   └── controller-b.md
├── behaviour/                        # User-facing behaviours
│   ├── browse-and-search.md
│   └── inspect-edit-delete.md
├── components/                       # Per-component deep dives
│   ├── presentation.md
│   ├── host-and-composition.md
│   ├── application-services.md
│   ├── browser-state-and-localisation.md
│   └── integration-models.md
├── flows/                            # End-to-end execution flows
│   ├── startup-and-rendering.md
│   ├── calendar-search.md
│   └── detail-mutation.md
├── api-usage-examples.md             # Example requests/responses for API usage
├── ambiguities-and-open-questions.md # Unresolved items, TODOs, known gaps
├── architecture.md                   # High-level architecture (complements root ARCHITECTURE.md)
├── build-and-deployment.md           # Build pipeline, deployment, environments
├── change-guide.md                   # How to modify common areas safely
├── configuration.md                  # Configuration schema, sources, precedence
├── concurrency-and-scheduling.md     # Threading, async, schedulers, locks
├── data-model.md                     # Domain entities, relationships, persistence
├── dependencies.md                   # External and internal dependencies
├── design-decisions.md               # Key architectural/design choices and rationale
├── documentation-maintenance.md      # How to keep docs current, ownership
├── error-handling.md                 # Error taxonomy, handling patterns, recovery
├── faq.md                            # Frequently asked questions
├── INDEX.md                          # Master index and navigation
├── invariants.md                     # System-wide invariants and contracts
├── integrations.md                   # External system integrations
├── logging.md                        # Logging framework, levels, structured fields, correlation, sinks
├── quick-start.md                    # Getting started guide for newcomers
├── repository-overview.md            # Repository purpose, scope, entry points
├── repository-structure.md           # Source tree layout, module organisation
├── security.md                       # Security model, threats, mitigations (complements root SECURITY.md)
├── state-and-persistence.md          # State management, stores, caches, migrations
├── testing.md                        # Test strategy, organisation, coverage
└── troubleshooting.md                # Common issues and solutions
```

## Naming Standards

- **Files**: kebab-case (`state-and-persistence.md`, not `stateAndPersistence.md`)
- **Directories**: kebab-case, plural for collections (`components/`, `flows/`, `behaviour/`, `api-reference/`)
- **Headings**: Sentence case (`## Repository purpose`, not `## Repository Purpose`)
- **Cross-references**: Relative links from `docs/` root (`[Architecture](./architecture.md)`)
- **Code symbols**: Backticks with full namespace (``Namespace.Class.Method``)

## API Reference Requirements

The `api-reference/` directory must contain one file per controller. Each controller file must document every endpoint with:

### Per-Endpoint Documentation

For each endpoint, include:

1. **HTTP method and path** — `GET /api/v1/resource/{id}`
2. **Controller action** — Fully qualified method name (``ControllerName.ActionName``)
3. **Authentication/authorisation** — Required schemes, roles, policies
4. **Request**:
   - Path parameters (name, type, constraints, example)
   - Query parameters (name, type, required/optional, default, example)
   - Headers (name, required/optional, example)
   - Body schema (JSON example, field descriptions, validation rules)
5. **Response**:
   - Success status code(s) with JSON example(s)
   - Error status codes with JSON error response examples
   - Response headers (if relevant)
6. **Behaviour summary** — What the endpoint does, side effects, idempotency
7. **Flow references** — Links to relevant `flows/*.md` files
8. **Error scenarios** — Documented error codes, conditions, and example responses

### Controller File Structure

Each controller file (`controller-name.md`) must follow:

```markdown
# ControllerName

Base path: `/api/v1/controller-name`

## ActionName (HTTP_METHOD /path)

[Per-endpoint documentation as above]

## AnotherAction (HTTP_METHOD /path)

[Per-endpoint documentation as above]
```

### api-reference/INDEX.md

Must provide:

- Summary table of all endpoints (Method, Path, Controller, Action, Auth)
- Links to each controller file
- Global authentication schemes
- Versioning strategy
- Rate limiting / throttling policies
- Links to related `flows/`, `components/`, `data-model.md`

## INDEX.md Requirements

The `INDEX.md` must provide:

1. **Repository summary** — one-paragraph purpose and scope
2. **Root document map** — links to `ARCHITECTURE.md`, `SECURITY.md`, `ROADMAP.md`, `PRIVACY.md`, `LICENSE` at repository root (if present)
3. **Documentation catalogue** — grouped, linked list of every file under `docs/` with one-line descriptions
4. **Navigation aids** — "Start here" for newcomers, "Deep dive" for component owners, "Flows" for debuggers
5. **Maintenance metadata** — last reviewed date, owner, coverage status

## Logging Documentation Requirements

The `logging.md` file must document:

1. **Logging framework** — Library used (e.g., Serilog, NLog, log4net, Winston), configuration source
2. **Log levels** — Which levels are used (Debug, Info, Warning, Error, Fatal) and their semantics
3. **Structured fields** — Standard properties attached to every log entry (request ID, user ID, correlation ID, timestamp format)
4. **Correlation** — How requests are traced across components (correlation IDs, trace IDs, span IDs)
5. **Sinks/destinations** — Where logs are written (console, file, database, external service) and their configuration
6. **Redaction/masking** — What sensitive data is redacted or masked in logs
7. **Retention** — Log retention policies, rotation, archiving
8. **Sampling** — Whether log sampling is used and under what conditions
9. **Performance considerations** — Impact of logging on throughput, async vs sync logging
10. **Error logging** — How exceptions are logged (stack traces, inner exceptions, context)
11. **Audit logging** — Security-relevant events that are logged separately
12. **Configuration** — Where logging is configured and how to change levels at runtime

## Root Document Integration

- Reference root `ARCHITECTURE.md`, `SECURITY.md`, `ROADMAP.md`, `PRIVACY.md`, `LICENSE` from `INDEX.md` and relevant `docs/` files
- Do not duplicate root document content under `docs/`
- Complement, don't replicate: `docs/architecture.md` elaborates on root `ARCHITECTURE.md`; `docs/security.md` elaborates on root `SECURITY.md`

------------------------------------------------------------------------

# Final Standard

Approach this task at the level expected from an expert software architect performing exhaustive repository reverse engineering for long-term institutional knowledge preservation.

Do not aim for documentation that merely permits somebody to understand the repository.

Aim for documentation that permits a future capable coding agent to **avoid having to rediscover that understanding from source code**.

Use sufficient context, repeated verification, and as much analysis as necessary to achieve that objective.
