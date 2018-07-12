# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import codecs
codecs.register(lambda name: codecs.lookup('latin-1'))

LANGUAGE = "spanish"
SENTENCES_COUNT = 2

# def sumariza(url):
# 	try:
# 		parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
# 		stemmer = Stemmer(LANGUAGE)
# 		summarizer = Summarizer(stemmer)
# 		summarizer.stop_words = get_stop_words(LANGUAGE)
# 		resumen = ''

# 		for sentence in summarizer(parser.document, SENTENCES_COUNT):
# 			resumen+=str(sentence)
# 			resumen+=str('\n')
# 		return {'data':resumen}
# 	except:
# 		return {'data: Error en URL proporcionado'}

def sumariza(entrada):
	entrada = entrada.replace(',',' ')
	try:
		parser = PlaintextParser.from_string(entrada, Tokenizer(LANGUAGE))
		stemmer = Stemmer(LANGUAGE)
		summarizer = Summarizer(stemmer)
		summarizer.stop_words = get_stop_words(LANGUAGE)
		resumen = ''
		for sentence in summarizer(parser.document, SENTENCES_COUNT):
			resumen+=str(sentence)
			#resumen+=str('\n')
		return {'data':resumen}
	except:
		return {'data': 'Error en la entrada de datos proporcionada..:'}

texto = """
Benito Pablo Juárez García nació el 21 de marzo de 1806 en el poblado
de San Pablo Guelatao, (palabra que en zapoteco quiere decir "noche honda"),3​
población ubicada en la cadena montañosa ahora conocida como Sierra Juárez y
entonces perteneciente a la jurisdicción de Santo Tomás de Ixtláncotoyol en el
estado de Oaxaca (en el presente el municipio de Guelatao de Juárez). Fue
bautizado al día siguiente de su nacimiento en la parroquia de Santo Tomás
Ixtlán.
  ​
El nombre de sus padres era Marcelino Juárez y Brígida García de acuerdo al acta
de bautismo levantada al día siguiente de su nacimiento​ y quien según sus propias
palabras, eran «indios de la raza primitiva del país​ y ambos fueron agricultores.
Los dos padres murieron cuando él tenía tres años; su madre durante el alumbramiento
de su hermana María Alberta Longinos. Benito junto con sus hermanas María Josefa
y Rosa quedaron bajo el amparo de sus abuelos paternos Pedro Juárez y Justa
López igualmente indios de la «nación zapoteca» y su muy pequeña hermana María
Longinos con su tía materna Cecilia.6​ A los pocos años murieron también sus
abuelos y las dos hermanas mayores de Benito se casaron, quedando él finalmente
bajo la custodia de su tío Bernardino Juárez. A partir de entonces trabajó
como peón del campo y como pastor de ovejas hasta la edad de doce años. Su tío
Bernardino conocía el castellano y se lo enseñaba a Benito que mostraba entusiasmo
en aprenderlo, sin embargo, las labores del campo y el hecho de que en el pueblo
no se hablara el castellano no permitieron que Benito avanzase mucho en su
aprendizaje. En su pueblo, como sucedía en las poblaciones pequeñas, no existía
ni la más elemental escuela. Benito se daba cuenta que quienes aprendían a
leer lo hacían viajando a la ciudad, ya sea costeándose una pensión o trabajando
como sirvientes en las casas ricas, lo que alimentó su deseo de ir a la
ciudad, lo cual solicitaba a su tío con mucha frecuencia sin concederle este
jamás su deseo. Finalmente, el 17 de diciembre de 1818 Benito decidió
marcharse de su pueblo natal después de haber elegido entre los sentimientos
y su deseo de educarse. Dirigió sus pasos a la ciudad de Oaxaca.6​ Esta
fuga pudo motivarse tras haber perdido una oveja y evitar el castigo que
le esperaba.7​8​ Hasta este momento la lengua única de Juárez era el zapoteco
siendo sus conocimientos de castellano básicos.
"""
print("Texto:\n", texto)
resumen = sumariza(texto)
restokens = resumen['data'].split()
line = []
resumen2 = ''
for i, word in enumerate(restokens):
    if i % 13 == 0 and i != 0:
        line.append(word)
        resumen2 += " ".join(line) + '\n'
        line = []
    elif i >= len(restokens) - 1:
        line.append(word)
        resumen2 += ' '.join(line)
    else:
        line.append(word)
print("Resumen:\n", resumen2)
