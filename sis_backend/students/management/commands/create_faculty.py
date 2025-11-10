from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from students.models import FacultyProfile


class Command(BaseCommand):
    help = 'Create a faculty user with a FacultyProfile and assign to Teacher group. Usage: create_faculty --username bhushan --email bhushan@example.com --password secret --subjects "Data Structures,DAA" --classes "SY-COMP-A,SY-COMP-B"'

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True)
        parser.add_argument('--email', required=True)
        parser.add_argument('--password', required=True)
        parser.add_argument('--first_name', default='')
        parser.add_argument('--last_name', default='')
        parser.add_argument('--subjects', default='')
        parser.add_argument('--classes', default='')

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        email = options['email']
        password = options['password']
        first_name = options['first_name']
        last_name = options['last_name']
        subjects = options['subjects']
        classes = options['classes']

        user, created = User.objects.get_or_create(username=username, defaults={'email': email, 'first_name': first_name, 'last_name': last_name})
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created faculty user: {username}'))
        else:
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Updated faculty user: {username}'))

        # Ensure Teacher group exists and add user to it
        teacher_group, _ = Group.objects.get_or_create(name='Teacher')
        user.groups.add(teacher_group)
        user.save()

        # Create or update FacultyProfile
        profile, prof_created = FacultyProfile.objects.get_or_create(user=user)
        profile.subjects = subjects
        profile.classes = classes
        profile.save()

        self.stdout.write(self.style.SUCCESS(f'FacultyProfile set for {username}: subjects={subjects} classes={classes}'))
