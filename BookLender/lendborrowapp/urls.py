from django.urls import path
from . import views

urlpatterns = [
    path('portal/', views.portal, name='portal'),
    path('add_book/', views.add_book, name='add_book'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('lend/<int:book_id>/', views.lend_book, name='lend_book'),
    path('book_list/', views.book_list, name='book_list'),
    path('book_requests/', views.book_requests, name='book_requests'),
    path('approve_request/<int:book_id>/', views.approve_request, name='approve_request'),
]