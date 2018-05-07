from nltk.corpus import wordnet, wordnet_ic
import sys
#Information Content
semcor_ic_add1 = wordnet_ic.ic('ic-semcor-add1.dat') #IC paling mendekati, berdasarkan Wordnet 3.0

#synset
headset = wordnet.synset('headset.n.01')
# keyboard = wordnet.synset('keyboard.n.01')
# monitor = wordnet.synset('monitor.n.04')
charger = wordnet.synset('charger.n.02')
speaker = wordnet.synset('speaker.n.02')
microphone = wordnet.synset('microphone.n.01')
headphone = wordnet.synset('headphone.n.01')

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

#contoh inputan
# input_1 = "keyboard"
# input_2  = "monitor"

input_1 = input()
input_2 = input() 

### block algoritma jiang-conrath calculation ###
def list_corpus(param):
    temp = []
    data = wordnet.synsets(param, pos=wordnet.NOUN) #hanya synset yang berupa kata benda saja yang dipilih
    if len(data) != 0:  #pengecekan apakah inputan memiliki synset atau tidak
        for kata in range(len(data)):
            hasil = data[kata]
            temp += [data[kata]]
        return temp
    else:
        print("Inputan tidak memiliki synset")
        sys.exit() #validasi jika inputan tidak memiliki synset maka proses akan langsung dihentikan


def jcn_result(a,b):
    list_corpus(a)
    list_corpus(b)
    temp = []
    for data_a in list_corpus(a):        
        for data_b in list_corpus(b):
            temp += [data_a.jcn_similarity(data_b, semcor_ic_add1)]         
    hasil = max(temp)    
    return hasil
### endblock ####
print(jcn_result(input_1,input_2))

# print(list_corpus(monitor))
# print("monitor & charger = " + str(mon.jcn_similarity(charger, semcor_ic_add1)))