from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    url(r'^create/(?:no_order-(?P<no_order>\d+)/)$', views.order_create, name='order_create'),
    url(r'^order_form/$', views.order_form, name='order_form'),
    # url(r'^order_pelanggan/$', views.order_pelanggan, name='order_pelanggan'),
    # url(r'^rating/(?P<author>[-\w]+)/$', views.rating, name='rating'),
    path('rating/<id_produk>', views.rating, name='rating'),
    url(r'^upload_bukti/(?:no_order-(?P<no_order>\d+)/)$', views.upload_bukti, name='upload_bukti')
]