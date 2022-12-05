import numpy as np
import pandas as pd
import sys

def char_normalise(chars):
    chars = chars.replace(chr(2437)+chr(2494),chr(2438)) # অ + া = আ
    chars = chars.replace(chr(2503)+chr(2494),chr(2507)) # ে +  া = ো
    chars = chars.replace(chr(2503)+chr(2519),chr(2508)) # ে + ৗ  = ৌ
    chars = chars.replace(chr(2476)+chr(2492),chr(2480)) # ব\t+\t়\t=\tর
    chars = chars.replace(chr(2465)+chr(2492),chr(2524)) # ড\t+\t়\t=\tড়
    chars = chars.replace(chr(2466)+chr(2492),chr(2525)) # ঢ\t+\t়\t=\tঢ়
    chars = chars.replace(chr(2479)+chr(2492),chr(2527)) # য\t+\t়\t=\tয়
    chars = chars.replace(chr(8204),'') #zero width non-joiner = ''
    chars = chars.replace(chr(8205),'') # zero width joiner = ''
    return chars



# modified g2p dict (dataset) preparation
data = pd.read_csv(sys.argv[1],index_col = False, sep = ',',encoding = 'utf8')
print(data.shape)

words = [char_normalise(str(word)) for word in data.iloc[:,0].to_list()]
syllables = [str(ipa) for ipa in data.iloc[:,1].to_list()]
freqs = [int(freq) for freq in data.iloc[:,2].to_list()]
phonemes ="".join(syllables)
phonemes = set(phonemes)
print(phonemes)

with open('unique_symbol.txt','r',encoding="utf-8") as ph_file:
    target_ch=ph_file.readlines()
df = pd.DataFrame(target_ch,columns=['TARGET'])
df = df.replace('\n','', regex=True)
target_chars=df.TARGET.to_list()
print("phonemes ",target_chars)
print(len(target_chars))
 #['’', "'", ',', 'j', '̃', ' ', '/', '̈', '.', '\n', 'ɪ', 'f', '\\', '।', '͡']



spaced_syllables = []
updated_words = []
#space separated phoneme representation
length =len(syllables)
print(length)
print(len(words))
for k in range(length):
    syllable = syllables[k]
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
        spaced_syllables.append(phone)
        updated_words.append(words[k])
        #print(phone)
    else:
        print(words)
df = pd.DataFrame(zip(updated_words,spaced_syllables,freqs))
df.columns = ['word','ipa','freq']
df.to_csv('output/word_ipa_freq_v1.csv' , index = None)
