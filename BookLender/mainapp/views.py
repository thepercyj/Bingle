from django.template.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from .forms import BookForm, UserRegisterForm
from .models import UserBook, User, UserProfile
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

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


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            form.save_profile()
            return redirect('login_view')  # Redirect to login page or wherever you'd like
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
    token = {'form': form}
    # No need to manually add the CSRF token in Django templates, {% csrf_token %} does this
    return render(request, 'login.html', token)


@never_cache
def profile(request):
    form = BookForm(request.POST or None)
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    user_books = UserBook.objects.filter(owner_book_id=user_profile)
    books_count = user_books.count()  # Count the number of books
    context = {'form': form, 'user_books': user_books, 'user_profile': user_profile, 'user': user,
               'user_book_count': books_count}
    return render(request, 'profile_page.html', context)


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
        return redirect('/main/profile_page')
    else:
        # Handle non-POST request
        return render(request, 'profile_page.html')
