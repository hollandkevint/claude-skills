#!/usr/bin/env python3
"""
Slack Message Generator - Format feedback items into Slack summary.

Creates copy-paste ready Slack messages with:
- Executive summary (2-3 sentences)
- Notable quotes (up to 3 most impactful)
- Action items (P0/P1 priorities)
- Link to Google Sheets database
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List


class SlackMessageGenerator:
    """Generate formatted Slack messages from feedback items."""

    def generate_summary(self, items: List[Dict]) -> str:
        """Generate 2-3 sentence executive summary."""
        if not items:
            return "No feedback items to summarize."

        total = len(items)
        high_priority = len([i for i in items if i.get('priority') in ['P0', 'P1']])

        # Group by product
        products = {}
        for item in items:
            product = item.get('product', 'Other')
            products[product] = products.get(product, 0) + 1

        top_products = sorted(products.items(), key=lambda x: x[1], reverse=True)[:3]
        product_str = ', '.join([f"{p} ({c})" for p, c in top_products])

        # Group by category for themes
        categories = {}
        for item in items:
            category = item.get('category', 'Other')
            categories[category] = categories.get(category, 0) + 1

        top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]
        theme_str = ', '.join([c.lower() for c, _ in top_categories])

        # Get meeting info if available
        meeting_info = ""
        if items and items[0].get('meeting_type'):
            meeting_type = items[0].get('meeting_type', 'Call')
            meeting_date = items[0].get('meeting_date', '')
            if meeting_date:
                meeting_info = f" from {meeting_type} on {meeting_date}"

        summary = f"Processed {total} feedback items{meeting_info}. "
        summary += f"Key themes: {theme_str}. "
        summary += f"Products affected: {product_str}. "

        if high_priority > 0:
            summary += f"{high_priority} high priority items require attention."

        return summary

    def select_quotes(self, items: List[Dict], max_quotes: int = 3) -> List[Dict]:
        """Select most impactful quotes from feedback items."""
        items_with_quotes = [
            item for item in items
            if item.get('quote') and item.get('quote').strip()
        ]

        # Prioritize by:
        # 1. P0/P1 items first
        # 2. Longer quotes (more detail)
        # 3. Items with explicit quotes

        def quote_score(item):
            priority_score = {'P0': 1000, 'P1': 100, 'P2': 10, 'P3': 1}.get(item.get('priority', 'P3'), 0)
            length_score = len(item.get('quote', ''))
            return priority_score + length_score

        sorted_items = sorted(items_with_quotes, key=quote_score, reverse=True)

        return sorted_items[:max_quotes]

    def identify_actions(self, items: List[Dict]) -> List[Dict]:
        """Extract P0/P1 priority action items."""
        high_priority = [
            item for item in items
            if item.get('priority') in ['P0', 'P1']
        ]

        # Sort by priority (P0 first)
        sorted_items = sorted(
            high_priority,
            key=lambda x: 0 if x.get('priority') == 'P0' else 1
        )

        return sorted_items

    def format_slack_message(
        self,
        items: List[Dict],
        sheet_url: str,
        include_quotes: bool = True,
        include_actions: bool = True
    ) -> str:
        """Generate complete Slack message."""
        if not items:
            return "No feedback items to format."

        # Header
        meeting_info = ""
        if items and items[0].get('meeting_type'):
            meeting_type = items[0].get('meeting_type', 'Call')
            meeting_date = items[0].get('meeting_date', '')
            if meeting_date:
                meeting_info = f" - {meeting_type} ({meeting_date})"

        message = f"📋 *NeuroBlu Feedback Summary{meeting_info}*\n\n"

        # Executive Summary
        message += f"*Executive Summary*\n"
        message += self.generate_summary(items) + "\n\n"

        # Notable Quotes
        if include_quotes:
            quote_items = self.select_quotes(items)
            if quote_items:
                message += f"*Notable Quotes*\n"
                for item in quote_items:
                    quote = item.get('quote', '')
                    context = f"{item.get('product', 'Unknown')}: {item.get('title', 'Untitled')[:40]}"
                    message += f"• \"{quote}\" - Re: {context}\n"
                message += "\n"

        # Action Items
        if include_actions:
            action_items = self.identify_actions(items)
            if action_items:
                message += f"*Action Items*\n"
                for item in action_items:
                    priority = item.get('priority', 'P3')
                    product = item.get('product', 'Other')
                    title = item.get('title', 'Untitled')
                    impact = item.get('impact', '')
                    context = f" - {impact}" if impact else ""
                    message += f"• [{priority}] {product}: {title}{context}\n"
                message += "\n"

        # Link to Database
        message += f"🔗 <{sheet_url}|View in Feedback Database>\n"

        return message


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate Slack summary message from feedback items"
    )
    parser.add_argument(
        '--input',
        '-i',
        type=str,
        required=True,
        help="Path to feedback JSON file"
    )
    parser.add_argument(
        '--url',
        '-u',
        type=str,
        required=True,
        help="Google Sheets URL to include in message"
    )
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        help="Path to save message markdown (default: stdout)"
    )
    parser.add_argument(
        '--no-quotes',
        action='store_true',
        help="Exclude quotes section"
    )
    parser.add_argument(
        '--no-actions',
        action='store_true',
        help="Exclude action items section"
    )

    args = parser.parse_args()

    try:
        # Load feedback items
        with open(args.input, 'r') as f:
            feedback_items = json.load(f)

        if not isinstance(feedback_items, list):
            print("Error: Input JSON must be an array of feedback items")
            sys.exit(1)

        # Generate message
        generator = SlackMessageGenerator()
        message = generator.format_slack_message(
            feedback_items,
            args.url,
            include_quotes=not args.no_quotes,
            include_actions=not args.no_actions
        )

        # Output
        if args.output:
            with open(args.output, 'w') as f:
                f.write(message)
            print(f"✅ Saved Slack message to {args.output}")
        else:
            print(message)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
