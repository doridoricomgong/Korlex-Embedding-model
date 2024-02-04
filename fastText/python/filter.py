import pandas as pd

df = pd.read_csv('ws353_eng_score.tsv',encoding='cp949', engine='python', sep='\t')
df.to_csv('ws353_score_eng.tsv', encoding='utf-8', index=None, header=None, sep='\t')
