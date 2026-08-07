---
description: "Use when the user inquires regarding revising, creating, or generating a ROADMAP.md. Auto-invoked by requests such as 'revise the roadmap', 'create a roadmap', 'compose the roadmap', or 'generate the roadmap'. Populates project-specific priorities and applies the standard structure and conditional sections."
applyTo: "ROADMAP.md"
---
This is the `ROADMAP.md` template that shall be utilised.
---

# [[Project Title]] Roadmap

[[[Brief summary of roadmap scope, planning horizon, and maintenance expectations.]]]

## 📑 Table of Contents

<!-- Generate one entry per ##/###/#### heading present in the final output, in order. -->

<!-- Only if there is active labour in progress. -->
## 🎯 Current Focus

- **[[Status: In Progress / Planned / Tentative]]**: [[Initiative name]] — [[Intended result]] ([[Target period, if defined]])
- **[[Status: In Progress / Planned / Tentative]]**: [[Initiative name]] — [[Intended result]] ([[Target period, if defined]])

<!-- Only if there is forthcoming labour beyond Current Focus. -->
## 🗺️ Planned Labour

### [[Near-Term Horizon e.g. Next 30 days or Q4 2026]]

- [[Priority 1]]
- [[Priority 2]]

### [[Mid-Term Horizon e.g. Next quarter or H1 2027]]

- [[Priority 1]]
- [[Priority 2]]

<!-- Use this subsection when target periods are not defined for upcoming priorities. -->
### [[No Fixed Horizon]]

- [[Priority 1]]
- [[Priority 2]]

<!-- Only if long-range planning is meaningful for this repository. -->
### [[Long-Term Horizon e.g. Future Exploration]]

- [[Idea 1]]
- [[Idea 2]]

<!-- Only if date-based checkpoints exist. -->
## 🧱 Objectives

| Objective | Target Period | Result | Status |
|-----------|---------------|---------|--------|
| [[Objective name]] | [[Period]] | [[Expected result]] | [[Planned / In Progress / Complete]] |

<!-- Only if notable external constraints or material risks exist. -->
## ⚠️ Dependencies and Risks

- [[Dependency or risk]] — [[Potential impact]] — [[Mitigation plan]]

<!-- Only if there are explicit non-goals for this horizon. -->
## 🚫 Out of Scope

- [[Non-goal 1]]
- [[Non-goal 2]]

<!-- Only if `CHANGELOG.md` exists. -->
## 📋 Delivered Labour

See [CHANGELOG.md](./CHANGELOG.md) for completed labour.
