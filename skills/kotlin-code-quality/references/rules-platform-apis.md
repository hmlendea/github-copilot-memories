# Kotlin Rules: Platform APIs

One directive per Kotlin rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Pass valid 1-based indices to `PreparedStatement` setters and `ResultSet` getters; never 0 or beyond the parameter or column count.
- Prefer Kotlin and JDK capabilities to Guava: `joinToString` for `Joiner`, function types for `Predicate`, `setOf`, `listOf`, and `mapOf` for `ImmutableSet.of`, `ImmutableList.of`, and `ImmutableMap.of`, `java.util.Base64` for `BaseEncoding`, and nullable types or `java.util.Optional` for Guava `Optional`.
