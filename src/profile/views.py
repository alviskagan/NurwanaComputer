import locale
from django.shortcuts import render

locale.setlocale(locale.LC_ALL, '')

# Create your views here.
def index(request):

    return render(request, 'profile/profil.html')