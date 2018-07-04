from django import forms
from django.contrib.auth.models import User
from .models import Pelanggan
from django.utils.translation import ugettext_lazy as _


class ProfileCreateForm(forms.Form):
    address = forms.CharField()
    phone_number = forms.CharField()
    bio = forms.CharField()
    birth_date = forms.DateField()
    # profile_pic = forms.FileField()