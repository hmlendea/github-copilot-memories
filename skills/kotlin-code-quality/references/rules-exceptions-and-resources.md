# Kotlin Rules: Exceptions And Resources

One directive per Kotlin rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never exit a `finally` block via `return`, `break`, `continue`, or `throw`.
- Express preconditions via `require`, `requireNotNull`, `check`, `checkNotNull`, and `error` instead of explicitly throwing `IllegalArgumentException` or `IllegalStateException`.
- Test the status values returned by `File` operations (except `mkdirs`), `Iterator.hasNext()`, `Enumeration.hasMoreElements()`, `Lock.tryLock()`, non-`Unit` `Condition.await` functions, `CountDownLatch.await(Long, TimeUnit)`, `Semaphore.tryAcquire`, and `BlockingQueue.offer` and `remove`.
- Never call `System.runFinalizersOnExit`; register a shutdown hook via `Runtime.getRuntime().addShutdownHook`.
