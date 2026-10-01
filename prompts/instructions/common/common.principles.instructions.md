---
description: "Use when writing or editing any code or documentation. Covers foundational principles and repository documentation synchronisation."
applyTo: "**"
---

## Privacy And Security

- Minimise collected, processed, persisted, and exposed personal data.
- Never log, display, commit, telemeter, or include secrets or personal data in exceptions unless explicitly required and appropriately protected or redacted.
- Apply established security practices throughout design, implementation, testing, deployment, and maintenance; prefer the most secure practical option.

## Evidence And Execution

- Never fabricate facts, results, capabilities, or completed actions; base system-state and failure claims on direct evidence.
- Distinguish unattempted, failed, unsupported, and successful actions.
- Label observed, inferred, and unknown information; never present inference as exact result or absent evidence as proof.
- Execute available requested actions directly. Use fallbacks only after direct failure; disclose fallback limitations.
- State uncertainty when evidence is incomplete or conflicting.

## Repository Documentation

- After changes, assess `README.md`, `SECURITY.md`, `ROADMAP.md`, and `ARCHITECTURE.md`; revise each affected document only.
- New or revised planning and policy documents require an accurate `README.md` section or link.
- Verify repository-relative links before adding them to GitHub documentation.
