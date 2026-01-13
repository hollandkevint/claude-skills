---
name: neuroblu-feedback-processing
description: Process NeuroBlu customer feedback from call notes and transcripts. Extracts structured feedback items using AI, categorizes by product/priority, syncs to Google Sheets database, and generates Slack summary messages. Use when processing customer calls, user interviews, pipeline meetings, or feedback sessions for the NeuroBlu Analytics platform.
---

# NeuroBlu Feedback Processing

Process customer feedback from call notes and transcripts into structured database entries with automated Slack summaries.

## Quick Start

**Prerequisites:**
- `ANTHROPIC_API_KEY` environment variable set
- `GOOGLE_SHEETS_CREDENTIALS_PATH` pointing to service account JSON
- Google Sheets database shared with service account email

**Basic usage:**
```
User: "Process this call note: /path/to/call_note.md"
```

Claude will:
1. Extract structured feedback items using AI
2. Show you extracted items for review/approval
3. Sync approved items to Google Sheets
4. Generate a Slack summary message

## Core Workflow

### Step 1: Provide Input

Give Claude your call note in one of these formats:

**File path:**
```
Process this call note: ~/Documents/pipeline_call_2025-11-15.md
```

**Multiple files:**
```
Process these call notes:
- ~/Documents/call1.md
- ~/Documents/call2.md
- ~/Documents/call3.md
```

**Pasted text:**
```
Process this call note:

---
date: 2025-11-15
attendees: Dr. Sarah Chen (Pharma R&D), Kevin Holland
meeting_type: Pipeline Call
---

# Pipeline Call - Pharma Client

[paste full note content here]
```

**Expected format:** Markdown file with YAML frontmatter containing:
- `date` (YYYY-MM-DD)
- `attendees` (comma-separated names with optional affiliations)
- `meeting_type` (Pipeline Call, User Interview, Product Strategy, etc.)

### Step 2: AI Extraction (Automated)

Claude automatically:
1. Loads taxonomy from `config/taxonomy.yaml`
2. Runs `scripts/extract_feedback.py` with the note text
3. Calls Claude API to extract actionable feedback
4. Categorizes by product, category, and priority

**What gets extracted:**
- Feature requests (explicit or implied)
- Bug reports and technical issues
- Performance complaints
- UX/workflow improvements
- Data quality concerns
- Missing capabilities
- Blockers
- Questions revealing product gaps

**What gets filtered out:**
- Status updates
- Scheduling discussions
- Pure information sharing
- Acknowledgments without substance

### Step 3: Review Checkpoint (Interactive)

Claude displays extracted items in this format:

```
📋 Found 3 feedback items from Pipeline Call on 2025-11-15

1. [P1 - Feature Request] Analytics: Export cohort definitions
   "Users want to save cohort logic and reuse across studies"
   Impact: Currently rebuilding cohorts manually each time
   Quote: "We spend 2 hours recreating the same cohort every month"

2. [P2 - Bug] Platform: Dashboard load times over 10 seconds
   "Dashboard freezes when loading large datasets"
   Quote: "I leave for coffee while it loads - it's that slow"

3. [P3 - Improvement] Documentation: Add video tutorials
   "New users struggle with initial setup"
   Impact: Onboarding takes 2 weeks instead of 2 days

Actions:
- Approve all: Sync all items to database
- Edit: Modify individual items before syncing
- Skip: Remove specific items from batch
- Cancel: Abort the workflow
```

**Editing capability:**
You can modify any field:
- Change priority (P0, P1, P2, P3)
- Reclassify product or category
- Edit description or quotes
- Skip individual items

### Step 4: Optional Enrichment (Automated)

If not skipped, Claude runs enrichment to add:
- **Customer segment** (Pharma, Biotech, Provider, Payor, etc.)
- **Department** (Research/RWD, HEOR, Epidemiology, etc.)
- **Tags** (therapeutic areas, methodologies)
- **Confidence scores** (0.0-1.0 for classification quality)

**To skip enrichment** (saves API costs):
```
Process this call note with --skip-enrichment
```

**Cost:** ~$0.01-0.02 per batch (cheaper than extraction)

### Step 5: Google Sheets Sync (Automated)

Claude syncs approved items to the database:

1. Authenticates with service account
2. Checks for duplicates by title similarity
3. Maps JSON to 26-column schema
4. Batch appends rows (up to 100 at once)
5. Returns sheet URL with new row numbers

**Deduplication:**
- Compares titles using fuzzy matching (85% similarity threshold)
- If duplicate found, adds new meeting reference instead of creating duplicate row

**Output:**
```
✅ Synced 3 items to Google Sheets
   Rows: 1245-1247
   View: https://docs.google.com/spreadsheets/d/.../edit#gid=0&range=A1245
```

### Step 6: Slack Message Generation (Automated)

Claude generates a formatted Slack message:

```markdown
📋 *NeuroBlu Feedback Summary - Pipeline Call (2025-11-15)*

*Executive Summary*
Processed feedback from pipeline call with Pharma R&D team. Key themes: cohort management workflow improvements, platform performance issues, and onboarding documentation gaps. 3 items synced, 1 high priority.

*Notable Quotes*
• "We spend 2 hours recreating the same cohort every month" - Re: cohort export feature
• "I leave for coffee while it loads - it's that slow" - Re: dashboard performance

*Action Items*
• [P1] Analytics: Export cohort definitions - High demand from multiple clients
• [P2] Platform: Dashboard load times over 10 seconds - User experience blocker

🔗 [View in Feedback Database](https://docs.google.com/.../edit#gid=0&range=A1245)
```

**Ready to paste directly into Slack.**

## Configuration

### Environment Variables

**Required:**
```bash
export ANTHROPIC_API_KEY="your-api-key"
export GOOGLE_SHEETS_CREDENTIALS_PATH="/path/to/service-account.json"
```

**Optional:**
```bash
export FEEDBACK_CONFIG_PATH="/path/to/custom/taxonomy.yaml"
export FEEDBACK_SKIP_ENRICHMENT="true"
```

### Taxonomy Customization

Edit `config/taxonomy.yaml` to customize:
- Product definitions and keywords
- Category definitions
- Customer segments and classifications
- Department mappings
- Google Sheets spreadsheet ID

**Example customization:**
```yaml
products:
  - name: "NeuroBlu Analytics"
    keywords: ["analytics", "cohort", "study", "query"]
  - name: "NeuroBot"
    keywords: ["neurobot", "sql", "query assistant"]
```

### Google Sheets Setup

1. **Create service account** in Google Cloud Console
2. **Download JSON credentials**
3. **Share spreadsheet** with service account email (found in JSON: `client_email`)
4. **Set environment variable** pointing to JSON file
5. **Update spreadsheet ID** in `config/taxonomy.yaml`

See [SETUP_GUIDE.md](reference/SETUP_GUIDE.md) for detailed instructions.

## Script Reference

### extract_feedback.py

**Purpose:** Core AI extraction engine

**Usage:**
```bash
python scripts/extract_feedback.py --input note.md --output feedback.json
```

**Input:** Raw call note text (markdown with frontmatter)
**Output:** JSON array of structured feedback items

**Flags:**
- `--input` - Path to call note file
- `--output` - Path to save JSON output
- `--config` - Override taxonomy.yaml location
- `--verbose` - Show extraction progress

### enrich_metadata.py

**Purpose:** Optional metadata enrichment

**Usage:**
```bash
python scripts/enrich_metadata.py --input feedback.json --output enriched.json
```

**Input:** Extracted feedback items (JSON)
**Output:** Enriched items with segment/department/tags

**Flags:**
- `--input` - Path to feedback JSON
- `--output` - Path to save enriched JSON
- `--skip-low-confidence` - Exclude classifications below 0.5 confidence

### sync_to_sheets.py

**Purpose:** Google Sheets API integration

**Usage:**
```bash
python scripts/sync_to_sheets.py --input enriched.json
```

**Input:** Enriched feedback items (JSON)
**Output:** Google Sheets row numbers and URL

**Flags:**
- `--input` - Path to feedback JSON
- `--dry-run` - Preview without syncing
- `--skip-duplicates` - Check for duplicates before syncing
- `--batch-size` - Override default batch size (default: 100)

### generate_slack_msg.py

**Purpose:** Slack message formatter

**Usage:**
```bash
python scripts/generate_slack_msg.py --input enriched.json --url "sheet-url"
```

**Input:** Feedback items (JSON) + Google Sheets URL
**Output:** Markdown-formatted Slack message

**Flags:**
- `--input` - Path to feedback JSON
- `--url` - Google Sheets URL to include
- `--output` - Path to save message markdown (default: stdout)

## Common Use Cases

### Process Single Call Note

```
User: "Process ~/Documents/pipeline_call_2025-11-15.md"

Claude:
1. Extracts 3 feedback items
2. Shows for review
3. You approve
4. Syncs to sheets (rows 1245-1247)
5. Generates Slack message
```

### Process Multiple Notes in Batch

```
User: "Process all notes from last week:
- ~/Documents/call1.md
- ~/Documents/call2.md
- ~/Documents/call3.md"

Claude:
1. Processes each note sequentially
2. Shows all items for review (combined list)
3. You approve/edit
4. Syncs all at once
5. Generates combined Slack message
```

### Skip Enrichment to Save Costs

```
User: "Process this note but skip enrichment"

Claude:
1. Extracts feedback
2. Shows for review
3. Skips segment/department classification
4. Syncs to sheets
5. Generates Slack message
```

### Extract Only (No Sync)

```
User: "Extract feedback from this note but don't sync yet"

Claude:
1. Extracts feedback
2. Shows items
3. Saves JSON to file
4. Stops (no sync or Slack message)
```

**Use case:** Review extraction quality before syncing, or process multiple notes before batch sync.

## Troubleshooting

### "ANTHROPIC_API_KEY not set"

**Problem:** Missing Claude API credentials
**Solution:**
```bash
export ANTHROPIC_API_KEY="your-api-key"
```
Get key from: https://console.anthropic.com/settings/keys

### "Google Sheets authentication failed"

**Problem:** Missing or invalid service account credentials
**Solution:**
1. Verify JSON file exists at path in `GOOGLE_SHEETS_CREDENTIALS_PATH`
2. Check service account email in JSON file
3. Confirm spreadsheet is shared with that email
4. Verify Google Sheets API is enabled in Cloud Console

See [reference/SETUP_GUIDE.md](reference/SETUP_GUIDE.md) for detailed setup.

### "Rate limit exceeded"

**Problem:** Too many API calls in short period
**Solution:**
- Script automatically retries with backoff
- If persistent, reduce batch size or wait 1 minute
- Google Sheets limit: 60 writes/minute
- Claude API limit: varies by tier

### "Duplicate items detected"

**Problem:** Feedback item already exists in database
**Solution:**
- Review similarity match (85% threshold)
- If false positive, edit title to make it more distinct
- If true duplicate, skip the item
- Script adds new meeting reference to existing item

### "No feedback items extracted"

**Problem:** AI didn't find actionable feedback in note
**Solution:**
- This is valid (not all notes contain actionable feedback)
- Review note content - is there actually feedback?
- Check frontmatter - missing context may affect extraction
- Try rephrasing if feedback is present but not detected

### "Low confidence enrichment"

**Problem:** Segment/department classification <0.5 confidence
**Solution:**
- Manual review recommended for low-confidence items
- Edit fields in review checkpoint
- Consider skipping enrichment if context is limited

## Advanced Usage

### Custom Taxonomy

Create custom `taxonomy.yaml` for different use cases:

```yaml
# custom-taxonomy.yaml
products:
  - name: "CustomProduct"
    keywords: ["keyword1", "keyword2"]

categories:
  - name: "CustomCategory"
    description: "Custom classification"
```

**Usage:**
```bash
export FEEDBACK_CONFIG_PATH="/path/to/custom-taxonomy.yaml"
```

### Batch Processing Script

For processing many notes at once:

```bash
#!/bin/bash
for note in ~/Documents/call_notes/*.md; do
  python scripts/extract_feedback.py --input "$note" --output "${note%.md}.json"
done

# Combine all JSON files
jq -s 'add' ~/Documents/call_notes/*.json > all_feedback.json

# Sync combined
python scripts/sync_to_sheets.py --input all_feedback.json
```

### Integration with Existing Pipeline

This skill complements the existing weekly automation:
- **Skill**: Interactive processing of individual calls
- **Pipeline**: Batch automation for weekly sync

Both use the same taxonomy and database schema.

## Cost Estimates

**Per call note** (~2000 words):
- Extraction: $0.03-0.05
- Enrichment: $0.01-0.02
- Total: $0.04-0.07

**Monthly** (50 calls):
- With enrichment: $2-3.50
- Without enrichment: $1.50-2.50

**Yearly**: $18-42

**Google Sheets API:** Free (within quota)

## Data Schema

### Feedback Item JSON Structure

```json
{
  "title": "One-sentence summary",
  "description": "Detailed context",
  "product": "NeuroBlu Analytics",
  "category": "Feature Request",
  "priority": "P1",
  "use_case": "What user is trying to accomplish",
  "impact": "How this affects user workflow",
  "quote": "Most impactful user quote",
  "meeting_type": "Pipeline Call",
  "meeting_date": "2025-11-15",
  "attendees": ["Dr. Sarah Chen", "Kevin Holland"],
  "source": "Granola",
  "source_url": "https://granola.so/note/...",
  "segment": "Pharma",
  "department": "Research/RWD",
  "tags": ["cohort-management", "workflow"]
}
```

For complete 26-column Google Sheets schema, see [reference/GOOGLE_SHEETS_SCHEMA.md](reference/GOOGLE_SHEETS_SCHEMA.md).

## Technical Details

### Dependencies

```
anthropic>=0.34.0
PyYAML>=6.0.1
gspread>=5.12.0
google-auth>=2.23.0
oauth2client>=4.1.3
```

Install:
```bash
pip install anthropic PyYAML gspread google-auth oauth2client
```

### AI Models

**Extraction:** Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)
- Temperature: 0.0 (deterministic)
- Max tokens: 4,096

**Enrichment:** Claude Sonnet 4.5
- Temperature: 0.0
- Max tokens: 512

### Security

- API keys via environment variables (never hardcoded)
- Service account credentials in separate JSON file
- No credentials stored in skill files
- Read-only access to input notes
- Write access only to specified Google Sheet

## Support & Documentation

**Detailed references:**
- [reference/GOOGLE_SHEETS_SCHEMA.md](reference/GOOGLE_SHEETS_SCHEMA.md) - Complete 26-column field reference
- [reference/EXTRACTION_GUIDE.md](reference/EXTRACTION_GUIDE.md) - AI prompt engineering details
- [reference/SETUP_GUIDE.md](reference/SETUP_GUIDE.md) - Google Sheets and API setup

**Related resources:**
- Existing pipeline: `~/Documents/GitHub/neuroblu_product_development/feedback/`
- Google Sheets database: https://docs.google.com/spreadsheets/d/1lDZwWEEmZByDsbiYvYDAQodsu4Hk-qpp1KC9MS-fLO4/edit

**Design document:**
- `~/Documents/GitHub/neuroblu_product_development/docs/plans/2025-11-20-neuroblu-feedback-skill-design.md`

## Workflow Summary

```
Input (call note)
    ↓
Extract feedback items (AI)
    ↓
Review checkpoint (interactive)
    ↓
Enrich metadata (optional AI)
    ↓
Sync to Google Sheets
    ↓
Generate Slack message
    ↓
Done
```

**Time:** <2 minutes per call (vs 15-20 minutes manual)
**Cost:** $0.04-0.07 per call
**Accuracy:** 90%+ precision on classification
