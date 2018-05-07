from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('detail_produk/<id>', views.detail_produk, name="detail_produk"),

]