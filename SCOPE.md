# LedgerLens AI — Anomaly Detection Scope

## Overview

This document defines the complete anomaly detection scope for LedgerLens AI, including all supported anomaly types, detection logic, severity levels, and default actions. The anomaly detection system is designed to ensure high data quality and provide a comprehensive audit trail.

---

## Anomaly Log Specification

| # | Anomaly Type | Example | Detection Logic | Severity | Action Taken | Rationale |
|---|--------------|---------|-----------------|----------|--------------|-----------|
| 1 | **Duplicate Transaction** | Row 5 and Row 12 both have same date, payer, amount, and description | Checks for rows with matching date, payer, amount, and similar description within the same import | Warning | Flagged (user decides) | Duplicates may be intentional (recurring expenses) or accidental; user should review |
| 2 | **Missing Payer** | Row 7 has empty "Paid By" column | Validates that payer field is not empty | Critical | Rejected | Payer is a required field for expense tracking |
| 3 | **Missing Participant** | Split list contains empty entries | Validates that split participants are not empty strings | Info | Auto-corrected (removed) | Minor formatting issue, safe to auto-remove |
| 4 | **Invalid Date** | Date formatted as "02/30/2024" (invalid date) or unparseable string | Attempts to parse date with multiple format strategies; if all fail, it's invalid | Critical | Rejected | Invalid dates break chronological ordering and analytics |
| 5 | **Future Date** | Date is "2026-12-31" (after current date) | Compares parsed date to today's date | Warning | Flagged (user decides) | Future dates may be intentional (planned expenses) |
| 6 | **Negative Amount** | Amount is "-150.00" | Checks if amount is less than zero | Warning | Flagged (user decides) | Negative amounts may be refunds or data entry errors |
| 7 | **Zero Amount** | Amount is "0.00" | Checks if amount equals zero | Warning | Rejected | Zero-amount expenses provide no value |
| 8 | **Empty Description** | Row 10 has no expense description | Validates that description is not empty | Critical | Rejected | Description is required for audit trail and categorization |
| 9 | **Unknown User** | Payer is "Alex" but no user with that username exists | Checks if user exists in the system; if not, auto-creates | Info | Auto-corrected (user created) | Auto-creation maintains import flow; user can manage later |
| 10 | **Currency Issue** | Currency is "XYZ" (invalid code) or empty | Validates currency codes against allowed list (USD, INR, EUR); defaults to INR if empty | Info | Auto-corrected | Currency defaults ensure consistent data |
| 11 | **Inconsistent Splits** | Percentage splits sum to 95% instead of 100% | Validates that split details sum correctly for percentage/share/unequal splits | Warning | Flagged (user decides) | Inconsistent splits may be intentional (rounding) or errors |
| 12 | **Malformed Row** | Row has fewer columns than expected or unparseable data | Checks column count and basic data structure | Critical | Rejected | Malformed data cannot be reliably processed |
| 13 | **Extra Columns** | Row has more columns than expected | Validates column count against header | Info | Auto-corrected (ignored) | Extra columns don't prevent processing |
| 14 | **Excessive Decimal Precision** | Amount is "123.4567" (4 decimal places) | Rounds to 2 decimal places | Info | Auto-corrected | Standard currency precision is 2 decimals |
| 15 | **Name Variant** | Payer is "rohan" (lowercase) or "Rohan " (with space) | Normalizes names using a predefined mapping | Info | Auto-corrected | Ensures consistent user identification |
| 16 | **Inactive Member in Split** | Split includes user who left the group before expense date | Validates member active period against expense date | Warning | Auto-corrected (removed) | Inactive members shouldn't be included in splits |

---

## Severity Levels

| Level | Description | Impact |
|-------|-------------|--------|
| **Critical** | Data integrity at risk; row cannot be processed reliably | Row is rejected |
| **Warning** | Potential issue that requires review | Row is flagged for user decision |
| **Info** | Minor formatting issue; no data integrity risk | Auto-corrected without user intervention |

---

## Action Types

| Action | Description |
|--------|-------------|
| **Rejected** | Row is excluded from import |
| **Flagged** | Row is highlighted for user review (user decides import) |
| **Auto-corrected** | Issue is fixed automatically, row is imported |
| **Imported** | Row is imported as-is (no issues) |

---

## Data Quality Guarantees

1. **100% Audit Trail**: All anomalies are logged in the database with original/resolved values
2. **No Silent Failures**: Every anomaly is reported to the user
3. **Deterministic Behavior**: Same input always produces same anomaly detection results
4. **Configurable**: Severity levels and actions are configurable via system settings
5. **Backward Compatible**: All valid rows from previous versions continue to import successfully

---

## Performance Requirements

- Anomaly detection for 10,000 rows < 2 seconds
- Memory usage < 500MB for 10,000-row import
- No significant impact on import performance for anomaly-free files
