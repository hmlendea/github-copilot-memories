---
name: leak-prevention
description: "Use before finishing any task that changed repository files, and before any commit, push, pull request, issue, comment, release, or publication. Detects and removes secrets, credentials, personal data, system-specific details (home paths, usernames, hostnames, private addresses, git identity, internal names), and agent configuration details (names or paths of skills, instructions, prompts, agents, or memories that the repository does not track) from tracked or trackable content, with redacted reporting and safe remediation."
---

# Leak Prevention

Find and remove protected information before it leaves the machine. The categories and allowed locations are defined in `instructions/common/common.security.instructions.md`; this skill supplies the procedure.

Absolute constraint: never print, echo, quote, or store a protected value while scanning or reporting. Report `path:line` and category only.

## Step 1: Define The Scope

- Changed content: `git status --porcelain` lists modified, added, and untracked files.
- Staged content: `git diff --cached -U0` shows only the lines that will be committed.
- Whole project: run every search twice and combine the results. Plain `git grep` searches all tracked files, including tracked files that an ignore rule matches. `git grep --untracked` adds untracked files that are not ignored, but it skips tracked files that an ignore rule matches, so it never replaces the plain pass.
- Ignored files are out of scope only when `git check-ignore -q <path>` succeeds **and** `git ls-files --error-unmatch <path>` fails. A tracked file is in scope even when a `.gitignore` rule matches it.
- Outside a Git repository, scan every file in the target.

## Step 2: Scan For The Local Identity

This is the most reliable check: it searches for the actual values of this machine without displaying them. It lists matching file names only.

Bash:

```bash
for value in "$(git config user.name)" "$(git config user.email)" "${USER:-}" "$(hostname)" "${HOME:-}"; do
  [ "${#value}" -ge 4 ] || continue
  { git grep -IilF -e "$value" -- .; git grep --untracked -IilF -e "$value" -- .; } | sort -u
done
```

PowerShell:

```powershell
$values = @((git config user.name), (git config user.email), $env:USERNAME, $env:COMPUTERNAME, $env:USERPROFILE, $env:USERDNSDOMAIN) | Where-Object { $_ -and $_.Length -ge 4 }
foreach ($value in $values) { @(git grep -IilF -e $value -- .) + @(git grep --untracked -IilF -e $value -- .) | Sort-Object -Unique }
```

- Any file name printed is a finding to inspect. No output means no match.
- Also check the path form with the other separator (for example `C:/Users/<name>` as well as `C:\Users\<name>`), the e-mail local part, and the given name and surname separately.
- Skip a value shorter than four characters; it produces noise rather than evidence. Both scripts already do so.
- When this check reports a file, inspect the matching lines yourself and do not paste them into the reply.

## Step 3: Scan For Patterns

Run each pattern with `git grep -nIE` and again with `git grep --untracked -nIE` (add `-i` where noted). For staged content only, pipe `git diff --cached -U0` through `grep -nE` and keep lines that start with `+`.

| Category | Extended regular expression |
|----------|-----------------------------|
| Home or profile path | `(/home/\|/Users/\|[A-Za-z]:[\\/]+Users[\\/]+)[A-Za-z0-9._-]+` |
| Cloud-synchronised folder | `OneDrive - \|Dropbox/\|Google Drive/\|iCloud Drive` |
| E-mail address | `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}` |
| IPv4 address | `([0-9]{1,3}\.){3}[0-9]{1,3}` |
| MAC address | `([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}` |
| Phone number | `\+[0-9]{1,3}[ ()0-9-]{7,}` |
| Credential in URL | `[A-Za-z][A-Za-z0-9+.-]*://[^/ :@]+:[^/ @]+@` |
| Private key | `-----BEGIN [A-Z ]*PRIVATE KEY-----` |
| Provider token | `gh[pousr]_[A-Za-z0-9]{36}\|github_pat_[A-Za-z0-9_]{20,}\|AKIA[0-9A-Z]{16}\|AIza[0-9A-Za-z_-]{35}\|xox[abprs]-[A-Za-z0-9-]{10,}\|sk-[A-Za-z0-9_-]{20,}\|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.` |
| Secret assignment (`-i`) | `(password\|passwd\|pwd\|secret\|token\|api[_-]?key\|client[_-]?secret\|connection[_-]?string\|access[_-]?key)["']?[[:space:]]*[:=][[:space:]]*["'][^"'<>${}]{8,}` |
| Disabled TLS verification (`-i`) | `ssl[_-]?verify[[:space:]]*=[[:space:]]*false\|verify[_-]?ssl[[:space:]]*=[[:space:]]*false\|InsecureSkipVerify\|rejectUnauthorized["']?[[:space:]]*:[[:space:]]*false` |

In the table, `\|` is Markdown escaping; type a plain `|` in the command.

Also flag any changed file named `.env` or `.env.*` (except `.env.example`), `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks`, `*.keystore`, `id_rsa*`, `id_ed25519*`, `*.tfstate`, `credentials*`, or `secrets*` that is tracked or trackable.

Also look for names that only this user or employer would recognise: internal repository names, project codenames, private hostnames, and private package feeds. No pattern finds them reliably; review the changed lines.

## Step 4: Scan For Agent Configuration Details

The skills, instructions, prompts, custom agents, and memories that directed the task are private configuration. Their names, paths, and any assertion that they were invoked or followed must not appear in tracked content, commit messages, or publications unless the working repository tracks the corresponding file.

Search for the names of the locally installed agent configuration. Names that a tracked repository path contains are skipped. The commands print `path:name` pairs only.

Bash:

```bash
tracked="$(git ls-files)"
set --
while IFS= read -r file; do
  case "$file" in
    */SKILL.md) name="${file%/SKILL.md}"; name="${name##*/}" ;;
    *) name="${file##*/}"; name="${name%.md}"; name="${name%.*}" ;;
  esac
  [ "${#name}" -ge 4 ] || continue
  case "$tracked" in *"$name"*) continue ;; esac
  set -- "$@" -e "$name"
done <<EOF
$(for root in "$HOME/.copilot" "${CODEX_HOME:-$HOME/.codex}" "$HOME/.agents" "$HOME/.claude" "$HOME/.config/Code/User/prompts" "$HOME/Library/Application Support/Code/User/prompts"; do
  [ -d "$root" ] && find -L "$root" -maxdepth 4 \( -name SKILL.md -o -name '*.instructions.md' -o -name '*.prompt.md' -o -name '*.agent.md' -o -name '*.chatmode.md' \) 2>/dev/null
done)
EOF
[ "$#" -gt 0 ] && { git grep -IiowF "$@" -- .; git grep --untracked -IiowF "$@" -- .; } | sort -u
```

PowerShell:

```powershell
$roots = @("$HOME\.copilot", $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { "$HOME\.codex" }), "$HOME\.agents", "$HOME\.claude", "$env:APPDATA\Code\User\prompts") | Where-Object { Test-Path $_ }
$tracked = git ls-files
$names = Get-ChildItem $roots -Recurse -Depth 4 -File -Include SKILL.md, *.instructions.md, *.prompt.md, *.agent.md, *.chatmode.md -ErrorAction SilentlyContinue |
    ForEach-Object { if ($_.Name -eq 'SKILL.md') { $_.Directory.Name } else { $_.Name -replace '\.(instructions|prompt|agent|chatmode)\.md$', '' } } |
    Sort-Object -Unique | Where-Object { $_.Length -ge 4 -and -not ($tracked -clike "*$_*") }
if ($names) { $patterns = $names | ForEach-Object { '-e'; $_ }; @(git grep -IiowF @patterns -- .) + @(git grep --untracked -IiowF @patterns -- .) | Sort-Object -Unique }
```

Also run these patterns with `git grep -nIE` and `git grep --untracked -nIE`, and against commit messages, pull request text, and other prose pending publication:

| Category | Extended regular expression |
|----------|-----------------------------|
| Agent configuration file (`-i`) | `SKILL\.md\|\.instructions\.md\|\.prompt\.md\|\.agent\.md\|\.chatmode\.md\|copilot-instructions\.md\|AGENTS\.md\|CLAUDE\.md` |
| Agent home path (`-i`) | `\.copilot[\\/]\|\.codex[\\/]\|\.claude[\\/]\|\.agents[\\/]\|Code[\\/]+User[\\/]+prompts` |
| Local work directory | `(^\|[^A-Za-z0-9_])\.work([\\/]\|$\|[^A-Za-z0-9_])` |
| Attribution to agent guidance (`-i`) | `(per\|according to\|following\|as required by\|invoked\|applied\|using\|via) (the )?[A-Za-z0-9._-]+ (skill\|instructions?\|prompt\|agent\|chat ?mode\|memory)` |

Also review the changed lines and messages for prose that names or paraphrases private guidance, such as an assertion that a change was made because a local rule, skill, or memory required it, and for any mention of the local work directory, its contents, or its existence. Information taken from that directory is stated as standalone fact or attributed to its original source, as the `work-directory` skill defines.

## Step 5: Classify Each Match

A match is a **false positive** only when it is one of the following:

- A reserved or documentation value: `example.com`, `example.org`, `example.net`, `localhost`, `127.0.0.0/8`, `0.0.0.0`, `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`, `2001:db8::/32`, or a `noreply` address.
- A placeholder or variable: `<username>`, `~`, `$HOME`, `%USERPROFILE%`, `${VARIABLE}`, or a generic illustrative path such as `/home/user/`.
- A value from the `test-values` skill.
- A detection pattern, test fixture, or documentation example that cannot authenticate anywhere and identifies nobody.
- Identity that the project already publishes in that same place (licence holder, repository owner, package author, maintainer contact).
- A version number, OID, or other dotted number that the IPv4 pattern matched.
- A skill, instruction, prompt, agent, or memory name or path whose file the working repository tracks, or a word that only coincides with a configuration name and refers to something else in context.
- A local work directory reference inside the tracked agent configuration files that define the `work-directory` procedure, or inside the documentation that describes them.
- An agent configuration file name used as public, tool-defined vocabulary rather than as a reference to private guidance, such as documentation of how a project's own tracked `AGENTS.md` works.

Every other match is a **finding**. When unsure, treat it as a finding and ask the user.

## Step 6: Remediate

- **Uncommitted:** replace the value with a substitute from the security instruction (relative path, environment variable, placeholder, reserved example, or run-time secret lookup). Move a real secret into a Git-ignored file or secret store, and commit a placeholder template instead. For an agent configuration detail, restate the convention in the project's own terms or eliminate the reference.
- **Staged:** fix the file and tell the user that it needs restaging. Run no Git operation without permission.
- **Committed but not pushed:** tell the user, and propose amending or rewriting the unpublished commits. Execute only with explicit permission.
- **Pushed or published:** tell the user at once. A secret must be rotated or revoked first, because a later commit that deletes it leaves it in the history. Propose history rewriting and cache purging only as follow-up steps, and execute them only with explicit permission.
- **Third-party request already sent:** tell the user which category of data left the machine and where, without repeating the value.

## Step 7: Report

Report the scope, the commands run, and the outcome:

- Clean: `Leak scan: <scope>; no findings.`
- Findings: one line each as `path:line - category - remediated | needs user action`. Never include the value or a fragment of it.
- Waived false positives: `path:line - category - waived: <reason>`.

A task that changed files is not complete until this report states no unresolved findings.
