---
name: performance-profiler
description: Use for a slow endpoint, memory growth, elevated processor usage, an oversized bundle, or a performance budget, prior to modifying anything. Covers baseline establishment, profiling by domain, load testing, and before-and-after measurement.
---

Establish a measured baseline prior to modifying anything, and substantiate a modification with a measured difference afterwards.

## Baseline

- Record latency percentiles (median, p95, p99), throughput, error rate, and memory prior to any modification, under a stated workload, dataset, and hardware.
- Confirm the constriction by measurement; a suspected defect is a premise, not a finding.
- Identify the narrowest reproduction that exhibits the constriction, and record it as the comparison workload.

## Investigation by Domain

- Processor: flamegraph or sampling profile; identify the dominant frame rather than the deepest.
- Memory: heap snapshot, allocation growth, and garbage-collection pressure; distinguish a leak from an elevated steady-state footprint.
- Data: query plans, repeated-query detection, absent indexes, and unbounded result sets.
- Network and interface: payload volume, request count, sequential round trips, and cache conduct.
- Distribution: bundle or artefact composition, and the cost each dependency contributes.
- Capacity: load testing with progressive arrival rates; record the point of degradation rather than the maximum sustained value alone.

## Discipline

- Modify one variable at a time, then re-measure under the identical workload and compare against the baseline.
- A modification without a measured difference is unsubstantiated; revert it rather than retain complexity.
- Report baseline and post-modification measurements, the workload, the tooling, and residual uncertainty. Never quote a quality improvement without its cost figure.
