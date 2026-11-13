# MethodScript Function Reference: Scheduling

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

11 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `clear_cron([cronID])` -> void (throws RangeException; CastException) [restricted] - Clears the previously registered cron job from the registered list. This will prevent the task from running again in the future.
- `clear_task([id])` -> void (throws CastException; InsufficientArgumentsException; NullPointerException) [restricted] - Stops the interval or timeout that is specified. The id can be gotten by storing the integer returned from either set_timeout or set_interval. An invalid id is simply ignored.
- `get_system_timezones()` -> array<string> [restricted] - Returns a list of time zones registered on this system.
- `nano_time()` -> int - Returns an arbitrary number based on the most accurate clock available on this system. Only useful when compared to other calls to nano_time(). The return is in nano seconds.
- `parse_date(dateFormat, dateString, [locale])` -> int (throws FormatException) - Parses a date string, and returns an integer timestamp representing that time. This essentially works in reverse of simple_date.
- `set_cron(cronFormat, closure)` -> int (throws CastException; FormatException) [restricted] - Sets a task to occur at a regular interval, given a cron style interval. This allows for an easier way to specify that a task should happen, for instance, every hour on the hour.
- `set_interval(int timeInMS, [int initialDelayInMS,] Callable task)` -> int (throws CastException; RangeException) [restricted] - Sets a task to run every so often. This works similarly to set_timeout, except the task will automatically re-register itself to run again.
- `set_timeout(timeInMS, closure)` -> int (throws CastException; RangeException) [restricted] - Sets a task to run in the specified number of ms in the future. The task will only run once. Note that the resolution of the time is in ms, however, the server will only have a resolution of up to 50...
- `simple_date(format, [time, [timezone, [locale]]])` -> mixed (throws CastException; FormatException) - Returns a date of the current time (or the time specified) in the format you give. See more...
- `sleep(seconds)` -> void (throws CastException; InterruptedException) [restricted] - Sleeps the script for the specified number of seconds, up to the maximum time limit defined in the preferences file. Seconds may be a double value, so 0.5 would be half a second.
- `time()` -> int - Returns the current unix time stamp, in milliseconds. The resolution of this is not guaranteed to be extremely accurate. If you need extreme accuracy, use nano_time()
