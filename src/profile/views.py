import locale
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Pelanggan
from .forms import ProfileCreateForm
from django.contrib import messages
locale.setlocale(locale.LC_ALL, '')

# Create your views here.

def profile(request):
    user_id = request.user
    pelanggan = Pelanggan.objects.filter(user__exact = user_id)
    form = ProfileCreateForm()
    profile = {
        "data_user" : pelanggan,
        "form"      : form
    }

    return render(request, 'profile/profil.html', profile)



def profile_create(request):
    user_id     = request.user.id
    # user     = request.user.username
    pelanggan = Pelanggan.objects.filter(user__exact = request.user)
    profile = {
        "data_user" : pelanggan,
    }

    if request.method == 'POST':
        form = ProfileCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd['address'], "address")
            print("aaa")
            Pelanggan.objects.create(
                user = request.user,
                address = cd['address'] ,
                phone_number = cd['phone_number'] ,
                bio = cd['bio'],
                birth_date = cd['birth_date'],
                profile_pic = cd['profile_pic'] 
            )
            return render(request, 'profile/profil.html', profile)
        else:
            messages.warning(request, 'Data yang anda isikan kurang tepat.')                
            form = ProfileCreateForm()
            return render(request, 'profile/edit_profile.html', {'form': form})
    else:
        form = ProfileCreateForm()
        return render(request, 'profile/edit_profile.html', {'form': form})