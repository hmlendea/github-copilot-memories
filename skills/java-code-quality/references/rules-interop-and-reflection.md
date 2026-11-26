# Java Rules: Interop And Reflection

One directive per Java rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never use classes from `sun.*` packages; use supported public APIs.
- Never call `System.gc()` or `Runtime.getRuntime().gc()`; garbage collection is the JVM's responsibility.
- Never instantiate an object solely to call `getClass()`; use the class literal (for example `Example.class`).
- Never use reflection to increase the accessibility of classes, methods, or fields (for example `setAccessible(true)`).
- Never load JDBC 4.0 or later drivers with `Class.forName()`; `DriverManager` loads them automatically.
- Use the two-argument `ClassFile.transformClass` overload when a class transform retains the class name.
- Transform classes with `ClassFile.transformClass` instead of `build` with manual element copying.
- Use `ClassBuilder.withMethodBody` instead of `withMethod` when only the method body is defined.
- Never compare classes by name (`getClass().getName().equals(...)`); use `instanceof` or compare `Class` objects.
- Never use reflection to test for annotations without `RUNTIME` retention.
- Never use reflection to modify the accessibility of record fields or their values; it throws `IllegalAccessException`.
