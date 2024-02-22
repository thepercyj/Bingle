from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('home/', views.index, name='index'),
    path('work/', views.work, name='work'),
    path('about/', views.about, name='about'),
    path('category/', views.category, name='category'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('add-book/', views.addBook, name='addBook'),
    path('remove-book/', views.removeBook, name='removeUserBook'),
    path('update-profile/', views.updateProfile, name='updateProfile'),

]