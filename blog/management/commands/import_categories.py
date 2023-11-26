import csv
import os
from django.core.management.base import BaseCommand
from blog.models import Categories, Subcategories

class Command(BaseCommand):
    help = 'Import subcategories for the "History" category from a CSV file in the same folder as manage.py'

    def handle(self, *args, **options):
        # Get or create the "History" category
        history_category, created = Categories.objects.get_or_create(name='History')

        # Get the path to the directory containing the manage.py file
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Path to your CSV file (assuming it's in the same folder as manage.py)
        csv_file = os.path.join(base_dir,'commands','history_subcategories.csv')

        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Each row in the CSV file represents a subcategory
                subcategory_name = row[0]
                # Create the subcategory under the "History" category
                Subcategories.objects.get_or_create(name=subcategory_name, category=history_category)

        self.stdout.write(self.style.SUCCESS('Successfully imported subcategories for the "History" category from the CSV file.'))
