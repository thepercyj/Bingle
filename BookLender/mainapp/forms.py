from django import forms
from .models import Book, UserBooks


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_title', 'book_author', 'genre', 'published_date']  # List all fields you want from the model
        labels = {
            'book_title': 'Book Title',
            'book_author': 'Book Author',
            'genre': 'Genre',
            'published_date': 'Publish Date',
        }
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),  # For example, to use a date picker in HTML5
        }


class UserBooksForm(forms.ModelForm):
    class Meta:
        model = UserBooks
        fields = ['owner_book_id', 'book_id', 'availability', 'booked']

