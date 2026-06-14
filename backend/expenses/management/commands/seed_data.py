from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from expenses.models import Group, GroupMembership
from datetime import datetime

class Command(BaseCommand):
    help = 'Seed initial users, groups, and memberships'

    def handle(self, *args, **options):
        # 1. Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'password123')
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' created with password 'password123'"))

        # 2. Seed Demo Users
        demo_users = [
            {'username': 'demo', 'email': 'demo@example.com', 'first_name': 'Demo'},
            {'username': 'user', 'email': 'user@example.com', 'first_name': 'User'},
        ]

        users = {}
        for u in demo_users:
            user, created = User.objects.get_or_create(username=u['username'], defaults={
                'email': u['email'],
                'first_name': u['first_name']
            })
            user.set_password('password123')
            user.save()
            self.stdout.write(f"User {u['username']} password set/reset to 'password123'")
            users[u['username']] = user

        # 3. Create default group
        group, created = Group.objects.get_or_create(name='LedgerLens Group')
        if created:
            self.stdout.write(self.style.SUCCESS(f"Group '{group.name}' created"))

        # 4. Create Memberships
        for username in users:
            membership, m_created = GroupMembership.objects.get_or_create(
                group=group,
                user=users[username],
                defaults={
                    'joined_date': datetime.now().date(),
                    'left_date': None
                }
            )
            if m_created:
                self.stdout.write(f"Membership configured for {username}")

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
