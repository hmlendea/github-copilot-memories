---
name: migration-architect
description: Use when a live schema, database, service, or host requires modification or cut-over without downtime. Covers phased planning with gates, compatibility determination, expand-contract and strangler patterns, and per-phase rollback.
---

Plan a migration of a live schema, database, service, or host so that interruption remains within the stated window and every phase is reversible.

## Phases and Gates

- Decompose the migration into phases, each with a validation gate, an entry condition, and an exit condition.
- No phase commences prior to its predecessor's verification; record the evidence that closed each gate.
- Estimate duration from the phase structure and state the assumptions; a single aggregate estimate conceals the phase that overruns.

## Compatibility Determination

Determine compatibility prior to any cut-over:
- schema changes, including column removal, type narrowing, nullability, and constraint modification;
- interface versions and serialised payload shapes;
- data-type, encoding, and format conversion requirements;
- referential integrity and business-rule changes.

Gate approval on a compatible determination, or on an explicit written acceptance of every breaking item by the owner, and on a rollback procedure for every phase. Re-run the determination after any schema revision.

## Patterns

- Schema evolution: expand (add alongside), dual write, backfill, validate parity, then contract (retire the superseded structure).
- Service replacement: intercept requests at a gateway, relocate capability incrementally, verify, then retire the legacy component.
- Data movement: change data capture or dual write, shadow traffic with result comparison, then progressive traffic shift and legacy retirement.
- Cut-over: progressive traffic increments with a measured trigger for advancement and for reversal.

## Rollback and Verification

- Record, per phase, the rollback trigger, the reversal procedure, and the point-in-time recovery path.
- Verify data parity, counts, checksums, and business invariants at every gate prior to advancing.
- Keep the legacy path intact and verified until the new path holds.
