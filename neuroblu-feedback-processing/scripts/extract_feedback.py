#!/usr/bin/env python3
"""
Extract actionable feedback from call notes using Claude API.

This script parses markdown call notes, extracts structured feedback using
the Claude API with NeuroBlu product taxonomy, and returns JSON-structured
items ready for database sync.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    import anthropic
    import yaml
except ImportError as e:
    print(f"Error: Missing required package: {e}")
    print("Install with: pip install anthropic PyYAML")
    sys.exit(1)


class FeedbackExtractor:
    """Extract and structure feedback from call notes."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize extractor with configuration."""
        if config_path is None:
            # Default to config directory relative to script location
            script_dir = Path(__file__).parent
            config_path = script_dir.parent / "config" / "taxonomy.yaml"

        # Allow override via environment variable
        config_path = os.getenv('FEEDBACK_CONFIG_PATH', config_path)

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Initialize Anthropic client
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable not set. "
                "Get your key from: https://console.anthropic.com/settings/keys"
            )
        self.client = anthropic.Anthropic(api_key=api_key)

        # Build extraction prompt from taxonomy
        self.extraction_prompt = self._build_extraction_prompt()

    def _build_extraction_prompt(self) -> str:
        """Build the feedback extraction system prompt from taxonomy."""
        # Get product names and keywords
        products = self.config['products']
        product_descriptions = []
        for product in products:
            keywords = ", ".join(product['keywords'][:5])  # First 5 keywords
            product_descriptions.append(f"- {product['name']}: {keywords}")

        product_list = "\n".join(product_descriptions)

        # Get category names and descriptions
        categories = self.config['categories']
        category_descriptions = []
        for cat in categories:
            category_descriptions.append(f"- {cat['name']}: {cat['description']}")

        category_list = "\n".join(category_descriptions)

        # Get priority definitions
        priorities = self.config['priorities']
        priority_descriptions = []
        for prio_name, prio_def in priorities.items():
            priority_descriptions.append(f"- {prio_name}: {prio_def['description']}")

        priority_list = "\n".join(priority_descriptions)

        return f"""You are a feedback extraction specialist for NeuroBlu product development.

Your task is to analyze meeting notes and extract ONLY actionable feedback items.

**Actionable Feedback includes:**
- Feature requests (explicit or implied needs)
- Bug reports and technical issues
- Performance complaints
- Workflow improvements or UX suggestions
- Data quality concerns
- Missing capabilities or gaps
- Blockers preventing user success
- Questions revealing product gaps
- Competitive intelligence
- Strategic opportunities

**NOT Actionable:**
- Status updates
- Scheduling discussions
- Pure informational sharing
- Acknowledgments without substance

**Product Taxonomy:**
{product_list}

**Categories:**
{category_list}

**Priority:**
{priority_list}

**Output Format:**
Return a JSON array of feedback items. Each item must have:
{{
  "title": "One-sentence summary (max 100 chars)",
  "product": "[Product name from taxonomy]",
  "category": "[Category name from taxonomy]",
  "priority": "P0 | P1 | P2 | P3",
  "description": "Detailed context with user quote",
  "use_case": "What they're trying to accomplish",
  "impact": "How this affects user workflow",
  "raw_context": "Full relevant quote from notes",
  "quote": "Most impactful user quote (if available)"
}}

If no actionable feedback found, return empty array: []

Extract feedback systematically. Preserve exact user quotes when possible.
Classify feedback using the taxonomy above. Default to "Other" product/category if unclear.
"""

    def parse_frontmatter(self, note_text: str) -> Dict:
        """Parse markdown frontmatter and content."""
        # Extract frontmatter (between --- markers)
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)', note_text, re.DOTALL)

        if frontmatter_match:
            frontmatter_text = frontmatter_match.group(1)
            body = frontmatter_match.group(2)

            # Parse frontmatter as YAML
            try:
                frontmatter = yaml.safe_load(frontmatter_text)
            except yaml.YAMLError:
                frontmatter = {}
        else:
            frontmatter = {}
            body = note_text

        return {
            'frontmatter': frontmatter,
            'body': body
        }

    def extract_meeting_metadata(self, parsed_note: Dict, file_name: Optional[str] = None) -> Dict:
        """Extract metadata from parsed note."""
        frontmatter = parsed_note['frontmatter']

        # Extract date (from frontmatter or filename)
        meeting_date = None
        if 'date' in frontmatter:
            meeting_date = str(frontmatter['date'])
        elif 'created' in frontmatter:
            meeting_date = str(frontmatter['created'])
        elif file_name:
            # Try to extract from filename (format: YYYY-MM-DD_Title.md)
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', file_name)
            if date_match:
                meeting_date = date_match.group(1)

        if not meeting_date:
            meeting_date = datetime.now().strftime('%Y-%m-%d')

        # Extract title
        title = frontmatter.get('title', file_name or 'Untitled Meeting')
        if file_name and title == 'Untitled Meeting':
            title = file_name.replace('.md', '')

        # Extract attendees
        attendees = frontmatter.get('attendees', [])
        if isinstance(attendees, str):
            attendees = [a.strip() for a in attendees.split(',')]

        # Extract meeting type
        meeting_type = frontmatter.get('meeting_type', 'Call')

        # Extract URL if available
        source_url = frontmatter.get('url', frontmatter.get('source_url', ''))

        return {
            'meeting_type': meeting_type,
            'meeting_date': meeting_date,
            'meeting_title': title,
            'attendees': attendees,
            'source_url': source_url
        }

    def extract_feedback_with_claude(
        self,
        note_content: str,
        metadata: Dict
    ) -> List[Dict]:
        """Use Claude API to extract structured feedback from note content."""

        user_prompt = f"""Meeting Type: {metadata['meeting_type']}
Meeting Title: {metadata['meeting_title']}
Meeting Date: {metadata['meeting_date']}
Attendees: {', '.join(metadata['attendees'])}

Meeting Notes:
{note_content}

Extract all actionable feedback items from these meeting notes. Return only valid JSON array.
"""

        try:
            response = self.client.messages.create(
                model=self.config['claude']['model'],
                max_tokens=self.config['claude']['extraction']['max_tokens'],
                temperature=self.config['claude']['extraction']['temperature'],
                system=self.extraction_prompt,
                messages=[{
                    "role": "user",
                    "content": user_prompt
                }]
            )

            # Extract JSON from response
            response_text = response.content[0].text.strip()

            # Handle markdown code blocks
            json_match = re.search(r'```(?:json)?\n?(.*?)\n?```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)

            feedback_items = json.loads(response_text)

            # Enrich each item with meeting metadata
            for item in feedback_items:
                item.update({
                    'meeting_type': metadata['meeting_type'],
                    'meeting_date': metadata['meeting_date'],
                    'attendees': metadata['attendees'],
                    'source': 'Manual',  # Source type
                    'source_url': metadata['source_url'],
                    'created_date': datetime.now().strftime('%Y-%m-%d'),
                    'updated_date': datetime.now().strftime('%Y-%m-%d'),
                    'status': 'New',
                    'internal': False
                })

            return feedback_items

        except json.JSONDecodeError as e:
            print(f"Error: Claude returned invalid JSON: {e}")
            print(f"Response text: {response_text[:500]}")
            return []
        except Exception as e:
            print(f"Error extracting feedback with Claude: {e}")
            return []

    def process_note_file(self, note_path: Path) -> List[Dict]:
        """Process a single note file and extract feedback."""
        print(f"Processing: {note_path.name}")

        with open(note_path, 'r', encoding='utf-8') as f:
            note_text = f.read()

        # Parse note
        parsed_note = self.parse_frontmatter(note_text)

        # Extract metadata
        metadata = self.extract_meeting_metadata(parsed_note, note_path.name)

        # Extract feedback using Claude
        feedback_items = self.extract_feedback_with_claude(
            parsed_note['body'],
            metadata
        )

        print(f"  → Found {len(feedback_items)} feedback items")

        return feedback_items

    def process_note_text(self, note_text: str) -> List[Dict]:
        """Process note text directly (not from file)."""
        # Parse note
        parsed_note = self.parse_frontmatter(note_text)

        # Extract metadata
        metadata = self.extract_meeting_metadata(parsed_note)

        # Extract feedback using Claude
        feedback_items = self.extract_feedback_with_claude(
            parsed_note['body'],
            metadata
        )

        print(f"Found {len(feedback_items)} feedback items")

        return feedback_items

    def deduplicate_feedback(self, feedback_items: List[Dict], existing_titles: Optional[List[str]] = None) -> List[Dict]:
        """Deduplicate similar feedback items."""
        if existing_titles is None:
            existing_titles = []

        unique_items = []
        seen_titles = set(title.lower().strip() for title in existing_titles)

        for item in feedback_items:
            title_lower = item['title'].lower().strip()
            if title_lower not in seen_titles:
                seen_titles.add(title_lower)
                unique_items.append(item)
            else:
                print(f"  ⚠️  Duplicate detected: {item['title']}")

        return unique_items


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Extract structured feedback from call notes using Claude AI"
    )
    parser.add_argument(
        '--input',
        '-i',
        type=str,
        required=True,
        help="Path to call note file or directory"
    )
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        help="Path to save JSON output (default: stdout)"
    )
    parser.add_argument(
        '--config',
        '-c',
        type=str,
        help="Path to taxonomy.yaml config file"
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help="Show extraction progress"
    )

    args = parser.parse_args()

    try:
        # Initialize extractor
        extractor = FeedbackExtractor(config_path=args.config)

        # Process input
        input_path = Path(args.input)
        all_feedback = []

        if input_path.is_file():
            feedback_items = extractor.process_note_file(input_path)
            all_feedback.extend(feedback_items)
        elif input_path.is_dir():
            # Process all markdown files in directory
            md_files = sorted(input_path.glob('*.md'))
            for note_path in md_files:
                feedback_items = extractor.process_note_file(note_path)
                all_feedback.extend(feedback_items)
        else:
            print(f"Error: Input path does not exist: {input_path}")
            sys.exit(1)

        # Deduplicate
        if extractor.config['processing']['deduplicate']:
            all_feedback = extractor.deduplicate_feedback(all_feedback)

        # Output
        output_json = json.dumps(all_feedback, indent=2)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_json)
            print(f"\n✅ Saved {len(all_feedback)} feedback items to {args.output}")
        else:
            print(output_json)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
