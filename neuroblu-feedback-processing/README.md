# NeuroBlu Feedback Processing Skill

AI-powered feedback extraction and database sync for NeuroBlu customer calls.

## Quick Start

```bash
# Set environment variables
export ANTHROPIC_API_KEY="your-api-key"
export GOOGLE_SHEETS_CREDENTIALS_PATH="/path/to/service-account.json"

# Process a call note
claude: "Process this call note: ~/Documents/call_2025-11-15.md"
```

Claude will:
1. Extract structured feedback items using AI
2. Show items for your review/approval
3. Sync to Google Sheets database
4. Generate Slack summary message

## What's Included

```
neuroblu-feedback-processing/
├── SKILL.md                      # Main workflow instructions
├── config/
│   └── taxonomy.yaml             # Product/category/segment definitions
├── scripts/
│   ├── extract_feedback.py       # AI extraction engine
│   ├── enrich_metadata.py        # Optional enrichment
│   ├── sync_to_sheets.py         # Google Sheets sync
│   └── generate_slack_msg.py     # Slack message formatter
└── reference/
    ├── GOOGLE_SHEETS_SCHEMA.md   # 26-column schema reference
    └── EXTRACTION_GUIDE.md       # Prompt engineering details
```

## Setup

### 1. Install Dependencies

```bash
pip install anthropic PyYAML gspread google-auth oauth2client
```

### 2. Get Anthropic API Key

1. Go to https://console.anthropic.com/settings/keys
2. Create new API key
3. Set environment variable:
   ```bash
   export ANTHROPIC_API_KEY="your-key-here"
   ```

### 3. Setup Google Sheets Access

1. Create service account in Google Cloud Console
2. Download JSON credentials
3. Share spreadsheet with service account email (found in JSON)
4. Set environment variable:
   ```bash
   export GOOGLE_SHEETS_CREDENTIALS_PATH="/path/to/credentials.json"
   ```

## Usage with Claude

### Process Single Call Note

```
User: "Process ~/Documents/pipeline_call_2025-11-15.md"
```

### Process Multiple Notes

```
User: "Process all notes from last week:
- ~/Documents/call1.md
- ~/Documents/call2.md
- ~/Documents/call3.md"
```

### Skip Enrichment (Save Costs)

```
User: "Process this note but skip enrichment"
```

## Expected Input Format

Call notes should be markdown files with YAML frontmatter:

```markdown
---
date: 2025-11-15
attendees: Dr. Sarah Chen (Pharma R&D), Kevin Holland
meeting_type: Pipeline Call
---

# Pipeline Call - Pharma Client

[Meeting content here...]
```

## Cost Estimates

**Per call note** (~2000 words):
- Extraction: $0.03-0.05
- Enrichment: $0.01-0.02 (optional)
- Total: $0.04-0.07

**Monthly** (50 calls): $2-3.50
**Yearly**: $18-42

## Customization

### Edit Product Taxonomy

Edit `config/taxonomy.yaml`:

```yaml
products:
  - name: "New Product"
    keywords:
      - keyword1
      - keyword2
```

### Edit Categories

```yaml
categories:
  - name: "New Category"
    description: "When to use this category"
```

### Update Google Sheets ID

```yaml
google_sheets:
  spreadsheet_id: "your-spreadsheet-id"
  worksheet_name: "Your Worksheet Name"
```

## Standalone Script Usage

You can also run the scripts directly:

```bash
# Extract feedback
python scripts/extract_feedback.py --input call.md --output feedback.json

# Enrich metadata
python scripts/enrich_metadata.py --input feedback.json --output enriched.json

# Sync to sheets
python scripts/sync_to_sheets.py --input enriched.json

# Generate Slack message
python scripts/generate_slack_msg.py --input enriched.json --url "sheet-url"
```

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY="your-api-key"
```

### "Google Sheets authentication failed"
1. Verify JSON file exists
2. Check service account email in JSON
3. Confirm spreadsheet shared with that email
4. Verify Google Sheets API enabled in Cloud Console

### "No feedback items extracted"
- Valid result if no actionable feedback in notes
- Check frontmatter format (must be valid YAML)
- Review note content - is there actual feedback?

## Documentation

- **SKILL.md** - Complete workflow guide
- **GOOGLE_SHEETS_SCHEMA.md** - Database schema reference
- **EXTRACTION_GUIDE.md** - AI extraction details

## Related Resources

- Existing pipeline: `~/Documents/GitHub/neuroblu_product_development/feedback/`
- Google Sheets database: https://docs.google.com/spreadsheets/d/1lDZwWEEmZByDsbiYvYDAQodsu4Hk-qpp1KC9MS-fLO4/edit
- Design document: `~/Documents/GitHub/neuroblu_product_development/docs/plans/2025-11-20-neuroblu-feedback-skill-design.md`

## Version

**Version**: 1.0
**Created**: 2025-11-20
**Status**: Production Ready
