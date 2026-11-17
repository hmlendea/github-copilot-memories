# Events and Decisions

## Events

Files live in `events/`. Every file begins with a **namespace**; event ids are `<namespace>.<number>`, unique per namespace and per number. The game assigns numbers automatically at startup, so no global id allocation is needed — but two events with the same `namespace.number` collide.

Event types decide the ROOT scope: `country_event`, `character_event`, `state_event`, `province_event`.

```
namespace = rel_flavor

rel_flavor.16 = {
    type = country_event                                     # ROOT scope
    title = rel_flavor.16.t                                  # localisation key
    desc = rel_flavor.16.desc
    picture = aqueducts
    hidden = no
    fire_only_once = yes
    goto_location = capital_scope

    left_portrait = current_ruler
    right_portrait = current_ruler

    weight_multiplier = { }                                  # modifies firing chance

    trigger = { }                                            # may the event fire at all

    immediate = { }                                          # after trigger, before options

    option = {
        name = rel_flavor.16.a
    }
    option = {
        name = rel_flavor.16.b
        trigger = { }                                        # option visibility
        exclusive = yes                                      # only option if available
        highlight = yes
    }

    after = { }                                              # after an option is clicked
}
```

Field order is not semantically significant, but the conventional order above keeps reviews cheap.

Notes:

- `hidden = yes` fires the event without showing a window; pair with `immediate`/`after` for pure scripting.
- `fire_only_once = yes` limits to once per tag.
- `goto_location` must evaluate to a province in the event's scope chain.
- Portraits expect a character-producing link valid in the event's root scope.
- Options are effects; the `after` block runs after any chosen option.

## Decisions

Files live in `decisions/`. A decision is a national scripted effect: invisible until `potential` passes, then selectable once `allow` passes.

```
country_decisions = {
    form_macedon = {
        potential = { ... }        # visibility (triggers)
        highlight = {              # optional map highlight
            scope:province = { province_id = 379 }
        }
        allow = { ... }            # selectability (triggers)
        effect = { ... }           # what happens (effects)
    }
}
```

Guidance drawn from vanilla practice:

- `potential` should gate on cheap, stable facts: tag, culture, government, capital region, whether the formable already exists.
- `allow` carries the expensive checks: `owns = <province_id>`, culture integration, `can_form_nation_trigger = yes`, and AI-specific relaxations via `trigger_if = { limit = { is_ai = no } ... }`.
- Wrap failure messaging in `custom_tooltip = { text = <loc key> <triggers> }` so the player sees why the decision is unavailable.
- Do irreversible work inside `hidden_effect = { }` and announce it with `custom_tooltip`, keeping the player-facing tooltip readable.
- `highlight` is a `scope:province` filter that marks the territories required for the decision.

## Scripted Triggers and Effects

Put reusable trigger and effect fragments in `common/scripted_triggers/` and `common/scripted_effects/`. They are called like built-ins, accept arguments (`$name$`), and are the correct place for logic reused by more than one event or decision.