from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_add, name='book_add'),
    path('books/<int:pk>/update/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('gallery/', views.gallery, name='gallery'),
    path('lend/', views.lend_books, name='lend_books'),
    path('borrow/', views.borrow_books, name='borrow_books'),
    path('login1/', views.CustomLoginView.as_view(), name='login1'),
    path('logout1/', auth_views.LogoutView.as_view(), name='logout1'),
    path('register1/', views.register, name='register1'),
]