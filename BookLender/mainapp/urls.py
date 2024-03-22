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
    path('add-book/', views.addBook, name='addBook'),
    path('library/', views.library, name='library'),
    path('search/', views.search, name='search'),
    path('borrow/<int:book_id>/', views.borrow, name='borrow'),
    path('remove-book/', views.removeBook, name='removeUserBook'),
    path('img_upload/', views.img_upload, name='img_upload'),
    path('lend/', views.lend, name='lend'),
    path('register/', views.register, name='register'),
    path('forgetpass/', views.forgetpass, name='forgetpass'),
    path('new_home/', views.new_home, name='new_home'),
    path('chat/', views.chat, name='chat'),
    #path('users_profiles/', views.profiles, name='profiles'),
]
