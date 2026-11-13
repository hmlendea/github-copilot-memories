---
name: pre-aggregate-data
description: Use when an assignment necessitates API, repository, or command data. Retrieve it during a preliminary step into files, then read only what is required.
---

Move data collection out of the token-billed agent loop.

- In a preliminary step, execute the requisite `gh`, API, or script invocations and persist trimmed results to `.work/*.json`.
- During the assignment, read only the specific `.work` files required.
- Never round-trip unprocessed payloads through the model.
