import numpy as np
import pandas as pd
import re
import sys

#input and output file
input_file = ''
phone_file = 'phonemes.txt'
output_file = ''
data = pd.read_csv(sys.argv[1],index_col = False, sep = ',', encoding = 'utf-8')
print(data.shape)
words = data.word.to_list()
syllables = data.ipa.to_list()
syllables = [syl.strip() for syl in syllables]

phone_dict = dict()

for sequence in syllables:
    phones = sequence.split(' ')
    for ph in phones:
        if ph in phone_dict:
            phone_dict[ph] += 1
        else:
            phone_dict[ph] = 1

sorted_dict = dict(sorted(phone_dict.items(), key=lambda x: x[1],reverse = True))
key_list = sorted_dict.keys()
value_list = sorted_dict.values()
df = pd.DataFrame(zip(key_list,value_list))
df.columns = ['phone','freq']

df.to_csv('output/phone_dist.csv', index = False)

print("Successfully Saved......")
