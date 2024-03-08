from django.urls import path
from .views import loadFullConversation, sendMessage

urlpatterns = [
    path('', loadFullConversation, name='conversation'),
    path('send/', sendMessage, name='sendMessage'),
]