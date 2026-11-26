# C# Rules: Collections And LINQ

One directive per C# rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Use `Any()` (or the `Count`/`Length` property when available) to test for elements; never `Count() == 0` or `Count() > 0`.
- Return a zero-length collection or array (for example `[]`), never `null`, from methods and properties returning collections.
- Never pass a collection as an argument to its own methods (for example `list.AddRange(list)`, `set.UnionWith(set)`).
- Never wrap `Enumerable.Sum` in `unchecked`; overflow invariably throws.
- Never return a copy of a collection from a property (`ToList()`, `ToArray()`, a copy constructor); expose a read-only view or convert the property into a method.
- Simplify LINQ: use `OfType<T>()` instead of a type-test `Where` plus cast `Select`, use predicate overloads (`Any(predicate)`, not `Where(predicate).Any()`), and use the `Count`/`Length` property when available.
- Never chain `OrderBy` calls; use `OrderBy(...).ThenBy(...)`.
- Never declare a `foreach` variable of a narrower type than the element type (an unchecked explicit conversion); use `OfType<T>()` or `Cast<T>()`.
- Replace loops that only filter or project with LINQ (`Where`, `Select`) when readability improves.
- Never test whether a collection count or array length is `< 0` or `>= 0`; those comparisons are constant.
- Never assign the identical key or index twice in succession without an intervening read (for example `list[0] = a; list[0] = b;`); delete the overwritten assignment.
- Never read from or iterate a collection established to contain no elements at that point; populate it first or delete the access.
- Filter with `Where` prior to ordering with `OrderBy`.
- On types implementing `IList`, `IList<T>`, or `IReadOnlyList<T>`, use the indexer (`list[0]`, `list[^1]`, `list[i]`) instead of `First()`, `Last()`, or `ElementAt(i)`. **Local precedence:** Collection contracts remain `IEnumerable<T>`; apply the indexer only where the static type is an array, `List<T>`, `IList<T>`, or `IReadOnlyList<T>`.
- Use the `Min` and `Max` properties of `SortedSet<T>` instead of the `Min()` and `Max()` extension methods.
- Use the `First` and `Last` properties of `LinkedList<T>` instead of the `First()` and `Last()` extension methods.
- Use `Contains(value)` instead of `Any(x => x == value)` for simple equality checks.
- Use `First()` or `Single()` instead of `FirstOrDefault()` or `SingleOrDefault()` on collections established to contain elements.
