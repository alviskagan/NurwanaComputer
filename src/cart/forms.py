from django import forms
from produk.models import Produk


class CartAddProductForm(forms.Form):
    PRODUCT_QUANTITY_CHOICES =  [(i, str(i)) for i in range(1, 100+1)]

    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)

    # quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size':'2','type':'number', 'value':'1', 'class':'quantity', 'maxlength':'5'}), 
    # error_messages={'invalid':'Please enter a valid quantity.'}, min_value=1)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    # def stok(instance):
    #     df = pd.read_sql_query('SELECT  stok_produk FROM produk_produk where id_produk = '+ instance.id_produk +'', connection)
    #     print(df)
    #     for line in df.itertuples():
    #         maks = line[1]
    #     # hasil = Produk.stok_produk(id_produk = product_id)
    #     # print(hasil)
    #     hasil = [(i, str(i)) for i in range(1, maks)]
    #     return hasil

    
    
    