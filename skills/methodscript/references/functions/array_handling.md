# MethodScript Function Reference: ArrayHandling

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

43 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `array_clear(array)` -> void (throws CastException) - Clears the array of all values. This keeps the array reference the same, but empties it. Both normal and associative arrays are supported, but the internal type (normal or associative) is not reset.
- `array_contains(array, testValue)` -> boolean (throws CastException) - Checks to see if testValue is in array. For associative arrays, only the values are searched, the keys are ignored.
- `array_contains_ic(array, testValue)` -> boolean (throws CastException) - Works like array_contains, except the comparison ignores case.
- `array_deep_clone(array)` -> array (throws CastException; InsufficientArgumentsException) - Performs a deep clone on an array (as opposed to a shallow clone). This is useful for multidimensional arrays. See the examples for more info.
- `array_every(array, closure)` -> boolean (throws CastException) - Returns true if every value in the array meets some test, which the closure should return true or false about. Not all values will necessarily be checked, once a value is determined to fail the check...
- `array_fill(array, fill)` -> array (throws CastException) - Fills the array fully with the given item. This works with both dynamic and fixed arrays, however with dynamic arrays, it must be a normal array, if the array is associative, a cast exception is throw...
- `array_filter(array, boolean closure(key, value))` -> array (throws CastException) - Filters an array by callback. The items in the array are iterated over, each one sent to the closure one at a time, as key, value.
- `array_get(array, index, [default])` -> mixed (throws CastException; IndexOverflowException) - Returns the element specified at the index of the array. If the element doesn't exist, an exception is thrown. See more...
- `array_get_rand(array)` -> mixed (throws CastException; LengthException) - Returns a random value from an array. If the array is empty a LengthException is thrown.
- `array_implode(array, [glue])` -> string (throws CastException) - Given an array and glue, to-strings all the elements in the array (just the values, not the keys), and joins them with the glue, defaulting to a space.
- `array_index(array, value)` -> mixed (throws CastException) - Works exactly like array_indexes(array, value)[0], except in the case where the value is not found, returns null.
- `array_index_exists(array, index...)` -> boolean (throws CastException) - Checks to see if the specified array has an element at index. If more than one index is specified, then it recursively checks down nested arrays.
- `array_indexes(array, value)` -> array (throws CastException) - Returns an array with all the keys of the specified array at which the specified value is equal. That is, for the array(1, 2, 2, 3), if value were 2, would return array(1, 2).
- `array_insert(array, item, index)` -> void (throws CastException; IndexOverflowException) - Inserts an item at the specified index, and shifts all other items in the array to the right one. If index is greater than the size of the array, an IndexOverflowException is thrown, though the index...
- `array_intersect(array1, array2, [comparisonMode] / array1, array2, comparisonClosure)` -> array (throws CastException; IllegalArgumentException) - Returns an array that is the intersection of the two provided arrays. If either array is associative, it puts the function in associative mode.
- `array_iterate(array, closure)` -> array (throws CastException) - Iterates across an array, calling the closure for each value of the array. The closure should accept two arguments, the key and the value.
- `array_keys(array)` -> array (throws CastException) - Returns the keys in this array as a normal array. If the array passed in is already a normal array, the keys will be 0 -> (array_size(array) - 1)
- `array_last_index(array, value)` -> mixed (throws CastException) - Finds the index in the array where value occurs last. If the value is not found, returns null. That is to say, if the value is contained in an array (even multiple times) the index of the last element...
- `array_map(array, closure)` -> array (throws CastException; IllegalArgumentException) - Calls the closure on each element of an array, and returns an array that contains the results.
- `array_merge(array1, array2, [arrayN...])` -> array (throws InsufficientArgumentsException; CastException) - Merges the specified arrays from left to right, and returns a new array. If the array merged is associative, it will overwrite the keys from left to right, but if the arrays are normal, the keys are i...
- `array_normalize(array)` -> array (throws CastException) - Returns a new normal array, given an associative array. (If the array passed in is not associative, a copy of the array is returned).
- `array_push(array, value, [value2...])` -> void (throws CastException) - Pushes the specified value(s) onto the end of the array. Unlike calling array_set(@array, array_size(@array), @value) on a normal array, the size of the array is increased first.
- `array_push_all(array, values)` -> void (throws CastException) - Pushes all the values of an array individually. If you try to push an array onto array_push, this will give you a two dimensional array, this method pushes the sub values of the values array into the...
- `array_rand(array, [number, [getKeys]])` -> array (throws RangeException; CastException) - Returns a random selection of keys or values from an array. The array may be either normal or associative. Number defaults to 1, and getKey defaults to true.
- `array_reduce(array, closure)` -> mixed (throws CastException; IllegalArgumentException) - Reduces an array to a single value. This is useful for, for instance, summing the values of an array. The previously calculated value, then the next value of the array are sent to the closure, which i...
- `array_reduce_right(array, closure)` -> mixed (throws CastException; IllegalArgumentException) - Reduces an array to a single value. This works in reverse of array_reduce(). This is useful for, for instance, summing the values of an array.
- `array_remove(array, index)` -> mixed (throws RangeException; CastException; PluginInternalException) - Removes an index from an array. If the array is a normal array, all values' indices are shifted left one. If the array is associative, the index is simply removed.
- `array_remove_values(array, value)` -> void (throws CastException) - Removes all instances of value from the specified array. For instance, array_remove_values(array(1, 2, 2, 3), 2) would produce the array(1, 3).
- `array_resize(array, size, [fill])` -> array (throws CastException) - Resizes the given array so that it is at least of size size, filling the blank spaces with fill, or null by default.
- `array_reverse(array)` -> array (throws CastException) - Reverses an array in place. However, if the array is associative, throws a CastException, since associative arrays are more like a map. Returns the array for easy chaining.
- `array_scontains(array, testValue)` -> boolean (throws CastException) - Checks if the array contains a value of the same datatype and value as testValue. For associative arrays, only the values are searched, the keys are ignored.
- `array_set(array, index, value)` -> mixed (throws CastException; IndexOverflowException) - Sets the value of the array at the specified index. The value that was set is returned, to allow for chaining.
- `array_shallow_clone(array)` -> array (throws CastException; InsufficientArgumentsException) - Performs a shallow clone on an array (as opposed to a deep clone). See the examples for more info.
- `array_size(array)` -> int (throws CastException) - Returns the size of this array as an integer.
- `array_some(array, closure)` -> boolean (throws CastException) - Returns true if any value in the array meets some test, which the closure should return true or false about. Not all values will necessarily be checked, once a value is determined to pass the check, e...
- `array_sort(array, [sortType])` -> array (throws CastException; FormatException) - Sorts an array in place, and also returns a reference to the array. See more...
- `array_sort_async(array, [sortType], closure(array))` -> void (throws CastException) - Works like array_sort, but does the sort on another thread, then calls the closure and sends it the sorted array.
- `array_subset_of(array, array)` -> boolean (throws IllegalArgumentException) - Returns true if first array is a subset of second array.
- `array_subtract(array1, array2, [comparisonMode])` -> array (throws CastException; IllegalArgumentException) - Returns a new array, which contains all the values in the left array, which are not present in the right array. comparisonMode defaults to HASH, but may also be EQUALS or STRICT_EQUALS.
- `array_unique(array, [compareTypes])` -> array (throws CastException) - Removes all non-unique values from an array. See more...
- `cslice(from, to)` -> slice (throws CastException) - Dynamically creates an array slice, which can be used with array_get (or the [bracket notation]) to get a range of elements.
- `map_implode(associativeArray, innerGlue, outerGlue)` -> string (throws CastException) - Implodes an associative array. The innerGlue is used to glue the key to the value, and then the outerGlue is used to glue those elements together.
- `range(start, finish, [increment] / finish)` -> array (throws CastException) - Returns an array of numbers from start to (finish - 1) skipping increment integers per count. start defaults to 0, and increment defaults to 1. All inputs must be integers.
