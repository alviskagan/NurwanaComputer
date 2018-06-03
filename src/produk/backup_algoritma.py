from nltk.corpus import wordnet, wordnet_ic
from sklearn import cross_validation as cv
from sklearn.metrics import mean_squared_error
from math import sqrt
import locale
import sys


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

#Information Content
semcor_ic_add1 = wordnet_ic.ic('ic-semcor-add1.dat') #IC paling mendekati, berdasarkan Wordnet 3.0


### Testing ###

cur = connection.cursor()

df = pd.read_sql_query('SELECT  id_produk_id, id_pelanggan_id, is_rating FROM produk_rating order by id_produk_id ', connection)

# print(df)
# for row in cur.execute('SELECT  id_produk_id, id_pelanggan_id, is_rating FROM produk_rating order by id_produk_id'):
#     print(row)
    
prd = pd.read_sql_query('SELECT id_produk FROM produk_produk', connection)
# print(prd)

n_users = df.id_pelanggan_id.unique().shape[0]
# n_items = df.id_produk_id.unique().shape[0]
n_items = prd.id_produk.unique().shape[0]
# print('Number of users = ' + str(n_users) + ' | Number of Products = ' + str(n_items))

### Uji Coba ###

def getRatingUser(id, item):
    query = pd.read_sql_query('SELECT  is_rating FROM produk_rating WHERE id_pelanggan_id = ' + str(id) + ' AND id_produk_id = ' +str(item) + '', connection)
    for line in query.itertuples():
        return line[1]
    # print(query)

def rataRatingUser(id):
    query = pd.read_sql_query('SELECT  AVG(is_rating) FROM produk_rating WHERE id_pelanggan_id = ' + str(id) + '', connection)
    for line in query.itertuples():
        if line[1] != None:
            return line[1]
        else :
            return 0

def rataRatingProduk(id):
    query = pd.read_sql_query('SELECT  AVG(is_rating) FROM produk_rating WHERE id_produk_id = ' + str(id) + '', connection)
    for line in query.itertuples():
        if line[1] != None:
            return line[1]
        else :
            return 0

def getSimilarity(item_1, item_2):
    query = pd.read_sql_query('SELECT  a.id_pelanggan_id FROM produk_rating a, produk_rating b WHERE a.id_produk_id = ' +str(item_1) +' AND b.id_produk_id = ' + str(item_2) +' AND a.id_pelanggan_id = b.id_pelanggan_id', connection)
    Atas = Bawah_i = Bawah_j = 0
    n_users = df.id_pelanggan_id.shape[0]
    # print(n_users)
    
    for line in query.itertuples():
        # print(line[1])
        rui = getRatingUser(line[1], item_1)
        ruj = getRatingUser(line[1], item_2)
        ru  = rataRatingUser(line[1])
        # print(rui, ruj, ru)
        atas = (rui-ru) * (ruj-ru)
        bawah_i = pow((rui-ru),2)
        bawah_j = pow((ruj-ru),2)
        # print(atas, bawah_i, bawah_j)
        Atas = Atas + atas
        Bawah_i = Bawah_i + bawah_i
        Bawah_j = Bawah_j + bawah_j
    # print(Atas, Bawah_i, Bawah_j)
    Bawah = (math.sqrt(Bawah_i)* math.sqrt(Bawah_j))
    if Bawah == 0:
        Bawah = 1
    hasil = Atas/Bawah
    return hasil  
    # while( n_users)
        
    # print(df)

# print(getSimilarity(1,21))

    

### end uji coba ###



### block algoritma jiang-conrath calculation ###

def list_corpus(param, status_data = 0):
    temp = []
    data = wordnet.synsets(param, pos=wordnet.NOUN) #hanya synset yang berupa kata benda saja yang dipilih
    if len(data) != 0:  #pengecekan apakah inputan memiliki synset atau tidak
        for kata in range(len(data)):
            if param == 'monitor':
                if kata == 3:
                    temp += [data[kata]]
            if param == 'mouse':
                if kata == 3:
                    temp += [data[kata]]
            if param == 'printer':
                if kata == 2:
                    temp += [data[kata]]
            if param == 'router':
                if kata == 2:
                    temp += [data[kata]]
            if param == 'charger':
                if kata == 1:
                    temp += [data[kata]]
            if param == 'speaker':
                if kata == 1:
                    temp += [data[kata]]
            if param == 'cable':
                if kata == 1:
                    temp += [data[kata]]            
            else:
                if kata == 0:
                    temp += [data[kata]]

        return temp[-1]
    else:
        print("Inputan tidak memiliki synset")
        sys.exit() #validasi jika inputan tidak memiliki synset maka proses akan langsung dihentikan


def jcn_result(a):
    
    temp_a = []
    temp_b = []
   
    # data_a sebagai kategori dari produk yang sudah dibeli dan diberi rating
    # data_a selanjutnya akan dibandingkan dengan kategori lain 
    # untuk mendapatkah nilai dari similaritas Jiang-Conrath
    data_a = list_corpus(a, 1)
    
    
    # for yang pertama berisi baris dari nama-nama kategori yang terdapat di dalam sistem
    for line in kategori.itertuples():
        # for yang kedua berfungsi untuk mencari synset dari setiap nama kategori
        # berfungsi juga untuk menghitung similaritas Jiang-Conrtah berdasarkan produk yang sudah dibeli tadi
        for data_b in wordnet.synsets(line[1], pos = wordnet.NOUN):
            
            #perhitungan similaritas Jiang-Conrath
            sim = data_a.jcn_similarity(data_b, semcor_ic_add1)
            
            # validasi untuk mencari yang kategorinya berbeda, 
            # karena jika bernilai 1 maka kategori tersebut berarti sama     
            if sim < 1: 
                # temp_a += [[sim, data_a, data_b]]
                # temp_a += [[sim, a, line[1]]]
                temp_a += [sim]
                
                # print(data_a, data_b, sim)

        # temp_a berisi hasil perhitungan Jiang-Conrath antara data_a dengan synsets data_b
        # temp_a diurutkan berdasarkan nilai terbesar dari hasil perhitungan diatas    
        # temp_a.sort( key = lambda x: float(x[0]),  reverse = True) 
        hasli_a = max(temp_a)
        # print(line[1])
        # print(temp_a)
        # print(hasli_a)

        # temp_b berisi nilai JCN tertinggi dari synsets data_b
        temp_b += [[hasli_a, line[1]]]
        temp_a = []
        # print("hasil:", temp_b)

    print(len(temp_b), temp_b)
    temp_b.sort( key = lambda x: float(x[0]),  reverse = True)     
    hasil = temp_b[:5] 
    return hasil
### endblock ####

id_input = 1
### Jiang-Conrath ###
### Jiang-Conrtah V2 ###
def corpus_kategori(param):
    # kategori = pd.read_sql_query('select produk_produk.nama_produk, produk_kategori.nama_kategori from produk_kategori, produk_produk where produk_produk.id_produk = ' + str(param) + ' and produk_produk.kategori_produk_id = produk_kategori.id_kategori', connection)
    kategori = pd.read_sql_query('select produk_kategori.nama_kategori from produk_kategori, produk_produk where produk_produk.id_produk = ' + str(param) + ' and produk_produk.kategori_produk_id = produk_kategori.id_kategori', connection)
    for line in kategori.itertuples():
        nama_synset = list_corpus(line[1])    
    return nama_synset
# print(jcn_result('monitor', 'keyboard'))
# print(jcn_result('monitor'))

def nama_produk(param):
    nama = pd.read_sql_query('select produk_produk.nama_produk from produk_kategori, produk_produk where produk_produk.id_produk = ' + str(param) + ' and produk_produk.kategori_produk_id = produk_kategori.id_kategori', connection)
    for line in nama.itertuples():
        return line[1]

# print(nama_produk(2))

def jcn_2(a,b):
    # print(corpus_kategori(a))
    # print(corpus_kategori(b))
    data_a = corpus_kategori(a)
    data_b = corpus_kategori(b)
    # print(data_a, data_b)
    if data_a != data_b:
        result_jcn = data_a.jcn_similarity(data_b, semcor_ic_add1)
        return result_jcn
    else:
        return 1
    # cf_a = hasil_cf(a)
    # cf_b = hasil_cf(b)
    # return result_jcn, cf_a, cf_b
    return result_jcn
# print(jcn_2(1,14))

a = 0.25

def combine(array):
    hasil_combine = []
    for i in range(len(array)):
        # for j in range(len(temp[i])):
        cf  = array[i][1]
        jcn = array[i][0]
        nama_produk_a = nama_produk(array[i][2])
        nama_produk_b = nama_produk(array[i][3])
        # print(array[i][0])
        # print(array[i][1])
        
        hasil_combine += [[(a)*cf + (1-a)*jcn, nama_produk_a, nama_produk_b]]
    
    hasil_combine.sort( key = lambda x: float(x[0]),  reverse = True)      
    return hasil_combine


# print(combine(temp))

def combinedSim(item_1, item_2):
    a = 0.25
    cf = getSimilarity(item_1, item_2)
    jcn = jcn_2(item_1, item_2)
    # print(cf, jcn)
    result = a*cf + (1-a)*jcn
    return result

# print(combinedSim(1,14)) 

def getListProduk():
    produk = pd.read_sql_query('SELECT id_produk FROM produk_produk ORDER by id_produk', connection)
    id_produk = []
    for line in produk.itertuples():
        id_produk += [line[1]]
    
    return id_produk

# def getJumlahProduk():
#     produk_count = pd.read_sql_query('SELECT COUNT(id_produk) FROM produk_produk ORDER by id_produk', connection)
    
#     for line in produk_count.itertuples():
#         jumlah_produk = line[1]
#         return jumlah_produk

def getIdProdukTerrating(id_user):
    query = pd.read_sql_query('SELECT id_produk_id FROM produk_rating WHERE id_pelanggan_id = ' + str(id_user) + '', connection)
    array_id = []
    for line in query.itertuples():
        array_id += [line[1]]
    return array_id

def getValuePrediksi(id_user, id_produk_a):
    produk_a = id_produk_a
    query_user = pd.read_sql_query('SELECT id_produk_id FROM produk_rating WHERE id_pelanggan_id = ' + str(id_user) + ' AND id_produk_id != ' + str(produk_a) +'', connection)
    Atas = Bawah = 0
    RataRating_a = rataRatingProduk(produk_a)
    
    if RataRating_a != 0:
        for line in query_user.itertuples():
            produk_b = line[1]
            rating_b = getRatingUser(id_user, produk_b)
            Rata_b = rataRatingProduk(produk_b)
            combine_ab = combinedSim(produk_a, produk_b)
            
            atas = (rating_b - Rata_b)*combine_ab 
            Atas = Atas + atas

            bawah = abs(combine_ab)
            Bawah = Bawah + bawah
            # print(produk_a , produk_b, atas, bawah)
        result = RataRating_a + (Atas/Bawah)

    elif RataRating_a == 0:
        for line in query_user.itertuples():
            produk_b = line[1]
            rating_b = getRatingUser(id_user, produk_b)
            combine_ab = combinedSim(produk_a, produk_b)
            
            atas = rating_b *combine_ab 
            Atas = Atas + atas

            bawah = abs(combine_ab)
            Bawah = Bawah + bawah
            # print(produk_a , produk_b, atas, bawah)
        result = Atas/Bawah
    # print(Atas, Bawah)
    
    return result

# print(getValuePrediksi(2,1))
# print(getValuePrediksi(2,21))
# print(getValuePrediksi(2,9))
# print(getValuePrediksi(2,23))
# print(getValuePrediksi(2,14))
# print(getValuePrediksi(2,12))

def getPrediksi(id_user):
    hasil = []
    for produk_a in getListProduk(): 
        nilai_prediksi = getValuePrediksi(id_user, produk_a)
        hasil += [[nilai_prediksi, produk_a]]

    hasil.sort( key = lambda x: float(x[0]),  reverse = True)      
    return hasil

# print(getPrediksi(2))

