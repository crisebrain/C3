import re
import gensim
from gensim.models import KeyedVectors
import pandas as pd
import numpy as np
from ejemplos.patrones_busqueda_b2b import Regexseaker

frases = pd.read_csv("../frases.txt", header=None, index_col=0)

frases = np.array([frase[0] for frase in frases.values])

spanishdic = "/home/ramon/Downloads/SBW-vectors-300-min5.txt"

word_vectors = KeyedVectors.load_word2vec_format(spanishdic, binary=False)

# ejemplos
# word_vectors.distance("mujer", "hombre")
# word_vectors.distance("mujer", "rata")
# word_vectors.distance("mujer", "madre")
# word_vectors.most_similar("cuenta")
# word_vectors.most_similar("Quiero comer")
# word_vectors.most_similar("comer")
# word_vectors.most_similar("coger")
# word_vectors.most_similar("amor")
# word_vectors.most_similar("Gabriel")
# word_vectors.most_similar(positive=["mujer", "rey"], negative=["hombre"])
# word_vectors.similarity(["hembra"],["mujer"])
# word_vectors.similar_by_word("mujer")
# word_vectors.similar_by_word("coseno")
# word_vectors.n_similarity(["negativo"],["no"])
# word_vectors.n_similarity(["no"],["si"])
# word_vectors.n_similarity(["hembra"],["mujer"])

def evalua(frase1, frase2):
    print(frase1,"\n", frase2)
    wordsfrase1 = [palabra for palabra in frase1.split(" ") if palabra in word_vectors.vocab.keys()]
    wordsfrase2 = [palabra for palabra in frase2.split(" ") if palabra in word_vectors.vocab.keys()]
    print("1:\t", wordsfrase1, "2:\t", wordsfrase2)
    return word_vectors.n_similarity(wordsfrase1, wordsfrase2)

similarities = []
for frase in frases:
    similarities.append(evalua(frases[0], frase))

massim = np.argsort(similarities)[-10:]
print(frases[massim])


# import gensim
# import pandas as pd
# import numpy as np
# frases = pd.read_csv("../frases.txt", header=None, index_col=0)
# frases = np.array([frase[0].split(" ") for frase in frases.values])
# model = gensim.models.Word2Vec(frases, min_count=1)
# model.accuracy(["dame facturas"])
