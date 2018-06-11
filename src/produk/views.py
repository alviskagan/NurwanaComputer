import locale, sys
from django.shortcuts import render
from .models import Produk, Kategori,Rating
from .algoritma import getPrediksi

locale.setlocale(locale.LC_ALL, '')

# Create your views here.
def index(request):
    user_id = request.user.id
    # print(user_id)
    # print(getSimilarity(user_id))
    daftar_prediksi = []
    nilai_prediksi = []
    
    if user_id != None and user_id > 1:
        list_prediksi = getPrediksi(user_id)
        for id_produk in list_prediksi:
            # print(id_produk[1])
            produk = id_produk[1]
            nilai_prediksi = id_produk[0]
            daftar_prediksi += Produk.objects.all().filter(id_produk__exact = produk).select_related('kategori_produk')  
        
    else:
        list_prediksi = None
    # print(user_id)
    print(daftar_prediksi)
    
    #select_related digunakan untuk memanggil foreign key
    all_produks		= Produk.objects.all().select_related('kategori_produk').order_by('kategori_produk')
    # print(all_produks)
    # print(daftar_prediksi)
    all_kategori 	= Kategori.objects.all()

    produk = {
        "user_id"           : user_id,
        "data_produk"		: all_produks,
        "kategori_produk"	: all_kategori,
        "data_prediksi"     : list_prediksi,
        "prediksi"          : daftar_prediksi
    }

    return render(request, 'index.html',produk)

def detail_produk(request, id):

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

    return render(request, 'produk/detail_produk.html', produk)

def beli_produk(request, id):

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