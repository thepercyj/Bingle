from django.contrib.auth.models import User
from django.db import models
from django import forms


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class BorrowRequest(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrow_requests')
    requested_date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.borrower.username} requests {self.book.title}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.message


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']