from django import forms
from .models import Order
from produk.models import Rating
import os


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code']
    

    
    
class UploadBuktiTransfer(forms.Form):
    image = forms.FileField(label='Upload Bukti Transfer ')

class RatingForm(forms.Form):
    rating_choice =  [(i, str(i)) for i in range(1, 5+1)]
    rating = forms.TypedChoiceField(choices=rating_choice, coerce=int)
