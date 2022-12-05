
# Set up libraries
import numpy as np
import pandas as pd
from pandas.core.common import flatten
import re
import sys

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
    return chars

#input and output file
input_file = sys.argv[1]
output_file = "output/mono_graph.csv"

#input file read module
#with open(input_file, mode = 'r', encoding = 'utf8') as file:
#    lines = file.readlines()

#sentence_list = [ sentence.replace('\n','').strip() for sentence in lines if sentence.replace('\n','').strip()!=""]
#print(data.shape)
#data.columns = ["ID","unnorm_sen","sentence"]
#data.columns = ["word"]

#size = data.shape[0]
#print(data.head())
#sentence_list = data.word.to_list()

data=pd.read_csv(input_file,sep=',')
sentence_list=data.word.to_list()

print('num of sentence: ', len(sentence_list))
normalised_texts=[char_normalise(sentence) for sentence in sentence_list]
nor_sentence_list = normalised_texts

graphemes = "".join(nor_sentence_list)
#graphemes = sorted(list(set(graphemes)))

grapheme_list=sorted(set(graphemes))


#distribution calculation

grapheme_dict = dict()
#grapheme_dict['...'] = 0
length = len(grapheme_list)
print(length)
for i in range(length):
    grapheme_dict[grapheme_list[i]] = 0

print(grapheme_dict)
sp_char = ['?','*','+','.','(',')']
#num_seq = len(phoneme_seq)
print(len(nor_sentence_list))
for sentence in nor_sentence_list:
    for key in grapheme_dict:
        if key in sp_char:
            key1 = "\\"+ key
        else:
            key1 = key
        grapheme_dict[key] += len(re.findall(key1,sentence))
        sentence = sentence.replace(key,'')

print(grapheme_dict)

sorted_dict = dict(sorted(grapheme_dict.items(), key=lambda x: x[0],reverse = False))
print(sorted_dict)
key_list = list(sorted_dict.keys())
value_list = list(sorted_dict.values())
df = pd.DataFrame(zip(key_list,value_list))
df.columns = ['grapheme','freq']
df.to_csv(output_file,index = False)
'''
# writing to Excel
file = pd.ExcelWriter(excel_file)
# write DataFrame to excel
df.to_excel(file, index = False)
  
# save the excel
file.save()

'''
# In[6]:


#pip install openpyxl


# In[ ]:




