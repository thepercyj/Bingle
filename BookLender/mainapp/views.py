from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.cache import never_cache

from .forms import BookForm
from .models import UserBooks, Book, User, UserProfile, Conversations
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create a test user and profile for testing
# test_user = User.objects.create_user("testUser", "testuser@email.com", password="password", first_name="Test", last_name="User")
test_user = User.objects.first()
# test_user_profile = UserProfile.objects.create(user=test_user, primary_location="Brighton", current_location="Brighton",review= 5)
test_user_profile = UserProfile.objects.first()


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
    user_books = UserBooks.objects.filter(owner_book_id=test_user_profile)
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
    new_user_book = UserBooks(
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
        book = UserBooks.objects.get(id=book_id, owner_book_id=test_user_profile)
        book.delete()
        messages.success(request, "Book removed successfully.")
    except UserBooks.DoesNotExist:
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
# def loadFullConversation(request):
# Tom
#     if request.method == 'POST':
#         our_id = test_user
#         their_id = post.their_id
#         messagesList = get Messages(ordered by time, messageDetails:sender_id, where recieved=our_id && sender=their_id
#                            || where recieved=thier_id && sender=our_id)
#         render(messageList)





