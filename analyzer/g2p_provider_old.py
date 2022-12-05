import pandas as pd
import numpy as np
import requests
import json
import re
import sys

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


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
    chars = chars.replace(chr(65279),'')
    chars = chars.strip()
    return chars

def get_spaced_ipa(syllable):
    spaced_syllables = []
    #space separated phoneme representation
    if len(syllable)> 0:
        #print(syllable)
        phone = syllable[0]
        length = len(syllable)
        for i in range(1,length):
            if syllable[i] in target_chars:
                phone += ' '
                phone += syllable[i]
            else:
                phone += syllable[i]
        return phone
    
    return syllable   

def get_ipa(token):
    response_g2p = requests.post('https://dev.revesoft.com:5556/g2p_predictor',json ={'text':token},verify = False)
    phoneme = response_g2p.json()['output']
    return phoneme.strip()

data = pd.read_csv(sys.argv[1],index_col= False, encoding = 'utf8', sep = ",")

print(data.shape)

word_ipa_freq_list = []
words = data.word.to_list()
freq_list = data.freq.to_list()
length = len(words)
initial = 0
print(length)
print('initial: ',initial)
for i in range(initial,length):
    print(i)
    word = char_normalise(words[i])
    phonemes = get_ipa(word)
    print(phonemes)
    #phoneme_list = phonemes.replace(".","").strip().split("   ")
    #print('len_ ', len(phoneme_list))
    #spaced_phonemes = [get_spaced_ipa(ipa) for ipa in phoneme_list]
    word_ipa_freq_list.append([word,phonemes,freq_list[i]])
    if (i+1) % 1 == 0:
        print(i+1)
        df = pd.DataFrame(word_ipa_freq_list)
        df.to_csv("output/word_ipa_freq.csv", index = None,header =None,mode = 'a')
        word_ipa_freq_list = []
