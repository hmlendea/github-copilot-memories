---
name: instruction-budget-audit
description: Use when creating, reviewing, splitting, or optimising Copilot instructions, agents, prompts, or skills for context cost.
---

Optimise context without changing policy outcomes.
- Inventory words/bytes and activation: always-on, `applyTo`, semantic on-demand, or manual.
- Measure automatic payload for representative paths; file size alone is not context cost.
- Prioritise verbose output, large always-on sources, injected tool schemas, repeated reads, then minor prompt wording.
- Always-on: universal invariants only. Move domain/workflow rules to narrow `applyTo` or semantic discovery.
- Keep one concern per file; remove only rules guaranteed by a co-activated source.
- Preserve protected mappings, templates, examples, thresholds, exceptions, and public contracts; hash or count them before/after mechanical edits.
- Prefer compact declarative invariants over procedural repetition.
- Keep model, reasoning effort, agent, skill, and tool configuration stable during a session; use `session-handoff` when changing them.
- Validate frontmatter, activation, required rules, whitespace, and focused representative tasks after each slice.
- Report baseline, changed surfaces, measured payload reduction, and residual risk; never infer billing savings from file size or request count.
