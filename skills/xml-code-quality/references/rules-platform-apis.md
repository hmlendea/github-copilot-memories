# XML Rules: Platform APIs

One directive per XML rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never reference deprecated `${pom.*}` properties in a Maven POM; use `${project.*}` instead (for example `${project.artifactId}-${project.version}`).
- Never declare a Maven dependency with `<scope>system</scope>` or a `<systemPath>`, which binds the project to a machine-specific path; resolve the artefact from a repository with an appropriate scope, for example `provided`.
- Set `reconnectOnException` to `true` on every Spring JMS `SingleConnectionFactory` bean (`p:reconnectOnException="true"` or a `<property name="reconnectOnException" value="true"/>` element); the default `false` prevents automatic connection restoration.
- Set `acceptMessagesWhileStopping` to `true` on every Spring JMS `DefaultMessageListenerContainer` bean, so that messages received during shutdown are processed, not abandoned.
- Set `hibernate.hbm2ddl.auto` only to `validate`, or omit the property; any other value (for example `update`, `create`, or `create-drop`) can modify, delete, or purge the database schema and its data.
