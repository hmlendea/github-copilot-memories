# Kotlin Rules: Concurrency And Coroutines

One directive per Kotlin rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never expose `MutableStateFlow` or `MutableSharedFlow` as `public` or `internal` properties; expose read-only `StateFlow` or `SharedFlow` views of `private` mutable properties.
- Respect structured concurrency: never launch coroutines in `GlobalScope` without opting in via `@OptIn(DelicateCoroutinesApi::class)`, and never pass `Job()` to coroutine builders.
- Preserve main-thread safety in suspending functions: execute prolonged blocking calls within `withContext` on an I/O dispatcher, or use suspending alternatives (`delay` instead of `Thread.sleep`).
- Never declare functions returning `Flow` or `Channel` as `suspend`.
- Inject dispatchers via constructor parameters (with `Dispatchers.*` defaults); never hardcode them in `withContext`, `launch`, or `async`.
- Never call a suspending function via `withContext` or `async` on another dispatcher merely to switch threads; correct the main-thread safety of the callee instead.
- Never declare `CoroutineScope` extension functions as `suspend`.
- Launch coroutines in `viewModelScope` from `ViewModel` classes; never expose `suspend` functions from them.
- Use the `Deferred` value returned by functions (via `await()`); never ignore it.
- Implement timeouts with `withTimeout` or `withTimeoutOrNull`, never manually via `delay` and `cancel`.
- Declare a function `suspend` only when its body calls at least one other suspending function.
- Pass every intermediate `Flow` result to a terminal operator (for example `collect`).
- Never configure a `ScheduledThreadPoolExecutor` with a `corePoolSize` of 0.
