from nltk.corpus import wordnet, wordnet_ic
from sklearn.metrics.pairwise import pairwise_distances
from sklearn import cross_validation as cv
from sklearn.metrics import mean_squared_error
from math import sqrt
from django.db import connection
import sys
import numpy as np
import pandas as pd
import sqlite3
import math

#Information Content
semcor_ic_add1 = wordnet_ic.ic('ic-semcor-add1.dat') #IC paling mendekati, berdasarkan Wordnet 3.0
brown = wordnet_ic.ic('ic-brown.dat')
#synset

headset = wordnet.synset('headset.n.01')
keyboard = wordnet.synset('keyboard.n.01')
monitor = wordnet.synset('monitor.n.04')
charger = wordnet.synset('charger.n.02')
speaker = wordnet.synset('speaker.n.02')
microphone = wordnet.synset('microphone.n.01')
headphone = wordnet.synset('headphone.n.01')
mouse   = wordnet.synset('mouse.n.04')
cable   = wordnet.synset('cable.n.02')
laptop  = wordnet.synset('laptop.n.01')
printer = wordnet.synset('printer.n.03')
router  = wordnet.synset('router.n.03')
modem   = wordnet.synset('modem.n.01')

array_kategori = [headset, keyboard, monitor, charger, speaker, microphone, headphone, mouse, cable, laptop, printer, router, modem]

# for data in array_kategori:
#     print(data)
hyp = lambda s:s.hypernyms()
print(headset.tree(hyp))

#list synsets
hs  = wordnet.synsets("headset")
hp  = wordnet.synsets("headphone")
mon = wordnet.synsets("monitor")[0]
lp  = wordnet.synsets("laptop")
key = wordnet.synsets("keyboard")
ch  = wordnet.synsets("charger")
sp  = wordnet.synsets("speaker")
mic = wordnet.synsets("microphone")
cab = wordnet.synsets("cable")
mos = wordnet.synsets("mouse")
pr  = wordnet.synsets("print")
rt  = wordnet.synsets("router")
mdm = wordnet.synsets("modem")
# apple = wordnet.synsets("apple")
# pear = wordnet.synsets("pear")

apple = wordnet.synset('apple.n.01')
pear = wordnet.synset('pear.n.01')
print(apple, pear)
print(mos)
#database sqlite
# con = sqlite3.connect("db.sqlite3")

# cur = connection.cursor()

# df = pd.read_sql_query('SELECT id, username  FROM auth_user WHERE id > 1', con)
# print(df)
# for row in cur.execute('SELECT id, username  FROM auth_user WHERE id > 1'):
#     print(row)

# df = pd.read_sql_query('SELECT * FROM produk_rating ', connection)
# print(df)
# for row in cur.execute('SELECT * FROM produk_rating'):
#     print(row)


#contoh inputan
# input_1 = "keyboard"
# input_2  = "monitor"

#Raw Input
# input_1 = input()
# input_2 = input() 
# print(wordnet.ic(speaker, semcor_ic_add1))

#Fungsi cari frekuensi dan N
def cari_ic(synset, ic):
    try:
        icpos = ic[synset._pos]
    except KeyError:
        msg = 'Information content file has no entries for part-of-speech: %s'
        raise WordNetError(msg % synset._pos)

    counts = icpos[synset._offset]
    if counts == 0:
        return _INF
    else:
        # print(synset)
        # print(counts, icpos[0])
        # print("==============")
        return -math.log(counts / icpos[0])    
    # icpos = brown[input._pos]
    # counts = icpos[input._offset]
    # # print(input._pos)
    # # print(input._offset)
    # return -math.log( counts / icpos[0] )

#Contoh Keluaran
# print("Posisi ic dari Headset: " + str(headset) + str(cari_ic(headset, semcor_ic_add1)))
# print("Posisi ic dari Speaker: " + str(speaker) + str(cari_ic(speaker, semcor_ic_add1)))
# print("Posisi ic dari Speaker: " + str(keyboard) + str(cari_ic(keyboard, semcor_ic_add1)))
# print("Posisi ic dari Speaker: " + str(monitor) + str(cari_ic(monitor, semcor_ic_add1)))

# print(wordnet.jcn_similarity(headset, speaker, semcor_ic_add1))
# print("=======break======")
# print(wordnet.jcn_similarity(apple, pear, semcor_ic_add1))

# print(wordnet._synset_from_pos_and_offset('n', 3505667))

### block algoritma jiang-conrath calculation ###
def list_corpus(param):
    temp = []
    data = wordnet.synsets(param, pos=wordnet.NOUN) #hanya synset yang berupa kata benda saja yang dipilih
    if len(data) != 0:  #pengecekan apakah inputan memiliki synset atau tidak
        for kata in range(len(data)):
            
            hasil = data[kata]
            
            temp += [data[kata]]
            # temp += [data[kata],cari_ic(hasil, semcor_ic_add1)]
            # print(cari_ic(hasil, semcor_ic_add1))
        return temp
    else:
        print("Inputan tidak memiliki synset")
        sys.exit() #validasi jika inputan tidak memiliki synset maka proses akan langsung dihentikan

# print(list_corpus(input_1))
# print(list_corpus(input_1))

def jcn_result(a,b):
    # print(list_corpus(a))
    # print(list_corpus(b))
    # print(cari_ic(a))
    # print(cari_ic(b))
    temp = []
    for data_a in list_corpus(a):        
        for data_b in list_corpus(b):
            temp += [data_a.jcn_similarity(data_b, semcor_ic_add1)]         
    hasil = max(temp)    
    return hasil
### endblock ####

#Contoh Hasil Perhitungan Jiang-Conrath
# print(jcn_result(input_1,input_2))
print(modem.jcn_similarity(cable, semcor_ic_add1))
#Contoh Keluaran
# print(list_corpus(monitor))
# print("monitor & charger = " + str(mon.jcn_similarity(charger, semcor_ic_add1)))

# #Collaborative Filtering Algorithm
# header = ['user_id', 'item_id', 'rating']
# df = pd.read_csv('ml-100k/rating.data.txt', sep=',', names=header)

# print(df)
# print("===========")
# n_users = df.user_id.unique().shape[0]
# n_items = df.item_id.unique().shape[0]
# # print('Number of users = ' + str(n_users) + ' | Number of Products = ' + str(n_items))
# # print('Number of users = ' + str(n_users))
# # print(df)
# train_data, test_data = cv.train_test_split(df, test_size=0.25)
# # print(train_data)
# # print(test_data)
# #Create two user-item matrices, one for training and another for testing

# ###train data uji coba###
# train_data_df = np.zeros((n_users, n_items))
# # print(train_data_df)
# for line in df.itertuples():
#     # line 1 = user_id, line_2 = item_id.
#     # matrix train_data_df berukuran (5,5) karena jumlah user = 5 dan item = 5 (contoh) 
#     # alasan dikurangi satu karena index di train_data_df dimulai dari 0
#     train_data_df[line[1]-1, line[2]-1] = line[3]  
# #####
# print(train_data_df)
# print("=============")
# train_data_matrix = np.zeros((n_users, n_items))

# for line in train_data.itertuples():
#     train_data_matrix[line[1]-1, line[2]-1] = line[3]

# test_data_matrix = np.zeros((n_users, n_items))
# for line in test_data.itertuples():
#     test_data_matrix[line[1]-1, line[2]-1] = line[3]

# user_similarity = pairwise_distances(train_data_matrix, metric='cosine')
# item_similarity = pairwise_distances(train_data_matrix.T, metric='cosine')

# ####

# item_df_sim     = pairwise_distances(train_data_df.T, metric='cosine')
# # item_df_sim_2   = pairwise_distances(train_data_df_2, metric='cosine')
# print(item_df_sim)
# # print(range(item_df_sim))
# for i in range(len(item_df_sim)):
#     for j in range(len(item_df_sim[i])): 
#         print("koordinat: ", i , j)
#         print(item_df_sim[i][j])
#         print("user_id: ", i+1)
#         print("item_id: ", j+1)
#         print("======")
#     # for column in line:
#         # for value in column:
#         # print(line)
#         # print(column)
#     # print(line)
#     # for x in len(item_df_sim):
#     #     for y in len(item_df_sim):
#     #         print(line[x,y])
# # print(item_df_sim_2)


# ####

# def predict(ratings, similarity, type='user'):
#     if type == 'user':
#         mean_user_rating = ratings.mean(axis=1)
#         #You use np.newaxis so that mean_user_rating has same format as ratings
#         ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
#         pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
#     elif type == 'item':
#         pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
#     return pred

# item_prediction = predict(train_data_matrix, item_similarity, type='item')
# user_prediction = predict(train_data_matrix, user_similarity, type='user')

# # print(user_similarity)
# # print(item_similarity)

# def rmse(prediction, ground_truth):
#     prediction = prediction[ground_truth.nonzero()].flatten()
#     ground_truth = ground_truth[ground_truth.nonzero()].flatten()
#     return sqrt(mean_squared_error(prediction, ground_truth))

# # print('User-based CF RMSE: ' + str(rmse(user_prediction, test_data_matrix))) 
# # print('Item-based CF RMSE: ' + str(rmse(item_prediction, test_data_matrix)))