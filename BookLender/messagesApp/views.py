from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from mainapp.forms import BookForm
from mainapp.models import UserBook, Book, User, UserProfile, Conversation, Message
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

# Gets a second test user for testing purposes
test_user2 = User.objects.get(username='TestUser2')
test_user_2_profile = UserProfile.objects.get(user=test_user2)

# def getConversation(request):
# Rob
#     if request.method == 'POST':
#         our_username = test_user
#         their_username = request.POST.get('their_username')
#
# def getConversationList(request):
# Rob
#     if request.method == 'POST':
#         our_username = test_user.username
#         conversationList = Conversations.objects.get(id_1=our_username || id_2=our_username)
#         for conversation in conversationList:
#             conversation_contents.append(get most recent conversation content and username from Messages)
#             render(messages.html, converation_contents)
#


def loadFullConversation(request):
    """
    This function loads the full conversation between two users.

    Parameters:
    request (HttpRequest): The Django HttpRequest object.

    Returns:
    HttpResponse: Renders the conversation page with the messages between the two users.
    """
    # Placeholder for actual user profile retrieval logic
    our_id = UserProfile.objects.get(user=request.user)
    their_id = test_user_2_profile

    # If id not found, returns a bad request
    if their_id is None:
        return HttpResponse("Bad Request", status=400)

    # Get the conversation between the two users
    messages_list = Message.objects.filter(
        Q(from_user=our_id, to_user=their_id) | Q(from_user=their_id, to_user=our_id)
    ).select_related('from_user__user', 'to_user__user').order_by('created_on')

    # Annotate each message with 'is_from_our_user' for use in styling
    for message in messages_list:
        message.is_from_our_user = (message.from_user == our_id)

    # Render the conversation page with the messages
    return render(request, 'messagesApp/conversation.html', {'messages': messages_list})


def sendMessage(request):
    """
    This function handles the POST request to send a message from one user to another.

    Parameters:
    request (HttpRequest): The Django HttpRequest object.

    Returns:
    HttpResponse: Redirects to the conversation page after the message is sent.
    """
    # Check if the request method is POST
    if request.method == 'POST':
        # Set the sender and receiver of the message
        our_id = UserProfile.objects.get(user=request.user)
        their_id = test_user_2_profile

        # Get the message from the POST data
        message = request.POST.get('message')

        # Create a new Message object with the provided details
        new_message = Message(
            from_user=our_id,
            to_user=their_id,
            details=message,
            request_type=1,
            request_value='default',
            created_on=datetime.now(),
            modified_on=datetime.now(),
            notification_status=1
        )

        # Save the new message to the database
        new_message.save()

        # Redirect to the conversation page
        return redirect('conversation')