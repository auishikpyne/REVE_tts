import numpy as np
import pandas as pd
import re
#from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import requests
import time
import sys
def get_phoneme_ngrams(ipa,n):
    tokens = ipa.split(' ')
    n_grams = ngrams(tokens, n)
    return [ ' '.join(grams) for grams in n_grams]

def get_dipthongs(bi_grams,vowel_phones):
    dipthongs = []
    for bi_gram in bi_grams:
        phones = bi_gram.split(" ")
        if phones[0] in vowel_phones and phones[1] in vowel_phones:
            dipthongs.append(bi_gram)
    return dipthongs

output_file = sys.argv[1]
data = pd.read_csv(output_file,index_col = False, sep = ',',encoding = 'utf8')
print(data.shape)
print(data.head())

ipa_list = data.ipa.to_list()
freq_list = data.freq.to_list()
cv_list = data.cv.to_list()

with open('vowel.txt','r',encoding="utf-8") as ph_file:
    vowel_ch=ph_file.readlines()
ph_file.close()
df = pd.DataFrame(vowel_ch,columns=['TARGET'])
df = df.replace('\n','', regex=True)
vowel_phones = df.TARGET.to_list()
print(vowel_phones)
dipthong_dict = dict()

ipas = ipa_list[:5]
cvs = cv_list[:5]
print(ipas)
print(cvs)
length = len(ipa_list)
for i in range(length):
    ipa = ipa_list[i].strip()
    freq = int(freq_list[i])
    bi_grams = get_phoneme_ngrams(ipa,2)
    #print(bi_grams)
    dipthongs = get_dipthongs(bi_grams,vowel_phones)
    for dt in dipthongs:
        if dt not in dipthong_dict:
            dipthong_dict[dt] = freq
        else:
            dipthong_dict[dt] += freq
df = pd.DataFrame(zip(dipthong_dict.keys(),dipthong_dict.values()))
df.columns = ['dipthong','freq']
df.to_csv('output/dipthong_dist.csv', index = None)
