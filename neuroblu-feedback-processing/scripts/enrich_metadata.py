#!/usr/bin/env python3
"""
Feedback Enrichment Agent - Claude AI powered metadata enrichment.

Analyzes feedback items and enriches them with:
- Segment classification (Pharma, Biotech, Payor, etc.)
- Department classification (Research/RWD, HEOR, etc.)
- Enhanced tags based on context
- Confidence scores for classifications
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    import anthropic
    import yaml
except ImportError as e:
    print(f"Error: Missing required package: {e}")
    print("Install with: pip install anthropic PyYAML")
    sys.exit(1)


class FeedbackEnricher:
    """Enrich feedback items with segment, department, and tags using Claude AI."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize enricher with configuration."""
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

        # Load enrichment configuration
        self.segments = self.config['segments']
        self.departments = self.config['departments']

        # Build enrichment system prompt
        self.enrichment_prompt = self._build_enrichment_prompt()

    def _build_enrichment_prompt(self) -> str:
        """Build Claude system prompt for enrichment."""
        # Format segment taxonomy
        segment_taxonomy = "\n".join([
            f"- **{segment}**: {', '.join(data['keywords'][:5])}"
            for segment, data in self.segments.items() if data['keywords']
        ])

        # Format department taxonomy
        department_taxonomy = "\n".join([
            f"- **{dept}**: {', '.join(data['keywords'][:5])}"
            for dept, data in self.departments.items() if data['keywords']
        ])

        return f"""You are a feedback classification specialist for NeuroBlu, a behavioral health real-world evidence (RWE) platform.

Your task is to analyze customer feedback and enrich it with structured metadata to enable better product insights and use case development.

# INPUT FIELDS

You will receive feedback items with these fields:
- **attendees**: Meeting attendees (may include company/role info)
- **description**: Detailed feedback description
- **use_case**: What user is trying to accomplish
- **raw_context**: Full original context

# OUTPUT REQUIRED

Return a JSON object with:
{{
  "segment": "<segment from taxonomy>",
  "department": "<department from taxonomy>",
  "enriched_tags": ["<tag1>", "<tag2>", ...],
  "segment_confidence": 0.0-1.0,
  "department_confidence": 0.0-1.0,
  "reasoning": "Brief explanation of classification"
}}

# SEGMENT TAXONOMY

{segment_taxonomy}
- **Other**: Use when none of the above fit

# DEPARTMENT TAXONOMY

{department_taxonomy}
- **Other**: Use when none of the above fit

# ENRICHMENT RULES

**Segment Classification:**
1. Analyze attendees for company names and industry keywords
2. If company matches segment keywords → assign that segment (high confidence)
3. If company unclear, use description + use_case context
4. Default to "Other" if uncertain (low confidence)

**Department Classification:**
1. Analyze attendees for department/role keywords
2. Analyze use_case and description for department keywords
3. Match to most relevant department taxonomy
4. For pharma/biotech, prioritize research-focused departments
5. Default to "Other" if uncertain (low confidence)

**Tag Enrichment:**
1. Preserve concept from existing feedback
2. Add use-case specific tags (e.g., "real-world-data", "patient-outcomes")
3. Add therapeutic area tags if mentioned (e.g., "schizophrenia", "depression")
4. Add methodology tags (e.g., "cohort-analysis", "time-series")
5. Keep tags concise and hyphenated (e.g., "safety-monitoring")
6. Maximum 10 total tags (prioritize most relevant)

**Confidence Scoring:**
- **1.0**: Exact keyword match in attendees/company
- **0.8-0.9**: Strong contextual evidence
- **0.6-0.7**: Moderate inference from description
- **0.4-0.5**: Weak inference, could be multiple categories
- **< 0.4**: Very uncertain, defaulting to "Other"

# IMPORTANT

- Always return valid JSON
- Use exact taxonomy values (case-sensitive)
- Provide confidence scores for transparency
- Default to "Other" when uncertain
- Brief reasoning helps human review
"""

    def enrich_feedback_item(
        self,
        feedback_item: Dict,
        dry_run: bool = False
    ) -> Dict:
        """
        Enrich a single feedback item with segment, department, and tags.

        Args:
            feedback_item: Feedback item dict with attendees, description, etc.
            dry_run: If True, skip API call and return mock enrichment

        Returns:
            Updated feedback item with enrichment metadata added
        """
        # Extract fields for enrichment
        attendees = feedback_item.get('attendees', [])
        if isinstance(attendees, str):
            attendees = [a.strip() for a in attendees.split(',') if a.strip()]
        attendees_str = ', '.join(attendees) if attendees else "(not provided)"

        description = feedback_item.get('description', '').strip()
        use_case = feedback_item.get('use_case', '').strip()
        raw_context = feedback_item.get('raw_context', '').strip()

        # Build user prompt (truncated to save input tokens)
        user_prompt = f"""Analyze this feedback item and return enrichment JSON:

**Attendees:** {attendees_str}
**Description:** {description[:300] if description else "(not provided)"}
**Use Case:** {use_case[:200] if use_case else "(not provided)"}
**Raw Context:** {raw_context[:200] if raw_context else "(not provided)"}

Return only valid JSON with segment, department, enriched_tags, segment_confidence, department_confidence, and reasoning.
"""

        if dry_run:
            # Return mock enrichment for testing
            return {
                "segment": "Other",
                "department": "Other",
                "enriched_tags": ["dry-run"],
                "segment_confidence": 0.5,
                "department_confidence": 0.5,
                "reasoning": "Dry run mode - no API call made"
            }

        try:
            # Call Claude API
            response = self.client.messages.create(
                model=self.config['claude']['model'],
                max_tokens=self.config['claude']['enrichment']['max_tokens'],
                temperature=self.config['claude']['enrichment']['temperature'],
                system=self.enrichment_prompt,
                messages=[{
                    "role": "user",
                    "content": user_prompt
                }]
            )

            # Parse JSON response
            response_text = response.content[0].text.strip()

            # Extract JSON (handle code blocks)
            json_match = re.search(r'```(?:json)?\n?(.*?)\n?```', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(1)

            enrichment = json.loads(response_text)

            # Validate required fields
            required_fields = ['segment', 'department', 'enriched_tags', 'segment_confidence', 'department_confidence']
            for field in required_fields:
                if field not in enrichment:
                    raise ValueError(f"Missing required field: {field}")

            # Validate taxonomies
            if enrichment['segment'] not in self.segments:
                print(f"  ⚠️  Invalid segment '{enrichment['segment']}', defaulting to 'Other'")
                enrichment['segment'] = 'Other'
                enrichment['segment_confidence'] = 0.0

            if enrichment['department'] not in self.departments:
                print(f"  ⚠️  Invalid department '{enrichment['department']}', defaulting to 'Other'")
                enrichment['department'] = 'Other'
                enrichment['department_confidence'] = 0.0

            return enrichment

        except json.JSONDecodeError as e:
            print(f"  ✗ JSON parse error: {e}")
            print(f"  Response: {response_text[:200]}")
            # Return fallback enrichment
            return {
                "segment": "Other",
                "department": "Other",
                "enriched_tags": [],
                "segment_confidence": 0.0,
                "department_confidence": 0.0,
                "reasoning": f"Parse error: {str(e)}"
            }

        except Exception as e:
            print(f"  ✗ Enrichment error: {e}")
            # Return fallback enrichment
            return {
                "segment": "Other",
                "department": "Other",
                "enriched_tags": [],
                "segment_confidence": 0.0,
                "department_confidence": 0.0,
                "reasoning": f"Error: {str(e)}"
            }

    def enrich_batch(
        self,
        feedback_items: List[Dict],
        dry_run: bool = False,
        skip_low_confidence: bool = False
    ) -> List[Dict]:
        """
        Enrich a batch of feedback items.

        Args:
            feedback_items: List of feedback item dicts
            dry_run: If True, skip API calls
            skip_low_confidence: If True, exclude classifications with <0.5 confidence

        Returns:
            List of feedback items with enrichment added
        """
        enriched_items = []

        for i, item in enumerate(feedback_items, 1):
            print(f"  Enriching item {i}/{len(feedback_items)}: {item.get('title', 'Untitled')[:50]}...")

            enrichment = self.enrich_feedback_item(item, dry_run=dry_run)

            # Apply enrichment to item
            item['segment'] = enrichment['segment']
            item['department'] = enrichment['department']
            item['segment_confidence'] = enrichment['segment_confidence']
            item['department_confidence'] = enrichment['department_confidence']

            # Handle low confidence
            if skip_low_confidence:
                if enrichment['segment_confidence'] < 0.5:
                    item['segment'] = 'Uncertain'
                if enrichment['department_confidence'] < 0.5:
                    item['department'] = 'Uncertain'

            # Add enriched tags
            existing_tags = item.get('tags', [])
            if isinstance(existing_tags, str):
                existing_tags = [t.strip() for t in existing_tags.split(',') if t.strip()]

            all_tags = list(set(existing_tags + enrichment['enriched_tags']))
            item['tags'] = all_tags

            enriched_items.append(item)

        return enriched_items


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Enrich feedback items with segment and department classifications"
    )
    parser.add_argument(
        '--input',
        '-i',
        type=str,
        required=True,
        help="Path to feedback JSON file"
    )
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        help="Path to save enriched JSON output (default: overwrites input)"
    )
    parser.add_argument(
        '--config',
        '-c',
        type=str,
        help="Path to taxonomy.yaml config file"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Skip API calls (for testing)"
    )
    parser.add_argument(
        '--skip-low-confidence',
        action='store_true',
        help="Mark classifications below 0.5 confidence as 'Uncertain'"
    )

    args = parser.parse_args()

    try:
        # Load feedback items
        with open(args.input, 'r') as f:
            feedback_items = json.load(f)

        if not isinstance(feedback_items, list):
            print("Error: Input JSON must be an array of feedback items")
            sys.exit(1)

        print(f"Loaded {len(feedback_items)} feedback items")

        # Initialize enricher
        enricher = FeedbackEnricher(config_path=args.config)

        # Enrich items
        print("\nEnriching feedback items...")
        enriched_items = enricher.enrich_batch(
            feedback_items,
            dry_run=args.dry_run,
            skip_low_confidence=args.skip_low_confidence
        )

        # Output
        output_path = args.output or args.input
        with open(output_path, 'w') as f:
            json.dump(enriched_items, f, indent=2)

        print(f"\n✅ Saved {len(enriched_items)} enriched items to {output_path}")

        # Print summary
        segments = {}
        departments = {}
        for item in enriched_items:
            seg = item.get('segment', 'Unknown')
            dept = item.get('department', 'Unknown')
            segments[seg] = segments.get(seg, 0) + 1
            departments[dept] = departments.get(dept, 0) + 1

        print("\nSegment distribution:")
        for seg, count in sorted(segments.items(), key=lambda x: x[1], reverse=True):
            print(f"  {seg}: {count}")

        print("\nDepartment distribution:")
        for dept, count in sorted(departments.items(), key=lambda x: x[1], reverse=True):
            print(f"  {dept}: {count}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
