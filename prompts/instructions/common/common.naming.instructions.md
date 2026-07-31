---
description: "Use when writing or editing any code. Covers naming conventions."
applyTo: "**/*.{c,cpp,cs,h,java,js,jsx,py,sh,ts,tsx}"
---
## General

### Naming

- Use clear, explicit variable, type, and method names with no unclear abbreviations or shortenings. This applies **everywhere**: local variables, fields, method parameters, lambda parameters, loop variables, and out-variables.
- Prefixes like `tex`, `msg`, `btn`, `img`, `val`, `obj`, `mgr`, `cfg`, `pos`, `dir`, `ray` are forbidden
- Single-letter names (`e`, `i`, `j`, `m`, `n`, `t`, `x`) are forbidden
- Single-letter/abbreviated prefixes (`tX`, `tY`, `dirX`, `dirY`, `rayX`, `rayY`, `checkX`)
- Abbreviations (`sp`, `sut`, `ttl`) are forbidden
- Shortenings (`acc`, `auth`, `config`, `def`, `dmg`, `ex`, `len`, `max`, `min`, `str`, `svc`) are forbidden
- `Min` and `Max` are likewise forbidden as standalone names or as prefixes/suffixes — use `Minimum`/`Maximum` instead (e.g. `minimumDamage`, not `minDamage`; `maximumSpeed`, not `maxSpeed`)
- Always write the full descriptive name (e.g. `textureYOffset`, `directionX`, `rayPositionX`, `samplePositionX`, `magnitude`, `minimumDamage`, `maximumDamage`, `damageRoll`, `attackerStrength`)
- Lambda parameters follow the same rules without exception: `items.Select(item => item.Name)`, never `items.Select(i => i.Name)` or `items.Select(x => x.Name)`.
 - Never use names where a suffix repeats a meaning already implied by an abbreviation, e.g. `jwtToken` or `atmMachine`.