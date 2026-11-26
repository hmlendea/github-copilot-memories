# Java Rules: Exceptions And Resources

One directive per Java rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never throw generic exceptions (`Exception`, `RuntimeException`, `Throwable`, `Error`); throw a specific exception type.
- Never override `Object.finalize()`; release resources via try-with-resources or a `Cleaner`.
- Delete superfluous exceptions from `throws` clauses: checked exceptions the method never throws, duplicates, and subtypes of another declared exception.
- Never nest `try`-`catch` blocks; extract the inner block into a dedicated method.
- Never throw exceptions within `finally` blocks.
- Declare every field of an exception class `final`.
- Retain `protected` visibility when overriding `Object.finalize()`; never relax it to `public`.
- Never catch `Throwable` or `Error`; catch specific exception types.
- Never test exception types with `instanceof` within `catch` blocks; declare dedicated `catch` clauses.
- Use try-with-resources for `AutoCloseable` resources instead of closing them in `finally` blocks.
- Log or rethrow a caught exception, never both. **Local precedence:** The error-handling instructions require log-and-rethrow (log the exception, then rethrow it unmodified); retain that policy and report each occurrence.
- Combine `catch` clauses with identical bodies into one multi-catch clause.
- Name classes with the `Exception` suffix only when they extend `Exception` or a subclass of it.
- Delete `catch` clauses that only rethrow the caught exception.
- Delete files with `java.nio.file.Files.delete`, never `File.delete()`, which conceals the reason for a failure.
- Never call `close()` explicitly on resources that try-with-resources manages.
- Never validate the parameters of `public` methods with `assert`; throw `IllegalArgumentException` or `NullPointerException` (for example via `Objects.requireNonNull`).
- Override `write(byte[], int, int)` in every `OutputStream` subclass; the default implementation transfers one byte at a time.
- Override `read(byte[], int, int)` in every `InputStream` subclass; the default implementation transfers one byte at a time.
- Delete `catch` clauses for a checked exception that preceding clauses render unreachable by catching every derived exception the `try` block throws, and delete such concealed types from multi-catch clauses.
- Declare unused exception parameters with the unnamed variable `_` (Java 22).
- Test the status values returned by `File` operations (except `mkdirs`), `Iterator.hasNext()`, `Enumeration.hasMoreElements()`, `Lock.tryLock()`, non-`void` `Condition.await` methods, `CountDownLatch.await(long, TimeUnit)`, `Semaphore.tryAcquire`, and `BlockingQueue.offer` and `remove`.
- Never call `Object.finalize()` explicitly.
- Never exit a `finally` block via `return`, `break`, `continue`, or `throw`.
- Never declare a method named `finalize` with parameters or a non-`void` return type.
- Close every resource (streams, connections, sockets, and other `AutoCloseable` instances) after use, preferably via try-with-resources.
- Never call `runFinalizersOnExit`.
- Test the value returned by `InputStream.read(byte[])` and similar stream reads; never presume they read the requested number of bytes.
- Use the return values of `read` and `readLine`; never discard them.
- Never append to an existing file via an `ObjectOutputStream`; the appended stream header corrupts the file.
- Throw every exception that is created; never instantiate an exception without throwing it.
- Return values from 0 to 255, or -1 when the stream is exhausted, from `InputStream.read()` implementations; never return a signed `byte`.
- Satisfy the documented requirements of every method call (argument values and object state) so that it never throws due to incorrect usage.
