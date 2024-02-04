import os
import pandas as pd
import gzip
import json
import numpy as np
#from KorLex_API.KorLex_api import krx_api

import json

'''# 서버의 주소입니다. hostname 또는 ip address를 사용할 수 있습니다.
HOST = '10.125.36.77'
# 서버에서 지정해 놓은 포트 번호입니다.
PORT = 9990

def send_and_get(send_str, answer):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        client_socket.sendall(send_str.encode())

        data_len = 0
        data_arr = bytearray()
        while True:
            try:
                data = client_socket.recv(1024)
                data_arr.extend(data)
                if not data:
                    break
            except:
                break

        text = data_arr.decode()
        res_data = text[:text.find('[\n ]\n}\n', ) + 7]
        result = json.loads(res_data)


        # print(data_len)
        # print(json.loads(data.decode()))
        client_socket.close()
        begin = send_str.find(answer)
        end = begin+len(answer) - 1
        return parse_wsd(result['sentence'][0]["WSD"], answer, begin, end)
    except SocketError as e:
        # 소켓을 닫습니다.
        client_socket.close()
        if 104 == e.errno:
            print("똑같은 데이터 재전달 해줘야됨 scoket errno 104는 어케 해결하는지 몰라...")
            print("짧은 줄 sent_str 한줄 같은거는 에러없이 잘되는듯?")
            print("아마 서버쪽에서 보낼려는거 버퍼 남아있어서 그런가 모르겠음.")
        print(e.errno)
        print("ERREERERERER !!!!")
def map_nouns(noun):
    if noun == "NNG" or noun == "NNP" or noun == "NNB" or noun == "NP":
        return 'n'
    else:
        return 'no'

def parse_wsd(wsd_list, answer, begin, end):
    sen = ""
    for ids in wsd_list:
        mapped = map_nouns(ids['type'])
        if mapped == 'no':
            continue
        else:
            #if ids['text'] == answer and (ids['begin'] != begin or ids['end'] != end):
            #    return "nonono"
            #else:
            sen += ids['text'] + '.' + mapped + '.' + ids['scode'] + ' '
    return sen'''

'''f = open('./KorLex_api/kwn_korean_synsets_vocab.json')
kor_vocab = json.load(f)
# Closing file
f.close()'''
#train_path = '../Korean_Korlex_dataset/korea_train/prev/korean_shp.tsv.gz'
#test_path = '../Korean_Korlex_dataset/korean_eval/prev/korean_simlex_shp.tsv'
#train_path = '../data/datasets/lch.tsv.gz'
#test_path = '../simlex/simlex_lch.tsv'
#train_path = '../../data/datasets/lch.tsv.gz'
#df = pd.read_csv(train_path, names=['vocab1', 'vocab2', 'score'],
#                             compression='gzip', header=None, sep='\t', quotechar='"', encoding='utf-8', engine='python')

'''ssInfo_path = "./KorLex_api/dic/korlex_ssInfo.pkl"
seIdx_path = "./KorLex_api/dic/korlex_seIdx.pkl"
reIdx_path = "./KorLex_api/dic/korlex_reIdx.pkl"
kwn_std_path = "./KorLex_api/dic/korlex_kwn_std.pkl"
krx_json_api = krx_api.KorLexAPI(ssInfo_path=ssInfo_path,
                                seIdx_path=seIdx_path,
                                reIdx_path=reIdx_path,
                                 kwn_std_path=kwn_std_path)
krx_json_api.load_synset_data()
test_path = '/home/ben/Downloads/topik_completion.csv'
df = pd.read_csv(test_path, sep=',', quotechar='"', encoding='utf-8', engine='python')
whole_sens = []
sense_id_ver = []
for idx, row in df.iterrows():
    answer = row[str(row['정답'])+'번']
    whole_sens.append(row['문제'].replace("()", answer))
    send_str = whole_sens[-1]
    nonono = send_and_get(send_str, answer)
    begin = nonono.find(answer)
    if begin == -1:
        continue
    real_answer = nonono[begin:begin+len(answer)+5]
    sense_id_ver.append([nonono.replace(real_answer, ''), real_answer])
    print(sense_id_ver[-1])


new_file_name = 'new_topik_completion.csv'
df1 = pd.DataFrame(sense_id_ver)
df1.to_csv(new_file_name,
                    sep=',',
                    header=False,
                    index=False,
                    encoding='utf-8'
                    )'''
'''new_line = []
f = open('word_analogy_korean.txt')
lines = f.readlines()
for line in lines:
    new_line.append(line.replace("\n\n", "\n").replace('\t', ' '))
    print(new_line[-1])
with open('new_word_analogy_korean.txt', 'w') as f:
    f.write(''.join(new_line))'''
'''test_path = '/home/ben/Downloads/ws353_korean.csv'
df = pd.read_csv(test_path, sep=',', quotechar='"', header=None, encoding='euc-kr', engine='python')
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df.to_csv('ws353_korean.tsv',
                    sep='\t',
                    header=False,
                    index=False,
                    encoding='utf-8'
                    )'''
'''f = open(test_path)
raw = f.readlines()
filtered = []
for line in raw:
    if line.startswith(':'):
        continue
    filtered.append(line.split())
df = pd.DataFrame(filtered, columns=['0','1','2','3'])
df = df[:5000]
temp0=[' ']*5000
temp1=[' ']*5000
temp2=[' ']*5000
temp3=[' ']*5000

for idx, row in df.iterrows():
    words0 = krx_json_api.eval_synset_from_word(row['0'], 'n')
    words1 = krx_json_api.eval_synset_from_word(row['1'], 'n')
    words2 = krx_json_api.eval_synset_from_word(row['2'], 'n')
    words3 = krx_json_api.eval_synset_from_word(row['3'], 'n')
    if len(words0) != 0 and len(words1) != 0 and len(words2) != 0 and len(words3) != 0:
        temp0[idx] = '/'.join(words0)
        temp1[idx] = '/'.join(words1)
        temp2[idx] = '/'.join(words2)
        temp3[idx] = '/'.join(words3)
    print(idx)
df['4'] = temp0
df['5'] = temp1
df['6'] = temp2
df['7'] = temp3
#df = pd.read_csv(test_path, sep=' ', quotechar='"', names=['vocab1', 'vocab2', 'vocab3', 'vocab4'], encoding='utf-8', engine='python')
print(df.head(3))
df.to_csv('new_word_analogy_korean.csv',
                    sep=',',
                    header=False,
                    index=False,
                    encoding='euc-kr'
                    )'''
'''temp1 = []
temp2 = []
hyper1 = [' ']*353
hypo1 = [' ']*353
holo1 = [' ']*353
hyper2 = [' ']*353
hypo2 = [' ']*353
holo2 = [' ']*353
print(len(hyper1))
for idx, row in df1.iterrows():
    words1 = krx_json_api.eval_synset_from_word(row['word 1'], 'n')
    words2 = krx_json_api.eval_synset_from_word(row['word 2'], 'n')
    if len(words1)!=0 and len(words2)!=0:
        if len(words1) != 1:
            po1 = ''
            per1 = ''
            lo1 = ''
            po2 = ''
            per2 = ''
            lo2 = ''
            for word in words1:
                test = krx_json_api.synset(word)
                per1 += '/'.join(map(str, test.hypernyms()))+'\n\n'
                print(per1)
                po1 += '/'.join(map(str, test.hyponyms()))+'\n\n'
                lo1 += '/'.join(map(str,test.member_holonyms()))+'\n\n'
            hyper1[idx] = per1
            hypo1[idx] = po1
            holo1[idx] = lo1
        if len(words2) != 1:
            for word in words2:
                test = krx_json_api.synset(word)
                per2 += '/'.join(map(str, test.hypernyms())) + '\n\n'
                po2 += '/'.join(map(str, test.hyponyms())) + '\n\n'
                lo2 += '/'.join(map(str, test.member_holonyms())) + '\n\n'
            hyper2[idx] = per2
            hypo2[idx] = po2
            holo2[idx] = lo2
        temp1.append('\n'.join(words1))
        temp2.append('\n'.join(words2))
    else:
        temp1.append(0)
        temp2.append(0)
df1['new_word1'] = temp1
df1['new_word2'] = temp2
df1['hyper1'] = hyper1
df1['hypo1'] = hypo1
df1['holo1'] = holo1
df1['hyper2'] = hyper2
df1['hypo2'] = hypo2
df1['holo2'] = holo2
new_df1 = df1[(df1['new_word1'].values!=0) & (df1['new_word2'].values!=0)]
print(len(new_df1))
print(df1.head(5)['hyper1'])
new_df1.to_csv('new_ws353.csv',
                    sep=',',
                    header=False,
                    index=False,
                    encoding='euc-kr'
                    )
    #if len(words1) == 1:
    #    df1.loc[idx]['new_word1']'''

'''set_train = set()
set_train = set_train.union(set(df['vocab1'].values))
set_train = set_train.union(set(df['vocab2'].values))
kor_vocab = list(set_train)
set_test = set()
set_test = set_test.union(set(df1['vocab1'].values))
set_test = set_test.union(set(df1['vocab2'].values))
print('각시.n.01' in set_train)
print(len(set_train.intersection(set_test)), len(set_test))

new_df = df1[df1['vocab1'].isin(kor_vocab) & df1['vocab2'].isin(kor_vocab)]
drop_df = df1[~(df1['vocab1'].isin(kor_vocab) & df1['vocab2'].isin(kor_vocab))]
print(len(df1), len(new_df), len(drop_df))'''
'''
new_df.to_csv('rm_'+test_path.split('/')[-1],
                    sep='\t',
                    header=False,
                    index=False,
                    encoding='utf-8'
                    )
drop_df.to_csv('drop_'+test_path.split('/')[-1],
                    sep='\t',
                    header=False,
                    index=False,
                    encoding='utf-8'
                    )'''


def map_format_of_std_num(std_num: str):
    if len(std_num) == 2:
        return std_num
    elif len(std_num) == 1:
        return '0' + std_num
    else:
        print('error', std_num)
        return std_num
'''f = open('../Korean_Korlex_dataset/korea_train/voca/kwn_korean_synsets_vocab.json')
kor_vocab = json.load(f)
# Closing file
f.close()'''

'''new_vocab = []
for vocab in kor_vocab:
    new_vocab.append(vocab.replace(" ", ""))

with open('new_kwn_korean_synsets_vocab.json', 'w') as f:
    json.dump(new_vocab, f)'''

'''# folder path
dir_path = '/home/ben/Documents/NLP/path2vec//Korean_Korlex_dataset/korean_eval/new_korean_simlex_jcn-semcor.tsv'
df1 = pd.read_csv(dir_path, names=['vocab1', 'vocab2', 'score'],sep='\t',
                             header=None, quotechar='"', encoding='utf-8', engine='python')
dir_path = '/home/ben/Documents/NLP/path2vec//Korean_Korlex_dataset/korean_eval/new_korean_simlex_lch.tsv'
df2 = pd.read_csv(dir_path, names=['vocab1', 'vocab2', 'score'],sep='\t',
                             header=None, quotechar='"', encoding='utf-8', engine='python')

df1['new_score'] = df2['score']
df1.to_csv('fse.tsv',
                  header=False,
                  index=False,
                  encoding='utf-8',
                  sep='\t')'''


'''df['str_score'] = df['score'].map(str)
df['transR_format'] = '(' + df['vocab1'] + ',' + df['vocab2'] + ',' + df['str_score'] + ')'

df['transR_format'].to_csv(dir_path.split('/')[-1].split('.')[0]+'_transR'+'.txt',
        header=False,
        index=False,)'''

#정제
'''dir_path = '/home/ben/Documents/NLP/path2vec/Korean_Korlex_dataset/korean_eval/simlex_synsets/'
# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        print(path)
        try:
            df = pd.read_csv(dir_path + path, names=['vocab1', 'vocab2', 'score'],
                             header=None, sep='\t', quotechar='"', encoding='utf-8', engine='python')
        except:
            print('error')
            pass
        print(len(df))
        df.drop_duplicates(inplace=True)
        print('after_dupl', len(df))
        df['vocab1'] = np.array(map(lambda x: x.replace(" ", "_"), df['vocab1'].values))
        df['vocab1'] = np.array(map(lambda x: x.replace(".", "",1) if x.count('.')!=2 else x, df['vocab1'].values))
        df['vocab1'] = np.array(map(lambda x: x.replace(".", "", 3) if x.count('.') != 2 else x, df['vocab1'].values))
        df['vocab2'] = np.array(map(lambda x: x.replace(" ", "_"), df['vocab2'].values))
        df['vocab2'] = np.array(map(lambda x: x.replace(".", "", 1) if x.count('.') != 2 else x, df['vocab2'].values))
        df['vocab2'] = np.array(map(lambda x: x.replace(".", "", 3) if x.count('.') != 2 else x, df['vocab2'].values))
        #get the data only in kwn
        new_df = df[df['vocab1'].isin(kor_vocab) & df['vocab2'].isin(kor_vocab)]
        drop_df = df[~(df['vocab1'].isin(kor_vocab) & df['vocab2'].isin(kor_vocab))]
        print(len(df), len(new_df))
        new_df.to_csv(dir_path+'new_'+path,
                            sep='\t',
                            header=False,
                            index=False,
                            encoding='utf-8'
                            )
        drop_df.to_csv(dir_path+'drop_'+path,
                     sep='\t',
                     header=False,
                     index=False,
                     encoding='utf-8'
                     )'''

'''for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        print(path)
        
        df = pd.read_csv(dir_path + path, names=['vocab1', 'vocab2', 'score'],
                         header=None, sep=',', quotechar='"', encoding='utf-8', engine='python')

        df.to_csv(dir_path + path + '.gz',
                  header=False,
                  index=False,
                  sep='\t',
                  compression="gzip")'''

#check to far score
'''dir_path = '/home/ben/Documents/NLP/path2vec//Korean_Korlex_dataset/korea_train/new_korean_shp.tsv.gz'
df1 = pd.read_csv(dir_path, names=['vocab1', 'vocab2', 'score'],sep='\t', compression='gzip',
                             header=None, quotechar='"', encoding='utf-8', engine='python')
print(len(df1[df1['score']<1/18].index))'''

dir_path = '/home/ben/Documents/NLP/path2vec//Korean_Korlex_dataset/korean_eval/rm_new_korean_simlex_wup.tsv'
fast_dir_path = '/home/ben/Documents/NLP/path2vec//Korean_Korlex_dataset/korean_eval/simlex_synsets/fast_rm_new_korean_simlex_wup.tsv'

df = pd.read_csv(dir_path, names=['vocab1', 'vocab2', 'score'],sep='\t',
                             header=None, quotechar='"', encoding='utf-8', engine='python')
df['vocab1'] = np.array(map(lambda x: x.split('.')[0], df['vocab1'].values))
df['vocab2'] = np.array(map(lambda x: x.split('.')[0], df['vocab2'].values))
df.to_csv(fast_dir_path,
                        sep='\t',
                        header=False,
                        index=False,
                        encoding='utf-8'
                        )