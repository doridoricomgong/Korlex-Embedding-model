import json

'''f = open('hypernym_dic.json')
hyper = json.load(f)
f.close()

f = open('hyponym_dic.json')
hypo = json.load(f)
f.close()'''

f = open('kwn_korean_synsets_vocab.json')
vocab = json.load(f)
f.close()
print(len(vocab))

'''vocab[8747]= '공고라교양주의자.n.00'
vocab[80372] = '22.n.00'
root = []

new_file_name = 'new_kwn_korean_synsets_vocab.json'

with open(new_file_name, 'w', encoding='utf-8') as f:
    f.write(json.dumps(vocab, indent=2))

for idx in range(len(hyper)):
    if len(hypo[str(idx)]) == 0 and len(hyper[str(idx)]) == 0:
        try:
            word, pos,_ = vocab[idx].split('.')
        except:
            print(idx, vocab[idx])
        #if pos == 'n':
        #    root.append(word)

print(len(root))
print(root)'''