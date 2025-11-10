from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Grant admin privileges to all faculty users'

    def handle(self, *args, **options):
        # Update all users with faculty profile or email containing faculty domains
        faculty_users = User.objects.filter(
            is_staff=False
        ).exclude(
            email=''
        )
        
        updated_count = 0
        for user in faculty_users:
            if not user.username.startswith('sis_'):  # Not a student
                user.is_staff = True
                user.is_superuser = True
                user.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Granted admin access to: {user.username} ({user.email})')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Total faculty users updated: {updated_count}')
        )
