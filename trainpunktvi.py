import nltk
import pickle
import os

path_vi = 'K:/vi_txt/Train_Full/Chinh tri Xa hoi'


def load_vi(direc):
    print("I'm in!")
    ll = os.listdir(direc)
    text = ''
    for val, files in enumerate(ll):
        ff = open(direc + "/" + files, 'r', encoding='utf_16_le')
        listsen = ff.readlines()
        for li in listsen:
            if li[0] == ' ':
                li = li[1:]
            text += li.strip('\n').replace('\ufeff', '')
        if val % 1000 == 0:
            print(val)
    return text


txt = load_vi(path_vi)

trainer = nltk.tokenize.punkt.PunktTrainer()
trainer.INCLUDE_ALL_COLLOCS = True
trainer.train(txt)

tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer(trainer.get_params())
print(tokenizer)
# out = open("vi.pickle", "wb")
# pickle.dump(tokenizer, out)
# out.close()
