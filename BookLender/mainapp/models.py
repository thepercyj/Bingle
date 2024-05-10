from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.db.models import F
from django_cryptography.fields import encrypt


class CustomUser:
    pass


class UserProfile(models.Model):
    """
    User Profile Model

    This model is used to store additional information about the user.

    Attributes:
    user: A foreign key to the User model.
    primary_location: A string representing the user's primary location.
    current_location: A string representing the user's current location.
    phone_number: A string representing the user's phone number.
    birth_date: A date representing the user's birth date.
    review: An integer representing the user's review score.
    notification_counter: An integer representing the user's notification counter.
    profile_pic: An image representing the user's profile picture.
    """
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
    """
    Conversation Model

    This model is used to store information about conversations between users.

    Attributes:
    id_1: A foreign key to the UserProfile model representing the first user.
    id_2: A foreign key to the UserProfile model representing the second user.
    latest_message: A string representing the latest message in the conversation.
    """
    id_1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='conversations_as_user_1')
    id_2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='conversations_as_user_2')
    latest_message = encrypt(models.CharField('Latest Message', max_length=255, null=False, default='default'))

    def __str__(self):
        return self.id_1.user.username + " and " + self.id_2.user.username + " conversation"


class Book(models.Model):
    """
    Book Model

    This model is used to store information about books.

    Attributes:
    book_title: A string representing the title of the book.
    book_author: A string representing the author of the book.
    genre: A string representing the genre of the book.
    published_date: A date representing the publish date of the book.
    """
    book_title = models.CharField('Book Title', max_length=255, null=False, default='default')
    book_author = models.CharField('Book Author', max_length=255, null=False, default='default')
    genre = models.CharField('Genre', max_length=255, null=False, default='default')
    published_date = models.DateField('Publish Date', null=False,
                                      default=date(2024, 1, 1))

    def __str__(self):
        return self.book_title


class UserBook(models.Model):
    """
    User Book Model

    This model is used to store information about books owned by users.

    Attributes:
    owner_book_id: A foreign key to the UserProfile model representing the owner of the book.
    currently_with: A foreign key to the UserProfile model representing the current user with the book.
    book_id: A foreign key to the Book model representing the book.
    availability: A boolean representing the availability of the book.
    booked: A string representing the booking status of the book.
    """
    owner_book_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='owner')
    currently_with = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='currently_with')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='user_books_book')
    availability = models.BooleanField('Available', null=False, default=True)
    booked = models.CharField('Booked', max_length=255, null=False, default='No')

    def __str__(self):
        return self.book_id.book_title


class Message(models.Model):
    """
    Message Model

    This model is used to store information about messages between users.

    Attributes:
    user_book_id: A foreign key to the UserBook model.
    to_user: A foreign key to the UserProfile model representing the recipient of the message.
    from_user: A foreign key to the UserProfile model representing the sender of the message.
    details: A string representing the details of the message.
    request_type: An integer representing the type of request.
    request_value: A string representing the value of the request.
    created_on: A date representing the creation date of the message.
    conversation: A foreign key to the Conversation model.
    """
    user_book_id = models.ForeignKey(UserBook, on_delete=models.CASCADE, null=True, related_name='messages_user_book')
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='received_messages')
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='sent_messages')
    details = encrypt(models.CharField('Details', max_length=255, null=False, default='default'))
    request_type = models.IntegerField('Request Type', null=False, default=1)
    request_value = models.CharField('Request Value', max_length=255, null=False, default='default')
    created_on = models.DateTimeField('Created On', null=False, default=datetime.now)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages_conversation')

    def __str__(self):
        """
        Return the message details.
        """
        return ("Message from " + self.from_user.user.username + " to " +
                self.to_user.user.username + " sent on " + self.created_on.strftime("%Y-%m-%d %H:%M:%S"))


class Booking(models.Model):
    """
    Booking Model

    This model is used to store information about bookings between users.

    Attributes:
    owner_id: A foreign key to the UserProfile model representing the owner of the book.
    borrower_id: A foreign key to the UserProfile model representing the borrower of the book.
    user_book_id: A foreign key to the UserBook model.
    from_date: A date representing the start date of the booking.
    to_date: A date representing the end date of the booking.
    returned: A boolean representing the return status of the booking.
    """
    owner_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='booking_owner')
    borrower_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, related_name='booking_borrower')
    user_book_id = models.ForeignKey(UserBook, on_delete=models.CASCADE, null=True, related_name='booking_user_book')
    from_date = models.DateField('From Date', null=False, default=date(2024, 1, 1))
    to_date = models.DateField('To Date', null=False, default=date(2024, 1, 1))
    returned = models.BooleanField('Returned', null=False, default=False)


class Transactions(models.Model):
    """
    Transactions Model

    This model is used to store information about transactions between users.

    Attributes:
    user_book_id: A foreign key to the UserBook model.
    borrower_id: A foreign key to the UserProfile model representing the borrower of the book.
    from_date: A date representing the start date of the transaction.
    to_date: A date representing the end date of the transaction.
    status: A string representing the status of the transaction.
    """
    user_book_id = models.ForeignKey(UserBook, on_delete=models.CASCADE, null=True,
                                     related_name='transaction_user_book')
    borrower_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True,
                                    related_name='transaction_borrower')
    from_date = models.DateField('From Date', null=False, default=date(2024, 1, 1))
    to_date = models.DateField('To Date', null=False, default=date(2024, 1, 1))
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')


class Notification(models.Model):
    """
    Notification Model

    Template messages for notification types.

    Attributes:
    notify_type: An integer representing the type of notification.
    notify_value: A string representing the value of the notification.
    details: A string representing the details of the notification.
    """
    notify_type = models.IntegerField('Notify Type', null=False, default=1)
    notify_value = models.CharField('Notify Value', max_length=255, null=False, default='default')
    details = models.CharField('Details', max_length=255, null=False, default='default')


class UserNotification(models.Model):
    """
    User Notification Model

    Notifications for users.

    Attributes:
    sender: A foreign key to the UserProfile model representing the sender of the notification.
    message: A foreign key to the Notification model representing the message of the notification.
    recipient: A foreign key to the UserProfile model representing the recipient of the notification.
    read: A boolean representing the read status of the notification.
    created_on: A date representing the creation date of the notification.
    book: A foreign key to the UserBook model.
    """
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications_sent', default=1)
    message = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='notifications', default=1)
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications', default=1)
    read = models.BooleanField('Read', default=False)
    created_on = models.DateTimeField('Created On', default=datetime.now)
    book = models.ForeignKey(UserBook, on_delete=models.CASCADE, related_name='notifications', null=True)

    def __str__(self):
        """Return the notification message."""
        if self.message.notify_type in [1, 7]:
            # 1: Message, 7: Review
            return f"{self.sender} {self.message.details}"
        elif self.message.notify_type in [2]:
            # 2: Borrow Request
            return f"{self.sender} {self.message.details} {self.book.book_id.book_title} from you."
        elif self.message.notify_type in [3, 4, 6]:
            # 3: Borrow Accept, 4: Borrow Deny, 6: Return Accepted
            return f"{self.sender} {self.message.details} for {self.book.book_id.book_title}."
        else:
            # 5: Return
            return f"{self.sender} {self.message.details} {self.book.book_id.book_title} to you."
