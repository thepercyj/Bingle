from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.db.models import F
from django_cryptography.fields import encrypt


class CustomUser:
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    primary_location = models.CharField('Primary Location', max_length=255, null=False, default='default')
    current_location = models.CharField('Current Location', max_length=255, null=False, default='default')
    phone_number = models.CharField('Phone Number', max_length=255, null=False, default='default')
    birth_date = models.DateField('Birth Date', null=False, default=date(2000, 1, 1))
    review = models.IntegerField('Review Score', null=True)
    notification_counter = models.IntegerField(default=0)
    profile_pic = encrypt(models.ImageField(upload_to='images', blank=True))

    def __str__(self):
        return self.user.username

    def increment_notification_counter(self):
        # Increment the notification counter
        self.notification_counter = F('notification_counter') + 1
        self.save()


class Conversation(models.Model):
    id_1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='conversations_as_user_1')
    id_2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='conversations_as_user_2')
    latest_message = encrypt(models.CharField('Latest Message', max_length=255, null=False, default='default'))

    def __str__(self):
        return self.id_1.user.username + " and " + self.id_2.user.username + " conversation"


class Book(models.Model):
    book_title = models.CharField('Book Title', max_length=255, null=False, default='default')
    book_author = models.CharField('Book Author', max_length=255, null=False, default='default')
    genre = models.CharField('Genre', max_length=255, null=False, default='default')
    published_date = models.DateField('Publish Date', null=False,
                                      default=date(2024, 1, 1))

    def __str__(self):
        return self.book_title


class UserBook(models.Model):
    owner_book_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='owner')
    currently_with = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='currently_with')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='user_books_book')
    availability = models.BooleanField('Available', null=False, default=True)
    booked = models.CharField('Booked', max_length=255, null=False, default='default')

    def __str__(self):
        return self.book_id.book_title


class Message(models.Model):
    user_book_id = models.ForeignKey(UserBook, on_delete=models.CASCADE, null=True, related_name='messages_user_book')
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='received_messages')
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='sent_messages')
    details = encrypt(models.CharField('Details', max_length=255, null=False, default='default'))
    request_type = models.IntegerField('Request Type', null=False, default=1)
    request_value = models.CharField('Request Value', max_length=255, null=False, default='default')
    created_on = models.DateTimeField('Created On', null=False, default=datetime(2024, 1, 1, 12, 0))
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages_conversation')

    def __str__(self):
        return ("Message from " + self.from_user.user.username + " to " +
                self.to_user.user.username + " sent on " + self.created_on.strftime("%Y-%m-%d %H:%M:%S"))


class Booking(models.Model):
    owner_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='booking_owner')
    borrower_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='booking_borrower')
    user_book_id = models.ForeignKey(UserBook, on_delete=models.CASCADE, null=True, related_name='booking_user_book')
    from_date = models.DateField('From Date', null=False, default=date(2024, 1, 1))
    to_date = models.DateField('To Date', null=False, default=date(2024, 1, 1))
    returned = models.BooleanField('Returned', null=False, default=False)


class Notification(models.Model):
    notify_type = models.IntegerField('Notify Type', null=False, default=1)
    notify_value = models.CharField('Notify Value', max_length=255, null=False, default='default')
    details = models.CharField('Details', max_length=255, null=False, default='default')
    # request_type = models.IntegerField('Request Type', null=False, default=1)  # Added for comparison

    def __str__(self):
        return f"{self.notify_value}: {self.details}"



