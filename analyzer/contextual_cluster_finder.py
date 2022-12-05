# Set up libraries
import numpy as np
import pandas as pd
import re
from collections import defaultdict
import requests
import time
import json
import sys



def get_graphemes(text):
    time.sleep(.5)
    norm_url = "http://dev.revesoft.com/normalisation-0.0.1/normalisation?input="+text
    response = requests.post(norm_url)
    #print('response: ',response.text)
    text_list = json.loads(response.text)
    
    token_list = [item['token'].strip() for item in text_list if item['tokenType'] == "self"]
    return token_list

def char_normalise(chars):
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

def add_to_dict(clus_dict,clus_list,freq):
    for cluster in clus_list:
        if cluster in clus_dict:
            clus_dict[cluster] += freq
        else:
            clus_dict[cluster] = freq

def get_first_cluster(sentence,cluster_dict,freq):
    #print(sentence)
    full = "[ক-হড়-য়]্[ক-হড়-য়]"
    partial = "্[ক-হড়-য়]"
    if bool(re.search("^"+full+partial+partial+partial,sentence)):
        cluster_list = re.findall("^"+full+partial+partial+partial, sentence)
        add_to_dict(cluster_dict,cluster_list,freq)
        #print(cluster_list)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        #print(sentence)
    elif bool(re.search("^"+full+partial+partial,sentence)):   
        cluster_list = re.findall("^"+full+partial+partial, sentence)
        add_to_dict(cluster_dict,cluster_list,freq)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
            
    elif bool(re.search("^"+full+partial,sentence)):       
        cluster_list = re.findall("^"+full+partial, sentence)
        add_to_dict(cluster_dict,cluster_list,freq)
        #print(cluster_list)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        #print(sentence)
    elif bool(re.search("^"+full,sentence)):
        cluster_list = re.findall("^"+full, sentence)
        add_to_dict(cluster_dict,cluster_list,freq)
        #print(cluster_list)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
    
    return sentence,cluster_dict

#internal_cluster function definition
def get_internal_cluster(sentence,cluster_dict,freq):
    #print(sentence)
    full = "[ক-হড়-য়]্[ক-হড়-য়]"
    partial = "্[ক-হড়-য়]"
    if bool(re.search(full+partial+partial+partial,sentence)):
        cluster_list = re.findall(full+partial+partial+partial, sentence)
        add_to_dict(cluster_dict,cluster_list,freq)
        #print(cluster_list)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        #print(sentence)
    elif bool(re.search(full+partial+partial,sentence)):   
        cluster_list = re.findall(full+partial+partial, sentence)
        add_to_dict(cluster_dict,cluster_list,freq)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
            
    elif bool(re.search(full+partial,sentence)):       
        cluster_list = re.findall(full+partial, sentence)
        add_to_dict(cluster_dict,cluster_list,freq)
        #print(cluster_list)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        #print(sentence)
    elif bool(re.search(full,sentence)):
        cluster_list = re.findall(full, sentence)
        add_to_dict(cluster_dict,cluster_list,freq)
        #print(cluster_list)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
    
    return sentence,cluster_dict

#final_cluster function definition
def get_last_cluster(sentence,cluster_dict,freq):
        
    full = "[ক-হড়-য়]্[ক-হড়-য়]"
    partial = "্[ক-হড়-য়]"
    remove_list = ['া','ি','ী','ু','ূ','ৃ','ে','র','ৈ','ো','ৌ','য়']
    
    if sentence.endswith('ের'):
        sentence = sentence[:-2]
    elif sentence.endswith(tuple(remove_list)):
        sentence = sentence[:-1]
    
    if bool(re.search(full+partial+partial+partial+"$",sentence)):
        cluster_list = re.findall(full+partial+partial+partial+"$", sentence)
        add_to_dict(cluster_dict,cluster_list,freq)
        #print(cluster_list)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        #print(sentence)
    elif bool(re.search(full+partial+partial+"$",sentence)):   
        cluster_list = re.findall(full+partial+partial+"$", sentence)
        add_to_dict(cluster_dict,cluster_list,freq)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
            
    elif bool(re.search(full+partial+"$",sentence)):       
        cluster_list = re.findall(full+partial+"$", sentence)
        add_to_dict(cluster_dict,cluster_list,freq)
        #print(cluster_list)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        #print(sentence)
    elif bool(re.search(full+"$",sentence)):
        cluster_list = re.findall(full+"$", sentence)
        add_to_dict(cluster_dict,cluster_list,freq)
        #print(cluster_list)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
    
    return sentence,cluster_dict


######################  Main Region starts #######################
#name = 'gfaridpur'
data = pd.read_csv(sys.argv[1],sep=',',encoding = 'utf8')
words = data.word.to_list()
freqs = data.freq.to_list()


cluster_dict1 = dict()
cluster_dict2 = dict()
cluster_dict3 = dict()
length = len(words)
print(length)
for i in range(length):
    word = words[i]
    freq = int(freqs[i])
    if i % 10 == 0:
        print(i)

    #print(word)
    word,cluster_dict1 = get_first_cluster(word,cluster_dict1,freq)
    #print(word)
    word,cluster_dict3 = get_last_cluster(word,cluster_dict3,freq)
    #print(word)
    word,cluster_dict2 = get_internal_cluster(word,cluster_dict2,freq)
    #print(word)

# print(cluster_dict1)
# print(cluster_dict2)
# print(cluster_dict3)

sorted_dict1 = dict(sorted(cluster_dict1.items(), key=lambda x: x[1],reverse = True))
sorted_dict2 = dict(sorted(cluster_dict2.items(), key=lambda x: x[1],reverse = True))
sorted_dict3 = dict(sorted(cluster_dict3.items(), key=lambda x: x[1],reverse = True))
#print(len(sorted_dict))
key_list1 = list(sorted_dict1.keys())
value_list1 = list(sorted_dict1.values())

key_list2 = list(sorted_dict2.keys())
value_list2 = list(sorted_dict2.values())

key_list3 = list(sorted_dict3.keys())
value_list3 = list(sorted_dict3.values())

final_list = []
final_list += key_list1
final_list += key_list2
final_list += key_list3
#print(final_list)
final_list = set(final_list)
dd = defaultdict(list,{ k:[] for k in final_list })
#print(dd)


for d in (sorted_dict1, sorted_dict2,sorted_dict3): # you can list as many input dicts as you want here

    for key in dd.keys():
        if key in d:
            dd[key].append(d[key])
        else:
            dd[key].append(0)

#final_sorted_dict = dict()
#for clus in sorted_cluster_list:
#    final_sorted_dict[clus] = dd[clus]
final_sorted_dict = dict(sorted(dd.items(),key = lambda x: x[0], reverse = False))
key_list = list(final_sorted_dict.keys())
value_list = list(final_sorted_dict.values())

df = pd.DataFrame(zip(key_list,value_list))
df.columns = ['cluster','freq']
df.to_csv('output/cluster_dist.csv',index = False)
