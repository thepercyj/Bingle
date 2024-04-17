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
    response = 19
    print(response)
    return HttpResponse(str(response))  # Return response as HTTP response



