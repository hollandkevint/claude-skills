#!/usr/bin/env python3
"""
Google Sheets Sync - Batch upload feedback items to database.

Handles:
- Service account authentication
- Duplicate detection by title similarity
- Batch operations (up to 100 rows at once)
- 26-column schema mapping
- Error handling and retries
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    import gspread
    from google.oauth2.service_account import Credentials
    import yaml
except ImportError as e:
    print(f"Error: Missing required package: {e}")
    print("Install with: pip install gspread google-auth oauth2client PyYAML")
    sys.exit(1)


class FeedbackSheetsSync:
    """Sync feedback items to Google Sheets database."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize sync with configuration."""
        if config_path is None:
            # Default to config directory relative to script location
            script_dir = Path(__file__).parent
            config_path = script_dir.parent / "config" / "taxonomy.yaml"

        # Allow override via environment variable
        config_path = os.getenv('FEEDBACK_CONFIG_PATH', config_path)

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Get credentials path
        credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
        if not credentials_path:
            raise ValueError(
                "GOOGLE_SHEETS_CREDENTIALS_PATH environment variable not set. "
                "Point to your service account JSON file."
            )

        if not Path(credentials_path).exists():
            raise FileNotFoundError(f"Credentials file not found: {credentials_path}")

        # Authenticate
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
        self.client = gspread.authorize(creds)

        # Open spreadsheet
        spreadsheet_id = self.config['google_sheets']['spreadsheet_id']
        worksheet_name = self.config['google_sheets']['worksheet_name']

        try:
            self.spreadsheet = self.client.open_by_key(spreadsheet_id)
            self.worksheet = self.spreadsheet.worksheet(worksheet_name)
        except gspread.exceptions.APIError as e:
            print(f"Error accessing Google Sheets: {e}")
            print(f"Make sure:")
            print(f"1. Spreadsheet ID is correct: {spreadsheet_id}")
            print(f"2. Worksheet '{worksheet_name}' exists")
            print(f"3. Service account has edit access to the spreadsheet")
            raise

    def get_existing_titles(self) -> List[str]:
        """Get all existing titles from database for duplicate detection."""
        try:
            # Get column B (titles) - skip header row
            titles = self.worksheet.col_values(2)[1:]  # Column B is index 2
            return [t.strip().lower() for t in titles if t.strip()]
        except Exception as e:
            print(f"Warning: Could not fetch existing titles: {e}")
            return []

    def check_duplicate(self, title: str, existing_titles: List[str], threshold: float = 0.85) -> bool:
        """Check if title is duplicate using simple string matching."""
        title_lower = title.strip().lower()

        for existing in existing_titles:
            # Simple exact match (can be enhanced with fuzzy matching)
            if title_lower == existing:
                return True

        return False

    def format_row(self, item: Dict) -> List[str]:
        """Format feedback item into 26-column row (A-Z)."""
        # Generate unique ID if not present
        if 'id' not in item or not item['id']:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            item['id'] = f"FB-{timestamp}-{hash(item.get('title', ''))}"[:20]

        # Helper to format list fields
        def format_list(field):
            if isinstance(field, list):
                return ', '.join(str(x) for x in field if x)
            return str(field) if field else ''

        # Map to 26 columns (A-Z)
        row = [
            item.get('id', ''),                                    # A: ID
            item.get('title', '')[:100],                          # B: Title (truncate to 100 chars)
            item.get('description', ''),                          # C: Description
            item.get('source', 'Manual'),                         # D: Type/Source
            item.get('status', 'New'),                            # E: Status
            item.get('priority', 'P3'),                           # F: Priority
            item.get('product', 'Other'),                         # G: Product
            item.get('category', 'Other'),                        # H: Category
            item.get('segment', ''),                              # I: Segment
            item.get('department', ''),                           # J: Department
            item.get('segment', ''),                              # K: Customer Segment (duplicate for legacy)
            format_list(item.get('attendees', [])).split(',')[0] if item.get('attendees') else '',  # L: Company (first attendee)
            '',                                                    # M: Persona (manual entry)
            '',                                                    # N: Email (manual entry)
            'N' if not item.get('internal', False) else 'Y',     # O: Internal (Y/N)
            format_list(item.get('attendees', [])).split(',')[0] if item.get('attendees') else '',  # P: Contact (first attendee)
            item.get('created_date', datetime.now().strftime('%Y-%m-%d')),  # Q: Created Date
            item.get('updated_date', datetime.now().strftime('%Y-%m-%d')),  # R: Updated Date
            format_list(item.get('attendees', [])),               # S: Attendees
            format_list(item.get('tags', [])),                    # T: Tags
            item.get('meeting_type', ''),                         # U: Meeting Type
            item.get('meeting_date', ''),                         # V: Meeting Date
            item.get('source', 'Manual'),                         # W: Source
            item.get('source_url', ''),                           # X: Source URL
            item.get('use_case', ''),                             # Y: Insights/Use Case
            item.get('quote', '')                                 # Z: Quote
        ]

        return row

    def batch_append(self, items: List[Dict], batch_size: int = 100) -> Dict:
        """Batch append items to spreadsheet."""
        if not items:
            return {'synced': 0, 'skipped': 0, 'rows': []}

        # Format rows
        rows = [self.format_row(item) for item in items]

        # Get existing titles for deduplication
        if self.config['processing']['deduplicate']:
            print("  Checking for duplicates...")
            existing_titles = self.get_existing_titles()

            # Filter out duplicates
            non_duplicate_items = []
            non_duplicate_rows = []
            skipped_count = 0

            for item, row in zip(items, rows):
                if self.check_duplicate(item['title'], existing_titles):
                    print(f"  ⚠️  Skipping duplicate: {item['title'][:50]}")
                    skipped_count += 1
                else:
                    non_duplicate_items.append(item)
                    non_duplicate_rows.append(row)

            items = non_duplicate_items
            rows = non_duplicate_rows
        else:
            skipped_count = 0

        if not rows:
            print("  No new items to sync (all duplicates)")
            return {'synced': 0, 'skipped': skipped_count, 'rows': []}

        # Append rows
        try:
            print(f"  Syncing {len(rows)} rows to Google Sheets...")
            self.worksheet.append_rows(rows, value_input_option='USER_ENTERED')

            # Get row numbers (assuming append goes to end)
            last_row = len(self.worksheet.col_values(1))  # Column A
            first_new_row = last_row - len(rows) + 1
            row_numbers = list(range(first_new_row, last_row + 1))

            print(f"  ✅ Synced rows {first_new_row}-{last_row}")

            return {
                'synced': len(rows),
                'skipped': skipped_count,
                'rows': row_numbers
            }

        except gspread.exceptions.APIError as e:
            if 'RATE_LIMIT_EXCEEDED' in str(e):
                print("  ⚠️  Rate limit exceeded, retrying in 60 seconds...")
                time.sleep(60)
                return self.batch_append(items, batch_size)
            else:
                raise

    def get_sheet_url(self, row_numbers: Optional[List[int]] = None) -> str:
        """Get URL to spreadsheet, optionally with row range."""
        base_url = f"https://docs.google.com/spreadsheets/d/{self.spreadsheet.id}/edit"

        if row_numbers and len(row_numbers) > 0:
            first_row = min(row_numbers)
            last_row = max(row_numbers)
            # Add range anchor to URL
            return f"{base_url}#gid={self.worksheet.id}&range=A{first_row}:Z{last_row}"

        return base_url


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Sync feedback items to Google Sheets database"
    )
    parser.add_argument(
        '--input',
        '-i',
        type=str,
        required=True,
        help="Path to feedback JSON file"
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
        help="Preview without syncing"
    )
    parser.add_argument(
        '--skip-duplicates',
        action='store_true',
        help="Check for duplicates before syncing (default: enabled)"
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=100,
        help="Batch size for syncing (default: 100)"
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

        if args.dry_run:
            print("\n🔍 DRY RUN - No changes will be made")
            # Just show what would be synced
            for i, item in enumerate(feedback_items, 1):
                print(f"  {i}. [{item.get('priority', 'P3')}] {item.get('product', 'Other')}: {item.get('title', 'Untitled')[:60]}")
            print(f"\nWould sync {len(feedback_items)} items")
            return

        # Initialize syncer
        syncer = FeedbackSheetsSync(config_path=args.config)

        # Sync items
        print("\nSyncing to Google Sheets...")
        result = syncer.batch_append(feedback_items, batch_size=args.batch_size)

        # Generate URL
        sheet_url = syncer.get_sheet_url(result['rows'])

        print(f"\n✅ Sync complete!")
        print(f"  Synced: {result['synced']} items")
        print(f"  Skipped: {result['skipped']} duplicates")
        if result['rows']:
            print(f"  Rows: {min(result['rows'])}-{max(result['rows'])}")
        print(f"\n🔗 View: {sheet_url}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
