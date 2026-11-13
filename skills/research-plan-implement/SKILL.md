---
name: research-plan-implement
description: Use for non-trivial capabilities or changes. Separate investigation, planning, and implementation into three phases, each in a fresh session.
---

Separate non-trivial work into three phases, each in a fresh session:
- Investigation: collect context and relevant files, document findings and constraints in `PLAN.md`, then cease.
- Planning: derive a precise ordered assignment list from `PLAN.md` alone, then cease.
- Implementation: execute the assignment list in a fresh session, loading only the files it names, and validate each substantive step with `verify-before-continue`.
- Trivial or single-file edits: implement directly; do not phase.
Commence each phase only from the durable artefact, never from the prior transcript, and hand off between phases with `session-handoff`.
