from django.core.management.base import BaseCommand
from shortener.models import URL
import csv

class Command(BaseCommand):
    help = 'Export data from YourModel to a CSV file'

    def handle(self, *args, **options):
        data = URL.objects.all()

        csv_file_path = 'short_urls.csv'

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write header
            writer.writerow(['short_url'])

            # Write data
            for item in data:
                writer.writerow([item.short_url])

        self.stdout.write(self.style.SUCCESS(f'Data exported to {csv_file_path}'))
