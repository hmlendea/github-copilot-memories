# JavaScript Rules: Collections And Arrays

One directive per JavaScript rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never test `indexOf()` results for positivity (`> 0`); compare with `-1` or use `includes()`.
- Never use `delete` on array elements; use `splice()`.
- Provide a compare function to every `sort()` and `toSorted()` call on arrays not composed of strings.
- Use only numeric indexes with arrays; use objects or `Map` for string keys.
- Return a value from every callback passed to array methods (`map()`, `filter()`, `reduce()`, `find()`, `every()`, `some()`, `sort()`).
- Never perform collection size or array length comparisons that are invariably true or false (`length >= 0`, `size < 0`).
- Never populate a collection without reading its contents.
- Never assign or use the result of `reverse()` or `sort()` as if it were a copy; use `toReversed()` or `toSorted()`.
- Use `for…of` rather than index-based `for` loops to iterate iterables when the index is unused.
- Never create sparse arrays with consecutive commas (`[1, , 3]`).
- Never overwrite a collection element unconditionally without reading it in between (`list[index] = a; list[index] = b;`).
- Never access or iterate collections that are invariably vacant.
- Never use `in` on arrays; use `includes()` to test for values.
- Use object spread syntax (`{ ...a, ...b }`) rather than `Object.assign()` with an object literal as the first argument.
- Provide an initial value to every `reduce()` and `reduceRight()` call.
- Use operands of a consistent type in conditional expressions within array spread syntax (`...(condition ? [1, 2] : [])`), never `''` as the alternative.
- Never pass function references directly to iterator methods (`array.map(parseInt)`); wrap them in an arrow function (`array.map(value => parseInt(value))`).
- Never pass the `thisArg` parameter to array methods; use arrow functions.
- Never include fallback objects in object spread syntax (`{ ...(value || {}) }`); use `{ ...value }`.
- Never check array length prior to `some()` or `every()` (`array.length > 0 && array.some(…)`).
- Never use spread syntax unnecessarily: on literals, on iterables passed to APIs accepting iterables (`Set`, `Map`, `Promise.all()`, `Array.from()`), or on `for…of` operands.
- Use `find()` or `findLast()` rather than `filter()` to retrieve a single element.
- Flatten arrays with `flat()`, not `reduce()` with `concat()` or spread syntax.
- Use `flatMap()` rather than `map().flat()`.
- Use `indexOf()` or `lastIndexOf()` rather than `findIndex()` or `findLastIndex()` for simple equality searches.
- Use `some()` rather than `filter().length` checks or `find()` to test for existence.
- Use `at()` rather than complex index expressions (`array[array.length - 1]`).
- Use `includes()` rather than `indexOf()` or `lastIndexOf()` comparisons for existence checks.
- Use negative indices (`slice(-2)`, `at(-1)`) rather than `length` arithmetic (`slice(array.length - 2)`).
- Use a `Set` rather than an array when the collection serves only for existence checks.
- Read the size of a `Set` via `size`, never by converting it to an array (`[...set].length`).
- Combine consecutive calls to methods that accept multiple arguments (`push()`, `classList.add()`, `classList.remove()`, `importScripts()`) into one call.
