# Scripting: Effects, Triggers, Scopes, Variables, and Templating

Apply to `common/` and `events/`. The language is the Paradox scripting language, sometimes called Jomini script after the Jomini library.

## Syntax Fundamentals

```
key = value
key = { ... }
key = { a b c }      # whitespace-separated list of entries
```

- `#` starts a comment to end of line.
- Indent with tabs; matching braces at the same column is the single most effective syntax check.
- Indentation has no effect on execution; readability and folding are the only reasons to use it.
- `=` is overloaded: assignment, block opener, trigger evaluation, effect activation, and scope change. Do not read it as assignment.
- Effects and triggers are never used alone — they need a right-hand side, even if it is only `= yes`.
- `= no` on a trigger is equivalent to wrapping it in `NOT = { ... }`.
- Numbers are fixed-point. Booleans are `yes` / `no`.
- Some blocks accept loose lists without a paired parameter, notably `events = { ... }` in on_actions.

## Documentation First

`script_docs` in the console dumps the authoritative lists into `logs/`:

| File | Contents |
|------|----------|
| `effects.log` | Every hardcoded effect, its arguments, and its legal scopes |
| `triggers.log` | Every hardcoded trigger, plus supported scopes and targets |
| `modifiers.log` | Every modifier and the object types it may be used in |
| `event_scopes.log` | Every valid scope type |
| `event_targets.log` | Every event target, with input and output scopes |
| `on_actions.log` | Every on_action with its scope |

Search these before trusting the wiki or another Paradox title's syntax. Folders also carry `.info` files describing their local format; read them where present (for example `common/on_action/on_actions.info`, `common/decisions/decision.info`).

## Limits of the Language

- No operating-system access, no string manipulation, no inline mathematics.
- One-dimensional lists and one-dimensional arrays; lists may not contain lists.
- Slower than game code; the engine's AI and army behaviour is not scriptable at all.
- Workarounds: log scraping via `error_log` / `debug_log` for export, `run` scripts for import, list variables over provinces or story cycles as pseudo-arrays.

## Scopes

A scope is a game object. Script is always evaluated in a context scope.

Scope types include `character`, `landed_title`, `province`, `county`, `faith`, `religion`, `culture`, `culture_group`, `dynasty`, `dynasty_house`, `artifact`, `activity`, `scheme`, `secret`, `story_cycle`, `struggle`, `war`, `army`, `combat`, `combat_side`, `casus_belli`, `great_holy_war`, `faction`, `council_task`, `important_action`, plus primitive scopes (numbers, booleans, `flag:<name>`).

### Accessing scopes

| Form | Meaning |
|------|---------|
| `root` | The default context of the enclosing block. Not necessarily a character, and not the player. Some blocks have no `root` (character interactions, for example) |
| `prev` | The previous scope. Cannot be chained as `prevprev`; use nested `prev = { prev = { ... } }` instead |
| `this` | The current scope, used in comparisons and as an argument |
| `<type>:<key>` | Database access, e.g. `title:k_france`, `faith:orthodox`, `culture:english`, `character:123456` |
| `.` chaining | `title:k_france.holder`, `primary_heir.faith.religious_head` |
| `scope:<name>` | A saved scope; see below |
| `var:<name>`, `global_var:`, `local_var:`, `dead_var:` | Variable access |

Characters have a historical ID (scriptable) and a runtime ID (not scriptable). Non-historical characters cannot be addressed by ID.

Do **not** prefix event targets, `root` or `prev` with `scope:` — that prefix is only for values explicitly saved.

### Context switching and guards

Opening a block with a scope changes context until the matching brace:

```
immediate = {
    title:k_france = {
        holder = { add_gold = 100 }
    }
    root = { add_prestige = 10 }
}
```

A misspelled key is a failed context switch, which is silent inside `every_*` lists and noisy elsewhere. Prefer existence guards:

```
exists = primary_spouse
primary_spouse = { add_gold = 10 }
```

`primary_spouse ?= liege` is the compact form: it checks existence and compares in one statement.

### Saved scopes and saved values

```
title:k_france.holder = { save_scope_as = king_of_france }
scope:king_of_france = { add_gold = 100 }

save_scope_value_as = { name = cost value = primary_heir.age }
add_gold = scope:cost
```

Inside trigger blocks use `save_temporary_scope_as` and `save_temporary_scope_value_as`; the non-temporary forms do not work there. Saved scopes survive into scripted effects and events called from the same chain, and vanish when the chain ends. Code-provided saved scopes include `scope:actor` and `scope:recipient` in interactions, and the scopes documented in each on_action file.

### List builders

| Builder | Kind | Behaviour |
|---------|------|-----------|
| `every_X` | effect | Runs the body for each item, in insertion order |
| `random_X` | effect | Runs the body for one random item, optionally weighted |
| `ordered_X` | effect | Orders by `order_by`, then optionally `position` / `min` / `max` |
| `any_X` | trigger | True if the condition holds for all items; accepts `count` and `percent` with comparison operators |
| `every_in_list`, `ordered_in_list`, `random_in_list`, `any_in_list` | both | Iterate a named `list =` or `variable =` list |

`every_*` and `random_*` accept `limit = { ... }`; `any_*` does not — it is already a trigger. Nesting unbounded iterators (for example `every_living_character = { every_province = { ... } }`) is a documented prohibitive cost.

## Effects

Effects change state. Examples: `add_gold`, `add_prestige`, `add_trait`, `set_variable`, `create_character`, `trigger_event`, `remove_short_term_gold`, `death = natural`.

Structural effect keywords:

| Keyword | Behaviour |
|---------|-----------|
| `if = { limit = { ... } ... }` | Conditional, `limit` behaves as AND |
| `else_if`, `else` | Branches; `else` needs no limit |
| `while = { count = N ... }` / `while = { limit = { ... } ... }` | Loop, capped at 1000 iterations, no `break` |
| `switch = { trigger = <trigger> <value> = { ... } }` | Selects the branch matching the trigger's value |
| `hidden_effect = { ... }` | Runs without generating tooltips |
| `random_list = { <weight> = { ... } ... }` | Weighted random branch |
| `custom_tooltip = <key>` | Replaces generated tooltips where tooltip fidelity matters |

Mutations use a `value` block, and maths may be nested rather than repeated:

```
set_variable = {
    name = test
    value = {
        add = 10
        divide = 5
        subtract = 1
    }
}
```

## Triggers

Triggers return true or false, and value comparisons can also return a value (so `add_gold = age` works).

### Logic blocks

| Block | True when |
|-------|-----------|
| `AND = { ... }` | All entries are true (this is also the default for any trigger block and `limit`) |
| `OR = { ... }` | Any entry is true |
| `NOT = { ... }` | Contents are false; keep it to a single trigger for clarity |
| `NOR = { ... }` / `all_false` | All entries false |
| `NAND = { ... }` / `any_false` | Any entry false |
| `switch = { trigger = <trigger> <value> = { ... } fallback = { ... } }` | Branch selection in a trigger context |

### Early out

A trigger block is true only if every entry is true, and evaluation stops at the first false entry. This is the primary performance and safety tool:

```
trigger = {
    exists = primary_spouse            # cheap, and protects the next line
    culture = primary_spouse.culture
}
```

Tooltipped blocks do **not** early-out and will error on a non-existent scope, so use the conditional form there:

```
trigger_if = {
    limit = { exists = primary_spouse }
    culture = primary_spouse.culture
}
```

`trigger_if` / `trigger_else_if` ladders **must** terminate with `trigger_else` (even empty) once `trigger_else_if` is used. A lone `trigger_if` needs none. `trigger_if` is trigger-only; never use it in an effect block.

### Comparison

- Scope comparison: `a = b`, `a != b`, existence-checked `a ?= b`. Both sides must be valid and of the same scope type.
- Value comparison: `<`, `<=`, `=`, `!=`, `>`, `>=`, using numbers, named values, script values, saved values or numeric variables.
- Inline complex triggers (undocumented, partial support): `value = "has_trait_xp(lifestyle_traveler|danger)"`.

## Variables

Four storage classes, each with its own accessor and mutation effects.

| Class | Set with | Accessor | Notes |
|-------|----------|----------|-------|
| Normal | `set_variable`, `change_variable`, `remove_variable` | `var:` | Stored on the scope where the effect ran. Lost when a character dies |
| Global | `set_global_variable`, `change_global_variable`, `remove_global_variable` | `global_var:` | One instance globally, reachable from anywhere |
| Local | `set_local_variable`, `change_local_variable`, `remove_local_variable` | `local_var:` | Lives only for the current script execution |
| Dead character | `set_dead_character_variable` | `dead_var:` | Requires a duration; no `change_` effect |

`set_variable = name` is shorthand for `value = yes`. Normal variables require scoping to the storing object each time: `player_heir = { has_variable = test }`, `add_gold = player_heir.var:test`. Do not use the accessor prefix in `change_variable` / `remove_variable` — those take the bare name.

Variables may hold numbers, scopes, booleans or flag values (`flag:<string>`).

## Lists

| Class | Add with | Contains test | Remove with | Clear with |
|-------|----------|---------------|-------------|------------|
| Simple (temporary) | `add_to_list` | `is_in_list` | `remove_from_list` | no clear; remove each |
| Local variable | `add_to_local_variable_list` | `is_target_in_local_variable_list` | `remove_list_local_variable` | `clear_local_variable_list` |
| Variable (scope-stored) | `add_to_variable_list` | `is_target_in_variable_list` | `remove_list_variable` | `clear_variable_list` |
| Global variable | `add_to_global_variable_list` | `is_target_in_global_variable_list` | `remove_list_global_variable` | `clear_global_variable_list` |

Adding creates the list if absent, and never duplicates an item. `add_to_temporary_list` is the only list effect usable from a trigger block. `*_list_size` triggers exist but return no value — count with a script value if the size is needed numerically. Clear a variable list before rebuilding it, and remember that `add_to_variable_list` runs on the **storing** scope while naming the target:

```
every_ruler = {
    root = {
        add_to_variable_list = { name = rulers target = prev }
    }
}
```

## Script Values

Script values live in `common/script_values` and are usable anywhere a number is.

```
my_value = {
    add = learning
    add = 10
    divide = 5
    max = 30
    min = 0
}
```

Available operations: `add`, `subtract`, `multiply`, `divide` (guard against zero), `modulo`, `value`, `max`, `min`, `round`, `ceiling`, `floor`, `if`/`else_if`/`else`, `fixed_range`, `integer_range`. Operations execute strictly in written order. Formulas can be inlined wherever a script value fits, chained through scopes (`mother.example_age`), expressed as ranges (`{ 1 5 }`), and applied per item of `every_` and `ordered_` lists. `any_` lists are trigger-only. `save_temporary_value_as` captures the running total mid-calculation.

Script values cannot change game state and are recalculated on every use — in UI that means every frame, so prefer storing a variable if the value is heavy and displayed.

## Templating

### Scripted effects

Define in `common/scripted_effects`, or locally in an event file prefixed with `scripted_effect`. Call with `= yes` (or as a block when passing arguments).

```
gift = { add_gold = $val$ }
# used as
gift = { val = 100 }
```

`$NAME$` substitution is literal text replacement performed before evaluation. It can stand in for parts of effect names (`every_$WHO$`) or whole script chunks. Capitalise parameter names by convention. Use `$$` in the definition only, never at the call site.

### Scripted triggers

Same mechanism in `common/scripted_triggers` (or locally with `scripted_trigger`), called with `= yes` or `= no`, the latter equivalent to `NOT = { ... }`. Avoid `root` and `prev` inside shared scripted triggers, since they resolve differently per call site.

### Scripted values

See above; `common/script_values`.

## Scripted GUIs

`common/scripted_guis` holds hidden events invoked from the UI.

```
my_sgui = {
    scope = character
    saved_scopes = { }
    confirm_title = "your_title"
    confirm_text = "your_text"
    is_shown = { }
    is_valid = { }
    ai_is_valid = { }
    effect = { add_gold = 100 }
}
```

Called from `.gui` with `GetScriptedGui('my_sgui').Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).End )`, or declared once per element with `datacontext` and then used as `ScriptedGui.Execute|IsShown|IsValid|BuildTooltip`. `is_valid` is always checked, even when the button has no `enabled` binding. `Execute` also drives `on_start` and `on_finish` animation states.

## Debugging Aids Inside Script

| Tool | Use |
|------|-----|
| `error_log = "..."` | Write to `error.log`; supports bracket text |
| `debug_log = "..."` | Write to `debug.log` |
| `run <file>.txt` | Execute a script file in the player's scope — the fastest iterate-and-verify loop |
| `effect <effect> = <args>` in console | Run one effect against the current scope |
| `trigger <trigger> = <args>` in console | Evaluate one trigger |
| `explorer` | In-game object inspector that runs arbitrary script |
