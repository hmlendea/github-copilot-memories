# Python Rules: Types And Inheritance

One directive per Python rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never compare values of incompatible types with `==` or `!=`; the result is constant.
- Never use `is` or `is not` with operands of dissimilar types.
- Never use `is` with `int`, `bytes`, `float`, `frozenset`, `tuple`, or string literals (cached types); use `==`.
- Never construct an object solely to test its identity with `is`.
- Use operators only with operands of compatible types.
- Use `in` and `not in` only with objects supporting membership (`__contains__`, `__iter__`, or `__getitem__`).
- Use item access, assignment, and deletion only on objects supporting them (`__getitem__`, `__setitem__`, or `__delitem__`).
- Never call non-callable values.
- Use iterable unpacking, `for`-`in` loops, and `yield from` only with iterable objects.
- Never perform operations that contradict an earlier type check.
- Use `isinstance()` instead of direct type comparisons (`type(value) == SomeType`).
- Return the expected type from special methods (for example `bool` from `__bool__` and `str` from `__str__`).
- Return an iterator from `__iter__`.
- Never return a value from `__init__`.
- Return `NotImplemented` from binary special methods (for example `__eq__` or `__add__`) for unsupported operands; never raise `NotImplementedError`.
- Never use `NotImplemented` in boolean contexts.
- Never change contracts in overriding methods: accept every parameter of the overridden method, and provide defaults for extra parameters.
- Return values consistent with the function's return type hint.
- Assign values corresponding to the variable's type annotation.
- Pass arguments corresponding to the parameter type annotations.
- Use union type expressions (`int | str`) instead of `typing.Union` in type hints.
- Define generic classes with the type parameter syntax (`class Box[ItemType]:`) instead of `Generic` with `TypeVar`.
- Declare type aliases with the `type` statement.
- Never use `TypeVar` in generic `type` statements; use the type parameter syntax.
- Define generic functions with the type parameter syntax (`def first[ItemType](items: list[ItemType]) -> ItemType:`) instead of `TypeVar`.
- Never access attributes on values that can be `None`; test for `None` first.
