# articles/models.py
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=255, null=True, blank=True)
    link = models.URLField()
    published_date = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=100, default='Unknown')

    def __str__(self):
        return self.title