
import re
import numpy as np
import pandas as pd
import sys

def add_to_dict(onset_dict,phone,freq):
    if phone in onset_dict:
        onset_dict[phone] += freq
    else:
        onset_dict[phone] = freq


def get_coda_analysis(ipa_list,cv_list,freq_list):
    length1 = len(cv_list)
    length2 = len(ipa_list)
    print(length1)
    print(length2)
    coda_dict = dict()

    for i in range(length1):
        cv_seq = cv_list[i]
        syl_seq = ipa_list[i]
        freq = int(freq_list[i])

        cvs = cv_seq.split('.')
        syls = syl_seq.split('.')
        len1 = len(cvs)
        for j in range(len1):
            cv = cvs[j]
            syl = syls[j]
            if cv.endswith('vc'):
                ph = syl.strip().split(' ')[-1]
                #if ph in target_chars: 
                add_to_dict(coda_dict,ph,freq)
    return coda_dict




def get_onset_analysis(ipa_list,cv_list,freq_list):

    length1 = len(cv_list)
    length2 = len(ipa_list)
    print(length1)
    print(length2)
    onset_dict = dict()

    for i in range(length1):
        cv_seq = cv_list[i]
        syl_seq = ipa_list[i]
        freq = int(freq_list[i])
        cvs = cv_seq.split('.')
        syls = syl_seq.split('.')

        len1 = len(cvs)
        for j in range(len1):
            cv = cvs[j]
            syl = syls[j].strip()
            if cv.startswith('cv'):
                add_to_dict(onset_dict,syl.split(' ')[0],freq)

    return onset_dict

##=====================main module============================

data = pd.read_csv(sys.argv[1], index_col = False, sep = ',', encoding = 'utf8')

print(data.shape)
ipa_list = data.ipa.to_list()
cv_list = data.cv_2.to_list()
freq_list = data.freq.to_list()

onset_dict = get_onset_analysis(ipa_list,cv_list,freq_list)    
sorted_dict_onset = dict(sorted(onset_dict.items(), key=lambda x: x[1],reverse = True))
print('onset_dict: ',sorted_dict_onset)
df = pd.DataFrame(zip(sorted_dict_onset.keys(),sorted_dict_onset.values()))
df.columns = ['onset','freq']
df.to_csv('output/onset_dist.csv',index = False)
print("Successfully Saved......Onset")


coda_dict = get_coda_analysis(ipa_list,cv_list,freq_list)    
sorted_dict_coda = dict(sorted(coda_dict.items(), key=lambda x: x[1],reverse = True))
print('coda_dict: ',sorted_dict_coda)

df = pd.DataFrame(zip(sorted_dict_coda.keys(),sorted_dict_coda.values()))
df.columns = ['phone','freq']
df.to_csv('output/coda_dist.csv',index = False)
print("Successfully Saved......Coda")
