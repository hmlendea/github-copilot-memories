# Kotlin Rules: Types And Inheritance

One directive per Kotlin rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Use `is` instead of `isInstance()` when the type is determined at compile time.
- Never override `equals` or `hashCode` in data classes with implementations that duplicate the generated behaviour.
- Use `Unit` instead of `Void`.
- Implement delegation via a `by` clause instead of overrides that only forward to a delegate.
- Implement singletons as `object` declarations or object expressions, never as classes with private constructors exposing a companion instance.
- Implement `fun` interfaces via lambda expressions instead of classes or object expressions.
- Declare single-abstract-function interfaces as `fun interface` (or replace them with function types), and delete `@FunctionalInterface` from them.
- Replace abstract classes containing only abstract functions (no properties or implemented functions) with interfaces.
- Delete type casts and type checks (`as`, `as?`, `is`) that can never succeed, together with the dead branches that result.
- Delete redundant type casts and type checks (`as`, `as?`, `is`) that invariably succeed, together with the dead branches that result.
- Delete deprecated code at the earliest opportunity; deprecation marks code for eventual deletion.
- Never use code annotated `@Deprecated`; migrate to the recommended substitute (`ReplaceWith`).
- Override `equals(other: Any?)` and `hashCode()` together, never one alone.
- Test the argument type in every `equals(other: Any?)` (via `is` or a `javaClass` comparison) prior to casting it.
- Override `equals` and `hashCode` in data classes with array properties, comparing arrays by content (`contentEquals`, `contentHashCode`).
