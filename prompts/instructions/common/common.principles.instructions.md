---
description: "Use for code or documentation edits. Covers privacy, security, evidence, execution, and documentation synchronisation."
applyTo: "**"
---

## Privacy And Security

- Minimise collected, processed, persisted, and exposed personal data.
- Never log, display, commit, telemeter, or expose secrets or personal data unless explicitly required and protected or redacted. Apply secure practices throughout; prefer the most secure practical option.

## Evidence And Execution

- Never fabricate facts, results, capabilities, or actions; ground system-state and failure claims in direct evidence.
- Label observed, inferred, and unknown information. Distinguish unattempted, failed, unsupported, and successful actions. Never present inference or absent evidence as proof.
- Execute available requested actions directly. Use fallbacks only after direct failure and disclose limitations. State uncertainty for incomplete or conflicting evidence.

## Repository Documentation

- After changes, assess `README.md`, `SECURITY.md`, `ROADMAP.md`, and `ARCHITECTURE.md`; revise only affected documents. Whenever a planning, policy, or project document has a corresponding README section, update the entire corresponding README section to match the README template, including its heading and fixed prose; a link alone is insufficient.
- Verify repository-relative links before adding them to GitHub documentation.
