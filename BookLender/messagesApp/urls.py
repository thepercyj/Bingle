from django.urls import path
from .views import loadFullConversation, sendMessage, getConversationList

urlpatterns = [
    path('conversation/<int:conversation_id>/', loadFullConversation, name='conversation'),
    path('send/<int:conversation_id>/', sendMessage, name='sendMessage'),
    path('', getConversationList, name='conversation_list'),
]