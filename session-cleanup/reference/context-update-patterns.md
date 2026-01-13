# Context Update Patterns

How to update CLAUDE.md and MOC files during session cleanup.

## CLAUDE.md Update Patterns

### Recent Developments Section

Location: After "## Recent Developments" header

**Format:**
```markdown
### [Topic Name] (NEW - [Month] [Day], [Year])
[Brief description of what's new]
- **Location**: `[path/to/files/]`
- **Key Document**: `[main-file.md]`
- **Status**: [Current status]
```

**When to add:**
- New project started
- New system/capability implemented
- Significant milestone reached

**Example:**
```markdown
### Session Cleanup Skill (NEW - Jan 12, 2026)
Automated end-of-session workflow for vault maintenance:
- **Location**: `~/.claude/skills/session-cleanup/`
- **Key Documents**: `SKILL.md`, `cleanup-rules.yaml`
- **Status**: Active
```

### Active Projects Table

Location: Under "**Active Projects:**" in Current Priorities

**Format:**
```markdown
| Project | Status | Next Milestone |
|---------|--------|----------------|
| **Project Name** | **Status** | Next milestone description |
```

**Status values:**
- `Active` - Work in progress
- `Paused` - On hold
- `✅ COMPLETE` - Finished (will move to archive)
- `🔜 Starting` - About to begin

**When to update:**
- Status changed
- Milestone completed
- New milestone identified

### Current Priorities Section

**Format:** Numbered list under "This Quarter's Focus"

**When to update:**
- Priority order changed
- Item completed (mark with ✅)
- New priority added

---

## MOC Update Patterns

### Adding New Document Links

**Location:** Relevant section within the MOC

**Format:**
```markdown
- [[Document-Name]] - Brief description (Date added)
```

**Or in table format:**
```markdown
| Document | Purpose | Status |
|----------|---------|--------|
| [[New-Doc]] | What it does | Active |
```

### Updating Status Sections

MOCs typically have status tracking sections. Update these with:
- Date of last update
- Current state
- Next actions

**Example pattern from S2N MOC:**
```markdown
## Current Status
*Last updated: [Date]*

**Active Workstreams:**
- [Workstream 1] - [Status]
- [Workstream 2] - [Status]

**Recent Completions:**
- [Completed item] (Date)
```

---

## Link Insertion Patterns

### Wiki-Links

Insert `[[filename]]` references where appropriate:

**In new content:**
- Link to related existing documents
- Link to source materials (literature notes)
- Link to parent MOC

**In existing content:**
- Add backlinks when new related content created
- Update "Related Resources" sections

### Cross-Reference Format

```markdown
## Related Resources
- [[Related-Document-1]] - How it relates
- [[Related-Document-2]] - How it relates
```

---

## Frontmatter Patterns

### Blog Posts
```yaml
---
tags:
  - "#type/blog"
  - "#status/draft"
  - "#topic/[relevant-topic]"
platform: blog
created: YYYY-MM-DD
---
```

### Literature Notes
```yaml
---
tags:
  - "#type/literature-note"
  - "#source/[type]"
source: "[URL or citation]"
author: "[Author name]"
created: YYYY-MM-DD
---
```

### Project Documents
```yaml
---
tags:
  - "#type/project-doc"
  - "#project/[project-name]"
project: "[Project Name]"
status: active
created: YYYY-MM-DD
---
```

### Meeting Notes
```yaml
---
tags:
  - "#type/meeting"
  - "#project/[relevant-project]"
attendees:
  - "[Person 1]"
  - "[Person 2]"
created: YYYY-MM-DD
---
```

---

## Detection Heuristics

### Identifying Content Type

**Blog post indicators:**
- Location in `📝 Content/Blog/`
- Filename contains "blog" or topic slug
- First line is `# [Title]` style header

**Literature note indicators:**
- Filename ends with `-Literature-Note.md`
- Contains `Source:` or `Author:` references
- Location in `🧠 Knowledge Base/Resources/`

**Meeting note indicators:**
- Contains "Meeting" in title
- Has attendee list
- Timestamped filename
- Located in `📞 Granola Meeting Notes/`

### Identifying Missing Links

**Signs a document needs links:**
- No `[[` wiki-links in body
- Not referenced in any MOC
- Related documents exist but aren't linked
- Orphan in Obsidian graph view

---

## Examples

### Session that created a new blog post

**CLAUDE.md update:**
```markdown
### CLI Tools Blog Series
Active 3-part blog series...
- **Status**: Part 0-2 at 85-90% → Part 3 draft started
```

**Content MOC update:**
```markdown
| [[cli-tools-part-3]] | Integration patterns | Draft |
```

### Session with S2N strategy work

**S2N MOC update:**
```markdown
## Current Status
*Last updated: 2026-01-12*

**Recent Activity:**
- Completed strategy deck review
- Added [[Strategy-Validation-Analysis-Jan2026]]
```

### Session adding literature notes

**Literature Notes Index update:**
```markdown
- [[New-Author-Topic-Literature-Note]] - Key insights from [source]
```

**Related blog post update (if exists):**
```markdown
## Sources
- [[New-Author-Topic-Literature-Note]] - Foundation for [section]
```
