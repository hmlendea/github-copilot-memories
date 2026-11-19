---
name: commit-craft
description: "Use when a working tree holds mixed modifications, or prior to composing a commit series or pushing. Covers logical grouping, staged-secret gating, subject and body discipline, and series verification."
---

Compose reviewable commits from a mixed working tree. Staging, committing, pushing, and any history rewrite remain user-authorised operations; prepare the series, propose the commands, and execute only what the user requests.

## Grouping

- Never stage the entire tree on a mixed working tree; stage each group by path or hunk.
- Group by logical change: manifest with its lockfile, pure relocations, formatting-only files, each module with its tests, then documentation and continuous-integration configuration.
- Flag a file that mixes formatting with functional hunks, and a relocation whose callers' import modifications sit in another group, since that commit would not build.

## Staged-Secret Gate

Scan the added lines of what is staged, prior to composing the message, for:
- provider-shaped tokens and credential prefixes;
- high-entropy values assigned to secret, key, token, or password names;
- sensitive paths (environment files, key material, state files, credential stores);
- conflict markers.

Present findings redacted. Waive a false positive only through a recorded path or fingerprint with a rationale. A blocked gate is a stoppage: extract the value and load it at execution time, and never bypass the gate. A published secret is rotated first, since deleting it in a later commit leaves it in the history.

## Message

- Subject: an imperative statement of conduct, at most 72 characters, without a trailing full stop.
- Blank line, then a body stating why the modification is necessary for any change of substantial size or width; the diff already states what changed.
- Declare a breaking change explicitly (a `!` marker or a `BREAKING CHANGE` trailer) where consumer conduct is affected.
- Reject a vague subject, an overlong subject, a missing body on a wide modification, and any work-in-progress commit.

## Series Verification

- Each commit must build in isolation, and its tests must accompany the modification.
- Retain conventional-commit form only where the repository already follows it.
- Report the planned series with its staging commands, the gate outcome, and the verification performed. Rewrite unpublished history only.
