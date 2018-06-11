from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('profile_pelanggan/', views.profile, name='profile_pelanggan'),
]