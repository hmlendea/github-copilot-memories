# MethodScript Function Reference: Recipes

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

6 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `add_recipe(recipeArray)` -> boolean (throws CastException; FormatException; IllegalArgumentException) [restricted] - Adds a recipe to the server and returns whether it was added or not. See more...
- `clear_recipes()` -> void [restricted] - Clears all recipes.
- `get_all_recipes()` -> array [restricted] - Gets all recipes on the server.
- `get_recipes_for(itemArray)` -> array (throws FormatException; CastException) [restricted] - Gets all recipes that have a result of the given item. NOTE: Gets all recipes for result item regardless of meta and enchants, although the array has correct data.
- `remove_recipe(recipe_key)` -> boolean [restricted] - Remove a certain recipe by its registered key. Returns whether the recipe was removed successfully or not.
- `reset_recipes()` -> void [restricted] - Resets all recipes to the default recipes.
