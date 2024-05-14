from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy


class CustomLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('new_landing_page')


urlpatterns = [
    path('new_about/', views.new_about, name='new_about'),
    path('', views.new_landing_page, name='new_landing_page'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', CustomLogoutView.as_view(), name='logout_view'),
    path('update-profile/', views.updateProfile, name='update_profile'),
    path('add-book/', views.addBook, name='addBook'),
    path('search/', views.search, name='search'),
    path('borrow/<int:user_book_id>/', views.borrow, name='borrow'),
    path('remove-book/', views.removeBook, name='removeUserBook'),
    path('img_upload/', views.img_upload, name='img_upload'),
    path('register/', views.register, name='register'),
    path('new_home/', views.new_home, name='new_home'),
    path('new_profile/', views.new_profile, name='new_profile'),
    path('chat/', views.chat, name='chat'),
    path('chat/<int:conversation_id>/', views.load_full_conversation, name='full_conversation'),
    path('chat/<int:conversation_id>/send_message/', views.send_message, name='send_chat_message'),
    path('chat/<int:conversation_id>/rate_user/', views.rate_user, name='rate_user'),
    path('viewprofile/<int:profile_id>/', views.view_profile, name='viewprofile'),
    path('decrement_counter/', views.decrement_counter, name='decrement_counter'),
    path('approve_borrow_request/<int:book_id>/', views.approve_borrow_request, name='approve_borrow_request'),
    path('deny_borrow_request/<int:book_id>/', views.deny_borrow_request, name='deny_borrow_request'),
    path('return_book/<int:book_id>/', views.return_book, name='return_book'),
    path('request_return_book/<int:book_id>/', views.request_return_book, name='request_return_book'),
    path('redirect_notification/<int:notification_id>', views.redirect_notification, name='redirect_notification'),
    path('mark_all_as_read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('new_conv/', views.new_conv, name='new_conv'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
