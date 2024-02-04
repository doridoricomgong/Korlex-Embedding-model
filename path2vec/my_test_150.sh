#!/bin/bash

python3 evaluation.py new_lch_embeddings_vsize300_bsize100_lr001_nn-True3_reg-False_graph_emb.vec.gz Korean_Korlex_dataset/test_data/lch_test.tsv Korean_Korlex_dataset/test_data/lch_test.tsv 

python3 evaluation.py new_shp_embeddings_vsize300_bsize100_lr001_nn-True3_reg-False_graph_emb.vec.gz Korean_Korlex_dataset/test_data/shp_test.tsv Korean_Korlex_dataset/test_data/shp_test.tsv 

python3 evaluation.py new_wup_embeddings_vsize300_bsize100_lr001_nn-True3_reg-False_graph_emb.vec.gz Korean_Korlex_dataset/test_data/wup_test.tsv  Korean_Korlex_dataset/test_data/wup_test.tsv 

