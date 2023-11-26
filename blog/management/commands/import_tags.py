import csv
import os
from django.core.management.base import BaseCommand
from blog.models import Tag

class Command(BaseCommand):
    help = 'Import tags from a CSV file in the same folder as manage.py'

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_file_path = os.path.join(base_dir, 'commands', 'tags.csv')  # Update the CSV file path

        try:
            with open(csv_file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row

                # Create tags
                tags = [Tag(name=row[0]) for row in reader]

                # Save tags to the database
                Tag.objects.bulk_create(tags)

                self.stdout.write(self.style.SUCCESS('Tags added successfully'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('CSV file not found'))
        except csv.Error:
            self.stdout.write(self.style.ERROR('Error reading CSV file'))
