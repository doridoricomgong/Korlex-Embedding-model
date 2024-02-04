#!/usr/bin/python3
# coding: utf-8

import gensim
import logging
import sys
from evaluate_lemmas import evaluate_synsets
'''from KorLex_API.KorLex_api import krx_api

ssInfo_path = "./KorLex_API/KorLex_api/dic/korlex_ssInfo.pkl"
seIdx_path = "./KorLex_API/KorLex_api/dic/korlex_seIdx.pkl"
reIdx_path = "./KorLex_API/KorLex_api/dic/korlex_reIdx.pkl"
kwn_std_path = "./KorLex_API/KorLex_api/dic/korlex_kwn_std.pkl"
krx_json_api = krx_api.KorLexAPI(ssInfo_path=ssInfo_path,
                                seIdx_path=seIdx_path,
                                reIdx_path=reIdx_path,
                                 kwn_std_path=kwn_std_path)
krx_json_api.load_synset_data()
'''
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Loading model and semantic similarity dataset
modelfile, wordnet_scores, static_scores = sys.argv[1:]

model = gensim.models.KeyedVectors.load_word2vec_format(modelfile, binary=False)

wordnet_synset_score = model.evaluate_word_pairs(wordnet_scores, dummy4unknown=True)
#static_synset_score = model.evaluate_word_pairs(static_scores, dummy4unknown=True)
#dynamic_synset_score = evaluate_synsets(model, '/home/ben/Documents/NLP/path2vec/Korean_Korlex_dataset/korean_eval/new_korean_simlex_original.tsv', logger, dummy4unknown=True, krx_api = krx_json_api)
#eval_word_score = model.evaluate_word_analogies('./Korean_Korlex_dataset/new_word_analogy_korean.txt', dummy4unknown=True)

name = modelfile.replace('_embeddings_', '_')[:-7]

print('Model\tWordnet\tStatic\tanalogy')
print(name + '\t' + str(round(wordnet_synset_score[1][0], 4)) + '\t')
#      + str(round(static_synset_score[1][0], 4)) + '\t')
#      + str(eval_word_score[0]))
