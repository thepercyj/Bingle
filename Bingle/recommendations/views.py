# recommendations/views.py
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

    print(borrowed_books)
    return JsonResponse({'borrowed_books': borrowed_books, 'our_profile_id': our_profile.id})
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

