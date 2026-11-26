# Kotlin Rules: Build Scripts

One directive per Kotlin rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Register Gradle tasks lazily via `tasks.register`, never `tasks.create`.
- Never hardcode dependency versions; use a version catalogue (`libs.versions.toml`), version variables, or a dependency management plugin.
- Define `rootProject.name` in `settings.gradle.kts`.
- Define `description` and `group` for every Gradle task.
- Group dependency declarations by destination configuration.
- Include a Gradle settings file (`settings.gradle.kts`) in every Gradle project.
- Apply plugins bundled with Gradle via their shortcut identifiers (`java`, `jacoco`, `` `maven-publish` ``) instead of fully qualified identifiers (`id("org.gradle.java")`).
