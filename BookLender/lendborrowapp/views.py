from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Book, BookForm, BookRequestForm, User


def portal(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        # Check if the user already exists in the database
        user, created = User.objects.get_or_create(name=user_name)
        request.session['user_name'] = user_name  # Store username in session
        print("Username stored in session:", request.session['user_name'])  # Debugging
        return redirect('add_book')
    return render(request, 'lendborrowapp/portal.html')


def add_book(request):
    user_name = request.session.get('user_name')
    try:
        user_instance = User.objects.get(name=user_name)
    except User.DoesNotExist:
        # Handle the case when the user does not exist
        # You can redirect the user to an error page or take appropriate action
        return redirect('error_page')

    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        Book.objects.create(title=title, author=author, owner=user_instance)
        return redirect('book_list')
    return render(request, 'lendborrowapp/add_book.html', {'user_name': user_instance.name})


def book_list(request):
    # Retrieve the username from the session
    user_name = request.session.get('user_name')
    try:
        # Fetch the User instance based on the username
        user_instance = User.objects.get(name=user_name)
        # Filter books by the fetched User instance
        books = Book.objects.filter(owner=user_instance)
    except User.DoesNotExist:
        # Handle the case where the user does not exist
        # You can redirect the user to an error page or take appropriate action
        return render(request, 'error.html', {'error_message': 'User does not exist'})
    return render(request, 'lendborrowapp/book_list.html', {'books': books})


def book_requests(request):
    if request.method == 'POST':
        form = BookRequestForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.session.get('user_name')
            book.save()
            messages.success(request, 'Book request sent successfully!')
            return redirect('book_requests')
    else:
        form = BookRequestForm()
    requests = Book.objects.exclude(borrower=None)
    return render(request, 'lendborrowapp/book_requests.html', {'form': form, 'requests': requests})


def approve_request(request, book_id):
    book = Book.objects.get(pk=book_id)
    book.borrower = book.owner
    book.owner = request.session.get('user_name')
    book.save()
    messages.success(request, f'Book "{book.title}" approved for lending!')
    return redirect('book_requests')


def borrow_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if book.borrower:
        messages.error(request, 'This book is already borrowed by someone else.')
    else:
        user_id = request.session.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        book.borrower = user
        book.save()
        messages.success(request, f'You borrowed "{book.title}" successfully!')
    return redirect('book_list')


def lend_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if book.owner != request.session.get('user_id'):
        messages.error(request, 'You do not own this book.')
    elif book.borrower:
        messages.error(request, 'This book is already lent out.')
    else:
        user_id = request.session.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        book.borrower = user
        book.save()
        messages.success(request, f'You lent "{book.title}" successfully!')
    return redirect('book_list')