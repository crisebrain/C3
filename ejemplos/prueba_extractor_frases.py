from gensim.models import Phrases
import pandas as pd
frases = pd.read_csv("/home/ramon/ebraintec/frases.txt", header=None,
                     index_col=0)

frases = [frase[0] for frase in frases.values]

sentence_stream = [doc.split(" ") for doc in frases]
bigram = Phrases(sentence_stream)
sents = [u'dame', u'las', u'facturas', u'de', u'hoy', u'con', u'acuse', u'rechazado']
print(bigram[sents])

punctuations = [",", ";", ".", ":"]
stop = [".\n"]
sentence_stream = [[i for i in word_tokenize(sent) if i not in punctuations and i not in stop] for sent in sents]
bigram = Phrases(sentence_stream, min_count=2, threshold=2, delimiter=b' ')
bigram_phraser = Phraser(bigram)
tokens_ = bigram_phraser[sentence_stream]
trigram = Phrases(tokens_, min_count=2, threshold=2, delimiter=b' ')
trigram_phraser = Phraser(trigram)
tokens__ = trigram_phraser[tokens_]
all_words = [i for j in tokens__ for i in j]
all_words