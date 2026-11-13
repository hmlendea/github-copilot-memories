# MethodScript Function Reference: ExecutionQueue

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

An execution queue is a queue of closures, which are queued up to be run in sequence by the engine. Unlike set_timeout and set_interval, there is no time component, it's simply a queue of operations to execute sequentially. See the article on the learning trail for more information.

8 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `queue_clear([queue])` -> void [restricted] - Clears out all tasks that are on the queue. If no tasks were on the queue, nothing happens.
- `queue_delay(x, [queue])` -> void (throws CastException; RangeException) [restricted] - Queues up a non-disruptive sleep at the end of the queue. This task will stall the execution thread for x milliseconds.
- `queue_delay_front(x, [queue])` -> void (throws CastException; RangeException) [restricted] - Works like queue_delay, but puts the delay at the front of the queue.
- `queue_push(closure, [queue])` -> void (throws CastException) [restricted] - Queues a task up at the end of the specified queue.
- `queue_push_front(closure, [queue])` -> void (throws CastException) [restricted] - Queues a task at the front of the queue.
- `queue_remove([queue])` -> void [restricted] - Removes the last task at the end of the queue from the queue.
- `queue_remove_front([queue])` -> void [restricted] - Removes a task from the front of the queue. That is, the next task that would have been run is removed.
- `queue_running([queue])` -> boolean [restricted] - Returns true if the specified queue still has tasks running on it.
