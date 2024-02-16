from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from .forms import BookForm
from .models import UserBooks, Book, User, UserProfile

# Create a test user
test_user = User.objects.first()
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


def profile(request):
    form = BookForm(request.POST or None)
    return render(request, 'profile_page.html', {'form': form})


def addBook(request):
    """Processes the request to add a new book"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            new_book = form.save()
            # Adds the book to the userBooks table
            addUserBook(request, new_book)

            return JsonResponse({'status': 'success', 'message': 'Book added successfully'})
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

def addUserBook(request, book):
    """Adds a book to the user's library based on the Book Form submitted"""
    new_user_book = UserBooks(
        user_id=test_user_profile,  # Set the current user as the user_id
        book_id=book,  # Set the newly created book as the book_id
        availability=True,  # Assuming you want to set the book as available by default
        booked='No'  # Or any default value that makes sense for your 'booked' field
    )

    # Save the new userBooks instance to the database
    new_user_book.save()



