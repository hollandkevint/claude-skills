---
name: s2n-github-observability
description: Weekly observability check for S2N Health GitHub activity. Run with "Check S2N GitHub status" or "What's shipping at S2N?"
---

# S2N GitHub Observability

This skill provides tactical and strategic visibility into S2N Health's GitHub activity across RepSignal and DataStreams products.

## Quick Commands

- **"Check S2N GitHub status"** - Full observability report
- **"Show S2N open PRs"** - List all pending pull requests
- **"What's shipping at S2N?"** - Recent merged PRs (last 7 days)
- **"S2N sprint status"** - Current sprint (v2.33) breakdown

## Workflow

When this skill is triggered, execute these steps in order:

### Step 1: Open Pull Requests

Query open PRs across active repos:
- `S2N-Health/bandon` (backend)
- `S2N-Health/salesforce-repsignal` (frontend)
- `S2N-Health/bandon-data` (data warehouse)

Report:
- PR number, title, author
- Days open (flag if > 7 days)
- Failing checks or review blockers

### Step 2: Recent Commits (Last 7 Days)

For each active repo, show:
- Commit count by author
- Most recent commit date
- Flag repos with no activity

### Step 3: Current Sprint (GitHub Projects v2)

Query project #81 (v2.33 or current sprint):
- Items by status (Done, In Progress, Todo, To Define)
- Stale items (no movement > 7 days)
- Blocked items

### Step 4: Summary Report

Generate markdown report with:
- **Tactical**: What's shipping this week
- **Strategic**: Are priorities aligned with roadmap?
- **Blockers**: PRs stuck, items stale

Save to: `💼 Work/S2N-Health/Engagement-Tracking/Weekly-GitHub-Reports/YYYY-MM-DD-GitHub-Report.md`

## Key Repos

| Repo | Product | Primary |
|------|---------|---------|
| bandon | RepSignal Backend | Blake, Nick |
| salesforce-repsignal | RepSignal UI | Andy, Lien, Pranav |
| bandon-data | DataStreams | Blake, Addie |
| repsignal-agentforce | AI/GenAI | (Kevin's focus) |

## Key Contributors

- @blakeaschenbrener - Backend + Data
- @AndyLeS2N - Frontend Lead
- @lien-s2n - Mobile
- @PranavS2N - Frontend
- @Kchirsch-s2n - Kelsey (Product)

## Cross-Reference

- [[GitHub-Repo-Inventory]] - Full repo details
- [[GitHub-Projects-Map]] - Sprint board structure
- [[S2N-Initiative-Backlog-Dec2025]] - Quarterly priorities
- FigJam: https://www.figma.com/board/D3Ca3FsQ4TN6NNWl7QQMzp/

## MCP Requirement

This skill requires the `s2n-github` MCP server to be active.

If MCP not available, use direct API calls with PAT stored in environment.

## Weekly Cadence

Run this skill:
- **Monday morning** - Start of week status
- **Friday afternoon** - End of week summary
- **Before Kelsey calls** - Context for discussions
