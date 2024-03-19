from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect
from mainapp.models import User, UserProfile, Message
from django.contrib import messages
from mainapp.models import Conversation


def login_required_message(function):
    """
    Custom decorator to ensure that the user is logged in before accessing a page.
    """

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to view this page.")
            return login_required(function)(request, *args, **kwargs)
        return function(request, *args, **kwargs)

    return wrapper


@login_required_message
def get_conversation_list(request):
    """
    View function to get the list of conversations for the logged-in user.
    """
    our_profile = UserProfile.objects.get(user=request.user)
    conversationList = Conversation.objects.filter(
        Q(id_1=our_profile) | Q(id_2=our_profile)
    ).exclude(
        Q(id_1=our_profile) & Q(id_2=our_profile)
    ).select_related('id_1__user', 'id_2__user')

    return render(request, "messagesApp/conversation_list.html", {'conversations': conversationList,
                                                                  'our_profile': our_profile})


@login_required_message
def load_full_conversation(request, conversation_id):
    """
    This function loads the full conversation between two users, ensuring the user is logged in.

    Parameters:
    request (HttpRequest): The Django HttpRequest object.
    conversation_id (int): The ID of the conversation between the two users.

    Returns:
    HttpResponse: Renders the conversation page with the messages between the two users.
    """
    try:
        our_profile = UserProfile.objects.get(user=request.user)
        conversation = get_object_or_404(Conversation, id=conversation_id)
        their_profile = get_object_or_404(UserProfile,
                                          (Q(id=conversation.id_1.id) | Q(id=conversation.id_2.id)) &
                                          ~Q(user=request.user))

        messages_list = Message.objects.filter(
            Q(from_user=our_profile, to_user=their_profile) | Q(from_user=their_profile, to_user=our_profile)
        ).select_related('from_user__user', 'to_user__user').order_by('created_on')

        for message in messages_list:
            message.is_from_our_user = (message.from_user == our_profile)

        return render(request, 'messagesApp/conversation.html',
                      {'messages': messages_list, 'conversation': conversation})
    except UserProfile.DoesNotExist:
        return HttpResponse("User profile not found", status=404)


@login_required_message
def send_message(request, conversation_id):
    """
    This function handles the POST request to send a message from one user to another,
    ensuring the user is logged in.

    Parameters:
    request (HttpRequest): The Django HttpRequest object.
    conversation_id (int): The ID of the conversation between the two users.

    Returns:
    HttpResponse: Redirects to the conversation page after the message is sent or error message if failed.
    """
    if request.method == 'POST':
        try:
            conversation = get_object_or_404(Conversation, id=conversation_id)
            our_profile = UserProfile.objects.get(user=request.user)
            their_profile = get_object_or_404(UserProfile,
                                              (Q(id=conversation.id_1.id) | Q(id=conversation.id_2.id)) &
                                              ~Q(user=request.user))

            message = request.POST.get('message')
            if not message:
                messages.error(request, 'Message cannot be empty.')
                return redirect('conversation', conversation_id=conversation_id)
            try:
                existing_conversation = Conversation.objects.get((Q(id_1=our_profile) & Q(id_2=their_profile)) |
                                                                 (Q(id_2=our_profile) & Q(id_1=their_profile)))
                conversation = existing_conversation

            except Conversation.DoesNotExist:
                Conversation(id_1=our_profile, id_2=their_profile).save()
                conversation = Conversation.objects.get((Q(id_1=our_profile) & Q(id_2=their_profile)) |
                                                        (Q(id_2=our_profile) & Q(id_1=their_profile)))

            new_message = Message(
                from_user=our_profile,
                to_user=their_profile,
                details=message,
                request_type=1,
                request_value='default',
                created_on=now(),
                conversation=conversation
            )

            new_message.save()
            conversation.latest_message = message
            conversation.save()
            return redirect('conversation', conversation_id=conversation.id)
        except UserProfile.DoesNotExist:
            messages.error(request, 'User profile not found.')
            return redirect('conversation', conversation_id=conversation_id)
    else:
        return HttpResponse("Invalid request method", status=405)


@login_required_message
def new_conversation(request):
    """
    View function to start a new conversation with another user, ensuring the user is logged in.
    """
    # If the form has been submitted
    if request.method == 'POST':
        username = request.POST.get('recipient')
        message = request.POST.get('message')

        # If the username is not empty
        try:
            user = User.objects.get(username=username)
            their_profile = get_object_or_404(UserProfile, user=user)
            our_profile = get_object_or_404(UserProfile, user=request.user)
            # Ensure the user is not trying to start a conversation with themselves
            if their_profile == our_profile:
                messages.error(request, 'You cannot start a conversation with yourself.')
                return redirect('new_conversation')

            # Ensure the conversation does not already exist
            with transaction.atomic():
                existing_conversation = Conversation.objects.filter(
                    (Q(id_1=our_profile) & Q(id_2=their_profile)) |
                    (Q(id_2=our_profile) & Q(id_1=their_profile))
                ).first()

                # If the conversation already exists, add the message to the existing conversation
                if existing_conversation:
                    if message:
                        new_message = Message(
                            from_user=our_profile,
                            to_user=their_profile,
                            details=message,
                            request_type=1,
                            request_value='default',
                            created_on=now(),
                            conversation=existing_conversation
                        )
                        new_message.save()
                        existing_conversation.latest_message = message
                        existing_conversation.save()
                    return redirect('conversation', conversation_id=existing_conversation.id)

                # If the conversation does not exist, create a new conversation
                new_conversation_object = Conversation(id_1=our_profile, id_2=their_profile)
                new_conversation_object.save()
                if message:
                    new_message = Message(
                        from_user=our_profile,
                        to_user=their_profile,
                        details=message,
                        request_type=1,
                        request_value='default',
                        created_on=now(),
                        conversation=new_conversation_object
                    )
                    new_message.save()
                    new_conversation_object.latest_message = message
                    new_conversation_object.save()

                return redirect('conversation', conversation_id=new_conversation_object.id)
        # If the user does not exist, display an error message
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('new_conversation')

    # If the form has not been submitted, display the new conversation page
    else:
        return render(request, 'messagesApp/new_conversation.html',
                      {'users': UserProfile.objects.exclude(user=request.user)})


def old_conversation(request):
    return render(request, 'messagesApp/conversation.html')


def rate_user(request, conversation_id):
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, id=conversation_id)
        their_profile = get_object_or_404(UserProfile,
                                          (Q(id=conversation.id_1.id) | Q(id=conversation.id_2.id)) &
                                          ~Q(user=request.user))

        rating = request.POST.get('rating')
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                messages.error(request, "Rating must be an integer between 1 and 5.")
                return HttpResponseBadRequest("Rating must be an integer between 1 and 5.")
        except ValueError:
            messages.error(request, "Invalid input. Rating must be an integer.")
            return HttpResponseBadRequest("Invalid input. Rating must be an integer.")

        current_rating = their_profile.review
        if current_rating:
            their_profile.review = (current_rating + rating) / 2
        else:
            their_profile.review = rating
        their_profile.save()
        return redirect('conversation', conversation_id=conversation_id)
