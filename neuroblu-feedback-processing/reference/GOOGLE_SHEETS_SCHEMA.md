# Google Sheets Database Schema

Complete reference for the 26-column NeuroBlu Feedback Database structure.

## Database URL

https://docs.google.com/spreadsheets/d/1lDZwWEEmZByDsbiYvYDAQodsu4Hk-qpp1KC9MS-fLO4/edit

## Schema Overview

The database uses columns A-Z (26 columns total) to store structured feedback items.

| Column | Field | Type | Required | Validation |
|--------|-------|------|----------|------------|
| A | ID | Text | Auto-generated | Unique identifier |
| B | Title | Text | Yes | Max 100 chars |
| C | Description | Long Text | Yes | Detailed feedback |
| D | Type | Dropdown | Yes | Source type |
| E | Status | Dropdown | Yes | Workflow status |
| F | Priority | Dropdown | Yes | P0-P3 priority |
| G | Product | Dropdown | Yes | Product taxonomy |
| H | Category | Dropdown | Yes | Category taxonomy |
| I | Segment | Text | No | Customer segment |
| J | Department | Text | No | Customer department |
| K | Customer Segment | Text | No | (Duplicate of I for legacy) |
| L | Company | Text | No | Organization name |
| M | Persona | Dropdown | No | User role/title |
| N | Email | Email | No | Contact email |
| O | Internal | Y/N | No | Internal vs external |
| P | Contact | Text | No | Contact person |
| Q | Created Date | Date | Yes | YYYY-MM-DD |
| R | Updated Date | Date | Yes | YYYY-MM-DD |
| S | Attendees | Text | No | Comma-separated |
| T | Tags | Text | No | Comma-separated |
| U | Meeting Type | Dropdown | No | Type of meeting |
| V | Meeting Date | Date | No | Specific date |
| W | Source | Text | No | Feedback source |
| X | Source URL | URL | No | Link to original |
| Y | Insights | Long Text | No | Key findings |
| Z | Quote | Long Text | No | Verbatim user quote |

## Field Definitions

### A: ID
**Type**: Text
**Required**: Auto-generated if not provided
**Format**: `FB-YYYYMMDDHHMMSS-HASH`
**Purpose**: Unique identifier for each feedback item

### B: Title
**Type**: Text (max 100 characters)
**Required**: Yes
**Purpose**: One-sentence summary of feedback
**Example**: "Export cohort definitions for reuse across studies"

### C: Description
**Type**: Long Text
**Required**: Yes
**Purpose**: Detailed context including user quote and situation
**Example**: "Users want to save cohort logic and reuse it across multiple studies without rebuilding from scratch. Currently spending 2+ hours recreating the same cohorts monthly."

### D: Type
**Type**: Dropdown
**Required**: Yes
**Options**:
- Granola (from Granola meeting notes)
- AirFocus (historical import)
- Interview (user interview snapshots)
- Manual (manually entered)
- Zapier (webhook automation)

### E: Status
**Type**: Dropdown
**Required**: Yes
**Options**:
- New (just added, not triaged)
- In Progress (being worked on)
- Done (completed)
- Closed (resolved or rejected)
- Archived (historical record)

### F: Priority
**Type**: Dropdown
**Required**: Yes
**Options**:
- P0 (Critical blocker)
- P1 (High priority, strategic)
- P2 (Medium priority, valuable)
- P3 (Low priority, nice-to-have)
- Not Prioritized

### G: Product
**Type**: Dropdown
**Required**: Yes
**Options**:
- NeuroBlu Analytics
- NeuroBot
- Symptom Intelligence
- Data Platform
- Documentation
- Data Quality
- Other

### H: Category
**Type**: Dropdown
**Required**: Yes
**Options**:
- Feature Request
- Bug
- Improvement
- Blocker
- Question
- Client Feedback
- Strategic Initiative
- Performance
- Usability
- Other

### I: Segment
**Type**: Text
**Required**: No (enriched via AI)
**Options**:
- Pharma
- Biotech
- Payor
- Provider
- Healthtech
- Government
- Academic Research
- Other

**Purpose**: Customer market segment classification

### J: Department
**Type**: Text
**Required**: No (enriched via AI)
**Options**:
- Research/RWD
- HEOR
- Epidemiology
- Clinical Development
- Medical Affairs
- Translational/Safety
- Commercial
- Market Access
- Academic Association
- Psych or CNS Department
- Other

**Purpose**: Customer department/function classification

### K: Customer Segment
**Type**: Text
**Required**: No
**Purpose**: Duplicate of column I for legacy compatibility
**Note**: Automatically populated with same value as Segment (column I)

### L: Company
**Type**: Text
**Required**: No
**Purpose**: Organization name
**Example**: "Bristol Myers Squibb", "Northwestern University"
**Note**: Usually extracted from first attendee name

### M: Persona
**Type**: Dropdown
**Required**: No
**Options**:
- Coder (writes SQL/code)
- Non-Coder (uses UI only)
- Rusty Coder (can code but prefers UI)

**Purpose**: Technical skill level of user

### N: Email
**Type**: Email
**Required**: No
**Validation**: Valid email format
**Purpose**: Contact email for follow-up

### O: Internal
**Type**: Y/N
**Required**: No (default: N)
**Purpose**: Flag internal vs external feedback
**Options**:
- Y (from Holmusk team member)
- N (from external customer/user)

### P: Contact
**Type**: Text
**Required**: No
**Purpose**: Primary contact person name
**Example**: "Dr. Sarah Chen"
**Note**: Usually extracted from first attendee

### Q: Created Date
**Type**: Date
**Required**: Yes (auto-populated)
**Format**: YYYY-MM-DD
**Purpose**: When feedback item was first created
**Example**: "2025-11-20"

### R: Updated Date
**Type**: Date
**Required**: Yes (auto-updated)
**Format**: YYYY-MM-DD
**Purpose**: When feedback item was last modified
**Example**: "2025-11-20"

### S: Attendees
**Type**: Text (comma-separated list)
**Required**: No
**Purpose**: List of meeting attendees
**Example**: "Dr. Sarah Chen (Pharma R&D), Kevin Holland, John Smith"
**Format**: Comma-separated names with optional affiliations in parentheses

### T: Tags
**Type**: Text (comma-separated list)
**Required**: No
**Purpose**: Categorical tags for filtering and grouping
**Example**: "cohort-management, workflow, analytics"
**Format**: Comma-separated, hyphenated tags (no spaces within tags)

### U: Meeting Type
**Type**: Dropdown
**Required**: No
**Options**:
- Pipeline Call
- User Interview
- Product Strategy
- Client Feedback
- Standup
- Other

**Purpose**: Type of meeting where feedback was collected

### V: Meeting Date
**Type**: Date
**Required**: No
**Format**: YYYY-MM-DD
**Purpose**: Specific date of meeting
**Example**: "2025-11-15"
**Note**: Different from Created Date (column Q) which is when item was added to database

### W: Source
**Type**: Text
**Required**: No
**Purpose**: Descriptive source of feedback
**Example**: "Granola", "Email", "Slack", "Manual Entry"

### X: Source URL
**Type**: URL
**Required**: No
**Purpose**: Link to original feedback source
**Example**: "https://granola.so/note/abc123"
**Validation**: Valid URL format

### Y: Insights
**Type**: Long Text
**Required**: No
**Purpose**: Key findings and use case description
**Example**: "User trying to perform quarterly reporting on recurring cohorts. Current workflow requires manual cohort recreation each time."

### Z: Quote
**Type**: Long Text
**Required**: No
**Purpose**: Verbatim user quote (most impactful statement)
**Example**: "We spend 2 hours recreating the same cohort every month - it's our biggest time sink"
**Note**: Should be exact user words, not paraphrased

## Data Validation Rules

### Dropdown Fields
All dropdown fields have validation configured in Google Sheets to prevent typos and ensure data consistency.

### Date Fields
- Must be in YYYY-MM-DD format
- Google Sheets validates as proper date type

### Email Fields
- Must be valid email format (name@domain.com)
- Google Sheets validates email pattern

### Text Length
- Title (Column B): Truncated to 100 characters if longer
- Other text fields: No hard limit but keep reasonable

## Usage Notes

### Auto-Population
The skill automatically populates these fields:
- ID (Column A) - generated if not provided
- Created Date (Column Q) - current date
- Updated Date (Column R) - current date
- Status (Column E) - defaults to "New"
- Internal (Column O) - defaults to "N"

### Manual Entry Required
These fields are left blank for manual entry:
- Persona (Column M) - technical skill level
- Email (Column N) - contact email

### AI Enrichment (Optional)
These fields are populated by enrichment script if enabled:
- Segment (Column I)
- Department (Column J)
- Tags (Column T) - enhanced with additional tags

### Deduplication
- Performed on Title (Column B)
- Uses 85% similarity threshold
- Prevents duplicate entries for same feedback

## Example Row

```
A: FB-20251120143022-AB123
B: Export cohort definitions for reuse
C: Users want to save cohort logic and reuse it across studies. Currently spending 2+ hours recreating cohorts monthly.
D: Granola
E: New
F: P1
G: NeuroBlu Analytics
H: Feature Request
I: Pharma
J: Research/RWD
K: Pharma
L: Bristol Myers Squibb
M: (blank - manual entry)
N: (blank - manual entry)
O: N
P: Dr. Sarah Chen
Q: 2025-11-20
R: 2025-11-20
S: Dr. Sarah Chen (Pharma R&D), Kevin Holland
T: cohort-management, workflow, analytics
U: Pipeline Call
V: 2025-11-15
W: Granola
X: https://granola.so/note/abc123
Y: User performing quarterly reporting on recurring cohorts
Z: "We spend 2 hours recreating the same cohort every month"
```

## Schema Version

**Version**: 1.0
**Last Updated**: 2025-11-20
**Database**: NeuroBlu Feedback Database (All Feedback worksheet)
