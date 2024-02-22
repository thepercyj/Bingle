from django.contrib import admin
from .models import Book, BorrowRequest, Notification

admin.site.register(Book)
admin.site.register(BorrowRequest)
admin.site.register(Notification)