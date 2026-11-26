# JavaScript Rules: Types And Inheritance

One directive per JavaScript rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Delete unused private class members (`#field`, `#method()`).
- Never use wrapper objects for primitives (`new String()`, `new Number()`, `new Boolean()`).
- Never duplicate member names in a class or object literal.
- Never construct an object with `new` without using the result.
- Never declare vacant classes.
- Never access properties of variables whose value is `null` or `undefined`.
- Never return values from setters.
- Never use `this` beyond functions and classes (the global `this`).
- Use `new` only with functions and classes; JSDoc annotations do not qualify a value as a constructor.
- Use `delete` only on object properties, never on variables or functions.
- Call each function either invariably with `new` or invariably without it.
- Never use `in` with primitive operands; use it only on objects.
- Never use `new` with `Symbol` or `BigInt`.
- Invoke `super()` exactly once in every constructor of a derived class, prior to accessing `this`, and never in a non-derived class.
- Compare `typeof` expressions only with valid type names: `'undefined'`, `'object'`, `'boolean'`, `'number'`, `'string'`, `'function'`, `'symbol'`, and `'bigint'`.
- Ensure getters and setters access the field they are named after, and return an explicit value from every getter path (a bare `return;` is prohibited).
- Define a `toString()` method on every object or class that is converted or coerced to a string.
- Never return values from constructors.
- Never modify the prototypes of native objects (`Array.prototype`, `Object.prototype`).
- Delete constructors that are vacant or only forward their arguments to `super()`.
- Use `Object.hasOwn()` rather than `hasOwnProperty()` or `Object.prototype.hasOwnProperty.call()`.
- Never use the `__proto__` property; use `Object.getPrototypeOf()` and `Object.setPrototypeOf()`.
- Use `new` with native constructors that require it (`Object`, `Array`, `Map`, `Set`, `Date`, `Error`, `Promise`, typed arrays), and never with `String`, `Number`, `Boolean`, `Symbol`, or `BigInt`.
- Never access a property recursively from its own getter or setter (`get name() { return this.name; }`).
- Never use `instanceof` with native types; use `typeof` for primitives and `Array.isArray()` for arrays.
- Never assign `this` to a variable (`const self = this`); use arrow functions.
- Compare with `undefined` directly (`value === undefined`) rather than via `typeof value === 'undefined'`.
- Declare class properties as class fields rather than assigning them in the constructor.
- Access methods from prototypes (`Array.prototype.slice.call()`), never from instances (`[].slice.call()`).
