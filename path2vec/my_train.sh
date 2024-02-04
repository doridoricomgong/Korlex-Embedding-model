#!/bin/bash

python3 embeddings_pytorch.py --input_file ./Korean_Korlex_dataset/pre_data_100/fixed_lchs_100.tsv.gz --vocab_file ./Korean_Korlex_dataset/korea_train/voca/new_kwn_korean_synsets_vocab.json.gz --use_neighbors True

python3 embeddings_pytorch.py --input_file ./Korean_Korlex_dataset/pre_data_100/fixed_shps_100.tsv.gz --vocab_file ./Korean_Korlex_dataset/korea_train/voca/new_kwn_korean_synsets_vocab.json.gz --use_neighbors True

python3 embeddings_pytorch.py --input_file ./Korean_Korlex_dataset/pre_data_100/fixed_wups_100.tsv.gz --vocab_file ./Korean_Korlex_dataset/korea_train/voca/new_kwn_korean_synsets_vocab.json.gz --use_neighbors True
