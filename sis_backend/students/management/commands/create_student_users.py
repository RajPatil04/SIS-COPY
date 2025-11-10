from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Student


class Command(BaseCommand):
    help = 'Create Django User accounts for students (username=enrollment_number).'

    def add_arguments(self, parser):
        parser.add_argument('--password', help='Default password to set for created users', default='student123')
        parser.add_argument('--force', action='store_true', help='Force reset password for existing users')

    def handle(self, *args, **options):
        default_password = options['password']
        force = options['force']
        students = Student.objects.all()
        created = 0
        updated = 0
        for s in students:
            username = s.enrollment_number
            email = s.email or ''
            if not username:
                self.stdout.write(self.style.WARNING(f'Skipping student with id={s.pk} (no enrollment_number)'))
                continue
            user, was_created = User.objects.get_or_create(username=username, defaults={'email': email})
            if was_created:
                user.set_password(default_password)
                user.save()
                created += 1
                self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))
            else:
                if force:
                    user.set_password(default_password)
                    user.email = email
                    user.save()
                    updated += 1
                    self.stdout.write(self.style.SUCCESS(f'Updated (password reset): {username}'))

        self.stdout.write(self.style.SUCCESS(f'Done. Created: {created}, Updated: {updated}'))
