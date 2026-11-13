# MethodScript Function Reference: ObjectManagement

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Provides functions for creating and using objects. None of these methods should normally be used, all of them provide easier to use compiler support.

2 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `define_object(AccessModifier accessModifier, array objectModifiers, ObjectType objectType, string objectName, array superclasses, array interfaces, ? enumList, map elementList, array annotations, ClassType containingClass, string classComment, array genericParameters)` -> void (throws ClassDefinitionError) [restricted] - Defines a new object. Not meant for normal use.
- `new_object(ClassType type, params...)` -> T - Constructs a new object of the specified type. The type must be hardcoded.
