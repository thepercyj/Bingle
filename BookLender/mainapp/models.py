from django.db import models
from datetime import date, datetime


class User(models.Model):
    first_name = models.CharField('First Name', max_length=255, null=False, default='default')
    last_name = models.CharField('First Name', max_length=255, null=False, default='default')
    username = models.CharField('Username', max_length=255, unique=True, null=False, default='default')
    password = models.CharField('Password', max_length=255, null=False, default='default')
    email = models.CharField('Email Address', max_length=255, null=False, default='default')
    primary_location = models.CharField('Primary Location', max_length=255, null=False, default='default')
    current_location = models.CharField('Current Location', max_length=255, null=False, default='default')
    review = models.IntegerField('Review Score', null=True)


class Book(models.Model):
    book_title = models.CharField('Book Title', max_length=255, null=False, default='default')
    book_author = models.CharField('Book Author', max_length=255, null=False, default='default')
    genre = models.CharField('Genre', max_length=255, null=False, default='default')
    published_date = models.DateField('Publish Date', null=False,
                                      default=date(2024, 1, 1))

    def __str__(self):
        return self.bookTitle


class userBooks(models.Model):
    owner_book_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='owner')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_books_user')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='user_books_book')
    availability = models.BooleanField('Available', null=False, default=True)
    booked = models.CharField('Booked', max_length=255, null=False, default='default')


class Messages(models.Model):
    user_book_id = models.ForeignKey(userBooks, on_delete=models.CASCADE, null=True, related_name='messages_user_book')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='from_user')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='to_user')
    details = models.CharField('Details', max_length=255, null=False, default='default')
    request_type = models.IntegerField('Request Type', null=False, default=1)
    request_value = models.CharField('Request Value', max_length=255, null=False, default='default')
    created_on = models.DateTimeField('Created On', null=False, default=datetime(2024, 1, 1, 12, 0))
    modified_on = models.DateTimeField('Modified On', null=False, default=datetime(2024, 1, 1, 12, 0))
    notification_status = models.IntegerField('Notification Status', null=False, default=1)


class Booking(models.Model):
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='booking_owner')
    borrower_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='booking_borrower')
    from_date = models.DateField('From Date', null=False, default=date(2024, 1, 1))
    to_date = models.DateField('To Date', null=False, default=date(2024, 1, 1))
    returned = models.BooleanField('Returned', null=False, default=False)
