# C# Rules: Interop And Reflection

One directive per C# rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never use reflection (`BindingFlags.NonPublic`) to access non-public types or members.
- Apply `[Pure]` only to methods that return a value.
- Never call `SafeHandle.DangerousGetHandle`; pass the `SafeHandle` itself in P/Invoke signatures.
- Use `Assembly.Load` instead of `Assembly.LoadFrom`, `Assembly.LoadFile`, or `Assembly.LoadWithPartialName`.
- Declare an assembly version (`<Version>` or `<AssemblyVersion>` in the project, or `[AssemblyVersion]`).
- Use `params` instead of `__arglist` (varargs).
- Declare P/Invoke (`extern`) methods `private` and expose them via a wrapper that validates arguments.
