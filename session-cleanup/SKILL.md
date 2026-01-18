---
name: session-cleanup
description: Use when ending a work session to preserve context, clean up files, and commit changes. Invoke with /session-cleanup or when user says "wrap up", "end session", "cleanup", or "done for today".
---

# Session Cleanup

End-of-session workflow that updates context files, cleans up stray files, adds proper metadata, and commits changes to git.

## Quick Start

Invoke: `/session-cleanup`

Or say: "wrap up", "end session", "cleanup", "done for today"

## Workflow

```
INVENTORY → ANALYZE → PREVIEW → EXECUTE → SUMMARY
```

Execute these steps in order:

### Step 1: Inventory Changes

Run git status to identify all changes:

```bash
git status --porcelain
```

Categorize files by vault location:

| Path Pattern | Category | Action |
|--------------|----------|--------|
| `📝 Content/` | Content | Check frontmatter, update Content MOC |
| `💼 Work/` | Work | Update engagement MOC |
| `🚀 Projects/` | Projects | Update project README |
| `🧠 Knowledge Base/` | Knowledge | Check literature note links |
| `📥 Landing Pad/` | Inbox | Suggest migration destination |
| `📞 Granola/` | Meetings | Link to relevant context |
| `CLAUDE.md` | Context | Note what was updated |

### Step 2: Auto-Detect Updates

**Context files to check:**

1. **CLAUDE.md** - Update if session involved:
   - New project or capability → Add to "Recent Developments"
   - Project milestone → Update "Active Projects" table
   - Status change → Update "Current Priorities"

2. **MOCs** - Based on path mappings in `config/cleanup-rules.yaml`:
   - S2N work → `_S2N-Health-MOC.md`
   - Content creation → `Content Creation Hub - MOC.md`
   - Personal projects → `Personal-Life-MOC.md`

**Files to clean up:**

1. **Landing Pad items** - Check for:
   - Files that should migrate to permanent locations
   - Pattern matching: `*-Literature-Note.md` → Resources/

2. **Missing frontmatter** - New markdown files need:
   - `tags:` appropriate for content type
   - `created:` date stamp
   - `status:` if applicable

3. **Missing links** - Cross-reference opportunities:
   - Literature notes ↔ Blog posts
   - Meeting notes ↔ Project files
   - New content ↔ MOCs

### Step 3: Preview (Single Confirmation)

Present all proposed changes in structured format:

```markdown
## Session Cleanup Preview

### Context Updates
**CLAUDE.md**:
+ [Specific addition to Recent Developments]
+ [Table update if applicable]

**[Relevant MOC]**:
+ [Link or section update]

### File Operations
**Landing Pad → Permanent:**
- [file.md] → [destination/]

**Frontmatter Additions:**
- [file.md]: tags, created date

**Links Added:**
- [file1.md] ↔ [file2.md]

### Git Commit
```
Session cleanup: [summary]

- [bullet points of changes]
```

**Proceed? [Y/n]**
```

Wait for user confirmation before proceeding.

### Step 4: Execute

After user approves:

1. **Apply context updates** - Edit CLAUDE.md and MOCs
2. **Migrate files** - Use `git mv` for Landing Pad items
3. **Add frontmatter** - Edit new files to add metadata
4. **Add links** - Insert wiki-links where appropriate
5. **Stage changes** - `git add -A`
6. **Commit** - With descriptive message
7. **Push** - `git push origin main`

### Step 5: Summary

Report completion:

```markdown
## Session Complete

**Commit:** [hash]
**Files:** [X] modified, [Y] new, [Z] moved

**Next session context:**
- [Active work items]
- [Pending tasks]

**Landing Pad:** [Empty/X items remaining]
```

## Configuration

See `config/cleanup-rules.yaml` for:
- Path → MOC mappings
- Frontmatter templates by content type
- Landing Pad migration rules

## Edge Cases

**No changes to commit:**
- Report "No changes detected"
- Skip git operations
- Still check Landing Pad for stale items

**Merge conflicts:**
- Abort and inform user
- Do not force push
- Suggest manual resolution

**Large/binary files in Landing Pad:**
- Warn about .gitignore implications
- Do not auto-migrate unless text-based

**Confidential files misplaced:**
- Flag files in wrong location (e.g., Work content in Content/)
- Require explicit confirmation before committing

## Common Patterns

**Session with S2N work:**
- Updates `_S2N-Health-MOC.md`
- Commit message: `S2N: [specific work]`

**Session with content creation:**
- Updates `Content Creation Hub - MOC.md`
- Checks blog frontmatter
- Commit message: `Content: [topic]`

**Mixed session:**
- Multiple MOC updates
- Commit message: `Session cleanup: [summary of areas]`

## Troubleshooting

**"Permission denied" on push:**
- Check SSH key or PAT configuration
- Verify remote URL: `git remote -v`

**Context file conflicts:**
- Read current file state before editing
- Use Edit tool, not Write, for updates

**Missing files after migration:**
- Check git status for unstaged moves
- Use `git mv` not shell `mv`
