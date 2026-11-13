# MethodScript Function Reference: Math

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Provides mathematical functions to scripts

37 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `abs(arg)` -> mixed (throws CastException) - Returns the absolute value of the argument.
- `acos(number)` -> double (throws CastException) - Returns the arc cos of the number
- `add(var1, [var2...])` -> mixed (throws CastException) - Adds all the arguments together, and returns either a double or an integer. Operator syntax is also supported: @a + @b
- `asin(number)` -> double (throws CastException) - Returns the arc sin of the number
- `atan(number)` -> double (throws CastException) - Returns the arc tan of the number
- `atan2(y, x)` -> double (throws CastException) - Returns the angle theta from the conversion of rectangular coordinates (x, y) to polar coordinates (r, theta). This method computes the phase theta by computing an arc tangent of y/x in the range of -...
- `ceil(number)` -> int (throws CastException) - Returns the ceiling of any given number. For example, ceil(3.2) returns 4, and ceil(-1.1) returns -1
- `clamp(value, min, max)` -> float (throws CastException) - Clamps a value between a certain range, inclusive. If the value is less than the min, the min is returned, if it is greater than the max, the max is returned, and if it is between the two values, the...
- `cos(number)` -> double (throws CastException) - Returns the cos of the number
- `cosh(number)` -> double (throws CastException) - Returns the hyperbolic cosine of the number
- `dec(var, [value])` -> ivar (throws CastException) - Subtracts value from var, and stores the new value. Value defaults to 1. Equivalent to --var (or var -= value) in other languages.
- `divide(var1, [var2...])` -> mixed (throws CastException; RangeException) - Divides the arguments from left to right, and returns either a double or an integer. If you divide by zero, a RangeException is thrown. Operator syntax is also supported: 2 / 2
- `expr(expression, [valueArray])` -> double (throws FormatException; CastException; PluginInternalException) - Sometimes, when you need to calculate an advanced mathematical expression, it is messy to write out everything in terms of functions.
- `floor(number)` -> int (throws CastException) - Returns the floor of any given number. For example, floor(3.8) returns 3, and floor(-1.1) returns 2
- `hypot(a, b)` -> number (throws RangeException; CastException) - Given two sides of a right triangle, returns the length of the hypotenuse, using the equation a² + b² = c², where a and b are the arguments provided.
- `inc(var, [x])` -> ivar (throws CastException) - Adds x to var, and stores the new value. Equivalent to ++var in other languages. Expects ivar to be a variable, then returns the ivar, or, if var is a constant number, simply adds x to it, and returns...
- `logarithm(val, [base])` -> double (throws CastException; RangeException) - Return the log of a number to the specified base, or the mathematical constant e if no base is provided (or ln). If val is less than or equal to zero, a RangeException is thrown.
- `math_const(constant)` -> number (throws CastException) - Returns the value of various math constants. The constant argument must be one of the following: NaN, NEGATIVE_INFINITY, INFINITY, DOUBLE_MAX, DOUBLE_MIN, LONG_MAX, LONG_MIN, SHORT_MAX, SHORT_MIN, INT...
- `max(num1, [num2...])` -> number (throws CastException; InsufficientArgumentsException) - Returns the highest number in a given list of numbers. If any of the arguments are arrays, they are expanded into individual numbers, and also compared.
- `min(num1, [num2...])` -> number (throws CastException; InsufficientArgumentsException) - Returns the lowest number in a given list of numbers. If any of the arguments are arrays, they are expanded into individual numbers, and also compared.
- `mod(x, n)` -> int (throws CastException; RangeException) - Returns x modulo n. Throws a RangeException when n is 0. Operator syntax is also supported: @x % @n
- `multiply(var1, [var2...])` -> mixed (throws CastException) - Multiplies the arguments together, and returns either a double or an integer. Operator syntax is also supported: 2 * 2
- `neg(number)` -> number (throws CastException) - Negates a number, essentially multiplying the number by -1
- `postdec(var, [x])` -> ivar (throws CastException) - Subtracts x from var, and stores the new value. Equivalent to var-- in other languages. Expects ivar to be a variable, then returns a copy of the old ivar, , or, if var is a constant number, simply ad...
- `postinc(var, [x])` -> ivar (throws CastException) - Adds x to var, and stores the new value. Equivalent to var++ in other languages. Expects ivar to be a variable, then returns a copy of the old ivar, or, if var is a constant number, simply adds x to i...
- `pow(x, n)` -> double (throws CastException) - Returns x to the power of n. Operator syntax is also supported: @x ** @n
- `rand([] / min/max, [max])` -> mixed (throws RangeException; CastException) - Returns a random number from 0 to max or min to max, depending on usage. Max is exclusive. Min must be less than max. This will return an integer.
- `round(number, [precision])` -> double (throws CastException; RangeException) - Unlike floor and ceil, rounds the number to the nearest double that is equal to an integer. Precision defaults to 0, but if set to 1 or more, rounds decimal places.
- `round15(value)` -> double (throws CastException) - Rounds value to the 15th place. This is useful when doing math using approximations. For instance, sin(math_const('PI')) returns 1.2246467991473532E-16, but sin of pi is actually 0.
- `sin(number)` -> double (throws CastException) - Returns the sin of the number
- `sinh(number)` -> double (throws CastException) - Returns the hyperbolic sine of the number
- `sqrt(number)` -> number (throws RangeException; CastException) - Returns the square root of a number. Note that this is mathematically equivalent to pow(number, .5). Imaginary numbers are not supported, so number must be positive.
- `subtract(var1, [var2...])` -> mixed (throws CastException) - Subtracts the arguments from left to right, and returns either a double or an integer. Operator syntax is also supported: @a - @b
- `tan(number)` -> double (throws CastException) - Returns the tan of the number
- `tanh(number)` -> double (throws CastException) - Returns the hyperbolic tangent of the number
- `to_degrees(number)` -> double (throws CastException) - Converts the number to degrees (which is assumed to have been in radians)
- `to_radians(number)` -> double (throws CastException) - Converts the number to radians (which is assumed to have been in degrees)
