from io import BytesIO
from urllib import request

from PIL import Image
from django.contrib.messages import success
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from .forms import BookForm, UserRegisterForm, ProfilePicForm
from .models import UserBook, User, UserProfile, Book, Conversation, Message, Notification
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.core.files.base import ContentFile
from django.db.models import Q, F
from django.db import transaction
from django.utils.timezone import now
from django.http import HttpResponseBadRequest
from BookLender import settings
from django.core.exceptions import ObjectDoesNotExist


# test_user2 = User.objects.get(username='TestUser2')
# test_user_2_profile = UserProfile.objects.get(user=test_user2)


def login_required_message(function):
    """
    Decorator to display a message if the user is not logged in
    """

    def wrap(request, *args, **kwargs):
        # If the user is logged in, call the function
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)

        # If the user is not logged in, display an error message and redirect to the login page
        else:
            messages.error(request, "You need to be logged in to view this page.")
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    # Retains the docstring and name of the original function
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


# test page
# def test(request):
#     if request.method == "POST":
#         searchquery = request.POST.get('searchquery')  # Retrieve the value of searchquery from POST data
#         user_profiles = UserProfile.objects.filter(user__username=searchquery)  # Filter user profiles based on username
#
#         return render(request, 'test.html', {'searchquery': searchquery,
#                                              'user_profiles': user_profiles})  # Pass the filtered user profiles to the template
#     else:
#         return render(request, 'about.html')


# Index Page
def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def lend(request):
    return render(request, 'lend.html')


def forgetpass(request):
    return render(request, 'forgetpass.html')


def new_home(request):
    return render(request, 'newhome.html')


def chat(request):
    return render(request, 'chat.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            form.save_profile()
            return redirect('login_view')  # Redirect to login page
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                # Handle the case where authentication fails
                form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    # Prepare the context
    token = {'form_log': form}
    # No need to manually add the CSRF token in Django templates, {% csrf_token %} does this
    return render(request, 'login.html', token)


@login_required_message
def profile(request):
    form = BookForm(request.POST or None)
    user = request.user
    library = Book.objects.all()
    user_profile = UserProfile.objects.get(user=user)
    user_books = UserBook.objects.filter(owner_book_id=user_profile)
    books_count = user_books.count()  # Count the number of books
    context = {'bookform': form, 'user_books': user_books, 'user_profile': user_profile, 'user': user,
               'user_book_count': books_count, 'library': library}
    return render(request, 'profile_page.html', context)


@login_required_message
def addBook(request):
    """Processes the request to add a new book"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            new_book = form.save()
            # Adds the book to the userBooks table
            addUserBook(request, new_book)
            return redirect('profile')
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


@login_required_message
def addUserBook(request, book):
    user_profile = UserProfile.objects.get(user=request.user)
    """Adds a book to the user's library based on the Book Form submitted"""
    new_user_book = UserBook(
        owner_book_id=user_profile,  # Set the current user as the user_id
        currently_with=user_profile,  # Defaults current user to currently_with on creation
        book_id=book,  # Set the newly created book as the book_id
        availability=True,  # Set available to true by default on creation
        booked='No'
    )

    # Save the new userBooks instance to the database
    new_user_book.save()


@login_required_message
def library(request):
    # Fetch all Book records without prefetch_related
    library = Book.objects.all()

    # Pass the result to the template
    return render(request, 'library.html', {'library': library})


@login_required_message
def removeBook(request):
    user_profile = UserProfile.objects.get(user=request.user)
    book_id = request.POST.get('book_id')
    try:
        book = UserBook.objects.get(id=book_id, owner_book_id=user_profile)
        book.delete()
        messages.success(request, "Book removed successfully.")
    except UserBook.DoesNotExist:
        messages.error(request, "Book not found.")
    return HttpResponseRedirect(reverse('profile') + '?remove=true')


@login_required_message
def updateProfile(request):
    if request.method == 'POST':
        user = request.user
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
        return redirect('profile_page')
    else:
        # Handle non-POST request
        return render(request, 'profile_page.html')


@login_required_message
def img_upload(request):
    if request.method == 'POST':
        form = ProfilePicForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if the user is authenticated
            if request.user.is_authenticated:
                image_file = form.cleaned_data['profile_pic']

                # Check file size
                if image_file.size > 2 * 1024 * 1024:  # 2 MB limit
                    return JsonResponse({'error': "File size exceeds the limit of 2 MB."})

                # Image compression
                img = Image.open(image_file)
                img = img.convert('RGB')
                img.thumbnail((1024, 1024))  # Resize to maximum dimensions of 1024x1024
                img_io = BytesIO()

                # Save in JPEG format
                img.save(img_io, format='JPEG', quality=70)  # Adjust quality as needed
                img_io.seek(0)
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.profile_pic.save(image_file.name, ContentFile(img_io.getvalue()), save=True)

                # Save in PNG format if the uploaded file is not already PNG
                if image_file.name.lower().endswith('.png'):
                    img_io = BytesIO()
                    img.save(img_io, format='PNG', optimize=True)
                    img_io.seek(0)
                    user_profile.profile_pic.save(image_file.name, ContentFile(img_io.getvalue()), save=True)

                # Save in WebP format if the uploaded file is not already WebP
                if image_file.name.lower().endswith('.webp'):
                    img_io = BytesIO()
                    img.save(img_io, format='WEBP', quality=70)
                    img_io.seek(0)
                    user_profile.profile_pic.save(image_file.name, ContentFile(img_io.getvalue()), save=True)

                return JsonResponse({'success': True})  # Indicate success
            else:
                # Handle case where user is not authenticated
                return JsonResponse({'error': "User not authenticated"}, status=401)
    else:
        form = ProfilePicForm()
    return render(request, 'profile_page.html', {'uploadpic': form})


@login_required_message
def display_pic(request):
    # Assuming you have a UserProfile instance associated with the currently logged-in user
    display = request.user.profile

    return render(request, 'profile_page.html', {'display': display})


@login_required_message
def search(request):
    if request.method == "POST":
        searchquery = request.POST.get('searchquery')  # Retrieve the value of searchquery from POST data
        users_profiles = UserProfile.objects.filter(
            user__username=searchquery)  # Filter user profiles based on username

        return render(request, 'search.html', {'searchquery': searchquery,
                                               'users_profiles': users_profiles})  # Pass the filtered user profiles to the template
    else:
        # Handle GET request
        # return render(request, 'search.html')
        users_profiles = UserProfile.objects.all()
        return render(request, 'search.html', {'users_profiles': users_profiles})


@login_required_message
def view_profile(request, profile_id):
    viewprofile = get_object_or_404(UserProfile, pk=profile_id)
    user = request.user
    pre_message = get_pre_message_content(request, user)
    print(pre_message)
    context = {'viewprofile': viewprofile, 'pre_message': pre_message}

    if request.method == 'POST':
        our_profile = UserProfile.objects.get(user=request.user)

        try:
            with transaction.atomic():
                existing_conversation = Conversation.objects.filter(
                    (Q(id_1=our_profile) & Q(id_2=viewprofile)) |
                    (Q(id_2=our_profile) & Q(id_1=viewprofile))
                ).first()

                if existing_conversation:

                    new_message = Message(
                        from_user=our_profile,
                        to_user=viewprofile,
                        details=pre_message,
                        request_type=1,
                        request_value='Simple Message' if pre_message else None,
                        created_on=now(),
                        conversation=existing_conversation
                    )
                    new_message.save()
                    sendnotify = send_notification_to_user(our_profile.user, 1)
                    print(sendnotify)
                    context['notification_message'] = sendnotify  # Add to context

                    return redirect('conversation', conversation_id=existing_conversation.id)
                else:
                    new_conversation_object = Conversation(id_1=our_profile, id_2=viewprofile)
                    new_conversation_object.save()

                    new_message = Message(
                        from_user=our_profile,
                        to_user=viewprofile,
                        details=pre_message,
                        request_type=1,
                        request_value='Simple Message' if pre_message else None,
                        created_on=now(),
                        conversation=new_conversation_object
                    )
                    new_message.save()
                    # Increment notification counters for other user
                    viewprofile.increment_notification_counter()

                    if pre_message:
                        notify_user(request, pre_message)

                    messages.success(request,
                                     pre_message if pre_message else 'Message sent successfully')
                    return HttpResponseRedirect(reverse('new_conversation') + f'?recipient={viewprofile}')
        except Exception as e:
            messages.error(request, 'An error occurred.')
            print(e)
            return redirect('search')

    return render(request, 'users_profiles.html',
                  {'viewprofile': viewprofile, 'pre_message': pre_message, })


def get_pre_message_content(request, user):
    notification = Notification.objects.filter(notify_type=1).first()
    if notification:
        if notification.notify_value == 'Simple Message':
            return f"{user} {notification.details}"
    return None


def get_notification_details(notify_type):
    try:
        # Retrieve an existing notification by type
        notification = Notification.objects.filter(notify_type=notify_type).first()
        if notification:
            return notification.details
        else:
            return "Default notification message."
    except ObjectDoesNotExist:
        return "Notification type not found."


def send_notification_to_user(recipient, notify_type):
    message_detail = get_notification_details(notify_type)
    return f" {recipient}: {message_detail}"


def user_notifications(request, recipient_id, notify_type):
    recipient = User.objects.get(pk=recipient_id)
    notification_message = send_notification_to_user(recipient.username, notify_type)
    return render(request, 'test.html', {'notification_message': notification_message})


# def notification_sender(request):
#     notifications = Notification.objects.all()
#     for notification in notifications:
#         notification.type_description = get_notification_details(notification.notify_type)
#     return {'global_notifications': notifications}


@login_required_message
def notify_user(request, message):
    success(request, message)


@login_required_message
def decrement_counter(request):
    if request.method == 'POST':
        # Assuming you have some way to identify the user
        user = request.user
        try:
            # Retrieve UserProfile object for the user
            user_profile = UserProfile.objects.get(user=user)
            # Ensure the counter is not already zero
            if user_profile.notification_counter > 0:
                # Decrement the notification counter
                user_profile.notification_counter -= 1
                user_profile.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Notification counter already at zero'})
        except UserProfile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User profile does not exist'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required_message
def borrow(request, book_id):
    """
    View function to initiate a borrow request for a book.
    """
    book = get_object_or_404(Book, id=book_id)
    user_books = book.user_books_book.all()
    # notifications = Notification.objects.all()
    # print(notifications)

    if request.method == 'POST':
        selected_owner_username = request.POST.get('owner')

        if selected_owner_username:
            selected_owner = get_object_or_404(UserProfile, user__username=selected_owner_username)
            our_profile = UserProfile.objects.get(user=request.user)
            userbookid = get_object_or_404(UserBook, book_id=book_id, owner_book_id=selected_owner)

            try:
                with transaction.atomic():
                    existing_conversation = Conversation.objects.filter(
                        (Q(id_1=our_profile) & Q(id_2=selected_owner)) |
                        (Q(id_2=our_profile) & Q(id_1=selected_owner))
                    ).first()

                    if existing_conversation:
                        # If conversation already exists, redirect to conversation
                        pre_message_content = f"{request.user.username} wants to borrow {book.book_title} from you."
                        new_message = Message(
                            from_user=our_profile,
                            to_user=selected_owner,
                            details=pre_message_content,
                            request_type=2,
                            request_value='Borrow Request',
                            created_on=now(),
                            user_book_id=userbookid,
                            conversation=existing_conversation
                        )
                        new_message.save()

                        # Display a popup alert to both parties
                        messages.success(request, pre_message_content)

                        return redirect('conversation', conversation_id=existing_conversation.id)
                    else:
                        # If conversation doesn't exist, create a new one
                        new_conversation_object = Conversation(id_1=our_profile, id_2=selected_owner)
                        new_conversation_object.save()
                        # Create a pre-message to notify both parties
                        pre_message_content = f"{request.user.username} wants to borrow {book.book_title} from you."
                        new_message = Message(
                            from_user=our_profile,
                            to_user=selected_owner,
                            details=pre_message_content,
                            request_type=2,
                            request_value='Borrow Request',
                            created_on=now(),
                            user_book_id=userbookid,
                            conversation=new_conversation_object
                        )
                        new_message.save()
                        selected_owner.increment_notification_counter()
                        send_notification_to_user(selected_owner.user, 2)

            except Exception as e:
                messages.error(request, 'An error occurred.')
                return redirect('library')
        else:
            messages.error(request, 'Please select an owner.')
            return redirect('borrow', book_id=book_id)

    return render(request, 'borrow.html', {'book': book, 'user_books': user_books})
