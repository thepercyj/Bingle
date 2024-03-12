from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
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
    path('add-book/', views.addBook, name='addBook'),
    # path('list-book/', views.listBook, name='listBook'),
    path('remove-book/', views.removeBook, name='removeUserBook'),
    path('update-profile/', views.updateProfile, name='updateProfile'),
    path('borrow/', views.borrow, name='borrow'),
    path('lend/', views.lend, name='lend'),
    path('register/', views.register, name='register'),
    path('forgetpass/', views.forgetpass, name='forgetpass'),
    path('new_home/',views.new_home, name='new_home'),
    # path('upload-profile/', views.upload_profile_picture, name='upload_profile_picture'),
]
