# Events and Text

Old World event stories are data-driven XML entries. The Event Browser and Event Wizard expose the same model; the Wizard can generate and connect event, text, option, and bonus identifiers.

## Event contract

An event needs valid metadata, including an author, a unique story `zType`, event text, and at least one option. Common fields include:

- `aeSubjects`: ordered subjects such as tile, unit, player, character, family, city, or leader.
- `iTriggerSubject` and `iTriggerExtra`: indexes into the ordered subject list for trigger data.
- `zTrigger`: the gameplay event trigger, or no specific trigger for turn-pool selection.
- `iWeight`: relative selection weight; zero means it cannot be selected.
- `iProb`: percentage chance of entering the valid event pool; default behaviour must be verified in the installed build.
- `iRepeatTurns`: repeat delay; `-1` is documented as once-only, `0` as unrestricted, but confirm current behaviour.
- `aeSubjectExtras`: additional subject constraints, such as requiring a unit type.
- `aeOptions`: option identifiers connected to the story.
- `zBackgroundName`, `zAudioTrigger`, `iImageSubject`, and `iImageExtra`: presentation and portrait context.

Subjects use ownership suffixes such as `_US`, `_THEM`, and `_US_OR_THEM`. Subject order matters: option bonuses apply to subjects in the same order. Trigger subject and extra indexes must point to the intended subjects.

## Options and bonuses

Each option has its own identifier, text, and ordered bonuses. Leave a subject's bonus empty when no effect is intended; apply the desired bonus at the matching subject position. Reuse established bonus types and verify their legal subject context.

## Text

Use the installed text reference and the official Text Editing Cheat Sheet. Event text supports indexed variables such as `{CHARACTER-0}`, `{CHARACTER-SHORT-0}`, `{TITLE-0}`, `{PLAYER-0}`, `{FAMILY-0}`, `{CITY-0}`, and `{UNIT-0}`; forms and modifiers vary by variable. Gender conditionals use the documented `{G1:Male text:Female text}` pattern. Links and predicate syntax must be copied from verified game examples.

Use the Event Style Guide for tone, historical context, naming, event classes, backgrounds, audio, portraits, and camera subjects. Keep internal `HelpText` useful for option intent. Test event links, trigger conditions, text variables, and localisation in-game.
