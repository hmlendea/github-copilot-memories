# Python Rules: Concurrency And Async

One directive per Python rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never accept timeout parameters in async functions; apply `asyncio.timeout`, `anyio.fail_after`, or `trio.move_on_after` at the caller.
- Use `Event` objects instead of `sleep` polling in async loops.
- Use `sleep_forever()` instead of sleeps exceeding 24 hours.
- Never call `subprocess` in async functions; use `asyncio.create_subprocess_exec`, `trio.run_process`, or `anyio.run_process`.
- Never call `time.sleep` in async functions; use `await asyncio.sleep` or the trio or anyio equivalent.
- Never perform synchronous OS calls (for example `os.wait`) in async functions; use `loop.run_in_executor` or `anyio.to_thread.run_sync`.
- Include a checkpoint (`await`) within every cancellation scope (`anyio.move_on_after`, `anyio.fail_after`, and trio cancel scopes).
- Use `trio.lowlevel.checkpoint()` or `anyio.lowlevel.checkpoint()` instead of `sleep(0)`.
- Never use synchronous file operations (`open()`) in async functions; use `aiofiles`, `anyio.open_file`, or `trio.open_file`.
- Re-raise cancellation exceptions (`asyncio.CancelledError`, `trio.Cancelled`, and the anyio cancellation exception) after cleanup.
- Never use synchronous HTTP clients (for example `requests`) in async functions; use `httpx.AsyncClient` or `aiohttp`.
- Never call `input()` in async functions.
- Retain a reference to the result of `asyncio.create_task()` or `asyncio.ensure_future()`, or use `TaskGroup`, to prevent premature garbage collection.
- Use `await`, `async for`, or `async with` in every `async def` function; otherwise declare it synchronous.
- Never use a TaskGroup or Nursery for a single start call; `await` the function directly.
- Never use `return`, `break`, or `continue` within TaskGroup or Nursery blocks; relocate them after the block, or cancel the scope.
- Use `async with` for asynchronous context managers (`__aenter__` and `__aexit__`).
