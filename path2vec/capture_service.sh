#!/bin/bash
while :
do
  pid=`ps -ef | grep 'embeddings_pytorch.py' | grep -v 'color' | awk '{print $2}'`
  if [ -z "$pid" ]; then
    echo $(date)
    echo "$pid"
    for vsize in new_korean_jcn-semcor.tsv.gz new_korean_shp.tsv.gz new_korean_wup.tsv.gz
        do
	    python3 embeddings_pytorch.py --input_file ./Korean_Korlex_dataset/korea_train/${vsize} --vocab_file ./Korean_Korlex_dataset/korea_train/voca/kwn_korean_synsets_vocab.json.gz --use_neighbors True
        done
  else
    echo "Running... " + "$pid"
  fi
  sleep 60
done

