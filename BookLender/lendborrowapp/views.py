from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .forms import BookForm
from mainapp.models import UserProfile, UserBook


def addBook(request):
    """Processes the request to add a new book"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            new_book = form.save()
            # Adds the book to the userBooks table
            addUserBook(request, new_book)
            return redirect('/main/profile_page')
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


@never_cache
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
