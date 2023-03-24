import os
import csv
from django.http import HttpResponse
from django.shortcuts import render
from .models import CsvEntry
from django.conf import settings
import datetime
from django.core.serializers import serialize



def import_csv():
    csv_path = os.path.join(settings.BASE_DIR, 'bizniz_app/data/post_content.csv')
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i == 0:  # Print the first row to check the field names
                print(row)
            CsvEntry.objects.update_or_create(
                userId=row['userId'],
                defaults={
                    'txid': row['txid'],
                    'pay': row['pay'],
                    'per': row['per'],
                    'skill': row['skill'],
                    'portfolio': row['portfolio'],
                    'available': row['available'],
                    'bio': row['bio'],
                    'createdAt': datetime.datetime.strptime(row['createdAt'], '%Y-%m-%dT%H:%M:%S.%f%z')
                }
            )



def index(request):
    import_csv()  # Import the CSV data
    entries = CsvEntry.objects.all().order_by('-createdAt')
    return render(request, 'index.html', {'entries': entries})

def card(request):
    print("Card view called")  # Add this line
    import_csv()  # Import the CSV data
    entries = CsvEntry.objects.all().order_by('-createdAt')
    return render(request, 'card.html', {'entries': entries})