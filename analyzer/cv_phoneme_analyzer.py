import numpy as np
import pandas as pd
import re
import sys

#output_file = 'g2p_dict_ver2.csv'
output_file = sys.argv[1]
data = pd.read_csv(output_file,index_col = False, sep = ',',encoding = 'utf8')
print(data.shape)
print(data.head())

word_list = data.word.to_list()
ipa_list = data.ipa.to_list()
freq_list = data.freq.to_list()

with open('vowel.txt','r',encoding="utf-8") as ph_file:
    vowel_ch=ph_file.readlines()
ph_file.close()
df = pd.DataFrame(vowel_ch,columns=['TARGET'])
df = df.replace('\n','', regex=True)
vowel_phones=df.TARGET.to_list()

with open('consonant.txt','r',encoding="utf-8") as ph_file:
    cons_ch =ph_file.readlines()
ph_file.close()
df = pd.DataFrame(cons_ch,columns=['TARGET'])
df = df.replace('\n','', regex=True)
cons_phones=df.TARGET.to_list()

print(vowel_phones)
print(cons_phones)

len1 = len(word_list)
print('word count: ',len1)
cv_list = []
concern_list = []
cv_pat_dict = dict()
for i in range(len1):
	word = word_list[i]
	ipa = ipa_list[i]
	freq = freq_list[i]
	ipas = ipa.strip().split(' ')
	cvs = []
	for ph in ipas:
		if ph in vowel_phones:
			cvs.append('v')
		elif ph in cons_phones:
			cvs.append('c')
		else:
			cvs.append(ph)
	cv_seq = "".join(cvs)
	cv_seq_2 = cv_seq.replace("vv","v")
	concern_list.append([word,ipa,cv_seq,cv_seq_2,freq])
	for cv in cv_seq_2.split('.'):
		if cv in cv_pat_dict:
			cv_pat_dict[cv] += int(freq)
		else:
			cv_pat_dict[cv] = int(freq)
print(concern_list[:5])
df = pd.DataFrame(concern_list)
df.columns = ['word','ipa','cv','cv_2','freq']
df.to_csv('output/cv_file.csv',index =False)

df = pd.DataFrame(zip(cv_pat_dict.keys(),cv_pat_dict.values()))
df.columns = ['pattern','freq']
df.to_csv('output/cv_dist.csv',index =False)
