# MethodScript Function Reference: Threading

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

This experimental and private API is subject to removal, or incompatible changes, and should not be yet heavily relied on in normal development.

11 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `synchronized(syncObject, code)` -> void (throws NullPointerException) [restricted] - Synchronizes access to the code block for all calls (from different threads) with the same syncObject argument. This means that if two threads will call synchronized('example', <code>), the second cal...
- `x_clear_interrupt()` -> boolean [restricted] - Clears the interrupt status of the current thread. If this call actually cleared the interrupt status, true is returned, if the thread was already not interrupted, false is returned.
- `x_get_current_thread()` -> string [restricted] - Returns the thread id (thread name) of the currently running thread.
- `x_get_lock(mixed lock, Callable action)` -> void (throws NullPointerException) [restricted] - Runs the specified action once the lock is obtained. Note that this lock is the same underlying lock object as used in synchronized().
- `x_interrupt([string id])` -> void [restricted] - Interrupts the thread with the given id, or the current thread if no id is given. When a thread is interrupted, its interrupt status is set to true.
- `x_is_interrupted([string id])` -> boolean [restricted] - Tests whether the thread with the given id (or the current thread if none is provided) is interrupted via x_interrupt. If the thread doesn't exist, or is not alive, false is returned.
- `x_new_thread(id, closure)` -> void (throws CastException) [restricted] - Creates a new thread, named id, and runs the closure on that thread. Note that many operations are not advisable to be run on other threads, and unless otherwise stated, functions are generally not th...
- `x_run_on_main_thread_later(closure)` -> void [restricted] - Runs the closure on the main thread later. If the function call is itself being run from the main thread, then the function still will not block, but it is not an error to call this from the main thre...
- `x_run_on_main_thread_now(closure)` -> mixed [restricted] - Runs the closure on the main thread now, blocking the current thread until it is finished. If the function call is itself being run from the main thread, then the function still will block as expected...
- `x_thread_is_alive(string id)` -> boolean [restricted] - Tests if this thread with the given id is alive. A thread is alive if it has been started and has not yet died.
- `x_thread_join(string id, [int maxWait])` -> void (throws InterruptedException) [restricted] - Waits for the thread with the given id to exit. By default, we wait potentially forever, but if maxWait is specified, we will only wait that many milliseconds.
