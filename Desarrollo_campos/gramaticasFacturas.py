import spaghetti as sgt
import re
import nltk
import numpy as np
import json

def regexextractor(expression, field):
    pattern = patterns[field]
    result = re.search(pattern=pattern, string=expression)
    if result:
        return result.group()
    else:
        return None

def do_tagging(exp, field, listTags):
    tokens = nltk.word_tokenize(exp)
    tagged = sgt.pos_tag(tokens)
    tagged = np.array([list(tup) for tup in tagged]).astype(str)

    # Inicializamos el diccionario de las etiquetas
    dicTags = {}
    for tag in listTags:
        dicTags.setdefault(tag, dictfacturas[tag])

    # Establecemos las etiquetas de cada palabra
    for i, token in enumerate(tokens):
        if token in dictfacturas[field]:
            tagged[i, 1] = str(field)
        for tag in dicTags:
            if token in dicTags[tag]:
                tagged[i, 1] = tag

    # Convertimos a tuplas y evalúamos si el dato potencialmente nos
    # interesa o no.
    mask = tagged[:, 1] == 'None'
    unknowns, = np.where(mask)
    for unknown in unknowns:
        if regexextractor(tokens[unknown], field) is not None:
            tagged[unknown, 1] = "dato"
        else:
            tagged[unknown, 1] = "unknown"
    return [tuple(wordtagged) for wordtagged in tagged]


def do_chunking(grammar, tagged, field, code):
    # añadir las condiciones que sean necesarias para contemplar
    # los posibles valores
    posibles = ["dato", "Z", "ncfs000", "ncms000", "Fz",
                "sps00"]
    # posibles son los tipos de palabras que pueden representar al dato

    cp = nltk.RegexpParser(grammar)
    chunked = cp.parse(tagged)
    continuous_chunk = []
    entity = []
    unknowns = []
    subt = []
    for i, subtree in enumerate(chunked):
        if isinstance(subtree, nltk.Tree) and subtree.label() == "NP":
            # añadir las condiciones que sean necesarias para contemplar los posibles valores
            entity += [token for token, pos in subtree.leaves()
                       if pos in posibles]
            unknowns += [token for token, pos in subtree.leaves()
                         if pos == "unknown"]
            subt.append(subtree)
    if entity == []:
        code = 0
        if len(unknowns) > 1:
            entity = unknowns[-1].upper()
        elif unknowns != []:
            entity = unknowns[0].upper()
        else:
            entity = None
    elif len(entity) > 1:
        code = 0
        entity = entity[-1].upper()
    else:
        entity = entity[0].upper()
        if regexextractor(entity, field) is not None:
            code = 1
        else:
            code = 0
    return entity, code, subt, tagged



def prueba(exp, field, listTags):
    tagged = do_tagging(exp.lower(), field, listTags)
    return do_chunking(grammar, tagged, field, 1)



######### Programa  ##############
dictfacturas = json.load(open("facturaskeys.json"))
#print("Diccionario:\n{0}\n\n".format(str(dictfacturas)))

patterns = dict(Cuenta=r"\b[A-Za-z]{3}\d{3}\b",
                Prefijo=r"\b[1-9a-zA-Z]\w{0,3}\b",  # wvect
                NoDocumento=r"\b[0-9a-zA-Z\-]{1,40}\b",  # w2vect
                NitAdquirienteMex=r"\b[A-Za-z]{4}\d{6}[A-Za-z0-9]{3}\b",
                Folio=r"\d{1,16}")



######## Pruebas Gabriel ####################
grammar = r"""
              NP: {<unknow> <pr\w+> <da0ms0> <Folio> <sps00> <Inicio> <vsip\w+> <dato>}
            """

# exp = 'facturas donde el folio de inicio fin final inicial empieza es 123'
exp = 'facturas donde el folio de inicio es 0123 y'
field = "Folio"
listTags = ["Inicio", "Fin"]


print("Tagging:\n{0}\n".format(
    str(do_tagging(exp, field, listTags))))

print("chunking:\n{0}".format(prueba(exp, field, listTags)))

#print(nltk.corpus.cess_esp.readme())

#########################################################