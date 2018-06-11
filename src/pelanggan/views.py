from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def profile(request):
    user_id = request.user.id
    pelanggan = User.objects.filter(id__exact = user_id)
    print(user_id)
    print(pelanggan)
    profile = {
        "data_user" : pelanggan,
    }
    return render(request, 'pelanggan/profile.html', profile)