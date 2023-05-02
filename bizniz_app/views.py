import os
from random import shuffle
import csv
import json
import random
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

def read_csv_file(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        rows = [row for row in csv_reader]

    # Sort rows by 'createdAt' in descending order
    rows.sort(key=lambda x: x['timestamp'], reverse=True)

    images = []
    for row in rows:
        if 'files' in row and row['files']:
            files = json.loads(row['files'].replace("'", '"'))
            for file in files:
                images.append({'file': file, 'userId': row['userId']})
    return images



def show_images(request):
    csv_file_path = 'bizniz_app/data/twetch_grid.csv'
    images = read_csv_file(csv_file_path)
    next_start_index = 50
    context = {'images': images[:50], 'next_start_index': next_start_index, 'previous_start_index': 0}
    return render(request, 'twetch.html', context)

def random_images(request):
    csv_file_path = 'bizniz_app/data/twetch_grid.csv'
    images = read_csv_file(csv_file_path)
    random.shuffle(images)  # Use random.shuffle to randomize the list
    images = images[:50]
    next_start_index = 50
    context = {'images': images, 'next_start_index': next_start_index, 'previous_start_index': 0}
    return render(request, 'twetch.html', context)


def next_images(request, start_index):
    start_index = int(start_index)
    csv_file_path = 'bizniz_app/data/twetch_grid.csv'
    images = read_csv_file(csv_file_path)
    end_index = start_index + 50
    images = images[start_index:end_index]
    next_start_index = end_index
    context = {'images': images, 'next_start_index': next_start_index, 'previous_start_index': start_index - 50 if start_index - 50 >= 0 else 0}
    return render(request, 'twetch.html', context)

def previous_images(request, start_index):
    start_index = int(start_index)
    if start_index - 50 < 0:
        previous_start_index = 0
    else:
        previous_start_index = start_index - 50

    csv_file_path = 'bizniz_app/data/twetch_grid.csv'
    images = read_csv_file(csv_file_path)
    images = images[previous_start_index:start_index]
    
    return render(request, 'twetch.html', {
        'images': images,
        'previous_start_index': previous_start_index - 50 if previous_start_index - 50 >= 0 else 0,
        'next_start_index': start_index,
    })
