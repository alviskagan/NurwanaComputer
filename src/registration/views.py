from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms  import UserCreationForm
import locale
from django.contrib.auth.models import User

# Create your views here.

locale.setlocale(locale.LC_ALL, '')

# Create your views here.
@login_required
def home(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return redirect('registration/login.html')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
