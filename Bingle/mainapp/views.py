from datetime import datetime
from io import BytesIO
from PIL import Image
from django.contrib.messages import success
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import BookForm, UserRegisterForm, ProfilePicForm
from .models import UserBook, User, UserProfile, Book, Conversation, Message, Notification, Booking, Transactions, \
    UserNotification
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.core.files.base import ContentFile
from django.db.models import Q, F
from django.db import transaction
from django.utils.timezone import now
from django.conf import settings
import json
from recommendations.views import getborrowed
from django.core.cache import cache



# test_user2 = User.objects.get(username='TestUser2')
# test_user_2_profile = UserProfile.objects.get(user=test_user2)


def login_required_message(function):
    """
    Decorator to display a message if the user is not logged in

    :param function: function
    """

    def wrap(request, *args, **kwargs):
        """
        Wrapper function to check if the user is logged in

        Parameters:
        :param request: HttpRequest
            The request object
        :param *args: tuple
            Additional positional arguments
        :param **kwargs: dict
        """
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
def test(request):
    if request.method == "POST":
        user_profile = UserProfile.objects.get(user=request.user)
        user_primary = user_profile.primary_location
        searchquery = request.POST.get('searchquery')  # Retrieve the value of searchquery from POST data
        user_profiles = UserProfile.objects.filter(user__username=searchquery,
                                                   primary_location=user_primary)  # Filter user profiles based on username

        return render(request, 'test.html', {'searchquery': searchquery,
                                             'user_profiles': user_profiles})  # Pass the filtered user profiles to the template
    else:
        return render(request, 'about.html')


# Index Page
def index(request):
    """
    Renders the index page

    :param request: HttpRequest - The request object
    """
    return render(request, 'index.html')


def about(request):
    """
    Renders the about page

    :param request: HttpRequest - The request object
    """
    return render(request, 'about.html')


def new_about(request):
    return render(request, 'new_about_us.html')


def lend(request):
    """
    Renders the lend page

    :param request: HttpRequest - The request object
    """
    return render(request, 'lend.html')


def forgetpass(request):
    """
    Renders the forgetpass page

    :param request: HttpRequest - The request object
    """
    return render(request, 'forgetpass.html')

@login_required_message
def new_home(request):
    """
    Renders the home page

    :param request: HttpRequest - The request object
    """
    form = BookForm(request.POST or None)
    user = request.user
    # Attempt to retrieve library from cache
    library = Book.objects.all()
    user_profile = UserProfile.objects.get(user=user)
    user_books = UserBook.objects.filter(owner_book_id=user_profile.id)
    pre_booking = Transactions.objects.filter(user_book_id__owner_book_id=user_profile.id)
    owner_bookings = Booking.objects.filter(owner_id=user_profile)
    borrower_bookings = Booking.objects.filter(borrower_id=user_profile)
    total_bookings = owner_bookings.count() + borrower_bookings.count()
    recs = getborrowed(request)

    # Search functionality implemented
    user_books_search_query = request.GET.get('user_books_search')
    if user_books_search_query:
        user_books = user_books.filter(book_id__book_title__icontains=user_books_search_query)

    library_search_query = request.GET.get('library_search')
    if library_search_query:
        library = library.filter(book_title__icontains=library_search_query)


    # Pagination for user_books
    page_number = request.GET.get('page')
    paginator = Paginator(user_books, 10)  # Show 10 user_books per page
    try:
        user_books = paginator.page(page_number)
    except PageNotAnInteger:
        user_books = paginator.page(1)
    except EmptyPage:
        user_books = paginator.page(paginator.num_pages)

    # Pagination for library
    library_page = request.GET.get('library_page')
    library_paginator = Paginator(library, 10)  # Show 10 books per page
    try:
        library = library_paginator.page(library_page)
    except PageNotAnInteger:
        library = library_paginator.page(1)
    except EmptyPage:
        library = library_paginator.page(library_paginator.num_pages)

    context = {
        'bookform': form,
        'user_books': user_books,
        'user_profile': user_profile,
        'user': user,
        # 'user_books_count': user_books_count,  # Update the count with user_books_count
        'library': library,
        'pre_booking': pre_booking,
        'owner_bookings': owner_bookings,
        'borrower_bookings': borrower_bookings,
        'total_bookings': total_bookings,
        'recs': recs,
    }

    return render(request, 'home.html', context)


def new_landing_page(request):
    return render (request, 'new_landing_page.html')

#Need to remove all modal related code as it is shifted to dashboard
def new_profile(request):
    """
    Renders the main dashboard page

    :param request: HttpRequest - The request object
    """
    form = BookForm(request.POST or None)
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    context = {
        'bookform': form,
        'user_profile': user_profile,
        'user': user,
        'library': library,
    }
    return render(request, 'new_profile.html', context)


@login_required_message
def chat(request):
    """
    Renders the chat page

    :param request: HttpRequest - The request object
    """
    our_profile = UserProfile.objects.get(user=request.user)
    conversation_list = Conversation.objects.filter(
        Q(id_1=our_profile) | Q(id_2=our_profile)
    ).exclude(
        Q(id_1=our_profile) & Q(id_2=our_profile)
    ).select_related('id_1__user', 'id_2__user')
    return render(request, 'chat.html',
                  {'conversation_list': conversation_list, 'our_profile': our_profile, 'initial': True})


def register(request):
    """
    Processes the request to register a new user

    :param request: HttpRequest - The request object
    """
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
    """
    Processes the request to log in a user

    :param request: HttpRequest - The request object
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('new_landing_page')
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
    """
    Renders the profile page

    :param request: HttpRequest - The request object
    """
    form = BookForm(request.POST or None)
    user = request.user
    library = cache.get('library')
    if library is None:
        library = Book.objects.all()
        cache.set('library', library, 60 * 5)  # Cache for 5 minutes
    lib_count = library.count()
    user_profile = UserProfile.objects.get(user=user)
    user_books = UserBook.objects.filter(owner_book_id=user_profile.id)
    user_books_count = UserBook.objects.filter(owner_book_id=user_profile).count()
    pre_booking = Transactions.objects.filter(user_book_id__owner_book_id=user_profile.id)
    owner_bookings = Booking.objects.filter(owner_id=user_profile)
    borrower_bookings = Booking.objects.filter(borrower_id=user_profile)
    total_bookings = owner_bookings.count() + borrower_bookings.count()

    # Search functionality
    user_books_search_query = request.GET.get('user_books_search')
    if user_books_search_query:
        user_books = user_books.filter(book_id__book_title__icontains=user_books_search_query)

    library_search_query = request.GET.get('library_search')
    if library_search_query:
        library = library.filter(book_title__icontains=library_search_query)

    # Pagination for user_books
    page_number = request.GET.get('page')
    paginator = Paginator(user_books, 10)  # Show 10 user_books per page
    try:
        user_books = paginator.page(page_number)
    except PageNotAnInteger:
        user_books = paginator.page(1)
    except EmptyPage:
        user_books = paginator.page(paginator.num_pages)

    # Pagination for library
    library_page = request.GET.get('library_page')
    library_paginator = Paginator(library, 10)  # Show 10 books per page
    try:
        library = library_paginator.page(library_page)
    except PageNotAnInteger:
        library = library_paginator.page(1)
    except EmptyPage:
        library = library_paginator.page(library_paginator.num_pages)

    context = {
        'bookform': form,
        'user_books': user_books,
        'user_profile': user_profile,
        'user': user,
        'user_books_count': user_books_count,  # Update the count with user_books_count
        'library': library,
        'lib_count': lib_count,
        'pre_booking': pre_booking,
        'owner_bookings': owner_bookings,
        'borrower_bookings': borrower_bookings,
        'total_bookings': total_bookings,
    }
    return render(request, 'profile_page.html', context)


@login_required_message
def addBook(request):
    """
    Processes the request to add a new book

    :param request: HttpRequest - The request object
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            new_book = form.save()
            # Adds the book to the userBooks table
            addUserBook(request, new_book)
            return redirect('new_home')
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
def sample_search(request):
    user_profile = UserProfile.objects.get(user=request.user)
    current_location = user_profile.current_location
    if request.method == "POST":
        searchquery = request.POST.get('searchquery')  # Retrieve the value of searchquery from POST data
        users_profiles = UserProfile.objects.filter(
            user__username=searchquery)  # Filter user profiles based on username and primary location

        return render(request, 'samplesearch.html', {'searchquery': searchquery,
                                                     'users_profiles': users_profiles})  # Pass the filtered user profiles to the template
    else:
        # Handle GET request
        # return render(request, 'search.html')
        users_profiles = UserProfile.objects.all()
        users_profiles = users_profiles.filter(current_location=current_location)
        return render(request, 'samplesearch.html', {'users_profiles': users_profiles})


@login_required_message
def addUserBook(request, book):
    """
    Adds a new book to the user's library

    :param request: HttpRequest - The request object
    :param book: Book - The book to add to the user's library
    """
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
    """
    Renders the library page

    :param request: HttpRequest - The request object
    """
    # Fetch all Book records without prefetch_related
    library = Book.objects.all()

    # Pass the result to the template
    return render(request, 'library.html', {'library': library})


@login_required_message
def removeBook(request):
    """
    Removes a book from the user's library

    :param request: HttpRequest - The request object
    """
    user_profile = UserProfile.objects.get(user=request.user)
    book_id = request.POST.get('book_id')
    try:
        book = UserBook.objects.get(id=book_id, owner_book_id=user_profile)
        book.delete()
        messages.success(request, "Book removed successfully.")
    except UserBook.DoesNotExist:
        messages.error(request, "Book not found.")
    return HttpResponseRedirect(reverse('new_home') + '?remove=true')


@login_required_message
def updateProfile(request):
    """
    Updates the user's profile

    :param request: HttpRequest - The request object
    """
    if request.method == 'POST':
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        user.username = request.POST.get('inputUserName')
        user.first_name = request.POST.get('inputFirstName')
        user.last_name = request.POST.get('inputLastName')
        user.email = request.POST.get('inputEmailAddress')
        user.save()

        user_profile.primary_location = request.POST.get('inputLocation')
        user_profile.phone_number = request.POST.get('inputPhone')
        user_profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('new_home')
    else:
        # Handle non-POST request
        return render(request, 'profile_page.html')


@login_required_message
def img_upload(request):
    """
    Handles the image upload functionality

    :param request: HttpRequest - The request object
    """
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
    """
    Displays the user's profile picture

    :param request: HttpRequest - The request object
    """
    # Get the user's profile
    display = request.user.profile

    return render(request, 'profile_page.html', {'display': display})


@login_required_message
def search(request):
    """
    Renders the search page and handles search functionality

    :param request: HttpRequest - The request object
    """
    user_profile = UserProfile.objects.get(user=request.user)
    current_location = user_profile.current_location
    if request.method == "POST":
        searchquery = request.POST.get('searchquery')  # Retrieve the value of searchquery from POST data
        users_profiles = UserProfile.objects.filter(
            user__username=searchquery)  # Filter user profiles based on username and primary location

        return render(request, 'search.html', {'searchquery': searchquery,
                                               'users_profiles': users_profiles})  # Pass the filtered user profiles to the template
    else:
        # Handle GET request
        # return render(request, 'search.html')
        users_profiles = UserProfile.objects.all()
        users_profiles = users_profiles.filter(current_location=current_location)
        return render(request, 'search.html', {'users_profiles': users_profiles})


@login_required_message
def view_profile(request, profile_id):
    """
    Renders the user profile page for a specific user

    :param request: HttpRequest - The request object
    :param profile_id: int - The ID of the user profile to view
    """
    viewprofile = get_object_or_404(UserProfile, pk=profile_id)
    user = request.user
    pre_message = get_pre_message_content(request, user)
    print(pre_message)

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

                    return redirect('chat', conversation_idconversation_id=existing_conversation.id)
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
                    return HttpResponseRedirect(reverse('chat') + f'?recipient={viewprofile}')
        except Exception as e:
            messages.error(request, 'An error occurred.')
            print(e)
            return redirect('search')

    return render(request, 'users_profiles.html',
                  {'viewprofile': viewprofile, 'pre_message': pre_message})


def get_pre_message_content(request, user):
    """
    Retrieves the pre-message content for the user

    :param request: HttpRequest - The request object
    :param user: User - The user object
    """
    notification = Notification.objects.filter(notify_type=1).first()
    if notification:
        if notification.notify_value == 'Simple Message':
            return f"{user} {notification.details}"
    return None


@login_required_message
def notify_user(request, message):
    """
    Notifies the user with a message

    :param request: HttpRequest - The request object
    :param message: str - The message to send
    """
    success(request, message)


@login_required_message
def decrement_counter(request):
    """
    Decrements the notification counter for the user

    :param request: HttpRequest - The request object
    """
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
def borrow(request, user_book_id):
    """
    Combined function to handle both initiating a borrow request and saving booking details.

    :param request: HttpRequest - The request object
    :param user_book_id: int - The ID of the user book to borrow
    """
    # Get the user_book object based on the user_book_id
    user_book = get_object_or_404(UserBook, id=user_book_id)
    # Get the book object based on the user_book object
    book = get_object_or_404(Book, id=user_book.book_id.id)
    # Get all user_books associated with the book
    user_books = book.user_books_book.all()

    # Check if the request method is POST
    if request.method == 'POST':
        # Get the selected owner from the POST data and retrieve the username
        selected_owner = request.POST.get('owner_id')
        selected_owner_username = UserProfile.objects.get(id=selected_owner).user.username
        # Check if the selected owner is not empty
        if not selected_owner_username:
            # Display an error message and redirect to the borrow page
            messages.error(request, 'Please select an owner.')
            return redirect('borrow', user_book_id=user_book_id)

        # Get the selected owner's UserProfile object
        selected_owner = get_object_or_404(UserProfile, user__username=selected_owner_username)
        # Get the current user's UserProfile object
        our_profile = UserProfile.objects.get(user=request.user)

        try:
            # Create a new conversation object or retrieve an existing one
            with transaction.atomic():
                existing_conversation = Conversation.objects.filter(
                    (Q(id_1=our_profile) & Q(id_2=selected_owner)) |
                    (Q(id_2=our_profile) & Q(id_1=selected_owner))
                ).first()

                # Check if the conversation already exists
                if existing_conversation:
                    conversation = existing_conversation
                # If the conversation does not exist, create a new one
                else:
                    conversation = Conversation(id_1=our_profile, id_2=selected_owner)
                    conversation.save()

                # Create a pre-message to notify the recipient
                pre_message_content = f"{request.user.username} wants to borrow {book.book_title} from you."
                new_message = Message(
                    from_user=our_profile,
                    to_user=selected_owner,
                    details=pre_message_content,
                    request_type=2,
                    request_value='Borrow Request',
                    created_on=now(),
                    user_book_id=user_book,
                    conversation=conversation
                )
                new_message.save()
                messages.success(request, pre_message_content)

                # Create a new booking object and save the booking details
                from_date = request.POST.get('from_date')
                to_date = request.POST.get('to_date')

                pre_booking = Transactions(
                    user_book_id=user_book,
                    borrower_id=our_profile,
                    from_date=from_date,
                    to_date=to_date,
                    status='pending',
                )
                pre_booking.save()
                print('pre booking details saved')

                # Creates a notification for the owner
                notification = UserNotification(
                    sender=our_profile,
                    message=Notification.objects.get(notify_type=2),
                    recipient=selected_owner,
                    book=user_book
                )
                notification.save()

                messages.success(request, 'Borrow request saved successfully!')

                # Redirect to appropriate chat page
                return redirect('chat')

        except Exception as e:
            print(e)
            messages.error(request, 'An error occurred.')
            return redirect('library')

    return render(request, 'borrow.html', {'book': book, 'user_books': user_books, 'user_book': user_book})


@login_required_message
def approve_borrow_request(request, book_id):
    """
    View function to approve a borrow request for a book.

    :param request: HttpRequest - The request object
    :param book_id: int - The ID of the book to approve the borrow request for
    """
    if request.method == 'POST':
        print("Book ID: ", book_id)
        # Get the message object based on the book ID and request type
        message = get_object_or_404(Message, user_book_id__id=book_id, request_type=2)

        # Create a pre-message to notify the recipient
        pre_message_content = f"Your borrow request for {message.user_book_id.book_id.book_title} has been approved."
        new_message = Message(
            from_user=message.to_user,
            to_user=message.from_user,
            details=pre_message_content,
            request_type=3,
            request_value='Request Accepted',
            user_book_id=message.user_book_id,
            conversation=message.conversation,
        )
        new_message.save()

        # Update booking status to approved
        pre_booking = Transactions.objects.get(user_book_id=message.user_book_id)
        pre_booking.status = 'approved'
        pre_booking.save()

        print('transactions updated')

        # Update UserBook values
        with transaction.atomic():
            user_book = message.user_book_id
            user_book.currently_with = message.from_user
            user_book.availability = False
            user_book.booked = True
            user_book.save()

            # Create a booking object
            booking = Booking.objects.create(
                owner_id=message.to_user,
                borrower_id=message.from_user,
                user_book_id=message.user_book_id,
                from_date=datetime.strptime(str(pre_booking.from_date), '%Y-%m-%d').date(),
                to_date=datetime.strptime(str(pre_booking.to_date), '%Y-%m-%d').date(),
                returned=False
            )

            booking.save()
            print('booking saved successfully')

            # Add a notification for the owner
            notification = UserNotification(
                sender=message.to_user,
                message=Notification.objects.get(notify_type=3),
                recipient=message.from_user,
                book=message.user_book_id
            )
            notification.save()

        # Display a success message
        messages.success(request, 'Borrow request approved successfully.')

        # Redirect to the chats page
        return redirect('chat', conversation_id=message.conversation.id)

    else:
        # If the request method is not POST, display an error message and redirect
        messages.error(request, 'Invalid request method.')
        return redirect('library')


@login_required_message
@transaction.atomic
def deny_borrow_request(request, book_id):
    """
    View function to deny a borrow request for a book.

    :param request: HttpRequest - The request object
    :param book_id: int - The ID of the book to deny the borrow request for
    """
    if request.method == 'POST':
        print("Book ID: ", book_id)
        # Get the message object based on the book ID and request type
        message = get_object_or_404(Message, user_book_id__id=book_id, request_type=2)

        # Create a pre-message to notify the recipient
        pre_message_content = f"Your borrow request for {message.user_book_id.book_id.book_title} has been denied."
        new_message = Message(
            from_user=message.to_user,
            to_user=message.from_user,
            details=pre_message_content,
            request_type=4,
            request_value='Request Denied',
            user_book_id=message.user_book_id,
            conversation=message.conversation,
        )
        new_message.save()

        # Update booking status to denied
        transaction = Transactions.objects.get(user_book_id=message.user_book_id)
        transaction.status = 'denied'
        transaction.save()

        # Add a notification for the owner
        notification = UserNotification(
            sender=message.to_user,
            message=Notification.objects.get(notify_type=4),
            recipient=message.from_user,
            book=message.user_book_id
        )
        notification.save()

        # Display a success message
        messages.success(request, 'Borrow request denied successfully.')

        # Redirect to the chas page
        return redirect('chat', conversation_id=message.conversation.id)

    else:
        # If the request method is not POST, display an error message and redirect
        messages.error(request, 'Invalid request method.')
        return redirect('library')


@login_required_message
def return_book(request, book_id):
    """
    View function to return a book.

    :param request: HttpRequest - The request object
    :param book_id: int - The ID of the book to return
    """
    if request.method == 'POST':
        print("Book ID: ", book_id)
        # Get the message object based on the book ID and request type
        message = get_object_or_404(Message, user_book_id__id=book_id, request_type=3)

        # Create a pre-message to notify the recipient
        pre_message_content = f"Your book {message.user_book_id.book_id.book_title} has been returned."
        new_message = Message(
            from_user=message.to_user,
            to_user=message.from_user,
            details=pre_message_content,
            request_type=5,
            request_value='Book Returned',
            user_book_id=message.user_book_id,
            conversation=message.conversation,
        )
        new_message.save()

        # Update UserBook values
        with transaction.atomic():
            user_book = message.user_book_id
            user_book.currently_with = message.from_user
            user_book.availability = True
            user_book.booked = "No"
            user_book.save()
            print('user_book updated successfully')

            # Update Booking values
            booking = Booking.objects.get(user_book_id=user_book)
            booking.returned = True
            booking.save()
            print('booking updated successfully')

            # Adds a notification for the owner
            notification = UserNotification(
                sender=message.to_user,
                message=Notification.objects.get(notify_type=5),
                recipient=message.from_user,
                book=message.user_book_id
            )
            notification.save()

        # Display a success message
        messages.success(request, 'Book returned successfully.')

        # Redirect to the chas page
        return redirect('chat', conversation_id=message.conversation.id)

    else:
        # If the request method is not POST, display an error message and redirect
        messages.error(request, 'Invalid request method.')
        return redirect('library')


@login_required_message
def request_return_book(request, book_id):
    """
    View function to request return a book.

    :param request: HttpRequest - The request object
    :param book_id: int - The ID of the book to return
    """
    if request.method == 'POST':
        print("Book ID: ", book_id)
        # Get the message object based on the book ID and request type
        message = get_object_or_404(Message, user_book_id__id=book_id, request_type=3)

        # Create a pre-message to notify the recipient
        pre_message_content = f" {message.from_user} has requested you to return {message.user_book_id.book_id.book_title}."
        new_message = Message(
            from_user=message.to_user,
            to_user=message.from_user,
            details=pre_message_content,
            request_type=8,
            request_value='Request Return',
            user_book_id=message.user_book_id,
            conversation=message.conversation,
        )
        new_message.save()

        # Update UserBook values
        with transaction.atomic():
            user_book = message.user_book_id
            user_book.currently_with = message.from_user
            user_book.availability = False
            user_book.booked = "Yes"
            user_book.save()
            print('user_book updated successfully')

            # Update Booking values
            booking = Booking.objects.get(user_book_id=user_book)
            booking.returned = False
            booking.save()
            print('booking updated successfully')

            # Adds a notification for the owner
            notification = UserNotification(
                sender=message.to_user,
                message=Notification.objects.get(notify_type=8),
                recipient=message.from_user,
                book=message.user_book_id
            )
            notification.save()

        # Display a success message
        messages.success(request, 'Book return request sent successfully.')

        # Redirect to the chats page
        return redirect('chat', conversation_id=message.conversation.id)

    else:
        # If the request method is not POST, display an error message and redirect
        messages.error(request, 'Invalid request method.')
        return redirect('library')


def redirect_notification(request, notification_id):
    """
    Marks notification as read and redirects the user to the appropriate page for the notification type.

    :param request: HttpRequest - The request object
    :param notification_id: int - The ID of the notification to redirect
    """
    notification = get_object_or_404(UserNotification, id=notification_id)
    notify_type = notification.message.notify_type
    # Mark the notification as read
    notification.read = True
    notification.save()

    # If message or review, find the conversation
    if notify_type in [1, 7]:
        # Find the matching conversation
        conversation = Conversation.objects.filter(
            (Q(id_1=notification.sender) & Q(id_2=notification.recipient)) |
            (Q(id_2=notification.sender) & Q(id_1=notification.recipient))
        ).first()
        # Redirect to the conversation page
        return redirect('chat', conversation_id=conversation.id)
    # If borrow request, accept, deny or return book, redirect to profile page
    elif notify_type in [2, 3, 4, 5]:
        return redirect('new_home')


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
            Q(from_user=our_profile, to_user=their_profile) | Q(
                from_user=their_profile, to_user=our_profile)
        ).select_related('from_user__user', 'to_user__user').order_by('created_on')

        for message in messages_list:
            message.is_from_our_user = (message.from_user == our_profile)

        conversations = Conversation.objects.filter(
            Q(id_1=our_profile) | Q(id_2=our_profile)
        ).exclude(
            Q(id_1=our_profile) & Q(id_2=our_profile)
        ).select_related('id_1__user', 'id_2__user')

        context = {'messages': messages_list, 'conversation': conversation, 'our_profile': our_profile,
                   'conversation_list': conversations}
        return render(request, 'chat.html', context)
    except UserProfile.DoesNotExist:
        return HttpResponse("User profile not found", status=404)


@login_required_message
def send_message(request, conversation_id):
    """
    This function handles the POST request to send a message from one user to another,
    ensuring the user is logged in.

    :param request: The Django HttpRequest object.
    :param conversation_id: The ID of the conversation between the two users.

    :return: HttpResponse: Redirects to the conversation page after the message is sent or error message if failed.
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
                return HttpResponseRedirect(reverse('full_conversation', args=[conversation_id]))
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
                request_value='Simple Message',
                created_on=now(),
                conversation=conversation
            )

            new_message.save()
            conversation.latest_message = message
            conversation.save()
            # Creates a notification for the recipient
            notification = UserNotification(
                recipient=their_profile,
                message=Notification.objects.get(notify_type=1),
                sender=our_profile,
            )
            notification.save()
            print(reverse('send_chat_message', args=[conversation_id]))
            return HttpResponseRedirect(reverse('chat', args=[conversation_id]))
        except UserProfile.DoesNotExist:
            messages.error(request, 'User profile not found.')
            return HttpResponseRedirect(reverse('chat', args=[conversation_id]))
    else:
        return HttpResponse("Invalid request method", status=405)

@login_required_message
def mark_all_as_read(request):
    """
    Marks all notifications as read for the user

    :param request: HttpRequest - The request object
    """
    if request.method == 'POST':
        user = request.user
        try:
            # Retrieve UserProfile object for the user
            user_profile = UserProfile.objects.get(user=user)
            # Get all notifications for the user
            notifications = UserNotification.objects.filter(recipient=user_profile)
            # Mark all notifications as read
            notifications.update(read=True)
            # Refresh the page to display the updated notifications
            return redirect(request.META.get('HTTP_REFERER', 'fallback_url'))
        except UserProfile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User profile does not exist'})

def new_conv(request):
    """
    View function to start a new conversation with another user, ensuring the user is logged in.

    Parameters:
    :param request: The Django HttpRequest object.
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
                messages.error(
                    request, 'You cannot start a conversation with yourself.')
                return redirect('new_conv')

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
                            request_value='Simple Message',
                            created_on=now(),
                            conversation=existing_conversation
                        )
                        new_message.save()
                        existing_conversation.latest_message = message
                        existing_conversation.save()
                    return redirect('chat', conversation_id=existing_conversation.id)

                # If the conversation does not exist, create a new conversation
                new_conversation_object = Conversation(
                    id_1=our_profile, id_2=their_profile)
                new_conversation_object.save()
                if message:
                    new_message = Message(
                        from_user=our_profile,
                        to_user=their_profile,
                        details=message,
                        request_type=1,
                        request_value='Simple Message',
                        created_on=now(),
                        conversation=new_conversation_object
                    )
                    new_message.save()

                    # Creates a notification for the recipient
                    notification = UserNotification(
                        recipient=their_profile,
                        message=Notification.objects.get(notify_type=1),
                        sender=our_profile,
                    )
                    notification.save()

                    new_conversation_object.latest_message = message
                    new_conversation_object.save()


                return redirect('chat', conversation_id=new_conversation_object.id)
        # If the user does not exist, display an error message
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('new_conv')

    # If the form has not been submitted, display the new conversation page
    else:
        return render(request, 'mainapp/new_conversation.html',
                      {'users': UserProfile.objects.exclude(user=request.user)})


