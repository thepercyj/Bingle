from django.contrib import admin
from .models import ChatRoom, Author, Message

admin.site.register(ChatRoom)
admin.site.register(Author)
admin.site.register(Message)

