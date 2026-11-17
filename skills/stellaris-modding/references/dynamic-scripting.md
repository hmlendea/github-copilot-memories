# Dynamic Scripting: Scripted Effects, Triggers, Loc, Variables, Values, Modifiers

## Scripted Effects

`common/scripted_effects/*.txt` (LIOS). A named block of effects, called like an effect.

```
example_scripted_effect = {
    shift_ethic = ethic_$ETHIC$
}

# call
example_scripted_effect = { ETHIC = materialist }
```

- Parameters are always strings and are substituted textually.
- A scripted effect is a **single** effect value: call `name = yes` when no parameters are needed, or `name = { KEY = value }`.
- Scripted effects may call other scripted effects, allowing chained inline math.

### Parameter guards

```
my_effect = {
    [[homeworld] set_species_homeworld = event_target:tempHomeworld ]   # only when passed
    [[!homeworld] some_fallback_effect = yes ]                          # only when absent or no
}
```

### Defaults

`has_global_flag = crisis_stage_$STAGE|1$` uses `1` when `STAGE` is not supplied.

## Scripted Triggers

`common/scripted_triggers/*.txt` (LIOS). Same parameter mechanics.

```
example_scripted_trigger = {
    has_ethic = ethic_$ETHIC$
}
```

A scripted trigger with parameters cannot be called as `xyz = no`; wrap it: `NOT = { example_scripted_trigger = { ETHIC = materialist } }`.

## Inline Math

`@\[ ... ]` inside a scripted effect or trigger. Operators: `+ - * /` only; anything else concatenates the operands.

```
add_monthly_resource_mult = {
    resource = unity
    value = $COUNT|1$
    min = @\[ $COUNT|1$ * 10 ]
    max = 99999999
}
```

Limits:
- Only the **first** `@\[ ... ]` in a given scripted effect is evaluated. Split additional maths into further scripted effects.
- Inline math can be passed as a parameter when quoted: `value = "@\[ $COUNT$ * 0.75 ]"`.

## Scripted Localisation

`common/scripted_loc/*.txt` (FIOS).

```
defined_text = {
    name = GetAuthorityName
    text = {
        trigger = { has_authority = auth_democratic }
        localization_key = auth_democratic
    }
    text = {
        trigger = { has_authority = auth_oligarchic }
        localization_key = auth_oligarchic
    }
}
```

Called as `[This.GetAuthorityName]`. Scripted loc blocks cannot themselves contain bracket commands; `[Root.GetName]` inside one prints literally.

## Scripted Variables

`common/scripted_variables/*.txt` (FIOS). A file **must** end with a blank or commented line.

```
@example = 2
```

These are the only `@` variables shared across files. File-local `@` variables are visible only inside their own file.

## Script Values

`common/script_values/*.txt` (LIOS), 3.3+. Referenced as `value:<key>`.

```
example_value = {
    base = 10
    add = 100
    multiply = value:some_other_script_value
    modulo = 5
    round_to = 5
    min = 0
    max = 500
    round = yes
    modifier = {
        max = owner.max_example_variable
        owner = { is_variable_set = max_example_variable }
    }
    complex_trigger_modifier = {
        trigger = count_owned_planet
        trigger_scope = owner
        parameters = { limit = { num_pops > 10 } }
        mode = add
        mult = 5
    }
}
```

Operations: `set`/`weight` (replace), `add`, `subtract`, `factor`/`mult`/`multiply`, `divide`, `modulo`, `round_to`, `max`, `min`, `pow`; and numberless `round`, `ceiling`, `floor`, `abs`, `square`, `square_root`.

`set`, `weight`, and `factor` overwrite the base value; prefer `multiply` and `add`.

Script values are evaluated on demand. In a frequently checked trigger they are a performance hazard.

## Scripted Modifiers

`common/scripted_modifiers/*.txt` (3.4+). Creation declares presentation only; the modifier has no effect until it is wired into something that reads it.

```
pop_job_trade_mult = {
    icon = mod_trade_value_mult
    percentage = yes
    good = yes
    category = pop
}
```

Settings: `icon` (filename in `gfx/interface/icons/modifiers` without `.dds`), `percentage`, `min_mult`, `max_decimals` (default 2), `good`, `neutral`, `hidden`, `no_diff`, `cap_zero_to_one`, `localize_with_value_key` (requires `$VALUE$` in the key), `category`.

`category` should be the lowest object in the hierarchy from which the modifier is read: `all`, `pop`, `ship`, `station`, `fleet`, `country`, `army`, `leader`, `planet`, `component`, `deposit`, `megastructure`, `habitability`, `starbase`, `economic_unit`, `system`, `trade`, `federation`, `espionage`. `pop_faction` is unused.

Apply it e.g. as `mult = modifier:my_modifier` inside a triggered modifier or resource table.

## Variables

Variables are scope-bound and persistent once set. Available on `megastructure`, `planet`, `country`, `ship`, `pop`, `fleet`, `galactic_object`, `leader`, `army`, `ambient_object`, `species`, `pop_faction`, `war`, `federation`, `starbase`, `deposit`, `sector`, `archaeological_site`, `first_contact`, `spy_network`, `espionage_operation`, `espionage_asset`.

```
set_variable = { which = star_temperature value = @G2V_star_temperature }
change_variable = { which = my_var value = 5 }
subtract_variable = { which = my_var value = 5 }
multiply_variable = { which = my_var value = 1.5 }
divide_variable = { which = my_var value = 2 }
modulo_variable = { which = my_var value = 3 }
set_variable_to_random_value = { which = my_var min = -100 max = 100 rounded = yes }
```

Export helpers: `export_trigger_value_to_variable`, `export_modifier_to_variable`, `export_resource_income_to_variable`, `export_resource_stockpile_to_variable`, `get_galaxy_setup_value`.

Right-hand values accept literals, `variable`, `scope.variable`, and `trigger:<name>`.

Inline in localisation: `[Scope.my_variable]`, and saved dates `[Scope.my_date_flag]` since 3.1.

## Modifier Application

```
add_modifier = { modifier = soul_diet1 multiplier = 6 days = 360 }
```

`multiplier` (3.0+) scales numeric modifier values. Modifiers without `days` persist until removed.

## Inline Scripts

`common/inline_scripts/*.txt` (3.5+, DUPL). Reusable fragments substituted into larger definitions. Whole-file replacement is the reliable usage; treat per-file merging as unreliable.

## Conventions

- Prefix every scripted effect, trigger, value, modifier, and loc key with the mod token; all share one namespace per folder.
- Keep scripted effects free of tooltip-visible side effects when they are used inside `potential` or `allow`.
- Wrap generated-effect-heavy blocks in `hidden_effect` and supply an explicit `custom_tooltip`.