---
name: test-design
description: Use when changing tested behaviour, correcting defects, or writing/revising tests. Covers case derivation, boundaries, interactions, assertions, coverage, and determinism.
---

Design tests from observable contracts, domain invariants, changed lines, and reachable control flow.
- Cover success and failure, guards, state transitions, exceptions, fallbacks, side effects, retries, cancellation, timeouts, stale state, repeated calls, and dependency failures when relevant.
- Boundaries: immediately below, at, and above each representable numeric, temporal, length, or range limit.
- Inputs: relevant absent/null, empty, cardinality, sign, extrema, overflow, duplicate, order, whitespace, case, Unicode, malformed, and large-value classes.
- Defect correction: regression test fails before correction and passes after it; exercise nearest observable boundary.
- Assert complete results: values, errors, state, persistence, events, dependency calls, and prohibited-side-effect absence. Do not assert internals or trivial accessors.
- Parameterise identical setup, control flow, and expectations; separate materially different cases. Every case must detect a distinct plausible defect.
- Aim for complete affected branch coverage; inspect omissions and justify any intentionally untested reachable branch.
- Keep tests deterministic and isolated. Control time, randomness, locale, environment, scheduling, and external dependencies; no real networks, delays, ordering dependencies, or residual state.
