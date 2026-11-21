---
description: "Use for all repository work. Prevents autonomous Git state changes and destructive operations."
applyTo: '**'
---

# Git Safety

- Never run `git commit`, `git push`, `git pull`, `git fetch`, `git stash`, `git stash clear`, `git rebase`, `git amend`, `git checkout`, `git reset`, `git clean`, branch deletion, tag deletion, merge, cherry-pick, revert, or any equivalent Git operation without the user's explicit permission for that specific operation.
- Treat permission for one Git operation as permission for that operation only; do not infer permission for related or subsequent operations.
- Do not use aliases, scripts, wrappers, IDE actions, or other commands to bypass this restriction.
- Before any permitted Git operation, state the exact operation and its effect, then execute only the requested operation.
- Inspecting Git state with read-only commands such as `git status`, `git diff`, and `git log` is allowed unless the user restricts it.
- Editing, creating, or deleting files is also prohibited when it would be destructive or outside the user's explicit request; never discard, overwrite, or revert existing user changes.
