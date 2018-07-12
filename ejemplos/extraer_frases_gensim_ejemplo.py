# coding: utf-8

import os
import sys
import re
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from gensim.models.phrases import Phraser, Phrases
import pandas as pd

def noPunctuation(sentence):
    return re.sub(pattern=r'[\!"#$%&\*+,-./:;<=>?@^_`()|~=]', repl='',
                  string=sentence)

def search4Phrases(sentences):
    """Segmentation of phrases in tokenized words to search for simple phrases.
    Parameters:
    Sentences - list of string Sentences.
    """
    bigram = Phrases(sentences, common_terms=common_terms, min_count=2,
                      threshold=1, delimiter=b' ', scoring="npmi")
    bigram_phraser = Phraser(bigram)
    tokens1 = bigram_phraser[sentences]
    trigram = Phrases(tokens1, min_count=2, threshold=2, delimiter=b' ')
    trigram_phraser = Phraser(trigram)
    tokens2 = trigram_phraser[tokens1]
    print(len(tokens2))
    print(tokens2)
    return tokens1, tokens2, trigram_phraser

def training(all_sentences):
    tokens1, tokens2, trigram_phraser = search4Phrases(all_sentences)
    # model = Word2Vec(all_sentences, min_count=3, size=200,
    #                  workers=2, window=5, iter=30)
    spanishdic = "/home/ramon/Downloads/SBW-vectors-300-min5.txt"
    model = KeyedVectors.load_word2vec_format(spanishdic, binary=False)
    return model, trigram_phraser

def makePhrases(thephraser, sentence):
    sentence = re.sub(pattern=r'[\!"#$%&\*+,-./:;<=>?@^_`()|~=]', repl='',
                      string=sentence)
    # sentence = [[e for e in sentence.split() if e not in punctuations]]
    sentence = [sentence.split()]
    print(sentence)
    return list(thephraser[sentence])

frases = pd.read_csv("/home/ramon/ebraintec/frases.txt", header=None,
                     index_col=0)

common_terms = ["de", "con", "para", "o", "y", "la"
                "el", "los", "las", "a", "por"]

frases = [noPunctuation(frase[0]) for frase in frases.values]

# all_sentences = [[word for word in doc.split(" ") if word not in common_terms] for doc in frases]
all_sentences = [doc.split(" ") for doc in frases]

model, tphraser = training(all_sentences)

print(makePhrases(tphraser, "quiero las facturas con acuse recibido, prefijo b, de la cuenta 13432 y rfc 34324"))

print(makePhrases(tphraser, "quiero las facturas con prefijo aaa133"))
# model.wv.get_vector("serie")
