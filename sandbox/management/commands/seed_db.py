from django.core.management.base import BaseCommand
import json
import os
from django.conf import settings
from sandbox.models import Employee, Subscriber

class Command(BaseCommand):
    help = 'Seed the database with test employees and subscribers from JSON'

    def handle(self, *args, **kwargs):
        Employee.objects.all().delete()
        Subscriber.objects.all().delete()
        
        seed_file_path = os.path.join(settings.BASE_DIR, 'seed_data.json')
        
        with open(seed_file_path, 'r') as f:
            data = json.load(f)
            
        for emp in data.get('employees', []):
            Employee.objects.create(**emp)
            
        for sub in data.get('subscribers', []):
            Subscriber.objects.create(**sub)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded database with {len(data.get("employees", []))} employees and {len(data.get("subscribers", []))} subscribers.'))
