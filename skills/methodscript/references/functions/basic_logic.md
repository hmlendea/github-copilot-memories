# MethodScript Function Reference: BasicLogic

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

These functions provide basic logical operations.

31 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `and(var1, [var2...])` -> boolean (throws CastException) - Returns the boolean value of a logical AND across all arguments. Uses lazy determination, so once an argument returns false, the function returns. Operator syntax is supported: @a && @b
- `bit_and(int1, int2, [int3...])` -> int (throws CastException; InsufficientArgumentsException) - Returns the bitwise AND of the values
- `bit_not(int1)` -> int (throws CastException) - Returns the bitwise NOT of the given value
- `bit_or(int1, int2, [int3...])` -> int (throws CastException; InsufficientArgumentsException) - Returns the bitwise OR of the specified values
- `bit_xor(int1, int2, [int3...])` -> int (throws CastException; InsufficientArgumentsException) - Returns the bitwise exclusive OR of the specified values
- `compile_error(message)` -> nothing [restricted] - Throws a compile error unconditionally at link time, if the function has not been fully compiled out with preprocessor directives.
- `dand(...)` -> mixed - Returns the first falsey value. The arguments to this function are lazily evaluated, so if the first value evaluates to falsey, the rest of the arguments will not be evaluated.
- `dor(...)` -> mixed - Returns the first true value. The arguments to this function are lazily evaluated, so if the first value evaluates to true, the rest of the arguments will not be evaluated.
- `equals(var1, var2[, varX...])` -> boolean (throws InsufficientArgumentsException) - Returns true if all the arguments are equal. Operator syntax is also supported: @a == @b
- `equals_epsilon(double d1, number d2, double epsilon / number d1, double d2, double epsilon)` -> boolean (throws CastException) - When comparing the equality of floating point numbers, it is often impossible to directly compare via == (equals) since two floating point numbers that might be actually semantically equivalent, are r...
- `equals_ic(val1, val2[, valX...])` -> boolean (throws InsufficientArgumentsException) - Returns true if all the values are equal to each other, while ignoring case.
- `gt(var1, var2)` -> boolean (throws CastException) - Returns the result of a greater than operation. Operator syntax is also supported: @a > @b
- `gte(var1, var2)` -> boolean (throws CastException) - Returns the result of a greater than or equal to operation. Operator sytnax is also supported: @a >= @b
- `hash(value)` -> int - Hashes the value, and returns an int representing that value.
- `lshift(value, bitsToShift)` -> int (throws CastException) - Left shifts the value bitsToShift times
- `lt(var1, var2)` -> boolean (throws CastException) - Returns the results of a less than operation. Operator syntax is also supported: @a < @b
- `lte(var1, var2)` -> boolean (throws CastException) - Returns the result of a less than or equal to operation. Operator syntax is also supported: @a <= @b
- `nand(val1, [val2...])` -> boolean (throws CastException) - Return the equivalent of not(and())
- `nequals(val1, val2)` -> boolean - Returns true if the two values are NOT equal, or false otherwise. Equivalent to not(equals(val1, val2)). Operator syntax is also supported: @a != @b
- `nequals_ic(val1, val2)` -> boolean - Returns true if the two values are NOT equal to each other, while ignoring case.
- `nor(val1, [val2...])` -> boolean (throws CastException) - Returns the equivalent of not(or())
- `not(var1)` -> boolean (throws CastException) - Returns the boolean value of a logical NOT for this argument. Operator syntax is also supported: !@var
- `or(var1, [var2...])` -> boolean (throws CastException) - Returns the boolean value of a logical OR across all arguments. Uses lazy determination, so once an argument resolves to true, the function returns. Operator syntax is also supported: @a \|\| @b
- `ref_equals(val1, val2)` -> boolean - Returns true if and only if the two values are actually the same reference. Primitives that are equal will always be the same reference, this method is only useful for object/array comparisons.
- `rshift(value, bitsToShift)` -> int (throws CastException) - Right shifts the value bitsToShift times
- `sequals(val1, val2)` -> boolean - Uses a strict equals check, which determines if two values are not only equal, but also the same type. So, while equals('1', 1) returns true, sequals('1', 1) returns false, because the first one is a...
- `sequals_ic(value1, value2)` -> boolean - Returns true if the values are the same type, as well as equal, according to equals_ic. Generally, equals_ic will suffice, because usually you will be comparing two strings, however, this function may...
- `snequals(val1, val2)` -> boolean - Equivalent to not(sequals(val1, val2)). Operator syntax is also supported: @a !== @b
- `urshift(value, bitsToShift)` -> int (throws CastException) - Right shifts value bitsToShift times, pushing a 0, making this an unsigned right shift.
- `xnor(val1, val2)` -> boolean (throws CastException) - Returns the xnor of the two values
- `xor(val1, val2)` -> boolean (throws CastException) - Returns the xor of the two values.
