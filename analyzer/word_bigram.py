import numpy as np
import pandas as pd
import requests
import time
import json
from nltk.util import ngrams

def get_grapheme_ngrams(token_list,n):
    
    n_grams = ngrams(token_list, n)
    return [ ' '.join(grams) for grams in n_grams]



def get_graphemes(text):
    time.sleep(.5)
    norm_url = "http://dev.revesoft.com/normalisation-0.0.1/normalisation?input="+ text
    response = requests.post(norm_url)
    text_list = json.loads(response.text)
    token_list = [item['token'].strip() for item in text_list if item['tokenType'] == "self"]
    return token_list


def char_normalise(chars):
    chars = chars.replace(chr(2437)+chr(2494),chr(2438)) # অ + া = আ
    chars = chars.replace(chr(2503)+chr(2494),chr(2507)) # ে +  া = ো
    chars = chars.replace(chr(2503)+chr(2519),chr(2508)) # ে + ৗ  = ৌ
    chars = chars.replace(chr(2476)+chr(2492),chr(2480)) # ব    +   ়   =   র
    chars = chars.replace(chr(2465)+chr(2492),chr(2524)) # ড    +   ়   =   ড়
    chars = chars.replace(chr(2466)+chr(2492),chr(2525)) # ঢ    +   ়   =   ঢ়
    chars = chars.replace(chr(2479)+chr(2492),chr(2527)) # য    +   ়   =   য়
    chars = chars.replace(chr(8204),'') #zero width non-joiner = ''
    chars = chars.replace(chr(8205),'') # zero width joiner = ''
    chars = chars.strip()
    return chars

def add_to_dict(bi_gram_dict,bi_gram):
    if bi_gram in bi_gram_dict:
        bi_gram_dict[bi_gram] += 1
    else:
        bi_gram_dict[bi_gram] = 1
'''
with open('script_text_v2.txt','r', encoding ='utf8') as file:
    lines = file.readlines()

sentence_list = [char_normalise(sentence.replace('\n','')) for sentence in lines if sentence.replace('\n','').strip()!=""] 

print(len(sentence_list))
#get word dictionary
bi_gram_list = []
count = 0
initial = 0
print('initial: ',initial)
vowel_dict = {'আ':'া','ই':'ি','ঈ':'ী','উ':'ু','ঊ':'ূ','ঋ':'ৃ','এ':'ে','ঐ':'ৈ','ও':'ো','ঔ':'ৌ'}
length = len(sentence_list)

for i in range(initial,length):
    sentence = sentence_list[i]
    words = get_graphemes(sentence)
    n_grams = get_grapheme_ngrams(words,2)
    #print(n_grams)
    for bi_gram in n_grams:
        idx = bi_gram.strip().index(' ')
        prev_char = bi_gram[idx -1]
        next_char = bi_gram[idx+1]
        if prev_char == next_char:
            bi_gram_list.append(bi_gram)
            #print('desired_bi_gram: ',bi_gram)
        elif next_char in vowel_dict.keys() and prev_char in vowel_dict.values():
            if vowel_dict[next_char] == prev_char:
                bi_gram_list.append(bi_gram)
                #print('desired_vowel_bi_gram: ', bi_gram)
    if i % 10 == 0:
        df = pd.DataFrame(bi_gram_list)
        print(i)
        #df.columns = ['word','freq']
        df.to_csv('output/word_bigram.csv',index = None,header = None, mode = 'a')
        bi_gram_list = []
'''
       
'''
sorted_dict = dict(sorted(word_dict.items(), key=lambda x: x[1],reverse = True))
#print(sorted_dict)

df = pd.DataFrame(zip(sorted_dict.keys(),sorted_dict.values()))
df.columns = ['word','freq']
df.to_csv('output/word_freq.csv',index = None)
'''

word_freq_dict = dict()
data = pd.read_csv('output/word_bigram.csv', encoding = 'utf8')
bi_gram_list = data.bi_gram.to_list()

for bi_gram in bi_gram_list:
    add_to_dict(word_freq_dict,char_normalise(bi_gram))

sorted_dict = dict(sorted(word_freq_dict.items(), key=lambda x: x[1],reverse = True))
#print(sorted_dict)

df = pd.DataFrame(zip(sorted_dict.keys(),sorted_dict.values()))
df.columns = ['bi_gram','freq']
df.to_csv('output/word_bigram_freq.csv',index = None)
