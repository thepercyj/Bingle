from django.urls import path
from .views import load_full_conversation, send_message, get_conversation_list, new_conversation

urlpatterns = [
    path('conversation/<int:conversation_id>/', load_full_conversation, name='conversation'),
    path('send/<int:conversation_id>/', send_message, name='sendMessage'),
    path('', get_conversation_list, name='conversation_list'),
    path('new_conversation/', new_conversation, name='new_conversation')
]