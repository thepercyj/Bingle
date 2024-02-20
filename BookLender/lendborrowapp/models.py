from django.db import models
from django.contrib.auth.models import User
from django import forms


class User(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_books')
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='borrowed_books')

    def __str__(self):
        return self.title


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']


class BookRequestForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'borrower']
