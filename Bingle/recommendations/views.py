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
    """
    View for the recommendations page.

    :param request: HttpRequest
    """
    # Any necessary logic can be added here
    recs = getborrowed(request)
    return render(request, 'recommendations/recommendations.html', {'recs': recs})

def generate_rec(request):
    """
    View for generating recommendations.

    :param request: HttpRequest
    """
    getborrowed_response = getborrowed(request)
    return getborrowed_response


def getborrowed(request):
    """
    View for getting borrowed books.

    :param request: HttpRequest
    """
      
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
    #create a dictionary of recommended_books
    recommended_books_dict = {}
    for book in recommended_books:
        recommended_books_dict[book.book_title] = book.book_author
    print(recommended_books_dict)
    return recommended_books
 
    

    
def login_required_message(function):
    """
    Custom decorator to ensure that the user is logged in before accessing a page.

    :param function: Function
    """

    def wrapper(request, *args, **kwargs):
        """
        Wrapper function for the decorator.

        This function checks if the user is logged in. If the user is not logged in, an error message is displayed.

        Parameters:
        -----------
        :param request: HttpRequest
            The request object.
        :param *args
            Variable length argument list.
        :param **kwargs
            Arbitrary keyword arguments.
        """
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to view this page.")
            return login_required(function)(request, *args, **kwargs)
        return function(request, *args, **kwargs)

    return wrapper

