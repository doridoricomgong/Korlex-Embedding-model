import json
import pandas as pd
import numpy as np
# Opening JSON file
f = open('/home/ben/Documents/NLP/path2vec/Korean_Korlex_dataset/korea_train/voca/kwn_korean_synsets_vocab.json')
# returns JSON object as
# a dictionary
kor_vocab = json.load(f)
# Closing file
f.close()

f = open('/home/ben/Documents/NLP/path2vec/Korean_Korlex_dataset/korea_train/voca/prev_vocab/korean_synsets_vocab.json')
# returns JSON object as
# a dictionary
pre_vocab = json.load(f)
# Closing file
f.close()
set1 = set(kor_vocab)
set2 = set(pre_vocab)

print(set2.difference(set1))
'''new_file_list = set()
data = pd.read_csv('OOV.txt', sep="  ", header=None, names=['vocab', 'idx'], engine='python')
vocabs = data['vocab'].values
check = 0
print(vocabs)
for idx, obj in enumerate(kor_vocab):
    if obj not in vocabs:
        new_file_list.add(obj)

new_file_name = 'rm_duplicate_new_korean_synsets_vocab.json'

with open(new_file_name, 'w', encoding='utf-8') as f:
    f.write(json.dumps(list(new_file_list), indent=2))'''
