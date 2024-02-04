import json
from KorLex_api.krx_api import *
import codecs

def vocab_from_file(inv_vocab):
    vocabulary = {}
    for no, word in enumerate(inv_vocab):
        vocabulary[word] = no
    return vocabulary


with codecs.open("./KorLex_api/kwn_korean_synsets_vocab.json", "r", encoding='utf-8', errors='ignore') as file_data:
    kor_vocab = json.load(file_data)
print(len(kor_vocab))
vocab_dic = vocab_from_file(kor_vocab)

'''f = open('./rm_duplicate_new_korean_synsets_vocab.json.gz')
kor_vocab = json.load(f)
vocab_dic = vocab_from_file(kor_vocab)
f.close()'''

ssInfo_path = "./KorLex_api/dic/korlex_ssInfo.pkl"
seIdx_path = "./KorLex_api/dic/korlex_seIdx.pkl"
reIdx_path = "./KorLex_api/dic/korlex_reIdx.pkl"
kwn_std_path = "./KorLex_api/dic/korlex_kwn_std.pkl"
krx_json_api = KorLexAPI(ssInfo_path=ssInfo_path,
                         seIdx_path=seIdx_path,
                         reIdx_path=reIdx_path,
                         kwn_std_path=kwn_std_path)
krx_json_api.load_synset_data()

hypernym_dict = {}
hyponym_dict = {}
hypernym_list = []
hyponym_list = []

neighbors_dict = {}
neighbors_nodes = []
for idx, obj in enumerate(kor_vocab):
    if idx%1000 == 0:
        print('pro: ', idx, '/', len(kor_vocab))
    synset = krx_json_api.synset(obj)
    if obj.split('.')[1] != 'n':
        print(obj)
        neighbors_dict[idx] = []
        continue

    hypernyms = synset.hypernyms()
    hyponyms = synset.hyponyms()
    for hyponym in hyponyms:
        if str(hyponym).split('.')[1] != 'n':
            continue
        hyponym_idx = vocab_dic.get(str(hyponym), -1)
        if hyponym_idx == -1:
            print(hyponym, hyponym_idx)
            continue
        neighbors_nodes.append(hyponym_idx)
        hyponym_list.append(hyponym_idx)
    for hypernym in hypernyms:
        if str(hypernym).split('.')[1] != 'n':
            continue
        hypernym_idx = vocab_dic.get(str(hypernym), -1)
        if hypernym_idx == -1:
            print(hypernym, hypernym_idx)
            continue
        neighbors_nodes.append(hypernym_idx)
        hypernym_list.append(hypernym_idx)
    neighbors_dict[idx] = neighbors_nodes
    hypernym_dict[idx] = hypernym_list
    hyponym_dict[idx] = hyponym_list
    neighbors_nodes = []
    hypernym_list = []
    hyponym_list = []

file_name = 'hypernym_list.json'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(json.dumps(hypernym_dict, indent=2))

file_name = 'hyponym_list.json'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(json.dumps(hyponym_dict, indent=2))

file_name = 'neighbor_list.json'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(json.dumps(neighbors_dict, indent=2))

