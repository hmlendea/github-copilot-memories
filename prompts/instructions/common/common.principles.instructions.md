---
description: "Use when writing or editing any code or documentation. Covers foundational principles and repository documentation synchronisation."
applyTo: "**"
---

## Privacy

- Always write privacy-respecting code and documentation.
- Collect, process, persist, and expose only the minimum personal data necessary for the defined purpose.
- Do not log, display, or commit secrets or personal data unless explicitly required and appropriately redacted or protected.

## Security

- Always write secure code and documentation.
- Apply industry security standards and best practices throughout design, implementation, testing, deployment, and maintenance.
- Treat security as a default requirement for every change, and prefer the most secure practical option when trade-offs are necessary.

## Repository Documentation

- After making changes, always assess whether `README.md`, `SECURITY.md`, `ROADMAP.md`, or `ARCHITECTURE.md` is affected, and revise every relevant document so that it remains accurate and complete.
- When generating or revising `ARCHITECTURE.md`, `SECURITY.md`, `ROADMAP.md`, or similar planning and policy files, ensure the corresponding section or link is present in `README.md` unless that section already exists and remains accurate.
- Treat each document independently and do not modify documents whose subject matter is unaffected by the change.
