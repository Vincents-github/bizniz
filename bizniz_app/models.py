from django.db import models
from django.utils import timezone

class CsvEntry(models.Model):
    userId = models.CharField(max_length=500)
    txid = models.CharField(max_length=500)
    pay = models.CharField(max_length=500)
    per = models.CharField(max_length=500)
    skill = models.CharField(max_length=500)
    portfolio = models.CharField(max_length=500)
    available = models.CharField(max_length=500)
    bio = models.TextField()
    createdAt = models.DateTimeField(default=timezone.now)
