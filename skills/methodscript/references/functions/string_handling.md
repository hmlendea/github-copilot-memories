# MethodScript Function Reference: StringHandling

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

These class provides functions that allow strings to be manipulated

32 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `char_from_unicode(unicode)` -> string (throws CastException; RangeException) - Returns the unicode character for a given unicode value. This is meant for dynamic input that needs converting to a unicode character, if you're hardcoding it, you should just use '\u1234' syntax inst...
- `char_is_uppercase(char)` -> boolean (throws FormatException; CastException) - Determines if the character provided is uppercase or not. The string must be exactly 1 character long and a letter, otherwise a FormatException is thrown.
- `concat(var1, [var2...])` -> string - Concatenates any number of arguments together, and returns a string
- `decrypt_secure_string(string)` -> array (throws CastException) [restricted] - Decrypts a secure_string into a char array. To keep backwards compatibility with strings in general, this function also accepts normal strings, which are not decrypted, but instead simply returned in...
- `length(str / Sizeable)` -> int - Returns the character length of str, if the value is castable to a string, or the length of the ms.lang.Sizeable object, if an array or other Sizeable object is given.
- `levenshtein(string1, string2)` -> int - Returns the levenshtein distance of two character sequences. For instance, "123" and "133" would have a string distance of 1, while "123" and "123" would be 0, since they are the same string.
- `lsprintf(locale, formatString, parameters... / locale, formatString, array(parameters...))` -> string (throws FormatException; InsufficientArgumentsException; CastException) - Returns a string formatted to the given formatString specification, using the parameters passed in. Locale should be a string in format, for instance, en_US, nl_NL, no_NO...
- `parse_args(string, [useAdvanced])` -> array - Parses string into an array, where string is a space seperated list of arguments. Handy for turning $ into a usable array of items with which to script against.
- `replace(subject, search, replacement)` -> string - Replaces all instances of 'search' with 'replacement' in 'subject'
- `sconcat(var1, [var2...])` -> string - Concatenates any number of arguments together, but puts a space between elements
- `secure_string(charArray / string)` -> secure_string (throws FormatException) - Constructs a secure_string from a given char array or string. See more...
- `split(split, string, [limit])` -> array (throws CastException) - Splits a string into parts, using the split as the index. Though it can be used in every single case you would use reg_split, this does not use regex, and therefore can take a literal split expression...
- `sprintf(formatString, parameters... / formatString, array(parameters...))` -> string (throws FormatException; InsufficientArgumentsException; CastException) - Returns a string formatted to the given formatString specification, using the parameters passed in. The formatString should be formatted according to [http://docs.oracle.com/javase/6/docs/api/java/uti...
- `string_append(Resource, toAppend...)` -> void (throws CastException) [restricted] - Appends any number of values to the underlying string builder. This is much more efficient than doing normal concatenation with a string when building a string in a loop.
- `string_compare(string s1, string s2)` -> int - Compares two strings lexicographically. The comparison is based on the Unicode value of each character in the strings.
- `string_compare_ic(string s1, string s2)` -> int - Compares two strings lexicographically ignoring casing. The comparison is based on the Unicode value of each character in the strings.
- `string_contains(haystack, needle)` -> boolean (throws NullPointerException) - Returns true if the string needle is found anywhere within the string haystack. This is functionally equivalent to string_position(@haystack, @needle) != -1, but is generally clearer.
- `string_contains_ic(haystack, needle)` -> boolean (throws NullPointerException; FormatException) - Returns true if the string needle is found anywhere within the string haystack (while ignoring case). This is functionally equivalent to string_position(to_lower(@haystack), to_lower(@needle)) != -1...
- `string_ends_with(teststring, keyword)` -> boolean (throws NullPointerException) - Determines if the provided teststring ends with the provided keyword. Note that this will cast both arguments to strings.
- `string_from_bytes(byte_array, [encoding])` -> string (throws CastException; FormatException) - Returns a new string, given the byte array encoding provided. The encoding defaults to UTF-8, but may be specified. A FormatException is thrown if the encoding type is invalid.
- `string_get_bytes(string, [encoding])` -> byte_array (throws CastException; FormatException) - Returns this string as a byte_array, encoded using the specified encoding, or UTF-8 if no encoding is specified. Valid encodings are the encoding types that java supports.
- `string_multiply(string, times)` -> string (throws RangeException; CastException) - Multiplies a string the given number of times. For instance, string_multiply('a', 3) returns 'aaa'. If the string is empty, an empty string is returned. If the string is null, null is returned.
- `string_position(haystack, needle)` -> int (throws NullPointerException) - Finds the numeric position of the first occurrence of needle in haystack. haystack is the string to search in, and needle is the string to search with.
- `string_starts_with(teststring, keyword)` -> boolean (throws NullPointerException) - Determines if the provided teststring starts with the provided keyword. This could be used to find the prefix of a line, for instance. Note that this will cast both arguments to strings.
- `substr(str, begin, [end])` -> string (throws RangeException; CastException) - Returns a substring of the given string str, starting from index begin, to index end, or the end of the string, if no index is given.
- `to_lower(str)` -> string (throws FormatException) - Returns an all lower case version of str
- `to_upper(str)` -> string (throws FormatException) - Returns an all caps version of str
- `trim(s)` -> string - Returns the string s with leading and trailing whitespace cut off
- `triml(s)` -> string - Returns the string s with leading whitespace cut off
- `trimr(s)` -> string - Returns the string s with trailing whitespace cut off
- `unicode_from_char(character)` -> int (throws CastException; RangeException) - Returns the unicode code point for a given character. The character is a string, but it should only be 1 code point character (which may be length(@character) == 2).
- `uuid(type, arg)` -> string (throws CastException) - Returns a UUID (also known as a GUID). Different types of UUIDs can be generated, by default, if no parameters are provided, a random uuid is returned (version 4).
