from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from mainapp.models import User, UserProfile, Message
from django.contrib import messages

# Fetches second test user and their profile for testing purposes
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


@login_required
def loadFullConversation(request):
    """
    This function loads the full conversation between two users, ensuring the user is logged in.

    Parameters:
    request (HttpRequest): The Django HttpRequest object.

    Returns:
    HttpResponse: Renders the conversation page with the messages between the two users.
    """
    try:
        our_profile = UserProfile.objects.get(user=request.user)
        their_profile = get_object_or_404(UserProfile, user__username='TestUser2')

        messages_list = Message.objects.filter(
            Q(from_user=our_profile, to_user=their_profile) | Q(from_user=their_profile, to_user=our_profile)
        ).select_related('from_user__user', 'to_user__user').order_by('created_on')

        for message in messages_list:
            message.is_from_our_user = (message.from_user == our_profile)

        return render(request, 'messagesApp/conversation.html', {'messages': messages_list})
    except UserProfile.DoesNotExist:
        return HttpResponse("User profile not found", status=404)

@login_required
def sendMessage(request):
    """
    This function handles the POST request to send a message from one user to another,
    ensuring the user is logged in.

    Parameters:
    request (HttpRequest): The Django HttpRequest object.

    Returns:
    HttpResponse: Redirects to the conversation page after the message is sent or error message if failed.
    """
    if request.method == 'POST':
        try:
            our_profile = UserProfile.objects.get(user=request.user)
            their_profile = get_object_or_404(UserProfile, user__username='TestUser2')

            message = request.POST.get('message')
            if not message:
                messages.error(request, 'Message cannot be empty.')
                return redirect('conversation')

            new_message = Message(
                from_user=our_profile,
                to_user=their_profile,
                details=message,
                request_type=1,
                request_value='default',
                created_on=now(),
                modified_on=now(),
                notification_status=1
            )
            new_message.save()
            return redirect('conversation')
        except UserProfile.DoesNotExist:
            messages.error(request, 'User profile not found.')
            return redirect('conversation')
    else:
        return HttpResponse("Invalid request method", status=405)
