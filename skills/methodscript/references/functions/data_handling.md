# MethodScript Function Reference: DataHandling

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

41 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `array([var1, [var2...]])` -> array - Creates an array of values.
- `assign([type], ivar, mixed)` -> ivariable (throws CastException) - Accepts an ivariable ivar as a parameter, and puts the specified value mixed in it. Returns the variable that was assigned. Operator syntax is also supported: <code>@a = 5;</code>.
- `associative_array([args...])` -> array - Works exactly like array(), except the array created will be an associative array, even if the array has been created with no elements.
- `boolean(item)` -> boolean - Returns a new construct that has been cast to a boolean. The item is cast according to the boolean conversion rules.
- `closure([params...], code)` -> closure [restricted] - Returns a closure on the provided code. A closure is a datatype that represents some code as code, not the results of some code after it is run.
- `double(item)` -> double (throws CastException) - Returns a new construct that has been cast to an double. This function will throw a CastException if is_numeric would return false for this item, but otherwise, it will be cast properly.
- `eval(script_string)` -> string (throws CastException; InsufficientPermissionException) [restricted] - Executes arbitrary MethodScript. Note that this function is very experimental, and is subject to changing or removal.
- `execute([values...], callable)` -> mixed (throws CastException) [restricted] - Executes the given closure or other Callable. You can also send arguments to the Callable, which it may or may not use, depending on the particular Callable's definition.
- `execute_array(valueArray, closure)` -> mixed (throws CastException) [restricted] - Executes the given closure, expanding the value array as individual arguments to the closure. If there are no arguments to be sent to the closure, an empty array can be sent.
- `executeas(sender, label, [values...], closure)` -> mixed (throws CastException) [restricted] - Executes the given closure in the context of a given player or ~console. A closure that runs player(), for instance, would return the specified player's name.
- `export(key, value)` -> void (throws IllegalArgumentException; IndexOverflowException) [restricted] - Stores a value in the global storage register. An arbitrary value is stored with the given key, and can be retrieved using import. If the value is already stored, it is overwritten. See import.
- `fixed_array(ClassType type, int size, [boolean nullOut])` -> fixed_array (throws RangeException; CastException) - Creates an array that can hold values of the given type, and is of the given size. The array cannot be resized or retyped later. The array cannot be associative.
- `g(func1, [func2...])` -> string - Groups any number of functions together, and returns void.
- `get_proc(reference)` -> Procedure (throws IllegalArgumentException) [restricted] - Returns a first class reference to the currently in scope procedure. This can be stored in variables and generally passed around, though it cannot be serialized.
- `iclosure([params...], code)` -> iclosure [restricted] - Returns a scope isolated closure on the provided code. An iclosure is a datatype that represents some code as code, not the results of some code after it is run.
- `import(key, [default])` -> mixed (throws IllegalArgumentException; IndexOverflowException) [restricted] - This function imports a value from the global value register. It looks for a value stored with the specified key (using the export function), and returns that value.
- `include(path)` -> void (throws IncludeException; IOException) - Includes external code at the specified path.
- `include_dir(directory, [recursive])` -> nothing - Works like include, but takes a directory, and includes all files within the directory. Recursive defaults to false, but if true, recurses down into all subdirectories as well.
- `instanceof(value, type)` -> boolean - Checks to see if the value is, extends, or implements the given type. Keyword usage is preferred: <code>@value instanceof int</code>. The opposite operation is <code>@value notinstanceof int</code>.
- `integer(item)` -> integer (throws CastException) - Returns a new construct that has been cast to an integer. This function will throw a CastException if is_numeric would return false for this item, but otherwise, it will be cast properly.
- `is_array(item)` -> boolean - Returns whether or not the item is an array
- `is_associative(array)` -> boolean (throws CastException) - Returns whether or not the array is associative. If the parameter is not an array, throws a CastException.
- `is_boolean(item)` -> boolean - Returns whether the given item is of the boolean datatype. Note that all datatypes can be used as booleans, however this function checks the specific datatype of the given item.
- `is_bytearray(item)` -> boolean - Returns whether or not the item is actually a ByteArray datatype.
- `is_closure(arg)` -> boolean - Returns true if the argument is a closure (could be executed) or false otherwise
- `is_double(item)` -> boolean - Returns whether or not the given item is a double. Note that numeric strings and integers can usually be used as a double, however this function checks the actual datatype of the item.
- `is_integer(item)` -> boolean - Returns whether or not the given item is an integer. Note that numeric strings can usually be used as integers, however this function checks the actual datatype of the item.
- `is_integral(item)` -> boolean (throws CastException) - Returns true if the numeric value represented by a given double or numeric string could be cast to an integer without losing data (or if it's an integer).
- `is_null(item)` -> boolean - Returns whether or not the given item is null.
- `is_number(item)` -> boolean - Returns whether or not the given item is an integer or a double. Note that numeric strings can usually be used as integers and doubles, however this function checks the actual datatype of the item.
- `is_numeric(item)` -> boolean - Returns false if the item would fail if it were used as a numeric value. If it can be parsed or otherwise converted into a numeric value, true is returned.
- `is_proc(procName)` -> boolean [restricted] - Returns whether or not the given procName is currently defined, i.e. if calling this proc wouldn't throw an exception.
- `is_string(item)` -> boolean - Returns whether or not the item is actually a string datatype. If you just care if some data can be used as a string, use is_stringable().
- `is_stringable(item)` -> boolean - Returns whether or not the item is convertable to a string. Everything but arrays can be used as strings.
- `mutable_primitive([primitive_value])` -> mutable_primitive (throws FormatException) - Creates a mutable primitive object, initially setting the value of the object to null, or the specified value. The value must be a primitive value, and cannot be an array or object. See more...
- `parse_int(value, radix)` -> int (throws CastException; RangeException; FormatException) - Converts a string representation of an integer to a real integer, given the value's radix (base). See to_radix for a more detailed explanation of number theory.
- `proc(procName, [params...], procCode)` -> void (throws FormatException) - Creates a new user defined procedure (also known as "function"), with the given name and parameters, that can be called later in code.
- `rclosure([params...], code)` -> closure [restricted] - Returns a non-linking closure on the provided code. The same rules apply for closures, except the top level internal code does not check for proper linking at compile time, and instead links at runtim...
- `string(item)` -> string - Creates a new construct that is the "toString" of an item. For arrays, an human readable version is returned; this should not be used directly, as the format is not guaranteed to remain consistent.
- `to_radix(value, radix)` -> string (throws CastException; RangeException; FormatException) - Given an int and a radix, returns a string representation of the integer value in the given base. A common use would be to output a hex or binary representation of a number, for instance. See more...
- `typeof(arg)` -> ClassType - Returns a ClassType value of the typeof a value. For instance 'array' is returned for typeof(array()). This is a generic replacement for the is_* series of functions.
