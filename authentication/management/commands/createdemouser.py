from django.core.management.base import BaseCommand

import authentication.models


class Command(BaseCommand):
    help = 'Creates default demo user'

    def handle(self, *args, **options):
        try:
            obj = authentication.models.User.objects.get(username = 'demo@demo.com')
        except authentication.models.User.DoesNotExist:
                demo_user = authentication.models.User()
                demo_user.username = 'demo@demo.com'
                demo_user.set_password('demo')
                demo_user.save()
                self.stdout.write('Demo user created')
