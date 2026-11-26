# C# Rules: Exceptions And Disposal

One directive per C# rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never throw general or reserved exceptions (`Exception`, `SystemException`, `ApplicationException`, `IndexOutOfRangeException`, `NullReferenceException`, `OutOfMemoryException`, `ExecutionEngineException`); throw the most specific applicable exception.
- Never throw from a finaliser; an exception escaping a finaliser terminates the process.
- Never throw from a `finally` block; it masks the original exception.
- Never call `GC.Collect()`; rely on the garbage collector.
- Never catch `NullReferenceException`; prevent the dereference with a null check.
- Either log a caught exception and conclude processing there, or rethrow or wrap it (with the original as `innerException`) without logging; never log and rethrow. **Local precedence:** Local policy deviation: the [error-handling instructions](../../../instructions/csharp/csharp.error-handling.instructions.md) require log-and-rethrow (log securely, then `throw;`). Retain that policy and report each conflicting occurrence instead of deleting the log or the rethrow.
- Name a class with the suffix `Exception` only when it derives from `Exception`.
- Never throw from property getters except `NotImplementedException`, `NotSupportedException`, and `InvalidOperationException`; use a method for retrieval that can throw other exceptions.
- Never catch an exception and ignore it silently; log it, rethrow it, or explain the intentional suppression in a comment.
- Use the count returned by `Stream.Read`/`ReadAsync`; never presume the entire buffer was populated. Use `ReadExactly` or `ReadAtLeast` when a complete buffer is required.
- Delete `catch` clauses that only rethrow (`catch { throw; }`); let the exception propagate.
- Dispose every locally created `IDisposable` with `using`; dispose `IDisposable` fields in the containing type's `Dispose`.
- Name a method `Dispose` only when it implements `IDisposable.Dispose`.
- Never return an `IDisposable` created by a `using` statement or declaration; it is disposed prior to the caller receiving it.
- Rethrow with `throw;`, never `throw ex;`, which resets the stack trace.
- Declare custom exception types `public`.
- Never throw from `ToString`, `Equals`, `GetHashCode`, `Dispose`, event accessors, static constructors, module initialisers, equality operators, or implicit conversion operators. Exempt: `NotImplementedException`; in event accessors also `InvalidOperationException`, `NotSupportedException`, and `ArgumentException`.
- Implement `IDisposable` via the standard dispose method: `Dispose()` calls `Dispose(true)` then `GC.SuppressFinalize(this)`, unsealed types declare `protected virtual void Dispose(bool disposing)`, any finaliser calls `Dispose(false)`, and derived types override `Dispose(bool)` rather than re-implementing `IDisposable`.
- Pass only names of genuine parameters to the `paramName` argument of `ArgumentException` and its subclasses, preferably via `nameof`.
- Never dispose an object more than once (for example an explicit `Dispose()` plus `using`).
- Call `GC.SuppressFinalize(this)` only within the `Dispose()` implementation.
- Never create an exception without throwing it.
- In `yield`-based iterator methods, validate arguments in a non-iterator wrapper method so exceptions surface at the call, not at enumeration.
- In `async` methods, validate arguments in a non-`async` wrapper method so argument exceptions surface synchronously at the call.
