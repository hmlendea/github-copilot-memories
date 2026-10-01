---
name: scoped-context
description: Use when the relevant files are known. Reference exact paths/symbols instead of whole-codebase search.
---
Target exact files and symbols.
- Read minimum useful ranges; avoid whole files when the symbol is known.
- Batch independent reads; never reread unchanged context.
- Filter command and API output to required matches or fields.
- Use codebase-wide search only for genuine location discovery.
- Stop discovery once controlling code and cheapest falsifying check are known.