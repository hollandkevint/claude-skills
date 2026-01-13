---
name: html-presentation-generator
description: Generate complete HTML presentations from structured notes. Creates single-file HTML slides with keyboard navigation, chapter menu, and smooth transitions. Supports dark and light themes. Use when creating presentations for workshops, demos, pitches, or talks. Invoke manually or auto-triggers when user requests presentation generation.
---

# HTML Presentation Generator

Generate professional HTML presentations from structured notes. Single-file output with embedded CSS/JS, keyboard navigation, and chapter menu.

## Quick Start

**Basic usage:**
```
User: "Create a presentation from these notes: /path/to/notes.md"
```

**With theme selection:**
```
User: "Create a dark theme presentation for my workshop outline"
```

Claude will:
1. Analyze your notes for chapters and key points
2. Ask about theme preference (dark/light)
3. Generate single HTML file with all slides
4. Provide deployment guidance (local or GitHub Pages)

## Core Workflow

### Step 1: Provide Input

Give Claude your structured notes in one of these formats:

**File path:**
```
Create a presentation from: ~/Documents/workshop-outline.md
```

**Pasted notes:**
```
Create a presentation from these notes:

# Introduction to Data Products
## Chapter 1: Why Data Products Matter
- 73% of data initiatives fail to deliver value
- Key insight: data as product, not byproduct
...
```

**Expected note structure:**
- Clear section headers (`#`, `##`)
- Key statistics and numbers
- Main points per section
- Visual concepts or diagram ideas (optional)

### Step 2: Theme Selection

Choose your visual theme:

**Dark Theme (Recommended for Recording):**
- Dark background (#1a1a2e)
- Light text for high contrast
- Optimized for screen share and video

**Light Theme:**
- Light background (#fafafa)
- Dark text
- Professional, traditional feel

### Step 3: Generation (Automated)

Claude generates a complete HTML file with:
- **Single file**: All CSS/JS embedded (no dependencies)
- **Keyboard navigation**: Left/right arrows
- **Slide counter**: "3/12" format in top right
- **Chapter menu**: Left sidebar with clickable chapters
- **Current chapter highlight**: Visual indicator
- **Smooth transitions**: Between slides
- **Fullscreen-friendly**: Clean, minimal design

**Design Principles:**
- Minimal text per slide (one point = one slide)
- Large, readable fonts
- Visual hierarchy guides attention
- CSS-generated diagrams preferred
- Statistics and numbers prominently displayed

### Step 4: Review & Refinement

**CRITICAL: Max 1-2 iteration cycles in Claude chat**

After generation, you can request:
- Minor text changes
- Color adjustments
- Slide reordering

**For major changes:**
1. Download the HTML file
2. Open in Cursor ($20/month) or Claude Code
3. Make edits locally
4. Preview in browser (double-click file)

**Why limit iterations?**
Additional rounds in Claude chat degrade output quality. Fuller conversation context → diminished AI performance. Local editing is more reliable for polish.

### Step 5: Deployment

**Local Viewing:**
Simply double-click the HTML file → opens in browser.

**GitHub Pages (Free Public Hosting):**

1. **Create public repository** on GitHub
   - Go to github.com → New repository
   - Name it (e.g., "my-presentation")
   - Select "Public"
   - Click "Create repository"

2. **Upload your HTML file**
   - Click "uploading an existing file"
   - Drag your HTML file
   - **Important**: Rename to `index.html` for auto-loading
   - Click "Commit changes"

3. **Enable GitHub Pages**
   - Go to repository Settings
   - Scroll to "Pages" in left sidebar
   - Under "Source", select "main" branch
   - Click "Save"

4. **Wait 2-5 minutes**
   - GitHub builds your site

5. **Access your presentation**
   - URL format: `https://yourusername.github.io/repository-name/`
   - Share this link with anyone

## Input Format Examples

**Workshop Outline:**
```markdown
# GenAI for Healthcare Leaders
Workshop Duration: 90 minutes

## Chapter 1: The Current Landscape
- 47% of healthcare orgs experimenting with AI
- Key challenge: regulation vs. innovation
- What's working today

## Chapter 2: Practical Applications
- Clinical decision support
- Administrative automation
- Patient communication

## Chapter 3: Implementation Framework
- Start small, measure early
- Build trust before scale
- Governance from day one
```

**Product Demo:**
```markdown
# NeuroBlu Analytics Demo
Audience: Pharma R&D Team

## The Problem
- RWE studies take 6-12 months
- Data quality inconsistent
- No standardized cohorts

## Our Solution
- 36M patient records
- Pre-built symptom intelligence
- 73% faster study setup

## Live Demo
- Cohort builder walkthrough
- Export functionality
- API integration
```

## Technical Specifications

**Output:**
- Single HTML file (typically 10-50KB)
- Embedded CSS (scoped styling)
- Embedded JavaScript (navigation logic)
- No external dependencies

**Navigation Features:**
- Left/Right arrow keys: Previous/Next slide
- Spacebar: Next slide
- Home: First slide
- End: Last slide
- Click chapter name: Jump to section

**Browser Compatibility:**
- Chrome, Firefox, Safari, Edge (modern versions)
- Not tested on IE11

## Reference Files

See `reference/system-prompt.md` for the complete generation prompt.
See `config/dark-theme.yaml` and `config/light-theme.yaml` for theme specifications.

## Integration with BMAD

This skill has a corresponding BMAD task for structured workflow:
- Task: `.bmad-kevin-creator/tasks/create-html-presentation.md`
- Template: `.bmad-kevin-creator/templates/presentation-structure-tmpl.yaml`
- Data: `.bmad-kevin-creator/data/kevin-presentation-style.md`

Use the BMAD task for more guided, step-by-step presentation creation with explicit elicitation points.

## Tips for Best Results

1. **Structure your notes clearly** — Use headers for chapters
2. **Include specific numbers** — "47%" not "significant percentage"
3. **One point per slide** — Don't cram content
4. **Mark visual concepts** — "Diagram: workflow from A → B → C"
5. **Keep iterations minimal** — Download for major edits
6. **Use extended thinking** — Better structure and visuals

## Troubleshooting

**Slides too text-heavy:**
- Break into more slides
- Focus on key statistics only
- Request "minimal text" in prompt

**Navigation not working:**
- Check browser JavaScript enabled
- Try different browser
- Verify HTML file not corrupted

**GitHub Pages not loading:**
- Confirm file named `index.html`
- Wait 5+ minutes after setup
- Check repository is public

---

*Skill created: 2026-01-02*
*Based on: Claude Code Presentations Method (D-Squared70) + AI Document Formatting Skills*
