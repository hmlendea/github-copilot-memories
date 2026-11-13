# MethodScript Function Reference: Cmdline

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

27 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `cd([dir])` -> void (throws IOException; InsufficientPermissionException) [restricted] - Changes the current working directory to the path specified, or the user's home directory if omitted. This only works from cmdline mode.
- `clear_screen()` -> void [restricted] - Clears the screen. This only works from cmdline mode, nothing happens otherwise.
- `exit([int])` -> void - Exits the program. If this is being run from the command line, works by exiting the interpreter, with the specified exit code (defaulting to 0).
- `get_env([variableName])` -> mixed [restricted] - Returns the environment variable specified, if variableName is set. Otherwise, returns an associative array of all the environment variables.
- `get_os()` -> string [restricted] - Returns the name of the current OS. Will be one of WINDOWS, MAC, LINUX, SOLARIS, or UNKNOWN.
- `get_terminal_width()` -> int (throws InsufficientPermissionException) [restricted] - Returns the current width of the terminal, measured in characters. This is useful for determining proper layout for dynamic output. This only works in cmdline mode.
- `in_cmdline_mode()` -> boolean - Returns true if the environment is in cmdline mode. False otherwise.
- `ls([directory])` -> array (throws InsufficientPermissionException; IOException) [restricted] - Returns an array of files in the current working directory, including "hidden" files, orif directory is specified, the files in that directory. This is only available in cmdline mode.
- `print_err(text)` -> void [restricted] - Writes the text to the system's std err, but does not automatically add a newline at the end. Unlike console(), this does not use anything else to format the output, though in many cases they will beh...
- `print_out(text)` -> void [restricted] - Writes the text to the system's std out, but does not automatically add a newline at the end. Unlike console(), this does not use anything else to format the output, though in many cases they will beh...
- `prompt_char(prompt)` -> string (throws InsufficientPermissionException; IOException) [restricted] - Prompts the user for a single character. They do not need to hit enter first. This only works in cmdline mode.
- `prompt_line(prompt)` -> string (throws InsufficientPermissionException; IOException) [restricted] - Prompts the user for a line. The line typed is returned once the user presses enter. This only works in cmdline mode.
- `prompt_pass(prompt, [mask])` -> secure_string (throws InsufficientPermissionException; IOException) [restricted] - Prompts the user for a password. This only works in cmdline mode. If mask is true (default), then the password displays * characters for each password character they type.
- `pwd()` -> string (throws ShellException) [restricted] - Returns the path to the current working directory. This is available outside cmdline mode, but is probably only useful for debugging, meta, or informational purposes when not in cmdline interpreter mo...
- `read_pipe_input([binary])` -> mixed (throws IOException; InsufficientPermissionException) [restricted] - Reads the input from a process that is piped to this script. It is assumed that the data piped to the script will come all at once, and it will be returned as a string (or byte_array if binary is true...
- `set_cmdline_prompt(closure)` -> void (throws CastException; InsufficientPermissionException) [restricted] - Sets the cmdline prompt. This is only usable or useful in cmdline interpreter mode. The closure should return a string, that string will be used as the prompt.
- `set_env(variableName, value)` -> void [restricted] - Sets the value of an environment variable. This only changes the environment value in this process, not system-wide.
- `shell(command, [options])` -> string (throws InsufficientPermissionException; ShellException; IOException; IllegalArgumentException) [restricted] - Runs a shell command. <code>command</code> can be either a string, or array of string arguments. This works mostly like shell_adv however, it buffers then returns the output for sysout once the proces...
- `shell_adv(command, [options])` -> void (throws InsufficientPermissionException; IOException; IllegalArgumentException) [restricted] - Runs a shell command. <code>command</code> can either be a string or an array of string arguments, which are run as an external process.
- `shell_on(os, command, [options])` -> string (throws InsufficientPermissionException; ShellException; IOException; FormatException) [restricted] - Executes the command if and only if on the given operating system (one of WINDOWS, MAC, LINUX, SOLARIS, or UNKNOWN). If not on the specified OS, this command returns null.
- `shell_on_adv(os, command, [options])` -> void (throws InsufficientPermissionException; ShellException; IOException; FormatException) [restricted] - Executes the command if and only if on the given operating system (one of WINDOWS, MAC, LINUX, SOLARIS, or UNKNOWN). If not on the specified OS, this command does nothing.
- `sys_beep()` -> void (throws InsufficientPermissionException; PluginInternalException) [restricted] - Emits a system beep, on the system itself, not in game. This is only useful from cmdline.
- `sys_err(text)` -> void [restricted] - Writes the text to the system's std err. Unlike console(), this does not use anything else to format the output, though in many cases they will behave nearly the same.
- `sys_out(text)` -> void [restricted] - Writes the text to the system's std out. Unlike console(), this does not use anything else to format the output, though in many cases they will behave the same.
- `sys_properties([propertyName])` -> mixed [restricted] - If propertyName is set, that single property is returned, or null if that property doesn't exist. If propertyName is not set, an associative array with all the system properties is returned.
- `user()` -> string - Returns the name of the current user. This is retrieved in a platform specific manner, and should be cross compatible in all scripts.
- `x_find(regex, [startFrom], [type] / regex, [startFrom], types)` -> array (throws IllegalArgumentException; InsufficientPermissionException) [restricted] - Returns a list of absolute paths of files whose name matches the given regex, searching recursively. Only available in cmdline mode. See more...
