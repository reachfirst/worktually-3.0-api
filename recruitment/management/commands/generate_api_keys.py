from django.core.management.base import BaseCommand
from recruitment.models import APIKey

class Command(BaseCommand):
    help = 'Generates API keys for all users'

    def handle(self, *args, **kwargs):
        APIKey.objects.create()  # Create a new API key instance
        self.stdout.write(self.style.SUCCESS('API keys generated successfully'))
