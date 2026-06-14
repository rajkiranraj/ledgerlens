import csv
import re
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, date
from django.contrib.auth.models import User
from expenses.models import Group, GroupMembership, Expense, ExpenseSplit, Settlement, Category

# Standard members name mapping
NAME_MAPPING = {
    'aisha': 'Aisha',
    'rohan': 'Rohan',
    'rohan ': 'Rohan',
    'priya': 'Priya',
    'priya s': 'Priya',
    'meera': 'Meera',
    'sam': 'Sam',
    'dev': 'Dev',
    'kabir': 'Kabir',
    "dev's friend kabir": 'Kabir'
}

def clean_name(name):
    if not name:
        return ''
    normalized = name.strip().lower()
    return NAME_MAPPING.get(normalized, name.strip())

def parse_decimal(val):
    if not val:
        return Decimal('0.0000')
    cleaned = re.sub(r'[^\d\.\-]', '', str(val))
    try:
        return Decimal(cleaned)
    except Exception:
        return Decimal('0.0000')

def parse_date(date_str, prev_date_str=None, next_date_str=None):
    date_str = date_str.strip()
    
    match_month_day = re.match(r'^([a-zA-Z]+)-(\d+)$', date_str)
    if match_month_day:
        month_str, day_str = match_month_day.groups()
        try:
            dt = datetime.strptime(f"{day_str}-{month_str}-2026", "%d-%b-%Y")
            return dt.date(), "Custom month-day format parsed (assumed Year 2026)"
        except Exception:
            pass

    for fmt in ["%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.date(), None
        except ValueError:
            continue

    return None, "Unparseable date format"

def is_future_date(date_obj):
    return date_obj > date.today()

def validate_anomalies(row, csv_row_number, group_id, parsed_rows):
    anomalies = []
    raw_date, raw_description, raw_paid_by, raw_amount, raw_currency, raw_split_type, raw_split_with, raw_split_details, raw_notes = row
    date_obj, date_warning = parse_date(raw_date)
    resolved_date = date_obj if date_obj else datetime(2026, 2, 1).date()

    if date_warning:
        anomalies.append({
            'type': 'date_format_issue',
            'severity': 'warning',
            'description': date_warning,
            'field': 'date',
            'raw_val': raw_date,
            'resolved_val': str(resolved_date),
            'action': 'corrected'
        })
    elif is_future_date(resolved_date):
        anomalies.append({
            'type': 'future_date',
            'severity': 'critical',
            'description': 'Date is in the future',
            'field': 'date',
            'raw_val': raw_date,
            'resolved_val': str(resolved_date),
            'action': 'flagged'
        })

    cleaned_amount = raw_amount.replace('"', '').replace(',', '')
    amount_decimal = parse_decimal(cleaned_amount)
    if ',' in raw_amount or '"' in raw_amount:
        anomalies.append({
            'type': 'amount_formatting',
            'severity': 'info',
            'description': "Amount contains formatting characters (commas or quotes)",
            'field': 'amount',
            'raw_val': raw_amount,
            'resolved_val': float(amount_decimal),
            'action': 'corrected'
        })

    if '.' in cleaned_amount and len(cleaned_amount.split('.')[-1]) > 2:
        amount_decimal = amount_decimal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        anomalies.append({
            'type': 'excessive_decimal_precision',
            'severity': 'info',
            'description': 'Amount has more than 2 decimal places',
            'field': 'amount',
            'raw_val': raw_amount,
            'resolved_val': float(amount_decimal),
            'action': 'corrected'
        })

    if amount_decimal < 0:
        anomalies.append({
            'type': 'negative_amount',
            'severity': 'warning',
            'description': 'Negative amount detected',
            'field': 'amount',
            'raw_val': raw_amount,
            'resolved_val': float(amount_decimal),
            'action': 'flagged'
        })
    elif amount_decimal == 0:
        anomalies.append({
            'type': 'zero_amount',
            'severity': 'warning',
            'description': 'Expense amount is zero',
            'field': 'amount',
            'raw_val': raw_amount,
            'resolved_val': 0.0,
            'action': 'rejected'
        })

    resolved_currency = raw_currency.strip().upper() or 'INR'
    if not raw_currency.strip():
        anomalies.append({
            'type': 'missing_currency',
            'severity': 'info',
            'description': 'Currency field is blank',
            'field': 'currency',
            'raw_val': raw_currency,
            'resolved_val': 'INR',
            'action': 'corrected'
        })

    if resolved_currency not in ['INR', 'USD', 'EUR']:
        anomalies.append({
            'type': 'invalid_currency',
            'severity': 'warning',
            'description': 'Invalid currency code',
            'field': 'currency',
            'raw_val': raw_currency,
            'resolved_val': 'INR',
            'action': 'corrected'
        })

    exchange_rate = Decimal('1.0000')
    if resolved_currency == 'USD':
        exchange_rate = Decimal('83.0000')

    resolved_paid_by = clean_name(raw_paid_by)
    if not raw_paid_by.strip():
        anomalies.append({
            'type': 'missing_required_field',
            'severity': 'critical',
            'description': 'Payer field is required and missing',
            'field': 'paid_by',
            'raw_val': '',
            'resolved_val': '',
            'action': 'rejected'
        })
    elif resolved_paid_by != raw_paid_by:
        anomalies.append({
            'type': 'name_variant',
            'severity': 'info',
            'description': f"Payer name variant detected: mapped '{raw_paid_by}' to '{resolved_paid_by}'",
            'field': 'paid_by',
            'raw_val': raw_paid_by,
            'resolved_val': resolved_paid_by,
            'action': 'corrected'
        })

    split_members_raw = [m.strip() for m in raw_split_with.split(';') if m.strip()]
    resolved_split_with = []
    for sm in split_members_raw:
        cleaned_sm = clean_name(sm)
        if cleaned_sm:
            resolved_split_with.append(cleaned_sm)
    resolved_split_with = list(dict.fromkeys(resolved_split_with))

    if ';;' in raw_split_with or raw_split_with.endswith(';'):
        anomalies.append({
            'type': 'split_list_formatting',
            'severity': 'info',
            'description': 'Split list contains empty separators',
            'field': 'split_with',
            'raw_val': raw_split_with,
            'resolved_val': ';'.join(resolved_split_with),
            'action': 'corrected'
        })

    memberships = GroupMembership.objects.filter(group_id=group_id)
    member_dates = {m.user.username: {'joined': m.joined_date, 'left': m.left_date} for m in memberships}
    inactive_members = []
    for member in resolved_split_with:
        if member in member_dates:
            joined = member_dates[member]['joined']
            left = member_dates[member]['left']
            if resolved_date < joined or (left and resolved_date > left):
                inactive_members.append(member)
    if inactive_members:
        anomalies.append({
            'type': 'inactive_member_in_split',
            'severity': 'warning',
            'description': f"Members {', '.join(inactive_members)} were inactive on {resolved_date}",
            'field': 'split_with',
            'raw_val': raw_split_with,
            'resolved_val': ';'.join([m for m in resolved_split_with if m not in inactive_members]),
            'action': 'corrected'
        })

    resolved_split_type = raw_split_type.strip().lower() or 'equal'
    if not raw_split_type.strip():
        anomalies.append({
            'type': 'missing_split_type',
            'severity': 'info',
            'description': "Split type was blank, defaulted to 'equal'",
            'field': 'split_type',
            'raw_val': '',
            'resolved_val': 'equal',
            'action': 'corrected'
        })

    if resolved_split_type == 'equal' and raw_split_details.strip():
        anomalies.append({
            'type': 'split_type_mismatch',
            'severity': 'warning',
            'description': 'Split type is equal but split details provided',
            'field': 'split_type',
            'raw_val': raw_split_details,
            'resolved_val': '',
            'action': 'corrected'
        })

    if resolved_split_type == 'percentage' and raw_split_details.strip():
        pcts = re.findall(r'([a-zA-Z\s]+)\s*(\d+)%', raw_split_details)
        if pcts:
            total_pct = sum(int(p[1]) for p in pcts)
            if total_pct != 100:
                anomalies.append({
                    'type': 'percentage_split_sum_error',
                    'severity': 'warning',
                    'description': f"Percentages sum to {total_pct}% instead of 100%",
                    'field': 'split_details',
                    'raw_val': raw_split_details,
                    'resolved_val': '',
                    'action': 'flagged'
                })

    is_duplicate = False
    for prev_row in parsed_rows:
        if (prev_row['date'] == str(resolved_date) and 
            prev_row['paid_by'] == resolved_paid_by and 
            abs(prev_row['amount'] - float(amount_decimal)) < 1.0 and
            (prev_row['description'].lower() in raw_description.lower() or raw_description.lower() in prev_row['description'].lower())):
            is_duplicate = True
            anomalies.append({
                'type': 'duplicate_transaction',
                'severity': 'warning',
                'description': f"Potential duplicate of row {prev_row['csv_row_number']}",
                'field': 'description',
                'raw_val': raw_description,
                'resolved_val': raw_description,
                'action': 'flagged'
            })
            break

    if not raw_description.strip():
        anomalies.append({
            'type': 'missing_required_field',
            'severity': 'critical',
            'description': 'Description is required and missing',
            'field': 'description',
            'raw_val': '',
            'resolved_val': '',
            'action': 'rejected'
        })

    return anomalies, {
        'csv_row_number': csv_row_number,
        'date': str(resolved_date),
        'description': raw_description.strip(),
        'paid_by': resolved_paid_by,
        'amount': float(amount_decimal),
        'currency': resolved_currency,
        'exchange_rate': float(exchange_rate),
        'amount_in_inr': float(amount_decimal * exchange_rate),
        'split_type': resolved_split_type,
        'split_with': ';'.join(resolved_split_with),
        'split_details': raw_split_details.strip(),
        'notes': raw_notes.strip(),
        'anomalies': anomalies,
        'exclude': False
    }

def parse_csv_export(file_content, group_id):
    decoded_file = file_content.splitlines()
    reader = csv.reader(decoded_file)
    
    header = next(reader, None)
    if not header:
        return []
    
    rows = list(reader)
    parsed_rows = []
    for idx, row in enumerate(rows):
        csv_row_number = idx + 2
        if not row or len(row) < 4:
            continue
        
        padded_row = row + [''] * max(0, 9 - len(row))
        if len(row) > 9:
            padded_row = padded_row[:9]
            anomalies = [{
                'type': 'extra_columns',
                'severity': 'info',
                'description': 'Row has extra unexpected columns',
                'field': None,
                'raw_val': str(row[9:]),
                'resolved_val': '',
                'action': 'corrected'
            }]
        else:
            anomalies = []
        
        row_anomalies, parsed_row = validate_anomalies(padded_row, csv_row_number, group_id, parsed_rows)
        parsed_row['anomalies'].extend(anomalies)
        parsed_row['anomalies'].extend(row_anomalies)
        if any(a['severity'] == 'critical' for a in parsed_row['anomalies']):
            parsed_row['exclude'] = True
        
        parsed_rows.append(parsed_row)
    
    return parsed_rows

def calculate_balances(group_id):
    group = Group.objects.get(id=group_id)
    memberships = GroupMembership.objects.filter(group=group)
    users = [m.user for m in memberships]
    
    balances = {u.username: Decimal('0.0000') for u in users}
    ledgers = {u.username: [] for u in users}

    expenses = Expense.objects.filter(group=group).order_by('date', 'id')
    settlements = Settlement.objects.filter(group=group).order_by('date', 'id')

    for exp in expenses:
        payer_username = exp.paid_by.username
        splits = exp.splits.all()
        
        for sp in splits:
            debtor_username = sp.user.username
            if debtor_username in balances:
                balances[debtor_username] -= sp.share_amount_in_inr
                ledgers[debtor_username].append({
                    'type': 'expense_owed',
                    'date': str(exp.date),
                    'description': exp.description,
                    'payer': payer_username,
                    'total_amount': float(exp.amount_in_inr),
                    'currency': exp.currency,
                    'split_value': sp.split_value,
                    'amount': -float(sp.share_amount_in_inr)
                })

        if payer_username in balances:
            balances[payer_username] += exp.amount_in_inr
            ledgers[payer_username].append({
                'type': 'expense_paid',
                'date': str(exp.date),
                'description': exp.description,
                'payer': payer_username,
                'total_amount': float(exp.amount_in_inr),
                'currency': exp.currency,
                'split_value': 'Payer Credit',
                'amount': float(exp.amount_in_inr)
            })

    for setl in settlements:
        payer = setl.payer.username
        payee = setl.payee.username
        
        if payer in balances:
            balances[payer] += setl.amount
            ledgers[payer].append({
                'type': 'settlement_paid',
                'date': str(setl.date),
                'description': f"Paid settlement to {payee}",
                'payer': payer,
                'total_amount': float(setl.amount),
                'currency': 'INR',
                'split_value': 'Settlement',
                'amount': float(setl.amount)
            })
            
        if payee in balances:
            balances[payee] -= setl.amount
            ledgers[payee].append({
                'type': 'settlement_received',
                'date': str(setl.date),
                'description': f"Received settlement from {payer}",
                'payer': payer,
                'total_amount': float(setl.amount),
                'currency': 'INR',
                'split_value': 'Settlement',
                'amount': -float(setl.amount)
            })

    formatted_balances = {uname: float(val.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) for uname, val in balances.items()}
    
    for uname in ledgers:
        ledgers[uname].sort(key=lambda x: x['date'])

    return {
        'balances': formatted_balances,
        'ledgers': ledgers
    }

def minimize_debts(balances):
    active_balances = []
    for uname, bal in balances.items():
        if abs(bal) >= 0.05:
            active_balances.append({'name': uname, 'balance': bal})

    debtors = sorted([x for x in active_balances if x['balance'] < 0], key=lambda x: x['balance'])
    creditors = sorted([x for x in active_balances if x['balance'] > 0], key=lambda x: x['balance'], reverse=True)

    transactions = []

    d_idx = 0
    c_idx = 0

    while d_idx < len(debtors) and c_idx < len(creditors):
        debtor = debtors[d_idx]
        creditor = creditors[c_idx]

        debt_amount = -debtor['balance']
        credit_amount = creditor['balance']

        settle_amount = min(debt_amount, credit_amount)
        settle_amount_rounded = round(settle_amount, 2)
        
        if settle_amount_rounded > 0:
            transactions.append({
                'from_user': debtor['name'],
                'to_user': creditor['name'],
                'amount': settle_amount_rounded
            })

        debtor['balance'] += settle_amount
        creditor['balance'] -= settle_amount

        if abs(debtor['balance']) < 0.01:
            d_idx += 1
        if abs(creditor['balance']) < 0.01:
            c_idx += 1

    return transactions
