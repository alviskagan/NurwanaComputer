import locale, sys
from django.shortcuts import render
from .models import Produk, Kategori,Rating

#modul CF
from django.db import connection
from scipy import sparse
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity
import math

#modul WN
from nltk.corpus import wordnet, wordnet_ic

from .algoritma import getPrediksi

#Information Content
semcor_ic_add1 = wordnet_ic.ic('ic-semcor-add1.dat') #IC paling mendekati, berdasarkan Wordnet 3.0

locale.setlocale(locale.LC_ALL, '')

# Create your views here.
def index(request):
    user_id = request.user.id
    print(user_id)
    # print(getSimilarity(user_id))
    if user_id != None:
        list_prediksi = getPrediksi(user_id)
    else:
        list_prediksi = None
    # print(user_id)
    print(list_prediksi)
    #select_related digunakan untuk memanggil foreign key
    all_produks		= Produk.objects.all().select_related('kategori_produk').order_by('kategori_produk')
    all_kategori 	= Kategori.objects.all()

    produk = {
        "user_id"           : user_id,
        "data_produk"		: all_produks,
        "kategori_produk"	: all_kategori,
        "data_prediksi"     : list_prediksi
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

def about(request):

    return render(request, 'produk/about.html')

def contact(request):

    return render(request, 'produk/contact.html')

def keranjang(request):

    return render(request, 'produk/keranjang.html')