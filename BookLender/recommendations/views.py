# recommendations/views.py
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect
from mainapp.models import User, UserProfile, Message, Book
from django.contrib import messages
from mainapp.models import Conversation
from django.http import JsonResponse
from django.shortcuts import render



def recommendations_view(request):
    # Any necessary logic can be added here
    return render(request, 'recommendations/recommendations.html')

def generate_rec(request):
    getborrowed_response = getborrowed(request)
    return getborrowed_response


def getborrowed(request):
      
    our_profile = UserProfile.objects.get(user=request.user)
    borrow_messages = Message.objects.filter(Q(request_value ="Borrow Request") &
        Q(from_user_id=our_profile) | Q(to_user_id=our_profile)
    ).exclude(
        Q(from_user_id=our_profile) & Q(to_user_id=our_profile)
    ).select_related('id_1__user', 'id_2__user')

    borrowed_books = list(borrow_messages.values_list('user_book_id', flat=True))
    borrowed_books = list(filter(None, borrowed_books))


    
    genres = []

    # Iterate over the borrowed_books list
    for book_id in borrowed_books:
        # Retrieve the book object from the Book table
        book = Book.objects.get(pk=book_id)
        # Append the genre of the book to the genres list
        genres.append(book.genre)

    # create variable to store the most common genre
    most_common_genre = None
    # create variable to store the count of the most common genre
    most_common_genre_count = 0
    # iterate over the genres list
    for genre in genres:
        # count the number of times the genre appears in the list
        genre_count = genres.count(genre)
        # if the genre appears more times than the current most common genre
        if genre_count > most_common_genre_count:
            # update the most common genre and the count of the most common genre
            most_common_genre = genre
            most_common_genre_count = genre_count

    # create a list to store the recommended books
    recommended_books = []
    # iterate over the books in the Book table
    for book in Book.objects.all():
        # if the book's genre is the most common genre

        if len(recommended_books) == 5:
            break
        if book.genre == most_common_genre:
            # add the book to the recommended books list
            recommended_books.append(book)
    
    print(recommended_books)

    print(borrowed_books)
    print(genres)
    return JsonResponse({'borrowed_books': borrowed_books, 'our_profile_id': our_profile.id, 'recommended_books': recommended_books})
    #return JsonResponse({'message': list(borrow_messages.values()), 'our_profile_id': our_profile.id})
    #response = 19
    #print(response)
    #return HttpResponse(str(response1))  # Return response as HTTP response

    
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

