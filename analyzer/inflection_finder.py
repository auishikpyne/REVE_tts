import pandas as pd
import sys
def char_normalize(chars):
    chars = chars.replace(chr(2437)+chr(2494),chr(2438)) # অ + া = আ
    chars = chars.replace(chr(2503)+chr(2494),chr(2507)) # ে +  া = ো
    chars = chars.replace(chr(2503)+chr(2519),chr(2508)) # ে + ৗ  = ৌ
    chars = chars.replace(chr(2476)+chr(2492),chr(2480)) # ব    +   ়   =   র
    chars = chars.replace(chr(2465)+chr(2492),chr(2524)) # ড    +   ়   =   ড়
    chars = chars.replace(chr(2466)+chr(2492),chr(2525)) # ঢ    +   ়   =   ঢ়
    chars = chars.replace(chr(2479)+chr(2492),chr(2527)) # য    +   ়   =   য়
    chars = chars.replace(chr(8204),'') #zero width non-joiner = ''
    chars = chars.replace(chr(8205),'') # zero width joiner = ''
    chars = chars.replace(chr(65279),'')
    chars = chars.strip()
    return chars


def get_status(words,inf_list):
    inf_dict = dict()
    for inf in inf_list:
        inf_dict[inf] = 'no'
    length = len(words)
    for i in range(length):
        word = words[i]
        #word = char_normalize(word)
        for inf in inf_list:
            if word.startswith(inf):
                inf_dict[inf] = 'yes'
                #break
    return inf_dict

#==========================Main Module=========================
input_file = sys.argv[1]
data = pd.read_csv(input_file,index_col = False, sep = ',', encoding = 'utf-8')
print(data.shape)
words = [char_normalize(word) for word in data.word.to_list()]
freqs = data.freq.to_list()

with open('prefix.txt','r',encoding = 'utf-8') as file:
    target_ch=file.readlines()

df = pd.DataFrame(target_ch,columns=['TARGET'])
df = df.replace('\n','', regex=True)
inf_list = [char_normalize(word.strip()) for word in df.TARGET.to_list()]
print(inf_list)

inf_dict = get_status(words,inf_list)

sorted_dict = dict(sorted(inf_dict.items(), key=lambda x: len(x[1]),reverse = True))
df = pd.DataFrame(zip(inf_dict.keys(),inf_dict.values()))
df.columns = ['prefix', 'status']
df.to_csv('output/prefix_dist.csv', index = None)

print("Successfully Saved......")