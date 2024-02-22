from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Book, BookForm, BorrowRequest, Notification, UserProfile


class CustomLoginView(LoginView):
    template_name = 'lendborrowapp/login1.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')


def dashboard(request):
    username = request.user.username
    return render(request, 'lendborrowapp/dashboard.html', {'username': username})


def base(request):
    return render(request, 'lendborrowapp/base.html')


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)  # Assuming you have a UserProfileForm

        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()  # Save the User instance
            user_profile = user_profile_form.save(commit=False)  # Create a UserProfile instance but don't save it yet
            user_profile.user = user  # Associate the UserProfile with the User instance
            user_profile.save()  # Save the UserProfile instance

            # Redirect to a success page or login page
            return redirect('login1')
    else:
        user_form = UserCreationForm()
        user_profile_form = UserProfileForm()  # Assuming you have a UserProfileForm

    return render(request, 'lendborrowapp/register1.html', {'user_form': user_form, 'user_profile_form': user_profile_form})


@login_required
def book_list(request):
    user_profile = request.user.userprofile
    books = Book.objects.filter(owner=user_profile)
    return render(request, 'lendborrowapp/gallery.html', {'books': books})


@login_required
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            messages.success(request, 'Book added successfully.')
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'lendborrowapp/book_form.html', {'form': form})


@login_required
def book_update(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully.')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'lendborrowapp/book_form.html', {'form': form})


@login_required
def book_delete(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully.')
        return redirect('book_list')
    return render(request, 'lendborrowapp/book_confirm_delete.html', {'book': book})


@login_required
def gallery(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    else:
        books = Book.objects.all()
    return render(request, 'lendborrowapp/gallery.html', {'books': books})


@login_required
def lend_books(request):
    user_books = Book.objects.filter(owner=request.user)
    return render(request, 'lendborrowapp/lend_books.html', {'user_books': user_books})


@login_required
def borrow_books(request):
    books = Book.objects.exclude(owner=request.user)
    return render(request, 'lendborrowapp/gallery.html', {'books': books})


@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user)
    return render(request, 'lendborrowapp/notifications.html', {'notifications': user_notifications})
