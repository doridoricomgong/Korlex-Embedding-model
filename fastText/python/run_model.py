import fasttext

# Skipgram model :
model = fasttext.train_unsupervised('alls.txt', model='skipgram', dim=300)
model.save_model("d300_model_fast.bin")
