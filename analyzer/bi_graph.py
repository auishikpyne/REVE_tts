import sys
import numpy as np
import pandas as pd
import re

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
    return chars

def add_to_dict(clus_dict,clus_list,freq):
    for cluster in clus_list:
        if cluster in clus_dict:
            cluster_dict[cluster] += freq
        else:
            cluster_dict[cluster] = freq


#input and output file
input_file = sys.argv[1] #Bangladeshi Indian
output_file = 'output/bi_gram_dist.csv'

#input file read module
data = pd.read_csv(input_file, index_col = False, encoding = 'utf8') #sep ="|"

print(data.shape)
print(data.head())
word_list = data.word.to_list()
word_list = [char_normalise(word) for word in word_list]
freq_list = data.freq.to_list()

cluster_dict = dict()
print(len(word_list))
consonant = "(?<!্)[ক-নপ-রলশ-হড়-য়]"
vowel = "[ািীুূৃে-ৌ]"
length = len(word_list)

for i in range(length):
    word = word_list[i]
    freq = freq_list[i]
    cluster_list = re.findall(consonant+vowel, word)
    add_to_dict(cluster_dict,cluster_list,freq)
    #print(cluster_list)
    #print(cluster_dict)
    for cluster in cluster_list:
        word = word.replace(cluster,'')
    
#print(cluster_dict)
#print(len(cluster_dict))


# In[33]:


sorted_dict = dict(sorted(cluster_dict.items(), key=lambda x: x[0],reverse = False))
# print(len(sorted_dict))
# print(sorted_dict)



consonant = "(?<!্)[ক-নপ-রলশ-হড়-য়]"
vowel = "[ািীুূৃে-ৌ]"
word_example_dict = dict()
bigram_list = sorted_dict.keys()
print('Total count of bigrapheme:',len(bigram_list))
for bigram in bigram_list:
    examples = []
    #print(cluster+ " "+str(len(cluster)))
    for word in word_list:
        if len(examples) >= 5 :
            break
        else:
            if bool(re.search("(?<!্)"+bigram,word)) and word not in examples:
                examples.append(word)  
    word_example_dict[bigram] = examples
           

key_list = list(sorted_dict.keys())
value_list = list(sorted_dict.values())
example_list = word_example_dict.values()
df = pd.DataFrame(zip(key_list,value_list,example_list))
df.columns = ['bi_gram','freq','example']
df.to_csv(output_file,index = False)




