---
description: "Use for C# edits. Defines coding invariants, contract exceptions, and mandatory csharp-code-quality skill activation."
applyTo: "**/*.{cs}"
---
# C# Coding

## Applicability And Precedence

- Apply to handwritten C#; do not edit generated code. Preserve public contracts, runtime semantics, disposal, and required interface, override, callback, and test signatures.
- Use only released syntax supported by the configured compiler, language version, and .NET targets; never introduce preview syntax or change project versions merely to satisfy style. If prescribed syntax is unsupported, use a compatible form and report the exception.
- Specific rules take precedence over general preferences: null patterns over equality calls; collection contracts over concrete-type preferences; required instance signatures over `static`. Report unresolved conflicts; do not silently select a policy.

## Conditional Quality Skill

Invoke [csharp-code-quality](../../skills/csharp-code-quality/SKILL.md) prior to editing or reviewing strings, JSON options, regexes, reusable arrays, dictionary lookups, URI composition, enum values, controller binding, parsing, exceptions, or option validation; also invoke it for C# analyser-rule remediation. Apply every relevant section, even without an analyser warning. Load each rule reference listed in its Rule Catalogue whose topic the change touches, and the [security instructions](csharp.security.instructions.md) for security-relevant changes. If skill invocation is unavailable, read the linked file directly; if inaccessible, report the blocker rather than omitting its rules.

## Expressions And Parameters

- Explicit types; never `var`. Prefer `+= 1` / `-= 1` over `a = a + 1` / `a = a - 1`.
- Conditional default: initialise first, then one overriding `if`, without a fallback-only `else`. Do not evaluate a default eagerly if that changes side effects, exceptions, or cost.
- Prefer static `Equals(a, b)` / `string.Equals(a, b)` over `==` or instance `.Equals()` only with equivalent semantics. Guard nullable instance calls; retain required operator, reference, and floating-point semantics.
- No ternary `condition ? a : b`; use `if`/`else`. `??=` and switch expressions are permitted; `??` and nested conditional expressions are not.
- Prefer early guard clauses for independent preconditions. Keep compound conditions readable; extract a cohesive named predicate or split independent validation into sequential guards when a long boolean chain obscures intent. Preserve short-circuit order and side effects.
- In loops, use `continue` guard clauses for per-item exclusions instead of nesting the remaining body in an `if`. Hoist loop-invariant checks only when semantics are unchanged. A `foreach` followed by an `if` is not inherently inefficient; do not replace it with LINQ or materialise a collection solely to remove the conditional.
- No tuples; use a dedicated result type. Do not declare `ref` parameters; prefer returns over `out`. Required external signatures and calls, including `TryParse` / `TryGetValue`, are exceptions.
- No optional/default parameters in authored APIs; use adjacent overloads, ordered from fewest/simplest to most parameters/complexity. Preserve required external signatures.
- Interface, implementation, and override parameter names agree exactly; XML `<param>` tags use those names.
- Derive numeric enum variant indices via `(int)value`; do not maintain parallel stored indices.
- Methods, constructors, and lambdas: at most 7 parameters; group cohesive inputs into a request/options type. Preserve required external signatures.

## Layout

- No `#region` / `#endregion`. Control-flow bodies require braces on separate lines, including bodies containing only `continue`, `break`, or `return`; retain `else if` on one line.
- Exactly one blank line between methods, including after `};`; none immediately preceding `}`, `]`, or `)`.
- Separate block control-flow statements (`if`, `for`, `foreach`, `while`, `do`, `switch`, `try`, `using` blocks) and `continue` / `break` from adjacent non-control-flow statements in their block by one blank line above and below. Non-control-flow statements include local declarations, assignments, and calls; a declaration whose variable the control-flow statement consumes is not exempt. For `return` / `throw`, separate only above. No padding at block boundaries (directly after `{` or directly before `}`) or between adjacent control-flow statements; never separate an `else`, `else if`, `catch`, or `finally` from its preceding clause.
- Use the co-activated [indentation rules](csharp.indentation.instructions.md) for the 72/96-character thresholds and expression-body layout.
- XML documentation attributes use no spaces around `=`: `/// <param name="clientInfo">`, `/// <exception cref="ArgumentOutOfRangeException">`, never `name = "clientInfo"` or `cref = "..."`.

Control-flow spacing:
```csharp
private static bool IsValidUtf8(byte[] body)
{
    ReadOnlySpan<byte> remaining = body;

    while (!remaining.IsEmpty)
    {
        OperationStatus status = Rune.DecodeFromUtf8(remaining, out _, out int bytesConsumed);

        if (status != OperationStatus.Done)
        {
            return false;
        }

        remaining = remaining[bytesConsumed..];
    }

    return true;
}
```

## Files, Types And Members

- Explicit namespace and type blocks, including `Program.cs`; no top-level code. Default entry point: `static void Main`; use `int`, `Task`, or `Task<int>` when exit codes or asynchronous execution require it.
- One type per identically named file; extract additional types. No `partial` classes except required host contracts, source generators (for example `GeneratedRegex`), or explicit user requests.
- Every non-static class with public instance methods implements a colocated equivalent interface, except domain models and data/entities. Mirror its public instance contract; controllers and test fixtures are not implicitly exempt.
- Classes are `sealed` unless designed for inheritance. Domain models, data/entities, and configuration classes: `public sealed class` unless inheritance is required.
- Domain/data types with significant equality implement `IEquatable<T>`, override `Equals(object)`, and supply consistent `GetHashCode()`.
- Declare accessibility explicitly wherever legal for fields, properties, events, constructors, and methods, including `private`. Do not invent modifiers for static constructors, destructors, or explicit interface implementations.
- Member order: fields -> properties -> events -> constructors/destructors -> methods.
- Field order: constants -> static readonly -> static mutable -> instance readonly -> instance mutable.
- Within each field subgroup and other member group: `public` -> `protected internal` -> `protected` -> `internal` -> `private protected` -> `private`. Preserve overload adjacency.
- Private/internal constants use `const Type Name = value;`; public constant values use `public static Type Name => value;`, never `public const`, to prevent client-side inlining. Use named constants for repeated protocol literals and fixed values.
- Preserve and refresh XML summaries for every public NuGet class/member, including enum members. Never eliminate a public NuGet member without an explicit request.
- Prefer concrete types for implementation details; retain mandatory class interfaces, collection contracts, and genuine substitution boundaries.

## Construction, Properties And Methods

- Services, controllers, and startup classes: C# 12 primary constructors; use parameters directly, without redundant fields, subject to the compatibility rule.
- Models/entities: target-typed object initialisers, for example `Account account = new() { Id = identifier };`. When the declaration supplies the type, use `new(...)`, not `new Type(...)`; supported collection expressions take precedence.
- Omit assignments repeating type/host defaults or field initialisers overwritten by every constructor prior to use; preserve intentional contract/default-state initialisers.
- Stored model/entity/request/response/settings properties use `{ get; set; }`; computed read-only properties use `=>`. No `init` accessors.
- Methods without instance state are `static`, unless required instance contracts apply.
- Mapping methods exist only as extensions in dedicated `*MappingExtensions.cs` files under `[xyz].Mapping`, never implementation classes.
- A body expressible as one equivalent expression uses `=>`, including void delegation, return, throw, and `new()` initialisers; no temporary-return local. Retain blocks for control-flow constructs, required local declarations, and disposal/exception scopes without an equivalent expression form, and predicates exceeding the boolean-expression limits below.
- Cognitive Complexity: at most 15. Extract cohesive named helpers without changing semantics or public contracts.
- Boolean expressions read as plain sentences:
  - At most 3 clauses, joined by one operator kind; never mix `&&` and `||` in one expression, even with parentheses.
  - Each clause is a comparison, a `bool` name, or a single call. A lambda inside a condition holds one clause; otherwise extract a predicate method and pass it as a method group.
  - Extract each further or mixed group into a named `bool` local (`is…`, `has…`, `are…`, `can…`) or a named predicate method stating the intent.
  - Prefer positive forms: `All(IsPermitted)`, never `!Any(x => !IsPermitted(x))`; never negate a call whose lambda contains a negation.
  - Evaluate a repeated subexpression (for example `context.EnumerateObject()`) once into a local.
  - Check `null` and structural guards separately from policy checks.
  - These limits take precedence over the expression-body preference: a predicate exceeding them uses a block body with named locals.

Readable conditions:
```csharp
private static void ValidateClientInfo(ClientInfo? clientInfo, int maximumFieldLength)
{
    bool isApplicationValid = clientInfo is not null &&
        !string.IsNullOrWhiteSpace(clientInfo.Application) &&
        IsFieldPermitted(clientInfo.Application, maximumFieldLength);
    bool isVersionValid = clientInfo?.ApplicationVersion is null ||
        IsFieldPermitted(clientInfo.ApplicationVersion, maximumFieldLength);

    if (!isApplicationValid || !isVersionValid)
    {
        throw new InvalidOperationException("The handshake parameters violate the admission policy.");
    }
}

private static bool IsFieldPermitted(string value, int maximumLength)
    => value.Length <= maximumLength && !SensitiveDataPolicy.ContainsSensitiveData(value);
```

Never:
```csharp
if (clientInfo is null ||
    string.IsNullOrWhiteSpace(clientInfo.Application) ||
    clientInfo.Application.Length > maximumFieldLength ||
    clientInfo.ApplicationVersion is not null &&
        clientInfo.ApplicationVersion.Length > maximumFieldLength ||
    SensitiveDataPolicy.ContainsSensitiveData(clientInfo.Application))
```

Single-expression void delegation retains `=>`, with the expression on the next line when the combined length exceeds 96 characters:
```csharp
private void ConfigureBankChannels(IEnumerable<FundingChannelSettings> channels)
    => ConfigureBankChannel(channels, "Salt Bank", "saltbank", SaltBank);
```

## Async And Completion

- Prefer synchronous service methods when no asynchronous operation/contract is required; do not introduce unnecessary `Task<T>` or `async`/`await`, or block existing asynchronous APIs to satisfy this preference.
- Use `CancellationToken` only when required. Place it last in authored asynchronous signatures; use named arguments as necessary. Preserve required external signatures.
- Propagate received tokens to every cancellation-aware subsequent call and blocking wait; use explicit `CancellationToken.None` only for intentional non-propagation.
- Treat reference types as nullable-aware without `#nullable enable` directives.
- Resolve actionable `TODO` comments in the changed area; record unresolved external decisions outside source comments and report them as incomplete.
