from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, blank=True, null=True)  # Corrected field name from 'ibsn' to 'isbn'
    isbn13 = models.CharField(max_length=17, blank=True, null=True)  # ISBN13 can include hyphens, hence 17 characters
    language = models.CharField(max_length=5)
    pages = models.IntegerField()

    def __str__(self):
        return self.title
