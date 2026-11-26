# C# Rules: Logging And Diagnostics

One directive per C# rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Use constant message templates with named placeholders in logging calls; never interpolate or concatenate values into the template.
- Never pass `Debug.Assert` an expression that modifies state or calls a mutating method; release builds omit the call.
- Ensure `[DebuggerDisplay]` strings reference only existing members.
- Limit logging calls per code block to 4 debug, 2 information, 1 warning, and 1 error; consolidate the rest.
- When logging within a `catch` clause, pass the caught exception to the logger's exception parameter.
- Pass logging arguments to the intended parameters (exception, event identifier, message template, template arguments); never pass an exception or event identifier as a template argument.
- Name logger fields and properties per `^_?[Ll]og(ger)?$` (for example `logger`, `Logger`, `log`). **Local precedence:** The naming instructions prohibit the underscore prefix; use `logger`.
- Never call `Trace.Write` or `Trace.WriteLine`; use `Trace.TraceInformation`, `Trace.TraceWarning`, `Trace.TraceError`, or a structured logger.
- Inject `ILogger<T>` with `T` equal to the enclosing type.
- Order message template placeholders identically to the supplied arguments.
- Ensure every log message template is syntactically valid: balanced braces, named placeholders, and valid alignment and format specifiers.
- Never pass `TraceSwitch` level properties (for example `traceSwitch.TraceError`) to `Trace.WriteLineIf`; guard a `Trace.WriteLine` call with an `if` on that property.
- Use each placeholder name at most once per log message template.
- Name message template placeholders in PascalCase (for example `{UserId}`).
