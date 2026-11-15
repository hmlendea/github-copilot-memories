---
name: qa-acceptance
description: Use when defining manual QA acceptance criteria or a structured validation plan for a feature, defect correction, or release candidate. Covers the Given-When-Then single-assertion contract, mandatory coverage dimensions, pass-fail evidence standards, and handoff classifications.
---

Formulate acceptance criteria that an independent reviewer can execute against a running application to determine acceptance without consulting the author. Acceptance criteria define the contract: automated tests establish regression correctness; QA validation establishes feature-level behaviour.

## Applicability

- **Use when:** a feature or user-facing modification requires a written validation plan, a reviewer must verify behavioural changes, an incident requires an explicit regression verification prior to resolution, or a release candidate requires a pre-distribution verification pass.
- **Do not use when:** a modification is purely internal (utility refactoring, identifier renaming, private performance calibration) where automated unit tests provide sufficient coverage, or when defining programmatic API interface contracts (use API contract specifications instead).

## Acceptance Criterion Format

Structure each criterion as an independent, individually verifiable statement with a single observable outcome:

```markdown
- **Given** <initial condition>, **when** <action>, **then** <observable outcome>.
```

Avoid combining multiple actions or multiple outcomes into a single criterion; separate them into distinct criteria.

## Mandatory Coverage Dimensions

Every comprehensive validation plan must evaluate each relevant dimension, or explicitly designate it as `N/A: <justification>`:

1. **Golden path:** the primary successful user journey, end to end.
2. **Empty and minimal states:** zero elements, a single element, and omitted optional inputs.
3. **Boundary inputs:** extreme string lengths, maximum and minimum numeric magnitudes, unusual Unicode characters, and right-to-left scripts where applicable.
4. **Error states:** network unavailability, authorization denial, validation rejections, resource conflicts, and missing entities.
5. **Concurrency and sequencing:** multiple concurrent operations, contention with background processing, and cancellation or interface refresh during active mutations.
6. **Performance envelope:** the largest plausible operational payload the modification must process without interface stalls or request timeouts.
7. **Backwards compatibility:** existing persisted records, historical identifiers, legacy configuration values, and user preferences continue operating correctly.
8. **Telemetry and audit:** required audit log entries, metrics, notifications, and operational diagnostics emitted during execution.

## Evidence Standards

Every evaluated criterion requires concrete recorded proof:

- Captured screen images or short video recordings for visual and user-interface behaviour.
- Terminal transcripts or HTTP response payloads for service and command behaviour.
- Diagnostic log extracts or persistence records for telemetry and audit requirements.
- Measured intervals for performance and latency criteria.

Subjective affirmations without recorded evidence do not constitute verification.

## Defect Quarantine and Follow-Up

- A failed criterion obstructs acceptance unless the system owner grants an explicit written waiver linked to a registered tracking issue.
- Unregistered defects or undocumented deferrals do not constitute valid waivers.
- Introducing a criterion during an active verification pass requires re-executing the entire plan from the start to prevent masked regressions.

## Reviewer Handoff

Deliver the validation outcome divided into three distinct categories:

- **Pass:** criteria fulfilled completely, accompanied by concise evidence summaries.
- **Fail:** criteria that failed, accompanied by reproducible step sequences and observed differences.
- **Blocked:** criteria that could not be evaluated, accompanied by the precise blocking dependency.

## Prohibited Patterns

- Describing implementation tests rather than observable conditions (acceptance describes what is true once delivered; test suites describe how the condition is checked).
- Coupling criteria to internal implementation details (internal identifiers, database query plans, unexposed component state).
- Providing uniform, unprioritised catalogues without distinguishing essential criteria from secondary observations.
- Declaring criteria passed without concrete verifiable proof.
