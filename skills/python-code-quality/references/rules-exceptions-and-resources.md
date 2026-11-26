# Python Rules: Exceptions And Resources

One directive per Python rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Order `except` clauses so every clause can catch exceptions; never place a parent exception class prior to its subclass.
- Never raise `Exception` or `BaseException` directly; raise a specific built-in or custom exception.
- Never compose `except` clauses that only re-raise the caught exception; delete them or process the exception within them.
- Raise every exception that is constructed; never construct exceptions without raising them.
- Raise only classes or instances deriving from `BaseException`.
- Catch only classes deriving from `BaseException`.
- Never use boolean expressions (`ValueError or TypeError`) in `except` clauses; use a tuple (`except (ValueError, TypeError):`).
- Never list a subclass in the identical `except` clause as its parent class.
- Never use bare `raise` in `finally` blocks.
- Use bare `raise` only within `except` blocks.
- Set exception `__cause__` only to an exception or `None` (`raise ... from exception`).
- Derive custom exception classes from `Exception` or its subclasses, never directly from `BaseException`.
- Re-raise `SystemExit` when catching it (including via bare `except:` or `except BaseException:`).
- Never re-raise the provided exception within `__exit__`; return a falsy value to propagate it.
- Never catch `ExceptionGroup` or `BaseExceptionGroup` with `except*`.
- Call `open()` with a valid mode string.
