from datetime import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.cache import never_cache

from .forms import BookForm
from .models import UserBook, Book, User, UserProfile, Conversation, Message
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create a test user and profile testing
test_user = User.objects.get(username='testUser')
test_user_profile = UserProfile.objects.get(user=test_user)
test_user2 = User.objects.get(username='TestUser2')
test_user_2_profile = UserProfile.objects.get(user=test_user2)


# Index Page
def index(request):
    return render(request, 'index.html')


def category(request):
    return render(request, 'category.html')


def about(request):
    return render(request, 'about.html')


def work(request):
    return render(request, 'work.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


@never_cache
def profile(request):
    form = BookForm(request.POST or None)
    user = test_user
    user_profile = test_user_profile
    user_books = UserBook.objects.filter(owner_book_id=test_user_profile)
    context = {'form': form, 'user_books': user_books, 'user_profile': user_profile, 'user': user}
    return render(request, 'profile_page.html', context)


def addBook(request):
    """Processes the request to add a new book"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            new_book = form.save()
            # Adds the book to the userBooks table
            addUserBook(new_book)
            return redirect('dashboard')
        else:
            # Form validation failed, return error details
            return JsonResponse({'status': 'error', 'message': 'Form validation failed', 'errors': form.errors},
                                status=400)
    else:
        # If the request method is not POST, inform the client appropriately
        # Or render a form for GET requests if that's intended behavior
        return HttpResponse('This endpoint expects a POST request.', status=405)

    # As a last resort, return a generic response for unexpected cases
    # This line should ideally never be reached if all cases are handled correctly above
    return HttpResponse('Unexpected error occurred.', status=500)


def addUserBook(book):
    """Adds a book to the user's library based on the Book Form submitted"""
    new_user_book = UserBook(
        owner_book_id=test_user_profile,  # Set the current user as the user_id
        currently_with=test_user_profile,  # Defaults current user to currently_with on creation
        book_id=book,  # Set the newly created book as the book_id
        availability=True,  # Set available to true by default on creation
        booked='No'
    )

    # Save the new userBooks instance to the database
    new_user_book.save()


@never_cache
def removeBook(request):
    book_id = request.POST.get('book_id')
    try:
        book = UserBook.objects.get(id=book_id, owner_book_id=test_user_profile)
        book.delete()
        messages.success(request, "Book removed successfully.")
    except UserBook.DoesNotExist:
        messages.error(request, "Book not found.")
    return HttpResponseRedirect(reverse('dashboard') + '?remove=true')


def updateProfile(request):
    if request.method == 'POST':
        user_id = test_user.id
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user)  # Adjust based on your UserProfile model relation

        user.username = request.POST.get('inputUserName')
        user.first_name = request.POST.get('inputFirstName')
        user.last_name = request.POST.get('inputLastName')
        user.email = request.POST.get('inputEmailAddress')
        user.save()

        user_profile.primary_location = request.POST.get('inputLocation')
        user_profile.phone_number = request.POST.get('inputPhone')
        user_profile.save()

        messages.success(request, "Profile updated successfully.")
        return profile(request)
    else:
        # Handle non-POST request
        return render(request, 'profile_page.html')


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
    """Loads the full conversation between two users."""
    # Placeholder for actual user profile retrieval logic
    our_id = test_user_profile
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
    return render(request, 'conversation.html', {'messages': messages_list})

def sendMessage(request):
    if request.method == 'POST':
        our_id = test_user_profile
        their_id = test_user_2_profile
        message = request.POST.get('message')
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
        new_message.save()
        return loadFullConversation(request)






