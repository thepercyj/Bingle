from django import forms
from .models import Book, UserBook, UserProfile
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


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Required.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    primary_location = forms.CharField(max_length=30, required=True, help_text='Required.')
    current_location = forms.CharField(max_length=30, required=True, help_text='Required.')
    phone_number = forms.CharField(max_length=30, required=True, help_text='Required.')
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD',
                                 widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # If you want to save the agrees_to_terms and wants_newsletter
            # You would typically handle this separately after user creation
        return user

    def save_profile(self, commit=True):
        new_profile = UserProfile.objects.create(user=self.instance,
                                                 primary_location=self.cleaned_data['primary_location'],
                                                 current_location=self.cleaned_data['current_location'],
                                                 phone_number=self.cleaned_data['phone_number'],
                                                 birth_date=self.cleaned_data['birth_date'])
        if commit:
            new_profile.save()
        return new_profile


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