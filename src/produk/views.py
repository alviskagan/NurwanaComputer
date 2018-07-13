import locale, sys
from django.shortcuts import render, get_object_or_404
from .models import Produk, Kategori,Rating
from .algoritma import getPrediksi
from cart.forms import CartAddProductForm
from django.contrib.auth.models import User
from profile.models import Pelanggan

locale.setlocale(locale.LC_ALL, '')
# Create your views here.

def index(request):
    user_id = request.user.id
    daftar_prediksi = []
    nilai_prediksi = []
    temp_kategori = None
    count = 0
    if user_id != None and user_id > 1:
        list_prediksi = getPrediksi(user_id)
        for id_produk in list_prediksi:
            produk = id_produk[1]
            nilai_prediksi = id_produk[0]
            produk_kategori = Produk.objects.get(id_produk__exact = produk).kategori_produk
            stok = Produk.objects.get(id_produk__exact = produk).stok_produk
            if temp_kategori != produk_kategori and count < 5 and stok > 0:
                daftar_prediksi += Produk.objects.all().filter(id_produk__exact = produk).select_related('kategori_produk')  
                temp_kategori = produk_kategori
                count += 1
    else:
        list_prediksi = None
    #select_related digunakan untuk memanggil foreign key
    all_produks		= Produk.objects.all().select_related('kategori_produk').order_by('id_produk').filter(stok_produk__gt = 0)
    all_kategori 	= Kategori.objects.all()
    data_user       = Pelanggan.objects.all().filter(id__exact = user_id)
    produk = {
        "user_id"           : user_id,
        "data_produk"		: all_produks,
        "kategori_produk"	: all_kategori,
        "data_prediksi"     : list_prediksi,
        "data_user"         : data_user,
        "prediksi"          : daftar_prediksi
    }
    return render(request, 'index.html',produk)

def detail_produk(request, id):
    user_id = request.user.id
    all_produks = Produk.objects.filter(id_produk__exact = id ).select_related('kategori_produk')
    stok = Produk.objects.get(id_produk__exact = id).stok_produk
    all_kategori = Kategori.objects.all()
    cart_product_form = CartAddProductForm()   
    daftar_prediksi = []
    nilai_prediksi = []
    temp_kategori = None
    count = 0
    if user_id != None and user_id > 1:
        list_prediksi = getPrediksi(user_id)
        for id_produk in list_prediksi:
            produk = id_produk[1]
            nilai_prediksi = id_produk[0]
            produk_kategori = Produk.objects.get(id_produk__exact = produk).kategori_produk
            stok = Produk.objects.get(id_produk__exact = produk).stok_produk
            if temp_kategori != produk_kategori and count < 5 and stok > 0:
                daftar_prediksi += Produk.objects.all().filter(id_produk__exact = produk).select_related('kategori_produk')  
                temp_kategori = produk_kategori
                count += 1
    else:
        list_prediksi = None
    print(daftar_prediksi)
    produk = {
        "user_id"           : user_id,
        "data_produk"       : all_produks,
        'cart_product_form' : cart_product_form,
        "kategori_produk"   : all_kategori,
        "prediksi"          : daftar_prediksi,
        "data_prediksi"     : list_prediksi,
    }
    return render(request, 'produk/detail_produk.html', produk)

def kategori_produk(request, id):
    user_id = request.user.id
    daftar_prediksi = []
    nilai_prediksi = []
    temp_kategori = None
    count = 0
    if user_id != None and user_id > 1:
        list_prediksi = getPrediksi(user_id)
        for id_produk in list_prediksi:
            produk = id_produk[1]
            nilai_prediksi = id_produk[0]
            produk_kategori = Produk.objects.get(id_produk__exact = produk).kategori_produk
            stok = Produk.objects.get(id_produk__exact = produk).stok_produk
            if temp_kategori != produk_kategori and count < 5 and stok > 0:
                daftar_prediksi += Produk.objects.all().filter(id_produk__exact = produk).select_related('kategori_produk')  
                temp_kategori = produk_kategori
                count += 1

    else:
        list_prediksi = None
    
    #select_related digunakan untuk memanggil foreign key
    all_produks		= Produk.objects.all().select_related('kategori_produk').order_by('kategori_produk').filter(stok_produk__gt = 0).filter(kategori_produk__exact = id)
    all_kategori 	= Kategori.objects.all()

    produk = {
        "user_id"           : user_id,
        "data_produk"		: all_produks,
        "kategori_produk"	: all_kategori,
        "data_prediksi"     : list_prediksi,
        "prediksi"          : daftar_prediksi
    }

    return render(request, 'produk/kategori_produk.html',produk)


def beli_produk(request, id):


    all_produks = Produk.objects.filter(id_produk__exact = id ).select_related('kategori_produk')
    all_kategori = Kategori.objects.all()
    produk = {
        "data_produk": all_produks,
        "kategori_produk": all_kategori
    }

    return render(request, 'produk/beli_produk.html', produk)

def invoice(request, id):

    #pashing data dari views index
    # if request.method == 'GET':
    # # blom fix
    # data_produk = request.GET.get("id_produk", "")
    all_produks = Produk.objects.filter(id_produk__exact = id ).select_related('kategori_produk')
    all_kategori = Kategori.objects.all()
    print(all_produks)
    print(id)
    # print(Kategori.objects.filter(id_kategori = 1))
    produk = {
        "data_produk": all_produks,
        "kategori_produk": all_kategori
    }

    return render(request, 'produk/invoice.html', produk)

def about(request):

    return render(request, 'produk/about.html')

def contact(request):

    return render(request, 'produk/contact.html')

def keranjang(request):

    return render(request, 'produk/keranjang.html')
		
def profil(request):

    return render(request, 'produk/profil.html')

def pembelian(request):

    return render(request, 'produk/pembelian.html')