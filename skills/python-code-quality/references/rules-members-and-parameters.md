# Python Rules: Members And Parameters

One directive per Python rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Declare at most 13 parameters per function, method, or lambda.
- Pass arguments corresponding in number and name to the function's parameters.
- Never pass an argument more than once (positionally and by keyword, or via unpacking).
- Never overwrite a parameter's initial value prior to reading it.
- Never mutate or reassign mutable default parameter values; default to `None` and construct the value within the function.
- Delete unused function parameters; overriding methods are exempt.
- Delete unused class-private methods (named `__name`).
- Delete unread private attributes (double-underscore names); single-underscore attributes are exempt.
- Delete unused private nested classes.
- Delete unused nested functions and classes.
- Never declare functions or methods with vacant bodies; raise `NotImplementedError` or include a comment explaining the reason. Abstract methods (`abc.abstractmethod`) are exempt.
- Never implement two functions or methods identically; delegate one to the other. Vacant and one-line functions are exempt.
- Never design a function whose every `return` provides an identical value.
- Never ignore the return values of builtins without side effects (for example `str.upper()` or `sorted()`).
- Never use the result of functions that return nothing (`None`).
- Never reference enclosing loop variables from functions or lambdas defined in the loop; bind them as default parameters. Functions called directly within the identical loop iteration are exempt.
- Declare at least one positional parameter on instance and class methods.
- Declare the expected number of parameters on special methods.
- Declare the expected number of parameters on property getters (1), setters (2), and deleters (1).
