import os
import sys



if not os.path.exists('output'):
	os.makedirs('output')

os.system("python3 word_dist.py script_text_v2.txt")
print("g2p provider")
os.system("python3 g2p_provider.py output/word_freq.csv")
print("space separated")
os.system("python3 space_separated.py output/word_ipa_freq.csv")
print("phone dist......")
os.system("python3 phone_dist.py output/word_ipa_freq_v1.csv")
print("cv_analyzer............")
os.system("python3 cv_phoneme_analyzer.py output/word_ipa_freq_v1.csv")
print("dipthong............")
os.system("python3 dipthong_finder.py output/cv_file.csv")
print("coda_onset............")
os.system("python3 coda_onset.py output/cv_file.csv")
print("grapheme............")
os.system("python3 grapheme_dist.py output/word_freq.csv")
print("chandra_bindu_analysis............")
os.system("python3 chandra_bindu_analysis.py output/word_freq.csv")
print("contextual_cluster_finder............")
os.system("python3 contextual_cluster_finder.py output/word_freq.csv")
print("tri_gram_grapheme............")
os.system("python3 tri_gram_grapheme.py output/word_freq.csv")
os.system("python3 bi_graph_cluster.py output/word_freq.csv")
os.system("python3 bi_graph.py output/word_freq.csv")
os.system("python3 inflection_finder.py output/word_freq.csv")
