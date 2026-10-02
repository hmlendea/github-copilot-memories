---
name: repository-orientation
description: Use when repository structure, architecture, documentation, conventions, or project context must be discovered before a change.
---

Orient with the smallest useful context:
- Check `ARCHITECTURE.md` first when present.
- Then inspect relevant files under `docs/`.
- Then consult the GitHub Wiki when present and necessary.
- Read only sources relevant to the requested change; stop once the owning code path and constraints are clear.
- Verify repository-relative links before including them in documentation.
