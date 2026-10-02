---
name: ai-credit-routing
description: Use when minimising GitHub Copilot AI credits, selecting a mode or model, reducing tool overhead, or deciding whether to start a fresh session.
---

Optimise outcome per billed token:
- Simple question or review: use Ask mode. Multi-step edits: use Agent mode.
- Default to Auto when eligible; use stronger models only for ambiguity or planning, then execute from a compact plan with the least costly adequate model.
- Keep model, reasoning effort, agent, skills, and tool set stable within a session to preserve cache reuse.
- Start a fresh session via `session-handoff` when changing these or when history is mostly irrelevant.
- Disable unused MCP servers and extensions; prefer the smallest capable tool set.
- Convert rich documents to Markdown before AI processing.
- Measure usage where available; never infer savings from request count alone.
