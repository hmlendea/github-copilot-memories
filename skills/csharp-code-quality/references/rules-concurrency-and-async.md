# C# Rules: Concurrency And Async

One directive per C# rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Release every acquired lock (`Monitor`, `Mutex`, `ReaderWriterLock`, `ReaderWriterLockSlim`, `SpinLock`) on every execution route, including exceptions; release it in `finally`.
- Lock only on `private readonly` fields; never lock on a field whose reference can be reassigned.
- Never lock on shared or publicly reachable objects (`this`, `typeof(T)`, `Type` instances, string literals or interned strings); lock on a dedicated `private readonly` lock object.
- Never initialise a `[ThreadStatic]` field inline; the initialiser executes only on the first thread. Initialise it lazily on access or use `ThreadLocal<T>`.
- Apply `[ThreadStatic]` only to `static` fields.
- Never declare `async void` methods except event handlers; return `Task`.
- Never call `Thread.Suspend` or `Thread.Resume`; synchronise with `Monitor`, wait handles, semaphores, or tasks.
- Never lock on objects with weak identity (`string`, `Type`, `MarshalByRefObject`, `Thread`, `ParameterInfo`, `MemberInfo`, `ExecutionEngineException`, `OutOfMemoryException`, `StackOverflowException`).
- Pair every delegate `BeginInvoke` call with `EndInvoke`; prefer `Task.Run`, considering that `BeginInvoke` is unsupported on .NET Core and later.
- Never return `null` from a non-`async` method returning `Task` or `Task<T>`; return `Task.CompletedTask` or `Task.FromResult(...)`.
- Await a `ValueTask` exactly once; never await it concurrently or read its result prior to completion; call `.AsTask()` when multiple consumers are required.
- In `ConcurrentDictionary` factory delegates (`GetOrAdd`, `AddOrUpdate`), use the lambda's key parameter instead of capturing the outer key variable.
- In asynchronous methods, `await` the asynchronous counterpart of a method (for example `ReadAsync`, `SaveChangesAsync`, `Task.Delay`) when one exists, instead of the synchronous call.
- Release a `ReaderWriterLock` or `ReaderWriterLockSlim` with the method corresponding to the acquired mode (`ExitReadLock` for read, `ExitWriteLock` for write).
- Acquire and release a lock within one method; never exit a method holding a lock that another method releases.
