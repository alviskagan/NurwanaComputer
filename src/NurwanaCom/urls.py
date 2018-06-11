"""NurwanaCom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

#static settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from django.contrib.admin import sites
from django.contrib.auth import views as auth_views
from produk.views import index, detail_produk
from profile.views import index
# from pelanggan.views import profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("produk.urls")),
    path('accounts/', include('allauth.urls')),
    # path('profile/',include("pelanggan.urls")),
    path('admin/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name="logout"),
    path('profile/', include("profile.urls")),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),             
    ]
