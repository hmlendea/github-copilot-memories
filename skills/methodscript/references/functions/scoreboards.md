# MethodScript Function Reference: Scoreboards

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

A class of functions for manipulating the server scoreboard.

21 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `create_objective(name, [criteria, [scoreboard]])` -> void (throws ScoreboardException) [restricted] - Adds a new objective to the scoreboard, throwing a CREScoreboardException if the name is already in use or is too long.
- `create_scoreboard(name)` -> void (throws NullPointerException; ScoreboardException) [restricted] - Creates a new scoreboard identified by the given name, and stores it internally for later use. Throws a ScoreboardException if the name is already in use.
- `create_team(name, [scoreboard])` -> void (throws ScoreboardException) [restricted] - Adds a new team to the scoreboard. Throws a ScoreboardException if that team name already exists or is too long.Scoreboard defaults to 'main' if not given.
- `get_objectives([scoreboard], [criteria])` -> array (throws ScoreboardException) [restricted] - Returns an array of arrays about the objectives on the given scoreboard, which defaults to 'main' if not given. If criteria is given, only objectives with that criteria will be returned.
- `get_pscore(objectiveName, name, [scoreboard])` -> int (throws LengthException; ScoreboardException) [restricted] - Returns the player's score for the given objective. A LengthException is thrown if the name is too long.Scoreboard defaults to 'main' if not given.
- `get_pscoreboard(player)` -> string (throws PlayerOfflineException; ScoreboardException) [restricted] - Returns the id of the scoreboard a player is assigned to. If it is not already cached, it will be added using the player's name.
- `get_pteam(player, [scoreboard])` -> array (throws ScoreboardException) [restricted] - Returns a team array for this player, or null if not in a team. Contains the keys name, displayname, color, prefix, suffix, size, options, and players.Scoreboard defaults to 'main' if not given.
- `get_scoreboard_entries([scoreboardName])` -> array (throws ScoreboardException) [restricted] - Gets a list of all the entries in the given scoreboard.
- `get_scoreboards()` -> array [restricted] - Returns an array of the registered scoreboard ID's. The special scoreboard 'main' represents the server's main scoreboard which can be managed by the vanilla /scoreboard command.
- `get_teams([scoreboard])` -> array (throws ScoreboardException) [restricted] - Returns an array of arrays about the teams on the given scoreboard, which defaults to 'main' if not given. The array keys are the team names, and each value is a team array containing the keys: name...
- `remove_objective(objectivename, [scoreboard])` -> void (throws ScoreboardException) [restricted] - Unregisters an objective from the scoreboard. Scoreboard defaults to 'main' if not given.
- `remove_scoreboard(scoreboard, [nullify])` -> void (throws ScoreboardException) [restricted] - Stops tracking the given scoreboard, unless it is 'main', because that never goes away. If nullify is true (defaults to true), all scores, teams, and objectives will be cleared, and all tracked player...
- `remove_team(teamname, [scoreboard])` -> void (throws ScoreboardException) [restricted] - Unregisters a team from the scoreboard. Scoreboard defaults to 'main' if not given.
- `reset_all_pscores(player, [scoreboard])` -> void (throws ScoreboardException) [restricted] - Resets all scores for a player tracked by the given scoreboard. This means they will not be show up on any displays. Scoreboard defaults to 'main' if not given.
- `set_objective_display(objectiveName, array, [scoreboard] / objectiveName, displayname, [scoreboard])` -> void (throws FormatException; LengthException; ScoreboardException) [restricted] - Sets the display name and/or slot of the given objective. If arg 2 is not an array, it is assumed to be the displayname, otherwise arg 2 should be an array with keys 'displayname' and/or 'slot', affec...
- `set_pscore(objectiveName, name, int, [scoreboard])` -> void (throws LengthException; ScoreboardException) [restricted] - Sets the player's score for the given objective. The name can be anything, not just player names. A LengthException is thrown if it's too long.Scoreboard defaults to 'main' if not given.
- `set_pscoreboard(player, [scoreboard])` -> void (throws PlayerOfflineException; ScoreboardException) [restricted] - Sets the scoreboard to be used by a player. The scoreboard argument is the id of a registered scoreboard. Scoreboard defaults to 'main' if not given.
- `set_team_display(teamName, array, [scoreboard] / teamName, displayname, [scoreboard])` -> void (throws LengthException; ScoreboardException; IllegalArgumentException) [restricted] - Sets the display name, color, prefix, and/or suffix of the given team. If arg 2 is not an array, it is assumed to be the displayname, otherwise arg 2 should be an array with keys 'displayname', 'color...
- `set_team_options(teamName, array, [scoreboard])` -> void (throws ScoreboardException; FormatException) [restricted] - Sets various options about the team from an array. The keys 'friendlyfire' and 'friendlyinvisibles' must be booleans.
- `team_add_player(teamName, entry, [scoreboard])` -> void (throws ScoreboardException) [restricted] - Adds a player (or entity UUID) to a team, given the team exists. It will be removed from any other team on the same scoreboard. Scoreboard defaults to 'main' if not given.
- `team_remove_player(teamname, entry, [scoreboard])` -> boolean (throws ScoreboardException) [restricted] - Attempts to remove a player (or entity UUID) from a team, and returns true if successful, for false if it was not part of the team.Scoreboard defaults to 'main' if not given.
