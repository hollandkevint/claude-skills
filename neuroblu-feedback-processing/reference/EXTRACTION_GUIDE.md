# Feedback Extraction Guide

Detailed guide to the AI-powered feedback extraction process, including prompt engineering details, decision rules, and customization options.

## Overview

The extraction process uses Claude Sonnet 4.5 with a structured system prompt to identify actionable feedback items from unstructured call notes and transcripts.

**Model**: `claude-sonnet-4-5-20250929`
**Temperature**: 0.0 (deterministic)
**Max Tokens**: 4,096

## What Gets Extracted

### Actionable Feedback (✓ Extract)

- **Feature requests** - Explicit or implied needs for new capabilities
- **Bug reports** - Broken functionality or incorrect behavior
- **Performance complaints** - Speed, latency, resource usage issues
- **Workflow improvements** - UX friction or process inefficiencies
- **Data quality concerns** - Missing, incorrect, or incomplete data
- **Missing capabilities** - Gaps in platform functionality
- **Blockers** - Critical issues preventing user success
- **Questions revealing gaps** - User confusion indicating product shortcoming
- **Competitive intelligence** - Mentions of competitors or alternatives
- **Strategic opportunities** - Longer-term market insights or use cases

### Non-Actionable Content (✗ Skip)

- **Status updates** - Project progress, timeline updates
- **Scheduling discussions** - Meeting logistics, calendar coordination
- **Pure information sharing** - FYI updates without action needed
- **Acknowledgments** - Simple confirmations or thank-yous
- **Small talk** - Social pleasantries, casual conversation

## Extraction System Prompt

The system prompt is dynamically built from `config/taxonomy.yaml` and includes:

### 1. Product Taxonomy
Lists all products with representative keywords for classification:
- NeuroBlu Analytics
- NeuroBot
- Symptom Intelligence
- Data Platform
- Documentation
- Data Quality
- Other (fallback)

### 2. Category Taxonomy
Defines feedback types with descriptions:
- Feature Request - New capability
- Bug - Broken functionality
- Improvement - Enhancement to existing
- Blocker - Critical issue
- Question - Reveals product gap
- Performance - Speed/scalability
- Usability - UX friction
- Data Quality - Data issues
- Documentation - Guidance gaps
- Other (fallback)

### 3. Priority Definitions
Decision rules for assigning priority:

**P0 (Critical Blocker)**:
- System down or inaccessible
- Data corruption or loss
- Security vulnerability
- Complete workflow blockage

**P1 (High Priority)**:
- Requested by multiple clients
- Strategic customer requirement
- Significant revenue impact
- Competitive disadvantage
- Major workaround required

**P2 (Medium Priority)**:
- Requested by single client
- Notable improvement available
- Workarounds exist but suboptimal
- Enhanced user experience

**P3 (Low Priority)**:
- Nice-to-have enhancement
- Polish or refinement
- Rare edge case
- Future consideration

## Output Format

Each extracted item must include:

```json
{
  "title": "One-sentence summary (max 100 chars)",
  "product": "[Product from taxonomy]",
  "category": "[Category from taxonomy]",
  "priority": "P0 | P1 | P2 | P3",
  "description": "Detailed context with user quote",
  "use_case": "What user is trying to accomplish",
  "impact": "How this affects user workflow",
  "raw_context": "Full relevant quote from notes",
  "quote": "Most impactful user quote (if available)"
}
```

## Classification Rules

### Product Classification

**Primary signals** (in order of priority):
1. **Explicit product mention** - User names specific product
   - "NeuroBot isn't working" → NeuroBot
   - "Cohort Explorer is slow" → NeuroBlu Analytics

2. **Feature-based inference** - Specific functionality mentioned
   - "SQL query assistant" → NeuroBot
   - "cohort builder", "SQL Studio" → NeuroBlu Analytics
   - "PHQ-9 scores", "assessment scales" → Symptom Intelligence

3. **Problem domain** - Type of issue indicates product
   - Performance, infrastructure → Data Platform
   - Missing documentation, unclear guides → Documentation
   - Incorrect data, completeness issues → Data Quality

4. **Default** - If unclear → "Other"

### Category Classification

**Decision flow**:
1. **Is something broken?** → Bug
2. **Is user completely blocked?** → Blocker
3. **Is user asking for new capability?** → Feature Request
4. **Is user suggesting improvement to existing feature?** → Improvement
5. **Is user confused/asking questions?** → Question (if reveals product gap)
6. **Is issue about speed/performance?** → Performance
7. **Is issue about user experience?** → Usability
8. **Is issue about data?** → Data Quality
9. **Is issue about guidance?** → Documentation
10. **Otherwise** → Other

### Priority Assignment

**Decision criteria**:

**Assign P0 if:**
- Words like "down", "broken", "can't access", "critical"
- Complete workflow blockage mentioned
- Data loss or corruption risk
- Security concern

**Assign P1 if:**
- Multiple clients mentioned or implied
- Revenue/contract impact stated
- Competitive disadvantage noted
- Strategic importance emphasized
- Significant manual workaround required

**Assign P2 if:**
- Single client request
- Improvement available but not critical
- Workaround exists and is reasonable
- "Would be nice", "could improve" language

**Assign P3 if:**
- Polish or refinement
- Edge case scenario
- "Someday", "eventually" language
- Low frequency issue

**Default**: P2 (when priority unclear)

## Extraction Quality Guidelines

### Title Writing

**Good titles** (clear, specific):
- ✓ "Export cohort definitions for reuse across studies"
- ✓ "Dashboard load times exceed 10 seconds for large datasets"
- ✓ "Add video tutorials for initial platform setup"

**Poor titles** (vague, ambiguous):
- ✗ "Improve cohort feature"
- ✗ "Dashboard is slow"
- ✗ "Need better documentation"

**Rules**:
- Start with verb or noun (not "User wants...")
- Be specific about what/where/when
- Max 100 characters
- No jargon or acronyms unless necessary

### Description Writing

**Good descriptions** (context + quote):
```
Users want to save cohort logic and reuse it across multiple studies
without rebuilding from scratch. Currently spending 2+ hours recreating
the same cohorts monthly. Quote: "We spend 2 hours recreating the same
cohort every month - it's our biggest time sink."
```

**Poor descriptions** (no context):
```
User wants cohort export feature.
```

**Rules**:
- Include user's situation (what they're trying to do)
- Include current pain point (what's not working)
- Include impact (how much time/effort wasted)
- Include direct quote when available
- 2-4 sentences typical

### Quote Selection

**Good quotes** (impactful, specific):
- ✓ "We spend 2 hours recreating the same cohort every month"
- ✓ "I leave for coffee while the dashboard loads - it's that slow"
- ✓ "Our new analyst spent a week just trying to understand the data dictionary"

**Poor quotes** (vague, generic):
- ✗ "This is a problem"
- ✗ "It doesn't work well"
- ✗ "We need this"

**Rules**:
- Use exact user words (not paraphrased)
- Choose most emotionally resonant quote
- Prefer quotes with specifics (numbers, timeframes, comparisons)
- Avoid quotes that need additional context to understand

## Use Case & Impact

### Use Case
**Purpose**: Describe what user is trying to accomplish (the "job to be done")

**Good examples**:
- "Quarterly reporting on recurring patient cohorts"
- "Comparing treatment outcomes across multiple studies"
- "Training new team members on platform capabilities"

**Format**: Brief phrase or sentence describing the goal/task

### Impact
**Purpose**: Describe how current limitation affects user

**Good examples**:
- "Spends 2+ hours monthly recreating cohorts manually"
- "Unable to meet client reporting deadlines"
- "New users take 2 weeks to become productive vs 2 days expected"

**Format**: Specific consequence with metrics when possible

## Customization

### Adding New Products

Edit `config/taxonomy.yaml`:

```yaml
products:
  - name: "New Product Name"
    keywords:
      - keyword1
      - keyword2
      - keyword3
```

The extraction prompt automatically includes all products from config.

### Adding New Categories

Edit `config/taxonomy.yaml`:

```yaml
categories:
  - name: "New Category Name"
    description: "Clear description of when to use this category"
```

### Adjusting Priority Thresholds

Priority assignment is based on language patterns in the extraction prompt. To adjust:

1. Edit the priority definitions in `scripts/extract_feedback.py`
2. Update the `_build_extraction_prompt()` method
3. Add/remove decision criteria in the priority section

**Note**: Changes to priority logic require code modification, not just config changes.

## Troubleshooting

### No Items Extracted

**Possible causes**:
- Notes contain no actionable feedback (valid result)
- Notes are pure status updates or scheduling
- Frontmatter missing (metadata extraction fails)

**Solutions**:
- Review notes content - is there actual feedback?
- Check frontmatter format (must be valid YAML)
- Run with `--verbose` flag to see extraction details

### Wrong Product/Category

**Possible causes**:
- Ambiguous language in notes
- Keywords not in taxonomy
- Multiple products mentioned

**Solutions**:
- Add missing keywords to `config/taxonomy.yaml`
- Make product/feature mentions more explicit in notes
- Manually correct during review checkpoint

### Priority Seems Wrong

**Possible causes**:
- Subjective priority assessment
- Missing context in notes
- Priority language not matching patterns

**Solutions**:
- Review priority definitions - do they match your criteria?
- Add more context to notes (impact, urgency, stakeholder)
- Manually adjust priority during review checkpoint

### Missing Quotes

**Possible causes**:
- No direct quotes in source notes
- Quotes too short or generic
- Extraction prompt prioritizing context over quotes

**Solutions**:
- Ensure call notes include verbatim user statements
- Use quote marks ("") around actual user words in notes
- Quotes are optional - extraction succeeds without them

## Cost & Performance

### API Costs
- Extraction: ~$0.03-0.05 per call note (varies by length)
- Model: Claude Sonnet 4.5 (premium tier)
- Token usage: Typically 2,000-4,000 input tokens, 500-1,500 output tokens

### Processing Time
- Single note: 3-10 seconds (depends on note length)
- Batch of 10 notes: 30-100 seconds
- Most time spent in API calls (not local processing)

### Rate Limits
- Claude API: Varies by tier (Enterprise: 4,000 RPM)
- Batch processing recommended for large volumes
- Built-in retry logic handles transient errors

## Best Practices

1. **Write detailed call notes** - More context = better extraction
2. **Include direct quotes** - Verbatim user words are most valuable
3. **Use consistent frontmatter** - Date, attendees, meeting_type required
4. **Review extracted items** - Always check before syncing to database
5. **Iterate on taxonomy** - Add products/categories as needed
6. **Monitor costs** - Track API usage, especially for large batches
7. **Test prompt changes** - Validate on sample notes before deploying
8. **Document edge cases** - Track cases where extraction fails or produces wrong results

## Version History

**Version 1.0** (2025-11-20):
- Initial extraction prompt design
- Dynamic taxonomy loading from YAML
- Priority decision rules
- JSON output format
- Error handling and fallbacks
