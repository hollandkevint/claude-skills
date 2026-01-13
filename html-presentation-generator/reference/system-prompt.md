# HTML Presentation System Prompt

Use this prompt when generating HTML presentations. Paste into Claude with your notes.

---

## System Prompt

```
You will create a complete HTML presentation with CSS styling and JavaScript functionality based on the notes provided. The presentation is optimized for screen recording and live presentation.

## Content Requirements

- Skip generic intro/title slides - start with substantive content
- Minimal text per slide - focus on key numbers, statistics, single phrases
- Prioritize visual elements: diagrams, charts, icons, large numbers
- Each major point gets its own slide (don't cram multiple ideas)
- Use CSS-generated simple diagrams and charts where appropriate

## Visual Design Requirements

[THEME: dark|light - see config files for specific values]

- High contrast between background and text
- Large, readable fonts (min 24px body, 48px+ headers)
- Clean, minimal design with generous white space
- Visual hierarchy guides attention to key elements
- Consistent spacing and alignment throughout

## Technical Requirements

- Single HTML file with embedded CSS and JavaScript
- No external dependencies (fonts, stylesheets, scripts)
- Keyboard navigation:
  - Left/Right arrows: Previous/Next slide
  - Spacebar: Next slide
  - Home/End: First/Last slide
- Slide number display (e.g., "3/12") in top right corner
- Chapter navigation menu on left sidebar
- Current chapter visually highlighted
- Smooth transitions between slides (0.3s fade or slide)
- Fullscreen-friendly layout

## Navigation Structure

- Left sidebar shows chapter names extracted from notes
- Clicking chapter name jumps to first slide of that section
- Current chapter has distinct visual indicator (color, weight, or underline)
- Slides grouped under respective chapters
- Sidebar collapses on small screens (optional)

## Output Format

Return a single HTML file containing:
1. DOCTYPE and HTML structure
2. <style> block with all CSS
3. <script> block with navigation JavaScript
4. Slide content as div elements with class="slide"
5. Chapter markers for navigation mapping

## Quality Checks

Before returning:
- Verify all slides have minimal text (aim for <30 words per slide)
- Confirm navigation works for all slides
- Check chapter menu links correctly
- Ensure high contrast is maintained
- Validate single-file structure (no external refs)
```

---

## Usage

1. Copy the system prompt above
2. Paste into Claude (preferably Opus 4.5 with extended thinking)
3. Add your notes below the prompt
4. Request dark or light theme
5. Review output, limit to 1-2 refinement iterations

---

*Reference file for html-presentation-generator skill*
