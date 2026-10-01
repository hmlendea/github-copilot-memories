---
name: symbol-navigation
description: Use when locating symbol definitions, references, implementations, call sites, or structurally similar code without reading broad file sets.
---

Navigate semantics before text.
- Known symbol: use language-server definitions, references, implementations, or rename support first.
- Structural pattern: use an installed syntax-aware query tool; do not install one solely for the query.
- Text fallback: search exact identifiers within relevant file types and directories; return paths, line numbers, and minimal context.
- Read only the owning definition and discriminating call sites.
- Stop when the controlling path and required edit surface are established.
