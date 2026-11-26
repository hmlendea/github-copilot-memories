# Kotlin Rules: Members And Parameters

One directive per Kotlin rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Limit each function to at most 7 parameters; functions annotated with Spring `@RequestMapping` (or its shortcut annotations) or `@JsonCreator` are exempt.
- Delete unused `private` functions; annotated functions, functions with `@Observes` parameters, and serialisation hooks (`writeObject`, `readObject`) are exempt.
- Delete unused function parameters.
- Never declare vacant functions; throw `UnsupportedOperationException` for unsupported operations, or comment why an override is intentionally vacant.
- Delete unused local variables.
- Never implement two functions identically; delegate one to the other. Functions with fewer than 2 statements are exempt. **Local precedence:** The coding instructions prohibit every duplicate implementation; apply that stricter requirement to functions with fewer than 2 statements as well.
- Delete assignments whose values are never read (dead stores), including initialisers overwritten prior to any read.
- Delete null checks on non-nullable values (`== null`, `!= null`, `?:`, `!!`, `requireNotNull`, `checkNotNull`); their results are invariant.
- Replace explicit getter and setter functions (`getIndex`, `setIndex`, `isFinished`) with property accessors.
- Use indexed access operators (`list[index]`, `map[key] = value`) instead of explicit `get` and `set` calls.
- Test structural equality with `==` and `!=`, never by calling `equals` directly.
