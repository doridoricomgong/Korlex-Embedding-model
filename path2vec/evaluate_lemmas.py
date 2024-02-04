#!/usr/bin/python3
# coding: utf-8

from gensim import models, utils
import logging
import sys
from scipy import stats
from itertools import product
import json
from smart_open import smart_open

def evaluate_synsets(emb_model, pairs, our_logger, delimiter='\t', dummy4unknown=False, krx_api=None):
    '''f = open('./KorLex_API/kwn_korean_synsets_vocab.json')
    word_vocab = json.load(f)
    f.close()'''

    ok_vocab = [(w, emb_model.key_to_index[w]) for w in emb_model.index_to_key]
    ok_vocab = dict(ok_vocab)

    similarity_gold = []
    similarity_model = []
    oov = 0

    original_vocab = emb_model.key_to_index
    emb_model.key_to_index = ok_vocab

    for line_no, line in enumerate(smart_open(pairs)):
        line = utils.to_unicode(line)
        if line.startswith('#'):
            # May be a comment
            continue
        else:
            try:
                a, b, sim = [word for word in line.split(delimiter)]
                sim = float(sim)
            except (ValueError, TypeError):
                our_logger.info('Skipping invalid line #%d in %s', line_no, pairs)
                continue

            # Finding correct synsets
            synsets_a = krx_api.eval_synset(a.strip(), 'n')
            synsets_b = krx_api.eval_synset(b.strip(), 'n')

            if len(synsets_a) == 0 or len(synsets_b) == 0:
                oov += 1
                if dummy4unknown:
                    our_logger.debug('Zero similarity for line #%d with words with no synsets: %s',
                                     line_no, line.strip())
                    similarity_model.append(0.0)
                    similarity_gold.append(sim)
                    continue
                else:
                    our_logger.debug('Skipping line #%d with words with no synsets: %s',
                                     line_no, line.strip())
                    continue

            best_pair = None
            best_sim = 0.0
            for pair in product(synsets_a, synsets_b):
                possible_similarity = emb_model.similarity(pair[0], pair[1])
                if possible_similarity > best_sim:
                    best_pair = pair
                    best_sim = possible_similarity
            our_logger.debug('Original words: %s', line.strip())
            our_logger.debug('Synsets chosen: %s with similarity %f', best_pair, best_sim)
            similarity_model.append(best_sim)  # Similarity from the model
            similarity_gold.append(sim)  # Similarity from the dataset

    emb_model.key_to_index  = original_vocab
    spearman = stats.spearmanr(similarity_gold, similarity_model)
    pearson = stats.pearsonr(similarity_gold, similarity_model)
    if dummy4unknown:
        oov_ratio = float(oov) / len(similarity_gold) * 100
    else:
        oov_ratio = float(oov) / (len(similarity_gold) + oov) * 100

    our_logger.debug('Pearson correlation coefficient against %s: %f with p-value %f',
                     pairs, pearson[0], pearson[1])
    our_logger.debug(
        'Spearman rank-order correlation coefficient against %s: %f with p-value %f',
        pairs, spearman[0], spearman[1])
    our_logger.debug('Pairs with unknown words: %d', oov)
    return pearson, spearman, oov_ratio


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Loading model and semantic similarity dataset
    modelfile, simfile = sys.argv[1:3]

    model = models.KeyedVectors.load_word2vec_format(modelfile, binary=False)

    # Pre-calculating vector norms
    model.init_sims(replace=True)

    scores = evaluate_synsets(model, simfile, logger, dummy4unknown=True)

    name = modelfile.replace('_embeddings_', '_')[:-7]

    print(name + '\t' + str(scores[1][0]))
