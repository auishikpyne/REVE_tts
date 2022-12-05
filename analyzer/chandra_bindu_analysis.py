import numpy as np
import pandas as pd
import re
import sys

def add_to_dict(clus_dict,clus_list):
    for cluster in clus_list:
        if cluster in clus_dict:
            clus_dict[cluster] += 1
        else:
            clus_dict[cluster] = 1


#module for chandrabindu distribution
def get_chandrabindu_distribution(sentence_list):
    cluster_dict = dict()
    print(len(sentence_list))
    for sentence in sentence_list:
        full = "[ক-হড়-য়]্[ক-হড়-য়]"
        partial = "্[ক-হড়-য়]"
        vowel_sound = "[ািীুূৃে-ৌ]"
        cluster_list = re.findall(full+partial+partial+partial+vowel_sound+"ঁ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        
        cluster_list = re.findall(full+partial+partial+partial+"ঁ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        
        
        cluster_list = re.findall(full+partial+partial+vowel_sound+"ঁ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
            
        cluster_list = re.findall(full+partial+partial+"ঁ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        
        cluster_list = re.findall(full+partial+vowel_sound+"ঁ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        
           
        cluster_list = re.findall(full+partial+"ঁ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'') 

        cluster_list = re.findall(full+vowel_sound+"ঁ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        #print(sentence)
        
        cluster_list = re.findall(full+"ঁ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        #print(sentence)
        
        cluster_list = re.findall("[অ-ঋএ-হড়-য়]"+vowel_sound+"ঁ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        #print(sentence)
        cluster_list = re.findall("[অ-ঋএ-হড়-য়]"+"ঁ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        #print(sentence)


    sorted_dict = dict(sorted(cluster_dict.items(), key=lambda x: x[1],reverse = True))

    return sorted_dict


#module for chandrabindu distribution
def get_bisorgo_distribution(sentence_list):
    cluster_dict = dict()
    print(len(sentence_list))
    for sentence in sentence_list:
        #print(sentence)
        full = "[ক-হড়-য়]্[ক-হড়-য়]"
        partial = "্[ক-হড়-য়]"
        vowel_sound = "[ািীুূৃে-ৌ]"

        cluster_list = re.findall(full+partial+partial+partial+vowel_sound+"ঃ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        
        cluster_list = re.findall(full+partial+partial+partial+"ঃ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        
        
        cluster_list = re.findall(full+partial+partial+vowel_sound+"ঃ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
            
        cluster_list = re.findall(full+partial+partial+"ঃ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        
        cluster_list = re.findall(full+partial+vowel_sound+"ঃ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        
           
        cluster_list = re.findall(full+partial+"ঃ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'') 

        cluster_list = re.findall(full+vowel_sound+"ঃ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        #print(sentence)
        
        cluster_list = re.findall(full+"ঃ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        #print(sentence)
        
        cluster_list = re.findall("[অ-ঋএ-হড়-য়]"+vowel_sound+"ঃ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        #print(sentence)
        cluster_list = re.findall("[অ-ঋএ-হড়-য়]"+"ঃ", sentence)
        add_to_dict(cluster_dict,cluster_list)
        #print(cluster_list)
        #print(cluster_dict)
        for cluster in cluster_list:
            sentence = sentence.replace(cluster,'')
        #print(sentence)

    sorted_dict = dict(sorted(cluster_dict.items(), key=lambda x: x[1],reverse = True))

    return sorted_dict

#====================================Main Module============================================

##input and output file
input_file = sys.argv[1]
chan_output_file = 'output/chandrabindu.csv'
bisorgo_output_file = 'output/bisorgo.csv'
#file read module
#with open(input_file, encoding = 'utf8', mode = 'r') as file:
#    lines = file.readlines()
data = pd.read_csv(input_file, sep = ',')
word_list = data.word.to_list()
#data = pd.read_csv(input_file, index_col = False, encoding = 'utf8')
#sentence_list = [sentence.replace('\n','') for sentence in lines]
#print(len(sentence_list))
#data.columns = ["sentence"]
#size = data.shape[0]
#sentence_list = data.sentence.to_list()
#print(sentence_list)
chandra_dict = get_chandrabindu_distribution(word_list)
#print(sentence_list)
bisorgo_dict = get_bisorgo_distribution(word_list)

print('chandra_dict: ',chandra_dict)
print('bisorgo_dict: ',bisorgo_dict)

df = pd.DataFrame(zip(chandra_dict.keys(),chandra_dict.values()))
df.columns = ['type','freq']
df.to_csv(chan_output_file,index = False)


df = pd.DataFrame(zip(bisorgo_dict.keys(),bisorgo_dict.values()))
df.columns = ['type','freq']
df.to_csv(bisorgo_output_file,index = False)
