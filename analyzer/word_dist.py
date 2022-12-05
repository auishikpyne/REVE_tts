import numpy as np
import pandas as pd
import requests
import time
import json
import sys
from tqdm import tqdm

def get_graphemes(text):
#    time.sleep(.1)
    norm_url = "http://dev.revesoft.com/normalisation-0.0.1/normalisation"
    response = requests.post(norm_url,json ={'input':text})
    text_list = json.loads(response.text)
    token_list=[]
    if response.status_code==200:
        token_list = [item['token'].strip() for item in text_list if item['tokenType'] == "self"]
        
    #token_list=["a","b","c"]
    return token_list


def char_normalise(chars):
    chars = chars.replace(chr(2437)+chr(2494),chr(2438)) # অ + া = আ
    chars = chars.replace(chr(2503)+chr(2494),chr(2507)) # ে +  া = ো
    chars = chars.replace(chr(2503)+chr(2519),chr(2508)) # ে + ৗ  = ৌ
    chars = chars.replace(chr(2494)+chr(2503),chr(2507)) # ে +  া = ো
    chars = chars.replace(chr(2519)+chr(2503),chr(2508)) # ে + ৗ  = ৌ
    
    chars = chars.replace(chr(2476)+chr(2492),chr(2480)) # ব    +   ়   =   র
    chars = chars.replace(chr(2465)+chr(2492),chr(2524)) # ড    +   ়   =   ড়
    chars = chars.replace(chr(2466)+chr(2492),chr(2525)) # ঢ    +   ়   =   ঢ়
    chars = chars.replace(chr(2479)+chr(2492),chr(2527)) # য    +   ়   =   য়
    chars = chars.replace(chr(8204),'') #zero width non-joiner = ''
    chars = chars.replace(chr(8205),'') # zero width joiner = ''
    chars = chars.strip()
    return chars

infile = sys.argv[1]

with open(infile,'r', encoding ='utf8') as file:
    lines = file.readlines()

print('total lines ',len(lines))
sentence_list = [char_normalise(sentence.replace('\n','')) for sentence in lines if sentence.replace('\n','').strip()!=""] 

#print(len(sentence_list))
#get word dictionary
#df = pd.read_csv('output/word_freq.csv', encoding = "utf8")

word_dict = dict()  #zip(df.word.to_list(),df.freq.to_list()))
#print('word_dict length: ',len(word_dict))
count = 0
initial = 0
count = initial
length = len(sentence_list)
print('length of sentence after char_normalization: ',length)
count_failed_sentence=0
for i in tqdm(range(initial,length)):
    sentence = sentence_list[i]
    #print(sentence[:100])
    words = get_graphemes(sentence)
#    print(len(words))
    if len(words)==0:
        count_failed_sentence=count_failed_sentence+1
#        print(sentence)
    count += 1
    for word in words:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1

   
    if count % 1 == 0:
        #print(count)
        #print(words)
        sorted_dict = dict(sorted(word_dict.items(), key=lambda x: x[1],reverse = True))
        #print(sorted_dict)

        df = pd.DataFrame(zip(sorted_dict.keys(),sorted_dict.values()))
        df.columns = ['word','freq']
        df.to_csv('output/word_freq.csv',index = None)
        #print('word_dict length: ',len(word_dict))
print("total number of failed sentence",count_failed_sentence)
