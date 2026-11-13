# MethodScript Function Reference: Statistics

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Provides a set of functions that deal with statistical analysis of numbers.

5 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `average(array / number input...)` -> number (throws CastException; IndexOverflowException) - Returns the average (also known as the arithmetic mean) across all the numbers in the set. The input may be an array of numbers, or individual numbers as arguments.
- `median(array / number input...)` -> number (throws CastException; IndexOverflowException) - Returns the median across all the numbers in the set. The input may be an array of numbers, or individual numbers as arguments.
- `mode(array / number input...)` -> array (throws CastException; IndexOverflowException) - Returns the mode across all the numbers in the set. The input may be an array of numbers, or individual numbers as arguments. The mode of a set of numbers is the values that occur most in the set.
- `percentile(number percentile, array / number percentile, number input...)` -> number (throws CastException; IndexOverflowException; RangeException) - Returns the nth-percentile across all the numbers in the set. The input may be an array of numbers, or individual numbers as arguments.
- `sum(array / number input...)` -> number (throws CastException; IndexOverflowException) - Returns the sum across all the numbers in the set. The input may be an array of numbers, or individual numbers as arguments. The sum is the result of adding all the numbers in the set together.
