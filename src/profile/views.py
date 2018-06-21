import locale
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
locale.setlocale(locale.LC_ALL, '')

# Create your views here.

def profile(request):
    user_id = request.user.id
    pelanggan = User.objects.filter(id__exact = user_id)
    profile = {
        "data_user" : pelanggan,
    }

    return render(request, 'profile/profil.html', profile)