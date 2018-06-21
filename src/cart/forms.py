from django import forms
from produk.models import Produk
from django.db import connection

import pandas as pd



def stok(product_id):
    df = pd.read_sql_query('SELECT  stok_produk FROM produk_produk where id_produk = '+ product_id +'', connection)
    print(df)
    for line in df.itertuples():
        maks = line[1]
    # hasil = Produk.stok_produk(id_produk = product_id)
    # print(hasil)
    hasil = [(i, str(i)) for i in range(1, maks)]
    return hasil
    
PRODUCT_QUANTITY_CHOICES =  [(i, str(i)) for i in range(1, 26+1)]

class CartAddProductForm(forms.Form):
       
    # def stok(instance):
    #     df = pd.read_sql_query('SELECT  stok_produk FROM produk_produk where id_produk = '+ instance.id_produk +'', connection)
    #     print(df)
    #     for line in df.itertuples():
    #         maks = line[1]
    #     # hasil = Produk.stok_produk(id_produk = product_id)
    #     # print(hasil)
    #     hasil = [(i, str(i)) for i in range(1, maks)]
    #     return hasil

    
    # quantity = forms.TypedChoiceField(choices=stok, coerce=int)
    
    PRODUCT_QUANTITY_CHOICES =  [(i, str(i)) for i in range(1, 26+1)]     
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
