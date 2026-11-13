# MethodScript Function Reference: ControlFlow

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

16 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `break([int])` -> nothing (throws CastException) - Stops the current loop. If int is specified, and is greater than 1, the break travels that many loops up. So, if you had a loop embedded in a loop, and you wanted to break in both loops, you would cal...
- `call_proc(proc_name, [var1...])` -> mixed (throws InvalidProcedureException) [restricted] - Dynamically calls a user defined procedure. call_proc(_myProc, 'var1') is the equivalent of _myProc('var1'), except you could dynamically build the procedure name if need be.
- `call_proc_array(proc_name, array)` -> mixed (throws InvalidProcedureException; CastException) [restricted] - Works like call_proc, but allows for variable or unknown number of arguments to be passed to a proc. The array parameter is "flattened", and call_proc is essentially called.
- `continue([int])` -> void (throws CastException) - Skips the rest of the code in this loop, and starts the loop over, with it continuing at the next index. If this function is called outside of a loop, the command will fail.
- `die([var1, var2...,])` -> nothing - Kills the command immediately, without completing it. A message is optional, but if provided, displayed to the user.
- `dowhile(code, condition)` -> void - Like while, but always runs the code at least once. The condition is checked after each run of the code, and if it is true, the code is run again.
- `for(assign, condition, loopExpr, loopCode)` -> void (throws CastException) - Acts as a typical for loop. The assignment is first run. Then, a condition is checked. If that condition is checked and returns true, loopCode is run. After that, loopExpr is run.
- `foreach(array, [key], ivar, code)` -> void (throws CastException; RangeException) - Walks through array, setting ivar equal to each element in the array, then running code. In addition, foreach(1..4, @i, code()) is also valid, setting @i to 1, 2, 3, 4 each time.
- `foreachelse(array, [key], ivar, code, else)` -> void (throws CastException; RangeException) - Works like a foreach, except if the array is empty, the else code runs instead. That is, if the code would not run at all, the else condition would.
- `forelse(assign, condition, loopExpr, loopCode, elseCode)` -> void - Works like a normal for loop, but if upon checking the condition the first time, it is determined that it is false (that is, NO code loops are going to be run) the else code is run instead.
- `if(cond, trueRet, [falseRet])` -> mixed (throws CastException) - If the first argument evaluates to a true value, the second argument is returned, otherwise the third argument is returned. If there is no third argument, it returns void.
- `ifelse([boolean1, code]..., [elseCode])` -> mixed (throws InsufficientArgumentsException) - Provides a more convenient method for running if/else chains. If none of the conditions are true, and there is no 'else' condition, void is returned.
- `return(mixed)` -> nothing - Returns the specified value from this procedure or closure. It cannot be called outside a procedure or closure. The function itself does not return a value as such, as it is a terminal function, and p...
- `switch(value, [equals, code]..., [defaultCode])` -> mixed (throws InsufficientArgumentsException) - Provides a switch statement. If none of the conditions match, and no default is provided, void is returned. See the documentation on Logic for more information. See more...
- `switch_ic(value, [equals, code]..., [defaultCode])` -> mixed (throws InsufficientArgumentsException) - Provides a case insensitive switch statement, for switching over strings. This works by compiler transformations, transforming this into a normal switch statement, with each case lowercased, and the i...
- `while(condition, [code])` -> void - While the condition is true, the code is executed. break and continue work inside a dowhile, but continuing more than once is pointless, since the loop isn't inherently keeping track of any counters a...
