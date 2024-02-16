from django.urls import path

from . import views
from .views import chat

urlpatterns = [
    path('lobby/', views.lobby, name='lobby'),
    path('chat/', views.chat, name='chat'),
    path('create-message/', views.create_message, name='create-message'),
    path('stream-chat-messages/', views.stream_chat_messages, name='stream-chat-messages'),
    path('chat/<str:room_name>/', chat, name='chat'),
]