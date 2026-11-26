# Kotlin Rules: Collections And Sequences

One directive per Kotlin rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Declare read-only collection types (`List`, `Set`, `Map`) and create them via `listOf`, `setOf`, and `mapOf` instead of mutable collections when their contents never change.
- Pass predicates directly to `any`, `none`, `count`, `first`, `firstOrNull`, `last`, `lastOrNull`, `single`, and `singleOrNull` instead of a preceding `filter` call.
- Replace `find`, `findLast`, `firstOrNull`, and `lastOrNull` compared with `null` by `any`, `none`, or `contains`.
- Test whether collections are vacant with `isEmpty()`, `isNotEmpty()`, or `isNullOrEmpty()`, never by comparing `size` or `count()` with zero or negating `isEmpty()`.
- Never pass a collection as an argument to its own functions.
- Never call `hashCode()` or `toString()` on arrays; use `contentHashCode()` or `contentToString()`, or the `contentDeep*` variants for nested arrays.
- Never pass arguments of unrelated types to collection membership and lookup functions (`contains`, `containsAll`, `containsKey`, `containsValue`, `get`, `indexOf`, `lastIndexOf`, `remove`, `removeAll`, `retainAll`); the result is invariably `false`, `-1`, or `null`.
- Pass every intermediate `Sequence` or `Stream` result to a terminal operation.
- Never compare collection sizes or array lengths with `>= 0` or `< 0`; the result is invariant.
- Never apply `!!` to `Map` lookups; manage the nullable result, or use `getValue`, `getOrElse`, `getOrDefault`, or `?:`.
