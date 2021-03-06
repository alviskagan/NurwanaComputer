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


cur = connection.cursor()

df = pd.read_sql_query('SELECT  id_produk_id, id_pelanggan_id, is_rating FROM produk_rating order by id_produk_id ', connection)

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
    query = pd.read_sql_query('SELECT  a.id_pelanggan_id FROM produk_rating a, produk_rating b WHERE a.id_produk_id = ' 
    +str(item_1) +' AND b.id_produk_id = ' 
    +str(item_2) +' AND a.id_pelanggan_id = b.id_pelanggan_id', connection)
    Atas = Bawah_i = Bawah_j = 0
    n_users = df.id_pelanggan_id.shape[0]
    
    for line in query.itertuples():
        rui = getRatingUser(line[1], item_1)
        ruj = getRatingUser(line[1], item_2)
        ru  = rataRatingUser(line[1])
        atas = (rui-ru) * (ruj-ru)
        bawah_i = pow((rui-ru),2)
        bawah_j = pow((ruj-ru),2)
        Atas = Atas + atas
        Bawah_i = Bawah_i + bawah_i
        Bawah_j = Bawah_j + bawah_j
    Bawah = (math.sqrt(Bawah_i)* math.sqrt(Bawah_j))
    if Bawah == 0:
        Bawah = 1
    hasil = Atas/Bawah
    # print(hasil)
    return hasil  

# print(getSimilarity(11,1))
# print(getSimilarity(11,2))
# print(getSimilarity(11,9))
# print(getSimilarity(11,21))
# print(getSimilarity(11,23))
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

### Jiang-Conrtah V2 ###
def corpus_kategori(param):
    # kategori = pd.read_sql_query('select produk_produk.nama_produk, produk_kategori.nama_kategori from produk_kategori, produk_produk where produk_produk.id_produk = ' + str(param) + ' and produk_produk.kategori_produk_id = produk_kategori.id_kategori', connection)
    kategori = pd.read_sql_query('select produk_kategori.nama_kategori from produk_kategori, produk_produk where produk_produk.id_produk = ' + str(param) + ' and produk_produk.kategori_produk_id = produk_kategori.id_kategori', connection)
    for line in kategori.itertuples():
        nama_synset = list_corpus(line[1])    
    return nama_synset

def nama_produk(param):
    nama = pd.read_sql_query('select produk_produk.nama_produk from produk_kategori, produk_produk where produk_produk.id_produk = ' + str(param) + ' and produk_produk.kategori_produk_id = produk_kategori.id_kategori', connection)
    for line in nama.itertuples():
        return line[1]

# print(nama_produk(2))

def jcn_similarity(a,b):
    data_a = corpus_kategori(a)
    data_b = corpus_kategori(b)
    # print(data_a, data_b)
    if data_a != data_b:
        result_jcn = data_a.jcn_similarity(data_b, semcor_ic_add1)
        return result_jcn
    else:
        return 1
    return result_jcn

# print(jcn_similarity(1,2))
# print(jcn_similarity(1,2))
# print(jcn_similarity(2,9))
# print(jcn_similarity(9,21))
# print(jcn_similarity(21,23))
# print("AAA")
def combinedSim(item_1, item_2):
    a = 0.25
    cf = getSimilarity(item_1, item_2)
    jcn = jcn_similarity(item_1, item_2)
    # print(cf, jcn)
    result = a*cf + (1-a)*jcn
    return result
# # print(combinedSim())
# print(combinedSim(1,1))
# print(combinedSim(1,2))
# print(combinedSim(2,9))
# print(combinedSim(9,21))
# print(combinedSim(21,23))
def getListProduk():
    produk = pd.read_sql_query('SELECT id_produk FROM produk_produk ORDER by id_produk', connection)
    id_produk = []
    for line in produk.itertuples():
        id_produk += [line[1]]
    
    return id_produk

def getIdProdukTerrating(id_user):
    query = pd.read_sql_query('SELECT id_produk_id FROM produk_rating WHERE id_pelanggan_id = ' + str(id_user) + '', connection)
    array_id = []
    for line in query.itertuples():
        array_id += [line[1]]
    return array_id

def getValuePrediksi(id_user, id_produk_a):
    produk_a = id_produk_a
    query_user = pd.read_sql_query('SELECT id_produk_id FROM produk_rating WHERE id_pelanggan_id = '+ str(id_user) + ' AND id_produk_id != ' + str(produk_a) +'', connection)
    
    Atas = Bawah = 0
    RataRating_a = rataRatingProduk(produk_a)
    # Perhitungan Prediksi Untuk Produk yang Pernah di Rating
    if RataRating_a != 0 :
        for line in query_user.itertuples():
            produk_b = line[1]
            rating_b = getRatingUser(id_user, produk_b)
            Rata_b = rataRatingProduk(produk_b)
            combine_ab = combinedSim(produk_a, produk_b)
            
            atas = (rating_b - Rata_b)*combine_ab 
            Atas = Atas + atas

            bawah = abs(combine_ab)
            Bawah = Bawah + bawah
        if Atas != 0 and Bawah != 0:
            result = RataRating_a + (Atas/Bawah)
        else:
            result = RataRating_a
    # Perhitungan Prediksi Untuk Produk yang Belum Pernah di Rating
    elif RataRating_a == 0 :
        for line in query_user.itertuples():
            produk_b = line[1]
            rating_b = getRatingUser(id_user, produk_b)
            combine_ab = combinedSim(produk_a, produk_b)
            
            atas = rating_b *combine_ab 
            Atas = Atas + atas

            bawah = abs(combine_ab)
            Bawah = Bawah + bawah
            # print(produk_a , produk_b, atas, bawah)
        # print(RataRating_a)
        if Atas == 0 and Bawah == 0:
            result = 0
        else:
            result = Atas/Bawah
    
    return result
# print(getValuePrediksi(29,11))
# print(getValuePrediksi(72,11))
# print(getValuePrediksi(37,11))
# print(getValuePrediksi(25,11))
# print(getValuePrediksi(45,11))
skenario = pd.read_sql_query('select id_pelanggan_id, id_produk_id from produk_rating', connection)
# for line in skenario.itertuples():
#     print(getValuePrediksi(line[1],line[2]))

def getListRating(id_user):
    query = pd.read_sql_query('SELECT id_produk_id FROM produk_rating WHERE id_pelanggan_id = ' + str(id_user) + '', connection)
    array_id = []
    for line in query.itertuples():
        array_id += [line[1]]
    return array_id

# print(getListRating(3))

def getPrediksi(id_user):
    if id_user > 1 :
        hasil = []
        #id produk yang pernah dibeli
        produk_terbeli = getListRating(id_user)
        for produk_a in getListProduk(): 
            nilai_prediksi = getValuePrediksi(id_user, produk_a)
            # memfilter agar produk yang pernah terbeli tidak dimunculkan pada rekomendasi
            if produk_a != produk_terbeli:
                hasil += [[nilai_prediksi, produk_a]]

        hasil.sort( key = lambda x: float(x[0]),  reverse = True)
        # print(hasil)      
        return hasil

# for line in skenario.itertuples():
#     print(line[1])
#     print(getPrediksi(line[1]))

# print("alvis")
# print(getPrediksi(21))
# print("bud")
# print(getPrediksi(4))
# print("cap")
# print(getPrediksi(5))