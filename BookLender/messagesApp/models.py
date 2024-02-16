from django.db import models

from django.db import models

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Author(models.Model):
    name = models.CharField(max_length=500)


class Message(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', null=True)




