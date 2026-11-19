---
name: ai-credit-routing
description: "Use when minimising GitHub Copilot AI credits, selecting a mode, model, or reasoning effort, gating escalation to a stronger model, attributing spend by tokens and by cost, classifying wasted spend, or deciding whether to start a fresh session."
---

Optimise outcome per billed token:
- Simple question or review: use Ask mode. Multi-step edits: use Agent mode.
- Default to Auto when eligible; use stronger models only for ambiguity or planning, then execute from a compact plan with the least costly adequate model.
- Escalate to a stronger model or higher reasoning effort only via a stated conditional gate: a failed first attempt, an assignment tagged as demanding, or an irreversible step. A gate that matches everything is the stronger model by default.
- Default reasoning effort one notch below the maximum; effort is predominantly output tokens and frequently the largest single lever. Escalate per assignment, never globally.
- Never cite a price, limit, or benchmark discount from memory or from an external source; verify it from the current source, or present it as the user's own measurement only after measuring.
- Keep model, reasoning effort, agent, skills, and tool set stable within a session to preserve cache reuse.
- Start a fresh session via `session-handoff` when changing these or when history is predominantly irrelevant.
- Disable unused MCP servers and extensions; prefer the smallest capable tool set.
- Convert rich documents to Markdown prior to AI processing.
- Attribute spend by tokens and by cost separately; a high-volume cheap model and a costly strong model rank differently, so never read a token ranking as a cost ranking.
- Judge savings by cost per completed assignment, not per token; retries or additional passes on the cheaper path can invert the gain.
- Label every cost figure as measured, estimated, or extrapolated, and state its period and scope. Never present an estimate as a measurement; extrapolation is the lowest-confidence class and carries its method.
- Separate the cost of the observed work from the cost of the observing or note-taking model, and never fold the note-taker into the reported per-assignment cost.
- Classify wasted spend by failure type rather than by operation type: repeated attempts at one defect, hedging, wrong approach, rework, regression, premature completion, unnecessary escalation, repeated context read, and duplicated work. Count each wasted turn once, in one set, in every view that reports it.
- Rework is a failure type, never an operation category; keep the intended operation type separate from the failure that occurred, and record both when both apply.
- Cap optional inference passes such as classification, review, or summarisation with an explicit spend ceiling, keep the pass inactive by default, and report its spend separately from the assignment it annotates.
- Establish which figure a source genuinely proves and which the user must measure on their own traffic; a published discount presumes a call rate or workload that the user's may not reproduce.
- Pair each attributed cost with its confidence, and list unpriced or partially priced usage explicitly rather than pricing it at zero.
- Measure usage where available; never infer savings from request count alone.
