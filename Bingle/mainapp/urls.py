from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('home/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('new_about/', views.new_about, name='new_about'),
    path('new_landing_page/', views.new_landing_page, name='new_landing_page'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout_view'),
    path('profile_page/', views.profile, name='profile'),
    path('update-profile/', views.updateProfile, name='update_profile'),
    path('add-book/', views.addBook, name='addBook'),
    path('library/', views.library, name='library'),
    path('search/', views.search, name='search'),
    path('sample_search/', views.sample_search, name='sample_search'),
    path('borrow/<int:user_book_id>/', views.borrow, name='borrow'),
    path('remove-book/', views.removeBook, name='removeUserBook'),
    path('img_upload/', views.img_upload, name='img_upload'),
    path('lend/', views.lend, name='lend'),
    path('register/', views.register, name='register'),
    path('forgetpass/', views.forgetpass, name='forgetpass'),
    path('new_home/', views.new_home, name='new_home'),
    path('new_profile/', views.new_profile, name='new_profile'),
    path('chat/', views.chat, name='chat'),
    path('chat/<int:conversation_id>/', views.load_full_conversation, name='full_conversation'),
    path('chat/<int:conversation_id>/send_message/', views.send_message, name='send_chat_message'),
    path('viewprofile/<int:profile_id>/', views.view_profile, name='viewprofile'),
    path('decrement_counter/', views.decrement_counter, name='decrement_counter'),
    # path('save_borrow_request/', views.save_borrow_request, name='save_borrow_request'),
    path('approve_borrow_request/<int:book_id>/', views.approve_borrow_request, name='approve_borrow_request'),
    path('deny_borrow_request/<int:book_id>/', views.deny_borrow_request, name='deny_borrow_request'),
    path('return_book/<int:book_id>/', views.return_book, name='return_book'),
    path('test/', views.test, name='test'),
    path('redirect_notification/<int:notification_id>', views.redirect_notification, name='redirect_notification'),
]
