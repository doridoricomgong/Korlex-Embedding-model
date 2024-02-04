#!/usr/bin/python3
# coding: utf-8

import gensim
import logging
import sys
#from evaluate_lemmas import evaluate_synsets
'''from KorLex_API.KorLex_api import krx_api

ssInfo_path = "./KorLex_API/KorLex_api/dic/korlex_ssInfo.pkl"
seIdx_path = "./KorLex_API/KorLex_api/dic/korlex_seIdx.pkl"
reIdx_path = "./KorLex_API/KorLex_api/dic/korlex_reIdx.pkl"
kwn_std_path = "./KorLex_API/KorLex_api/dic/korlex_kwn_std.pkl"
krx_json_api = krx_api.KorLexAPI(ssInfo_path=ssInfo_path,
                                seIdx_path=seIdx_path,
                                reIdx_path=reIdx_path,
                                 kwn_std_path=kwn_std_path)
krx_json_api.load_synset_data()'''

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Loading model and semantic similarity dataset
modelfile, wordnet_scores, static_scores, human_scores = sys.argv[1:]

model = gensim.models.fasttext.load_facebook_vectors(modelfile)

wordnet_synset_score = model.evaluate_word_pairs(wordnet_scores, dummy4unknown=True, restrict_vocab=7000000)
static_synset_score = model.evaluate_word_pairs(static_scores, dummy4unknown=True, restrict_vocab=7000000)
human_synset_score = model.evaluate_word_pairs(human_scores, dummy4unknown=True, restrict_vocab=7000000)
#dynamic_synset_score = evaluate_synsets(model, '/home/ben/Documents/NLP/path2vec/Korean_Korlex_dataset/korean_eval/new_korean_simlex_original.tsv', logger, dummy4unknown=True, krx_api = krx_json_api)
eval_word_score = model.evaluate_word_analogies('kats_Xshoulder_matching.txt', dummy4unknown=True, restrict_vocab=7000000)

#name = modelfile.replace('_embeddings_', '_')[:-7]
name = modelfile
print('Model\tWordnet\tStatic\thuman\tanalogy')
print(name + '\t' + str(round(wordnet_synset_score[1][0], 4)) + '\t'
      + str(round(static_synset_score[1][0], 4)) + '\t'
      + str(round(human_synset_score[1][0], 4)) + '\t'
      + str(eval_word_score[0]))


