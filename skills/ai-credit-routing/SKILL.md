---
name: ai-credit-routing
description: Use when minimising GitHub Copilot AI credits, selecting a mode, model, or reasoning effort, gating escalation to a stronger model, attributing spend, reducing tool overhead, or deciding whether to start a fresh session.
---

Optimise outcome per billed token:
- Simple question or review: use Ask mode. Multi-step edits: use Agent mode.
- Default to Auto when eligible; use stronger models only for ambiguity or planning, then execute from a compact plan with the least costly adequate model.
- Escalate to a stronger model or higher reasoning effort only through a stated conditional gate: a failed first attempt, a task tagged hard, or an irreversible step. A gate that matches everything is the stronger model by default.
- Default reasoning effort one notch below the maximum; effort is mostly output tokens and often the largest single lever. Escalate per task, never globally.
- Never cite a price, limit, or benchmark discount from memory or from an external source; verify it from the current source, or present it as the user's own measurement only after measuring.
- Keep model, reasoning effort, agent, skills, and tool set stable within a session to preserve cache reuse.
- Start a fresh session via `session-handoff` when changing these or when history is mostly irrelevant.
- Disable unused MCP servers and extensions; prefer the smallest capable tool set.
- Convert rich documents to Markdown before AI processing.
- Attribute spend by tokens and by cost separately; a high-volume cheap model and a costly strong model rank differently, so never read a token ranking as a cost ranking.
- Judge savings by cost per completed task, not per token; retries or extra loops on the cheaper path can invert the gain.
- Measure usage where available; never infer savings from request count alone.
