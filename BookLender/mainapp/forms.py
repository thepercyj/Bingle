from django import forms
from .models import Book, UserBook
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser  # Import your CustomUser model


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
        model = UserBook
        fields = ['owner_book_id', 'book_id', 'availability', 'booked']


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
            self.cleaned_data['user'] = user
        return self.cleaned_data
