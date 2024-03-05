from django.urls import path
from .views import loadFullConversation, sendMessage, getConversationList

urlpatterns = [
    path('', loadFullConversation, name='conversation'),
    path('send/', sendMessage, name='sendMessage'),
  path('conversation_list/', getConversationList, name='conversation_list'),
]