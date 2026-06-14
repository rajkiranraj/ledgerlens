from django.test import TestCase
from django.contrib.auth.models import User
from expenses.models import Group, GroupMembership, Expense, ExpenseSplit, Settlement, ImportReport
from expenses.utils import parse_csv_export, calculate_balances, minimize_debts
from datetime import datetime
from decimal import Decimal
import os

class SharedExpensesTestCase(TestCase):
    def setUp(self):
        # 1. Create default test group
        self.group = Group.objects.create(name="Test LedgerLens Group")

        # 2. Create standard profiles
        names = ['demo', 'admin', 'user']
        self.users = {}
        for name in names:
            user = User.objects.create_user(username=name, password='password123')
            self.users[name] = user

        # 3. Create memberships with date limits
        memberships_data = [
            {'user': 'demo', 'joined': '2026-02-01', 'left': None},
            {'user': 'admin', 'joined': '2026-02-01', 'left': None},
            {'user': 'user', 'joined': '2026-02-01', 'left': '2026-03-31'},
        ]

        for m in memberships_data:
            GroupMembership.objects.create(
                group=self.group,
                user=self.users[m['user']],
                joined_date=datetime.strptime(m['joined'], '%Y-%m-%d').date(),
                left_date=datetime.strptime(m['left'], '%Y-%m-%d').date() if m['left'] else None
            )

        # 4. Load CSV path
        self.csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'expenses_export.csv')

    def test_csv_parser_and_engine(self):
        # Ensure CSV exists
        self.assertTrue(os.path.exists(self.csv_path), "CSV export file must exist at project root")

        # Read CSV file
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            file_content = f.read()

        # Parse CSV
        parsed_rows = parse_csv_export(file_content, self.group.id)
        self.assertTrue(len(parsed_rows) > 0, "Parser should parse some rows")

        # Test writing split entries into database
        from expenses.views import save_expense_splits
        from expenses.utils import clean_name

        for r in parsed_rows:
            # Exclude zero-amount rows
            if float(r['amount']) == 0:
                continue

            date_val = datetime.strptime(r['date'], '%Y-%m-%d').date()
            payer_name = r['paid_by']
            if not payer_name:
                payer_name = 'demo'

            payer = self.users[payer_name] if payer_name in self.users else self.users['demo']
            amount = Decimal(str(r['amount']))
            currency = r['currency']
            exchange_rate = Decimal(str(r['exchange_rate']))
            amount_in_inr = amount * exchange_rate
            split_type = r['split_type']
            split_with = [clean_name(name) for name in r['split_with'].split(';') if name.strip()]
            split_details = r['split_details']

            if split_type == 'settlement':
                payee = self.users['admin']
                Settlement.objects.create(
                    group=self.group,
                    payer=payer,
                    payee=payee,
                    amount=amount_in_inr,
                    date=date_val,
                    notes=r['notes'] or 'Test Settlement'
                )
            else:
                expense = Expense.objects.create(
                    group=self.group,
                    description=r['description'],
                    paid_by=payer,
                    created_by=payer,
                    amount=amount,
                    currency=currency,
                    exchange_rate=exchange_rate,
                    amount_in_inr=amount_in_inr,
                    split_type=split_type,
                    date=date_val,
                    notes=r['notes']
                )
                save_expense_splits(expense, split_with, split_details)

        # Run balances calculations
        results = calculate_balances(self.group.id)
        self.assertIn('balances', results)

        # Run debt minimization
        minimized = minimize_debts(results['balances'])
        print("Minimized test transactions count:", len(minimized))
