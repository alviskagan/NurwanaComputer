from django import forms
from django.contrib.auth.models import User
from .models import Pelanggan
from django.utils.translation import ugettext_lazy as _


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Pelanggan
        fields = ['address', 'phone_number', 'postal_code']
    

    # address = forms.CharField()
    # phone_number = forms.CharField()
    # bio = forms.CharField()
    # postal_code = forms.CharField()
    # birth_date = forms.DateField()
    # profile_pic = forms.FileField()