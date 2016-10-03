from gensim.models import word2vec

# txtファイルをText8Corpusに変換
data = word2vec.Text8Corpus('80.txt')
# 300次元ベクトルへword2vec
model = word2vec.Word2Vec(data, size=300)
voc=model.vocab.keys()

if __name__ == "__main__":

  for x in voc:
    print(x,end=" ")
    for y in model[x]:
      print(y,end=" ")
    print("")
