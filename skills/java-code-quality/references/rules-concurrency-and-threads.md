# Java Rules: Concurrency And Threads

One directive per Java rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never call `Object.wait()` on `Condition` implementations; call `await()`.
- Never catch `IllegalMonitorStateException`; synchronise correctly instead.
- Call `Object.wait()` and `Condition.await()` only within a `while` loop that re-evaluates the awaited condition.
- Never pass a `Thread` instance where a `Runnable` is expected; pass a `Runnable`.
- Never synchronise on `Lock` instances with `synchronized`; call `lock()` and `unlock()`.
- Never use `ThreadGroup`; manage threads with an `ExecutorService`.
- Initialise `ThreadLocal` instances with `ThreadLocal.withInitial` instead of anonymous subclasses that override `initialValue`.
- Never call `Thread.run()` directly; call `start()`.
- Never synchronise on instances of value-based or cached classes (for example `String`, `Integer`, or `Boolean`); synchronise on a dedicated `private final Object` lock.
- Never configure a `ScheduledThreadPoolExecutor` with a `corePoolSize` of 0.
- Override `run()`, or pass a `Runnable` to the constructor, in every class that extends `Thread`.
- Never ignore `InterruptedException` or `ThreadDeath`: rethrow it, or restore the interrupt status with `Thread.currentThread().interrupt()`.
- Never use double-checked locking for lazy initialisation; use a nested `static` class for lazy initialisation, a `synchronized` method, or eager initialisation.
- Never compare `AtomicInteger` or `AtomicLong` instances with `equals()`; compare their `get()` results.
- Release every acquired lock on all execution paths; call `unlock()` in a `finally` block.
- Never call `wait()`, `notify()`, or `notifyAll()` on `Thread` instances.
- Call `wait()`, `notify()`, and `notifyAll()` only within code synchronised on the receiving object.
- Call `wait()` instead of `Thread.sleep()` while retaining a lock.
- Synchronise blocks only on `private final` fields, never on reassignable fields or parameters.
- Call `notifyAll()` instead of `notify()`.
- Never share non-thread-safe objects (for example `SimpleDateFormat` or `Calendar`) via `static` fields.
- Synchronise getters and setters in pairs; never synchronise only one of them.
- Never call `wait()` while retaining more than one lock; it releases only the lock of the receiving object.
- Assign the lazily initialised field as the final step of double-checked locking, after the object is fully constructed.
- Never synchronise on `getClass()`; synchronise on a class literal or a `private final` lock.
- Never declare non-primitive fields `volatile`; use `AtomicReference`, atomic arrays (for example `AtomicIntegerArray`), or synchronisation.
- Never apply compound operators (`++`, `--`, `+=`) to `volatile` variables; use atomic classes or synchronisation.
- Never apply identity-sensitive operations (`==` comparisons or synchronisation) to instances of value-based classes (for example `Optional` or `java.time` types).
- Retain the `synchronized` modifier when overriding a `synchronized` method.
- Call `ThreadLocal.remove()` when the thread-local value is no longer required, particularly in thread pools.
- Run operations that include blocking operations (for example I/O or HTTP requests) on virtual threads instead of platform threads (Java 21).
- Never call `setDaemon`, `setPriority`, or `getThreadGroup` on virtual threads.
- Never run operations containing `synchronized` code on virtual threads on Java versions prior to 24; synchronisation pins the carrier thread (use `ReentrantLock`).
