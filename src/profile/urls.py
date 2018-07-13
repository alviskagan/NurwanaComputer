from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('profile_pelanggan/', views.profile, name='profile_pelanggan'),
    path('edit_profile/', views.profile_create, name='edit_profile'),
    path('signup/', views.signup, name='signup'),
]