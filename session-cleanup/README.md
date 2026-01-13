# Session Cleanup

End-of-session workflow for Kevin's Obsidian vault.

## What It Does

- Updates context files (CLAUDE.md, MOCs) with session work
- Processes Landing Pad items to permanent locations
- Adds frontmatter and wiki-links to new files
- Commits and pushes all changes

## Quick Start

```
/session-cleanup
```

Or say: "wrap up", "end session", "cleanup", "done for today"

## Workflow

1. **Inventory** - Scan git status, categorize changes
2. **Analyze** - Auto-detect context updates, cleanup tasks
3. **Preview** - Single confirmation of all proposed changes
4. **Execute** - Apply updates, commit, push
5. **Summary** - Report completion, set up next session

## Key Features

| Feature | Description |
|---------|-------------|
| Auto-detect MOCs | Updates relevant MOC based on changed file paths |
| Landing Pad processing | Migrates items to proper permanent locations |
| Frontmatter check | Ensures new files have tags and dates |
| Single commit | All session work in one descriptive commit |

## Files

```
session-cleanup/
├── SKILL.md              # Full workflow
├── README.md             # This file
├── config/
│   └── cleanup-rules.yaml  # Path mappings, templates
└── reference/
    └── context-update-patterns.md  # Context file patterns
```

## Related

- [[CLAUDE.md]] - Main vault context file
- [[Content Creation Hub - MOC]] - Content system navigation
- [[_S2N-Health-MOC]] - S2N engagement tracking

---
*Created: 2026-01-12*
