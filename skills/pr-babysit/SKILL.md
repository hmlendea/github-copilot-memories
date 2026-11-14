---
name: pr-babysit
description: Use when monitoring a pull request or review cycle until it is ready to merge. Covers check observation, unresolved review threads, verification prior to resolution, and evidence-based completion.
---

Maintain observation until the pull request is genuinely mergeable.
- Identify the pull request number, head branch, and base branch, then inspect draft state, mergeability, checks, review decision, comments, and unresolved review threads.
- Observe pending checks until they conclude; poll at a practical interval, usually 30-60 seconds unless the user requests another cadence.
- Verify each actionable finding against the code prior to modifying it; treat bot summaries as indicative, not conclusive.
- Correct genuine defects in focused commits, execute the relevant tests or build, push, and return to the status inspection.
- Resolve a review thread only after confirming that the code or generated artefact now addresses the comment; an outdated thread is not evidence of a correction.
- Cease only when checks pass or are intentionally skipped, the review decision is acceptable, no actionable comment remains, and no unresolved review thread remains.
- Report concrete evidence: head commit identifier, check names and results, unresolved thread count, tests executed, and any local modification left untouched.
- Query with `gh pr view` for coarse status and GraphQL `reviewThreads` for unresolved threads, incorporating `pageInfo` and paging while `hasNextPage` is true; save each response to a file and read only the required fields.