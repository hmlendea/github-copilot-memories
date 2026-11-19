---
name: create-verification-skill
description: "Use when constructing a project-local verification skill that automates end-to-end execution, diagnostic health checks, surface interaction, evidence capture, and safe teardown for an application, service, or tool."
---

Generate an automated project-local verification skill (`.copilot/skills/verify-<application>/SKILL.md` or repository-designated equivalent) that executes an application precisely as a user interacts with it, evaluates behaviour, and preserves evidence. Author the generated skill so a subsequent automated agent can execute it without prior familiarity with the repository.

## Step 1: Examine Repository State

Extract operational facts directly from the repository; query the user only for unobservable environmental variables or credentials:

- **Surface:** identify the primary interaction surface: web interface, terminal or command-line utility, desktop application, HTTP service, mobile application, or software library.
- **Launch procedure:** determine how the application initiates locally, favouring repository-documented commands (package manifests, Makefiles, project README files). Record network ports, environment configurations, initial seed data, and authentication requirements.
- **Interaction mechanism:** identify existing programmatic harnesses first (browser automation suites, terminal pseudo-teletype harnesses, HTTP request collections, diagnostic sockets). Favour standard protocols (browser automation, pseudo-terminals, HTTP clients) when dedicated harnesses are absent.
- **Observable evidence:** determine verifiable outputs: captured screen images, terminal transcripts, HTTP response bodies, structured logs, termination codes, and database mutations.
- **Isolation:** determine whether multiple concurrent instances can execute simultaneously (distinct port assignments, isolated data directories, unique profiles). If concurrent execution is unsupported, instruct the generated skill to refuse execution against an active instance to prevent data corruption.

Verify that the repository builds and initiates prior to authoring the skill; authoring against a non-functional baseline produces erroneous instructions. When an inconsequential missing asset impedes startup, the generated harness may construct temporary verification fixtures and eliminate them during teardown.

## Step 2: Formulate the Verification Skill

Author the generated skill with complete, repository-specific commands and concrete values, containing these structured sections. Its frontmatter holds `name` equal to the skill directory and a single-line double-quoted `description` of at most 1024 characters; measure the value, because an oversized or unquoted description is a load error:

- **Launch:** the precise command initiating the application for verification, together with the explicit condition confirming readiness (a designated log message, a listening port, or an interactive prompt). Include orderly process termination. For brief command-line utilities, compile the binary once, then execute each scenario in an isolated session.
- **Doctor:** a non-destructive diagnostic check confirming whether the application instance is in a valid state to verify (process active, expected version, owned network port, valid credentials). Execute this check prior to each interaction.
- **Drive:** the interaction sequence utilizing concrete identifiers and selectors from the repository. Favour durable attributes (accessibility labels, semantic attributes, exact prompt strings, route paths) over positional coordinates or sequential tab indexes.
- **Evidence:** specific proof artefacts to collect and their preservation path. Exercise genuine user workflows rather than internal setters or test-only shortcuts; capture the user action and the resulting system state; inspect persistent side effects alongside interface manifestations. Mocks are permitted only where an established boundary isolates external third-party infrastructure.
- **Teardown:** reliable termination of every process initiated by the run. Never terminate processes by generic executable name; terminate only the specific process identifiers recorded during launch. Remove scratch data while preserving collected evidence intact at the designated proof destination.
- **Helper scripts:** any utility script accompanying the skill must be executable, portable, and referenced with clear execution examples in the skill text.

## Step 3: Map Core Features

Construct a companion feature map (`features/` directory adjacent to the generated skill) containing an index and individual feature guides for the primary user-facing journeys (commence with the principal 3 to 5 workflows identified from routes, commands, menus, or documentation).

Each feature guide must define:
1. **Sub-features:** distinct functional aspects evaluated by the guide.
2. **User journey:** how a user reaches and initiates the feature.
3. **Automated interaction:** the step-by-step programmatic commands driving the interaction harness.
4. **Observable proof:** concrete state changes proving the feature succeeded.
5. **Known edge cases:** non-obvious failure modes, timing considerations, or environmental prerequisites.

## Step 4: Validate the Generated Skill

Execute the newly authored skill instructions completely prior to delivery:
1. Initiate the launch sequence.
2. Execute the doctor check.
3. Drive at least one mapped feature workflow.
4. Collect the required evidence artefacts.
5. Execute the teardown procedure.
6. Verify that all captured proof artefacts remain accessible at the designated destination following teardown.

Remediate any execution failures and re-verify. A generated verification skill that has not been executed and proven is merely an unverified draft.
