---
name: test-audit
description: "Use when auditing or gardening a test suite to detect and eliminate redundant, vacuous, or implementation-coupled tests while preserving regression proof. Covers the removal decision gate, duplication prevention, and evidence-backed reporting."
---

Audit and garden test suites to reduce execution, maintenance, and continuous-integration expenditure whilst preserving meaningful regression detection. Investigate rigorously; delete only with concrete evidence. Retaining an area after examination is an entirely valid outcome.

## Decision Gate

For each candidate removal, demonstrate all of the following:

1. **Observable contract and regression risk:** which observable contract, specification boundary, and plausible regression do the assertions verify?
2. **Retained proof:** which retained test file or test case detects that identical regression via the responsible production code? If none, explain why the assertion is vacuous, redundant, or the underlying contract is retired.
3. **Independent failure mode:** does the candidate uniquely evaluate a transport, permission, lifecycle, persistence boundary, execution platform, default configuration, or distinct failure mode? If it does, retain it.
4. **Concrete benefit:** what specific dimension improves (execution duration, fixture complexity, process overhead, maintenance cost, or suite legibility)?

Prefer the most compact test that exercises the code responsible for the contract. A broader end-to-end suite is not automatically superior proof. Similarity, source volume, latency, or suspected automated generation never alone justify deletion.

## Duplication Prevention

Apply this gate to every test inserted or modified during gardening:

- Identify the specific regression that existing proof neglects. Extend an established test suite or parameterised table prior to introducing an additional suite; an additional layer requires a distinct risk model.
- Exercise the responsible production behaviour directly. Avoid mocks that supply the very outcome under assertion, or production hooks introduced solely for testing convenience.
- Verify observable outcomes that survive behaviour-preserving refactorings. A negative test case must encounter its designated guard under otherwise valid inputs.

## Gardening Procedure

1. **Inspect:** record the baseline commit; inspect candidates, retained suites, fixtures, production callers, revision history, and continuous-integration routing. Preserve unrelated work intact.
2. **Plan:** classify each candidate into retain, repair, consolidate, delete, or defer. Name the retaining proof and assertions requiring relocation; evaluate redundant test suites in addition to individual cases.
3. **Prove baseline:** establish the baseline pass state locally or from matching continuous-integration runs. Diagnose existing failures prior to treating affected tests as cleanup candidates.
4. **Modify:** relocate unique assertions first, then retire verified duplicates and obsolete test fixtures. Deleting production seams demands its own caller and contract evidence.
5. **Validate:** execute retained suites and affected sibling tests, confirm test selection, and verify intended failure detection where appropriate.
6. **Reconcile:** compare deleted contracts against retained proof.

## Reporting

- Record deletions and retained tests, deferred candidates, verification outcomes, and identified limitations.
- Distinguish unique cases from repeated executions, and test support modifications from production modifications.
- Label cost evidence as measured, estimated, or historical; a substantiated simplification does not require an artificial latency reduction claim.
- State the final status: observations, validated local patch, or published pull request. Stop at the agreed scope or completed delivery, never at an arbitrary deletion quota.
