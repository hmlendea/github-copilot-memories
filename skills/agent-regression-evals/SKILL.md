---
name: agent-regression-evals
description: "Use before shipping an agent, prompt, model, or tool modification, or when a pass-rate movement requires adjudication. Covers repeated trials, trajectory grading, flake quarantine, and paired statistical gating against a baseline."
---

Adjudicate a modification to an agent, prompt, model, or tool through repeated measurement rather than a single pass rate.

- Regard a pass-rate movement as unsubstantiated until it exceeds the noise band of the measurement; agents are non-deterministic, so one trial per case cannot distinguish a regression from a fluctuation.
- Execute every case at least three times per baseline and per candidate, each trial from a clean environment.
- Record one structured result per trial: case identifier, trial index, outcome, criticality, expenditure, and the tool trajectory.
- Grade the path where the path carries weight: required lookups present, prohibited tools absent, and ordering where ordering is the requirement. Match modes are strict, unordered, subset, and superset; default to superset, which tolerates exploration whilst confirming required conduct.
- Quarantine flaky cases prior to comparing baseline and candidate; a case that varies within one configuration contaminates every comparison it enters.
- Compare per case, in pairs, against the baseline; an aggregate pass rate conceals the individual case that regressed.
- Block a merge on a substantiated regression in a critical case, and report a pass-rate decline that lies within the noise band as inconclusive rather than as a regression.
- Report the trial count, the baseline and candidate figures, the statistical outcome, the quarantined cases, and the residual uncertainty.
