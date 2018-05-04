import locale
from django.shortcuts import render
from .models import Produk, Kategori

locale.setlocale(locale.LC_ALL, '')

# Create your views here.
def index(request):
	#select_related digunakan untuk memanggil foreign key
	all_produks		= Produk.objects.all().select_related('kategori_produk').order_by('kategori_produk')
	all_kategori 	= Kategori.objects.all()

	produk = {
    	"data_produk"		: all_produks,
    	"kategori_produk"	: all_kategori
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
