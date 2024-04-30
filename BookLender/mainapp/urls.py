from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('home/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout_view'),
    path('profile_page/', views.profile, name='profile'),
    path('update-profile/', views.updateProfile, name='update_profile'),
    path('add-book/', views.addBook, name='addBook'),
    path('library/', views.library, name='library'),
    path('search/', views.search, name='search'),
    path('borrow/<int:user_book_id>/', views.borrow, name='borrow'),
    path('remove-book/', views.removeBook, name='removeUserBook'),
    path('img_upload/', views.img_upload, name='img_upload'),
    path('lend/', views.lend, name='lend'),
    path('register/', views.register, name='register'),
    path('forgetpass/', views.forgetpass, name='forgetpass'),
    path('new_home/', views.new_home, name='new_home'),
    path('sample/', views.sample, name='sample'),
    path('chat/', views.chat, name='chat'),
    path('viewprofile/<int:profile_id>/', views.view_profile, name='viewprofile'),
    path('decrement_counter/', views.decrement_counter, name='decrement_counter'),
    # path('save_borrow_request/', views.save_borrow_request, name='save_borrow_request'),
    path('approve_borrow_request/<int:book_id>/', views.approve_borrow_request, name='approve_borrow_request'),
    path('deny_borrow_request/<int:book_id>/', views.deny_borrow_request, name='deny_borrow_request'),
    path('return_book/<int:book_id>/', views.return_book, name='return_book'),
    path('test/', views.test, name='test'),
]
