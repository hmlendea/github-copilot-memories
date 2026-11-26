---
name: work-directory
description: "Use at the start of every repository task, when creating temporary data, scratch files, or ad hoc utilities, and when recording progress, decisions, context, or data for reuse across sessions. Covers consulting the local .work/ directory, excluding it from Git without tracked references, its layout and entry format, freshness verification, and excluding its existence from every tracked artefact."
---

# Work Directory

`.work/` at the repository root is a private, local directory shared by every agent session on that clone. It holds temporary data, utilities, and durable notes that carry progress, decisions, context, and data from one session to the next. Git never tracks it, and nothing that Git tracks or that leaves the machine refers to it.

## Step 1: Consult Existing Entries

At the start of every task, when `.work/` exists:

1. Read `.work/INDEX.md`.
2. Read `.work/context.md` and every entry under `.work/decisions/`, `.work/progress/`, and `.work/data/` that the index or the file names associate with the task.
3. Treat each entry as a lead, not as proof. Verify any claim on which a change depends against the current repository state before relying on it, because the code may have changed since the entry was recorded. Revise or delete an entry that proves stale.

When `.work/` does not exist, create it only when the task produces something to store.

## Step 2: Exclude It From Git

Prior to the first write, ensure that Git ignores the directory without any tracked file mentioning it:

```bash
git check-ignore -q .work/ || printf '.work/\n' >> "$(git rev-parse --git-path info/exclude)"
```

```powershell
git check-ignore -q .work/; if ($LASTEXITCODE -ne 0) { Add-Content -Path (git rev-parse --git-path info/exclude) -Value '.work/' }
```

- Never add `.work/` to `.gitignore`, `.gitattributes`, editor settings, build files, or any other tracked file.
- When a tracked file already references `.work/`, report the `path:line` to the user and leave it unchanged unless the user requests its elimination.
- Outside a Git repository, use `.work/` only when the user confirms that the target is not published.

## Step 3: Layout

| Path | Contents | Lifetime |
|------|----------|----------|
| `.work/context.md` | Project context that is costly to rediscover: architecture notes, conventions, commands, environment peculiarities | Durable |
| `.work/data/` | Retrieved or computed data that merits reuse, such as trimmed API responses and inventories | Until stale |
| `.work/decisions/<yyyy-mm-dd>-<topic>.md` | One decision each: the decision, the alternatives rejected and the reasons, and the source | Durable |
| `.work/INDEX.md` | One line per entry: path, one-sentence summary, last-revised date | Durable |
| `.work/progress/<task>.md` | Task objective, state, completed and remaining steps, failed attempts, next action, and session handoffs | Until the task is complete |
| `.work/tmp/` | Disposable intermediates for the current session | Delete at task completion |
| `.work/tools/` | Reusable scripts and utilities | Durable |

Use lowercase kebab-case names, `yyyy-mm-dd` dates, and Markdown, JSON, or CSV formats. Maintain the index in alphabetical order by path.

## Step 4: Record Entries

- Start each durable entry with its last-revised date and its source: `Source: user`, `Source: documentation (<repository-relative path or public URL>)`, `Source: investigation (<command or file inspected>)`, or `Source: user interview`.
- Record facts, decisions, and their reasons; omit transcript narration and verbose tool output.
- Revise an existing entry instead of creating a duplicate, and revise `.work/INDEX.md` in the same step.
- Prior to task completion, or when a session handoff applies, bring `.work/progress/<task>.md` up to date. When the task is complete, transfer its lasting decisions and context into `decisions/` or `context.md`, then delete the progress file.
- Never store credentials or secrets. Store personal data only when the task requires it, and limit it to the minimum required.

## Step 5: Exclude It From Every Published Artefact

The directory, its paths, its file names, and the fact that it exists must not appear in:

- any tracked or trackable file, including code, comments, documentation, configuration, scripts, and tests;
- commit messages, branch and tag names, pull request and issue text, review comments, and release notes.

Information taken from it is presented as standalone fact, or is attributed to the original source recorded in the entry: the user, the documentation, an interview with the user, or the investigation. Never write phrases such as "according to the notes" or "as recorded earlier". Never invent a source; when an entry records none, state the information without attribution, or verify it again and cite that verification.

A utility proven useful beyond the current task is promoted into the repository only when the user requests it, and then as a standalone file with no reference to its origin.

In this repository's own agent configuration, the instruction and skill files that define this procedure, and the documentation that describes them, are exempt, because the procedure cannot be defined without naming the directory.

## Step 6: Verify Before Completion

Before completing a task that changed files, and before any commit or publication:

```bash
{ git grep -nIF -e '.work/' -e '.work\' -- .; git grep --untracked -nIF -e '.work/' -e '.work\' -- .; git diff --cached -U0 | grep -F -e '.work/' -e '.work\'; } | sort -u
git ls-files -- .work
git check-ignore -q .work/ && echo ignored
```

- Every reference printed is a finding to eliminate, except in the exempt files described in Step 5.
- `git ls-files -- .work` must print nothing, and `git check-ignore` must succeed.
- Apply the same check to the commit message, branch name, and pull request text, and delete `.work/tmp/`.
