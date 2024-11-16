from django.core.management.base import BaseCommand

from organization.models import Employee


class Command(BaseCommand):
    help = 'Create a default admin user if not exists'

    def handle(self, *args, **kwargs):
        if not Employee.objects.filter(username='admin').exists():
            Employee.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Successfully created new super user'))
        else:
            self.stdout.write(self.style.WARNING('Super user already exists'))
