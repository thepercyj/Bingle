from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import Book, BookForm, BorrowRequest, Notification


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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or login page
            return redirect('login1')
    else:
        form = UserCreationForm()
    return render(request, 'lendborrowapp/register1.html', {'form': form})


@login_required
def book_list(request):
    books = Book.objects.filter(owner=request.user)
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
