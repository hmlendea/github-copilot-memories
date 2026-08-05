---
description: "Use when writing or editing any code. Covers exception handling and error management best practices."
applyTo: "**/*.{c,cpp,cs,h,java,js,jsx,py,sh,ts,tsx}"
---

## Exception Handling

- Use the log-and-rethrow pattern: catch an exception, log it, then rethrow it without modifying the exception. This preserves the original stack trace and error context.
- When throwing exceptions, always pass as much detail as possible: include the relevant value(s), parameter name(s), and a descriptive message that clearly identifies what was invalid or missing and why. Help the developer understand the problem immediately without having to inspect the call stack or surrounding code.
- Prefer safe type conversion over exceptions when the conversion may fail. Use direct conversions that throw only when you are certain of the type and want an exception on failure.
