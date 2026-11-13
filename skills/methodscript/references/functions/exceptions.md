# MethodScript Function Reference: Exceptions

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

5 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `complex_try(tryBlock, [catchVariable, catchBlock]+, [catchBlock])` -> void - 
- `get_stack_trace()` -> array [restricted] - Returns an array of stack trace elements. This is the same stack trace that would be generated if one were to throw an exception, then catch it.
- `set_uncaught_exception_handler(closure(@ex))` -> closure (throws CastException) [restricted] - Sets the uncaught exception handler, returning the currently set one, or null if none has been set yet. If code throws an exception, instead of doing the default (displaying the error to the user/cons...
- `throw(exceptionType, msg, [causedBy] / exception)` -> nothing (throws FormatException) - This function causes an exception to be thrown. The exceptionType may be any valid exception type. See more...
- `try(tryCode, [varName, catchCode, [exceptionTypes]] / tryCode, catchCode)` -> void (throws CastException; FormatException) - This function works similar to a try-catch block in most languages. If the code in tryCode throws an exception, instead of killing the whole script, it stops running, and begins running the catchCode...
