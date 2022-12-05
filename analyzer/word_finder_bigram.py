import pandas as pd

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
    chars = chars.strip()
    return chars


data = pd.read_csv("cluster_bigrams.csv", encoding = "utf8")
bi_grams = [char_normalise(bigram) for bigram in data.bigram.to_list()]

data1 = pd.read_csv("pipilika_word_ipa.csv", encoding = "utf8")
words = [char_normalise(word) for word in data1.word.to_list()]
print('len of pipilika_words: ',len(words))
data2 = pd.read_csv("150k_words.csv",encoding = "utf8")
words2 = [char_normalise(word) for word in data2.word.to_list()]
print('len of 150k_words: ',len(words2))

final_words = list(set(words+words2))
print('len of final_words: ',len(final_words))

bigram_dict = dict()

for bigram in bi_grams:
	ex_list = []
	for word in final_words:
		if bigram in word:
			ex_list.append(word)
		if len(ex_list) >= 1:
			break
	bigram_dict[bigram] = ex_list[0]

df = pd.DataFrame(bigram_dict.values())
df.columns = ['example']
df.to_csv("output/cluster_bi_examples_only.csv",index = None)



