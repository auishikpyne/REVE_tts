import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import requests
import json
import time
import re
import sys

full = "[ক-হড়-য়]্[ক-হড়-য়]"
partial = "্[ক-হড়-য়]"


def get_grapheme_ngrams_modified(word,n):
    cluster_dict = dict()
    #print(word)
    if '্' not in word:
        return ["".join(k1) for k1 in list(ngrams(word,n))]
    
    #####codes for word containg cluster###
    ch = 1
    cluster_list = re.findall(full+partial+partial+partial+partial, word)
    for cluster in cluster_list:
        word = word.replace(cluster,str(ch))
        cluster_dict[str(ch)] = cluster
        ch += 1

    cluster_list = re.findall(full+partial+partial+partial, word)
    for cluster in cluster_list:
        word = word.replace(cluster,str(ch))
        cluster_dict[str(ch)] = cluster
        ch += 1

    cluster_list = re.findall(full+partial+partial,word)
    for cluster in cluster_list:
        word = word.replace(cluster,str(ch))
        cluster_dict[str(ch)] = cluster
        ch += 1

    cluster_list = re.findall(full+partial, word)
    for cluster in cluster_list:
        word = word.replace(cluster,str(ch))
        cluster_dict[str(ch)] = cluster
        ch += 1

    cluster_list = re.findall(full, word)
    for cluster in cluster_list:
        word = word.replace(cluster,str(ch))
        cluster_dict[str(ch)] = cluster
        ch += 1

    #print('word:',word)
    #print(cluster_dict)
    ng_list = []
    if len(word) >= 3:
        ngram_list = ["".join(k1) for k1 in list(ngrams(word,n))]
        #print(ngram_list)
        for ngram in ngram_list:
            for clus_idx in cluster_dict:
                if clus_idx in ngram:
                    ngram = ngram.replace(clus_idx,cluster_dict[clus_idx])
            ng_list.append(ngram)
        #print('ngrams: ',ng_list)
        #print('==============================')

    return ng_list


def get_phoneme_ngrams(text,n ):
    tokens = text.split(' ')
    n_grams = ngrams(tokens, n)
    return [ ' '.join(grams) for grams in n_grams]

def get_grapheme_ngrams(text,n):
    return ["".join(k1) for k1 in list(ngrams(text,n))]

def get_graphemes(text):
        time.sleep(.5)
        norm_url = "http://dev.revesoft.com/normalisation-0.0.1/normalisation?input="+text
        response = requests.post(norm_url)
        #print('response: ',response.text)
        text_list = json.loads(response.text)
        
        token_list = [item['token'].strip() for item in text_list if item['tokenType'] == "self"]
        return token_list

def add_to_dict(bi_gram_dict,bi_gram):
    if bi_gram in bi_gram_dict:
        bi_gram_dict[bi_gram] += 1
    else:
        bi_gram_dict[bi_gram] = 1


def char_normalize(chars):
    chars = chars.replace(chr(2437)+chr(2494),chr(2438)) # অ + া = আ
    chars = chars.replace(chr(2503)+chr(2494),chr(2507)) # ে +  া = ো
    chars = chars.replace(chr(2503)+chr(2519),chr(2508)) # ে + ৗ  = ৌ
    chars = chars.replace(chr(2476)+chr(2492),chr(2480)) # ব	+	়	=	র
    chars = chars.replace(chr(2465)+chr(2492),chr(2524)) # ড	+	়	=	ড়
    chars = chars.replace(chr(2466)+chr(2492),chr(2525)) # ঢ	+	়	=	ঢ়
    chars = chars.replace(chr(2479)+chr(2492),chr(2527)) # য	+	়	=	য়
    chars = chars.replace(chr(8204),'') #zero width non-joiner = ''
    chars = chars.replace(chr(8205),'') # zero width joiner = ''
    chars = chars.strip()
    return chars


#name = 'graj'
n = 3
#print('name: ',name)
print('value of n: ',n)
#with open('data/'+name+"_sample.txt", encoding = "utf8") as file:
  #  lines = file.readlines()
'''
data = pd.read_csv('output/word_freq.csv', encoding = 'utf8')
print(data.shape)
word_list = [char_normalize(str(word)) for word in data.word.to_list()]
'''
data1 = pd.read_csv(sys.argv[1], encoding = "utf8")
#words = [char_normalize(word) for word in data1.word.to_list()]
words = data1.word.to_list()
print('total words: ',len(words))
#data2 = pd.read_csv("150k_words.csv",encoding = "utf8")
#words2 = [char_normalize(word) for word in data2.word.to_list()]
#print('len of 150k_words: ',len(words2))

final_words = list(set(words))
print('len of unique_words: ',len(final_words))


#ipa_list = [str(word.strip()) for word in data1.ipa.to_list()]

tri_gram_dict = dict()


for word in words:
    #word = '_' + word + '_'
    tri_grams = get_grapheme_ngrams_modified(word,n)
    for ng in tri_grams:
        #if '্' not in ng:
        add_to_dict(tri_gram_dict,ng)


sorted_dict = dict(sorted(tri_gram_dict.items(),key = lambda x:x[0][1], reverse = False))
print('tri_gram count: ',len(sorted_dict))
df = pd.DataFrame(zip(sorted_dict.keys(),sorted_dict.values()))

df.columns = ['n_gram','freq']
df.to_csv('output/char_tri_gram.csv',index = None)

tri_gram_list = sorted_dict.keys()
print('len of tri gram list', len(tri_gram_list))

word_example_dict = dict()

print('tri_gram length: ', len(tri_gram_list))
#print('total word: ', len(word_list))
count = 0
for tg in tri_gram_list:
    examples = []
    #print(cluster+ " "+str(len(cluster)))
    for word in final_words:
        if len(examples) >= 3:
            break
        if bool(re.search(tg,word)) and word not in examples:
            examples.append(word)  
    word_example_dict[tg] = examples
    count += 1
    if count % 1000 == 0:
        print(count)
           

key_list = list(sorted_dict.keys())
value_list = list(sorted_dict.values())
example_list = word_example_dict.values()
df = pd.DataFrame(zip(key_list,value_list,example_list))
df.columns = ['tri_gram','freq','example']
df.to_csv('output/char_tri_gram_with_example.csv',index = False)
