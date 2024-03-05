from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from lendborrowapp.views import addBook, removeBook
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('', views.index, name='index'),
    path('home/', views.index, name='index'),
    path('work/', views.work, name='work'),
    path('about/', views.about, name='about'),
    path('category/', views.category, name='category'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout_view'),
    path('profile_page/', views.profile, name='profile'),
    path('add-books/', addBook, name='addBook'),
    # path('remove-book/', removeBook, name='removeUserBook'),
    path('update-profile/', views.updateProfile, name='updateProfile'),
    path('register/', views.register, name='register'),
]
