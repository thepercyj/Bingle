from django.contrib import admin
from .models import UserProfile, Book, UserBooks, Messages, Booking

admin.site.register(UserProfile)
admin.site.register(Book)
admin.site.register(UserBooks)
admin.site.register(Messages)
admin.site.register(Booking)

