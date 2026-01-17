---
name: sync-github-repos
description: Sync Kevin's active GitHub repos with Obsidian vault tracking. Run with "sync my repos", "/sync-repos", or "sync repos status".
---

# GitHub Repos Sync

Synchronizes Kevin's active GitHub repositories and updates Obsidian vault tracking files with recent commits and status.

## Quick Commands

- **"sync my repos"** - Full sync workflow (fetch, commit, pull, push)
- **"/sync-repos"** - Same as above
- **"/sync-repos status"** - Just show status, no changes
- **"/sync-repos commit"** - Only commit local changes

## Configuration

Tracked repos are defined in `repos.yaml` in this skill directory.

## Workflow

When this skill is triggered, execute these steps:

### Phase 1: Discovery

For each repo in repos.yaml:

```bash
# Check if repo exists
cd [repo_path] || skip with warning

# Fetch all remotes
git fetch --all 2>&1

# Get status
git status --short

# Check branch position
git log --oneline -1 HEAD
git log --oneline -1 origin/[branch] 2>/dev/null
```

Collect:
- Local uncommitted changes
- Commits ahead of remote
- Commits behind remote
- Current branch

### Phase 2: Report

Present summary table:

```markdown
## Repo Sync Status

| Repo | Local Changes | Ahead | Behind | Action Needed |
|------|---------------|-------|--------|---------------|
| [name] | [count] files | [n] commits | [n] commits | [action] |
```

**Actions:**
- `commit` - Has uncommitted changes
- `pull` - Behind remote
- `push` - Ahead of remote
- `sync` - Needs both pull and push
- `ok` - Fully synced

### Phase 3: User Confirmation

Present options:

```
What would you like to do?

1. Sync all repos (commit, pull, push)
2. Commit only (no pull/push)
3. Pull only (no commit/push)
4. Push only (no commit/pull)
5. Select specific repos
6. Skip - just show status

Select 1-6:
```

**IMPORTANT:** Wait for user input before proceeding.

### Phase 4: Execute

For each repo needing action:

#### Commit Local Changes
```bash
cd [repo_path]
git add -A
git commit -m "$(cat <<'EOF'
[Auto-generated message based on changes]

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

#### Pull Remote Changes
```bash
cd [repo_path]
# If clean working tree
git pull --rebase origin [branch]
# If has local commits
git pull origin [branch]
```

#### Push to Remote
```bash
cd [repo_path]
git push origin [branch]
```

#### Handle Errors
- **Merge conflict:** Abort, report, continue to next repo
- **Auth failure:** Report, suggest token check
- **Pre-commit hook failure:** Report error, ask user to fix or skip
- **Repo not found:** Skip with warning

### Phase 5: Update Vault Tracking

For each synced repo that has a vault tracking file:

1. **Get recent commits:**
```bash
git log --oneline -10 --format="%h|%s|%cr|%an"
```

2. **Update tracking file:**
```markdown
---
last_synced: [YYYY-MM-DD HH:MM]
local_status: clean|modified
---

## Recent Commits

| Hash | Message | When | Author |
|------|---------|------|--------|
| abc123 | Fix bug | 2 days ago | Kevin |
```

3. **Update dashboard:**
- Update `last_synced` in dashboard
- Add to "Recent Changes" section
- Clear from "Uncommitted Changes" alert if applicable

### Phase 6: Summary

Report completion:

```markdown
## Sync Complete

**Repos synced:** [X] of [Y]
**Commits made:** [N]
**Conflicts:** [list if any]

### Sync Results

| Repo | Status | Commits |
|------|--------|---------|
| [name] | synced | [hash] |
| [name] | skipped | [reason] |

**Vault updated:**
- [tracking files updated]

**Next sync:** Run `/sync-repos` anytime or as part of `/session-cleanup`
```

## Repo Categories

Repos are categorized for smart commit messages:

- **work** - Prefix: `Work:` (NeuroBlu, S2N)
- **side-project** - Prefix: `Project:` (Thinkhaven, InstantDoc)
- **personal** - Prefix: `Vault:` (Obsidian Vault)
- **portfolio** - Prefix: `Portfolio:` (CensusChat)

## Error Recovery

### Merge Conflict
1. Abort the pull: `git merge --abort` or `git rebase --abort`
2. Report conflicting files
3. Continue with other repos
4. List conflicts in final summary

### Pre-commit Hook Failure
1. Report which hook failed
2. Ask user: "Fix and retry, or skip this repo?"
3. If skip, note in summary

### Auth Failure
1. Report which repo and remote
2. Suggest: "Check GitHub token permissions"
3. Continue with other repos

## Integration

This skill works with:
- **`/session-cleanup`** - Can run sync as part of session end
- **GitHub Tracking Dashboard** - Updates `🚀 Projects/GitHub-Tracking/`
- **S2N GitHub Observability** - Shares S2N repo status

## Excluded Repos

These repos are NOT tracked (stale, broken, or archived):
- linksavvy (deleted)
- templardata (auth broken)
- omcp (git-lfs issues)
- Old coursework repos (Thanksgiving-Dinner, etc.)

To modify tracked repos, edit `repos.yaml` in this skill directory.
