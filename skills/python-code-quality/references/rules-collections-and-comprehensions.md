# Python Rules: Collections And Comprehensions

One directive per Python rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never compare collection sizes where the result is constant (`len(items) >= 0` or `len(items) < 0`).
- Never replace collection content unconditionally (assigning the identical key or index twice in succession).
- Never duplicate keys in dictionary literals.
- Never duplicate values in set literals.
- Never modify a collection while iterating over it; iterate over a copy.
- Never access dictionary keys that do not exist; use `.get()` or test with `in`.
- Unpack iterables into the identical number of targets as their elements.
- Never index sequences beyond their bounds (`IndexError`).
- Unpack only mapping objects with `**`.
- Use only hashable values as set members and dictionary keys.
- Use only objects with `__index__` as sequence indexes.
- Pass generator expressions, not list comprehensions, to `any()` and `all()`.
- Use comprehensions instead of wrapping generator expressions in constructors (`[item.name for item in items]` rather than `list(item.name for item in items)`).
- Never wrap literals or comprehensions in redundant type constructors (`list([...])` or `set({...})`).
- Use literals (`[]`, `()`, `{}`, or `{'key': value}`) instead of `list()`, `tuple()`, `dict()`, or `dict(key=value)`.
- Replace comprehensions that only copy (`[item for item in items]`) with constructor calls (`list(items)`).
- Never wrap iterables in `list()` when iterating over them in `for` loops or comprehensions.
- Use comprehensions or generator expressions instead of `map()` with `lambda` when creating collections.
- Never use a static key in a dictionary comprehension.
- Pass `default_factory` to `defaultdict` positionally, never as a keyword argument.
- Never nest redundant collection functions (`list()`, `tuple()`, `set()`, `sorted()`, or `reversed()`), for example `list(sorted(items))`.
- Use `sorted(items, reverse=True)` instead of `reversed(sorted(items))`.
- Never reverse an iterable (`[::-1]`) prior to passing it to `set()`, `sorted()`, or `reversed()`.
- Iterate with `.keys()` or `.values()` instead of `.items()` when one part is unused.
- Never wrap `sorted()` directly in `set()`.
- Iterate over dictionary key-value pairs with `.items()`.
- Use `dict.fromkeys()` to populate a dictionary with a constant value.
