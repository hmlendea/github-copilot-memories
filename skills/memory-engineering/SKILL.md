---
name: memory-engineering
description: Use prior to adding memory to an agent, or when a memory store grows without eviction. Covers family selection and pricing, record classification, provenance and control, and the mandatory forgetting policy.
---

Engineer what a memory system forgets, not only what it retains. Apply prior to adding memory to an agent, or when a memory store grows without eviction.

## Selection

- Price each candidate family (long context, retrieval, graph, agentic) against the expected workload: construction expenditure, query expenditure, and cost per correct answer.
- Name the cost the selected family imposes rather than declaring a single superior design; on an inconclusive comparison, state the tie and the condition that would resolve it.
- Quantify amortisation across the expected query horizon. Where construction dominates total expenditure, reduce construction tokens prior to adjusting retrieval.

## Content

- Classify each stored record as a fact, a competence, an event log, or prose.
- Retain facts and competences; archive event logs and relocate prose to documentation.
- Measure duplication, staleness, and density, and record the age distribution rather than the volume alone. Additional raw memory can degrade agent conduct.

## Control and Governance

- Treat memory as files under version control with an owner, a scope, and a rollback path.
- Never auto-merge contradictory memories; surface the contradiction for a human determination, since the evidence that the conflict existed is itself valuable.
- Record the provenance of every durable claim, so a remembered rule can be traced to its origin.

## Forgetting Policy

A design is incomplete without an explicit policy covering:
- expiry and time-to-live per record class;
- supersession when a recent record contradicts an older one;
- eviction criteria and the capacity that initiates it;
- contradiction handling and its escalation;
- audit and rollback of a promoted or injected record.

Never schedule a consolidation or pruning pass that has not first been executed manually and demonstrated to alter a determination.
Attribute every figure to its source and confidence; vendor customer figures are testimonials, not measurements.
