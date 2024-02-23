from django.contrib import admin
from .models import UserBook, Book, UserProfile, Conversation, Message, Booking

admin.site.register(UserBook)
admin.site.register(Book)
admin.site.register(UserProfile)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Booking)


