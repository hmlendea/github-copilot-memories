# C# Rules: Strings, Numbers And Dates

One directive per C# rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Use capital literal suffixes (`L`, `U`, `UL`, `F`, `D`, `M`); a minuscule `l` resembles `1`.
- Never hardcode absolute URIs or file system paths; read them from configuration or compose them from configurable base values.
- Extract a string literal repeated 3 or more times in a file into a named constant. Exempt: literals with fewer than 5 characters, literals identical to a parameter name, and attribute arguments.
- Never compare `float` or `double` values with `==` or `!=`; compare the absolute difference with a tolerance.
- Never concatenate strings with `+` or `+=` within a loop; use `StringBuilder`, `string.Join`, or `string.Concat`.
- Never shift an integral value by zero or by at least its bit width; shift `int` by 1-31 and `long` by 1-63.
- Never assign an integer division result to a floating-point variable; cast an operand to `double`, `float`, or `decimal` prior to dividing.
- Never compare a value with a constant beyond its type's interval (for example `byte b; b < 0`, or a `float` compared with `double.MaxValue`).
- Ensure composite format strings (`string.Format`, `StringBuilder.AppendFormat`, `Console.WriteLine`) contain valid indices and alignment/format components, and reference only supplied arguments.
- Delete bit operations with no effect (`x & -1`, `x | 0`, `x ^ 0`).
- Use escape sequences (for example `\t`, `\u00A0`) instead of literal tabs, control characters, or non-breaking spaces in string literals.
- Never compare with `double.NaN` or `float.NaN` via `==` or `!=`; use `double.IsNaN` or `float.IsNaN`.
- Compare `IndexOf` results with `-1` (`>= 0` or `< 0`), never `> 0`, which overlooks index 0; prefer `Contains` when the index is unused.
- Separate SQL keywords and identifiers with whitespace when concatenating query fragments (for example `"SELECT * FROM t " + "WHERE id = @id"`).
- Consume every `StringBuilder` (for example via `ToString()`); delete unused builders.
- Use `string.IsNullOrEmpty(s)` or `s.Length == 0` instead of `s == ""` or `s.Equals("")`.
- Ensure the right operand of `<<` and `>>` is an `int` or implicitly convertible to `int`, including `dynamic` operands.
- Never call `ToCharArray()` on a string or `ToArray()` on a `ReadOnlySpan<T>` only to iterate or index it; iterate or index the string or span directly.
- Use composite format strings correctly: indices start at 0 and correspond to supplied arguments, and every string passed to a formatting method contains placeholders.
- Prevent arithmetic overflow; use a wider type, a `checked` context, or explicit bounds checks.
- Never use `new Guid()` where a unique identifier is intended; use `Guid.NewGuid()`, or `Guid.Empty` when a zero value is intended.
- Use the start-index overloads of `IndexOf`, `LastIndexOf`, and similar methods instead of calling `Substring` first.
- Ensure every regular expression is syntactically valid.
- Measure elapsed time with `Stopwatch`, never with `DateTime.Now` differences.
- Specify `DateTimeKind` when constructing `DateTime` instances.
- Pass time zone identifiers directly to `TimeZoneInfo.FindSystemTimeZoneById` (.NET 6 and later converts IANA and Windows identifiers); never convert them first with `TimeZoneConverter`.
- Pass a format provider (for example `CultureInfo.InvariantCulture`) when parsing dates and times (`Parse`, `TryParse`, `ParseExact`, and `TryParseExact` on `DateTime`, `DateTimeOffset`, `DateOnly`, `TimeOnly`, `TimeSpan`).
- Use `DateTime.UnixEpoch` or `DateTimeOffset.UnixEpoch` instead of constructing 1970-01-01 manually.
- Use the `char` overloads of `StartsWith` and `EndsWith` for single-character arguments.
- Use `string.Create(CultureInfo.InvariantCulture, $"...")` instead of `FormattableString.Invariant(...)` or other `FormattableString` formatting.
