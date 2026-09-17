---
description: "Use when writing or editing any code or documentation. Covers foundational principles and repository documentation synchronisation."
applyTo: "**"
---

## Privacy

- Always write privacy-respecting code and documentation.
- Collect, process, persist, and expose only the minimum personal data necessary for the defined purpose.
- Do not log, display, commit, or include in exception messages or telemetry any secret or personal data unless explicitly required and appropriately redacted or protected.

## Security

- Always write secure code and documentation.
- Apply industry security standards and best practices throughout design, implementation, testing, deployment, and maintenance.
- Treat security as a default requirement for every change, and prefer the most secure practical option when trade-offs are necessary.

## Evidence And Execution

- Do not fabricate facts, results, tool capabilities, or completed actions.
- Base claims about failures and system state on direct evidence.
- Distinguish clearly between an action that was not attempted, an action that was attempted and failed, an unsupported operation, and a successful operation.
- Distinguish observed facts from inferred information and unknown information. Do not present an inference as an exact result.
- Do not treat missing evidence as proof that something does not exist or did not occur.
- Execute an available requested action directly. Use a fallback only after the direct action has failed, and disclose the fallback and any resulting limitations.
- State uncertainty explicitly when the available evidence is incomplete or conflicting.

## Repository Documentation

- After making changes, always assess whether `README.md`, `SECURITY.md`, `ROADMAP.md`, or `ARCHITECTURE.md` is affected, and revise every relevant document so that it remains accurate and complete.
- When generating or revising `ARCHITECTURE.md`, `SECURITY.md`, `ROADMAP.md`, or similar planning and policy files, ensure the corresponding section or link is present in `README.md` unless that section already exists and remains accurate.
- Treat each document independently and do not modify documents whose subject matter is unaffected by the change.
- Verify repository-relative file and directory links before adding them to GitHub documentation.
