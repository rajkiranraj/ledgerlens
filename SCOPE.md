# LedgerLens: Project Scope & Requirements Fulfillment

100% of assignment requirements are met—plus some extras I added to make it production-ready!

---

## Anomaly Detection: Full Implementation

Every required anomaly type is detected, with severity levels and clear action plans:

| Anomaly Type | Severity | Default Action | Notes |
|---|---|---|---|
| Missing Required Field | Error | Reject | Includes date, amount, description |
| Empty Row | Info | Skip | Rows with no data |
| Duplicate Transaction | Warning | Ask User | Same amount, date, and description |
| Invalid Date | Error | Reject | Can't parse date |
| Future Date | Warning | Ask User | Date after today |
| Invalid Currency Value | Error | Reject | Not a valid number |
| Negative Amount | Warning | Reject (configurable) | Negative expense |
| Missing Category | Info | Auto-Correct | Assigns "Uncategorized" |
| Invalid Category | Warning | Auto-Correct | Assigns "Uncategorized" |
| Malformed Record | Critical | Reject | Can't parse row at all |
| Extra Unexpected Columns | Info | Ignore | More columns than expected |
| Truncated Record | Warning | Ask User | Row ends abruptly |

---

## Database Schema: New Models I Added

### 1. `Category`
Stores allowed expense categories for validation.
- `name`: Unique category name (CharField)
- `description`: Optional description (TextField)

### 2. `Import`
Tracks every CSV import session end-to-end.
- `group`: ForeignKey to Group
- `file_name`: Original uploaded file name
- `file_size`: File size in bytes
- `total_rows`: Total rows processed
- `imported_rows`: Rows successfully imported
- `rejected_rows`: Rows rejected
- `corrected_rows`: Rows auto-corrected
- `created_by`: ForeignKey to User
- `started_at`, `completed_at`: Audit timestamps
- `status`: pending/importing/completed/failed

### 3. `Anomaly`
Detailed record of every anomaly found.
- `import`: ForeignKey to Import
- `csv_row_number`: Row number in original CSV
- `anomaly_type`: What kind of anomaly it was
- `severity`: Info/Warning/Error/Critical
- `description`: Human-readable explanation
- `action_taken`: Imported/Corrected/Flagged/Rejected
- `original_data`: JSON of original row
- `corrected_data`: JSON of fixed row (if applicable)
- `created_at`: Timestamp

### 4. `ImportReport`
Full summary of the import, downloadable as JSON.
- `import`: OneToOneField to Import
- `imported_at`: Completion timestamp
- `summary_data`: JSON with key metrics
- `log_data`: JSON with step-by-step logs
- `created_at`: Timestamp

---

## Assignment Requirements: 100% Complete!

| Requirement | Status | Notes |
|---|---|---|
| CSV Upload | ✅ | Drag & drop + file input |
| CSV Parsing | ✅ | Robust, handles malformed files |
| Database Persistence | ✅ | All imports, anomalies, expenses saved |
| Data Validation | ✅ | 12+ anomaly types covered |
| Anomaly Detection | ✅ | Full severity levels and user prompts |
| Import Reporting | ✅ | Viewable + downloadable JSON reports |
| Dashboard Analytics | ✅ | Overview cards + import history |
| Export Functionality | ✅ | Import report downloads |
| Deployment Readiness | ✅ | Production build tested, SQLite configured |
| Documentation | ✅ | 4 full docs (README, SCOPE, DECISIONS, AI_USAGE) |

---

## Extras I Added (10x Intern Bonus!)
- Full Django admin integration for debugging
- Analytics endpoint with spending breakdowns
- Import history table in the dashboard
- Zero-config local setup (switched to SQLite)
