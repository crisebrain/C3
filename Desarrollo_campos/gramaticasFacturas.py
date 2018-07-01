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


def do_chunking(grammar, tagged, field, code , posibles):
    # añadir las condiciones que sean necesarias para contemplar
    # los posibles valores
    # posibles = ["dato", "Z", "ncfs000", "ncms000", "Fz",
    #             "sps00"]
    # posibles son los tipos de palabras que pueden representar al dato

    cp = nltk.RegexpParser(grammar)
    chunked = cp.parse(tagged)
    #print(chunked)
    continuous_chunk = []
    entity = []
    unknowns = []
    subt = []
    for i, subtree in enumerate(chunked):
        if isinstance(subtree, Tree) and subtree.label() == "NP":
            if field in ["Prefijo", "NoDocumento"]:
                #print(subtree)
                for subsubtree in subtree.subtrees(filter=lambda t: t.label() == "Q"):
                    entity += [token for token, pos in subsubtree.leaves()]
                    subt.append(subsubtree)
                unknowns += [token for token, pos in subtree.leaves()
                             if pos in posibles]
            else:
                # añadir las condiciones que sean necesarias para contemplar los posibles valores
                entity += [token for token, pos in subtree.leaves()
                           if pos in posibles]
                unknowns += [token for token, pos in subtree.leaves()
                             if pos == "unknown"]
                subt.append(subtree)
    # Evalúa código de retorno
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
    return entity, code, #subt, "___________", tagged



def prueba(grammar, exp, field, listTags):
    tagged = do_tagging(exp.lower(), field, listTags)
    posibles = ["dato"]
    return do_chunking(grammar, tagged, field, 1, posibles)



######### Programa  ##############
dictfacturas = json.load(open("facturaskeys.json"))
#print("Diccionario:\n{0}\n\n".format(str(dictfacturas)))

patterns = dict(Cuenta=r"\b[A-Za-z]{3}\d{3}\b",
                Prefijo=r"\b[1-9a-zA-Z]\w{0,3}\b",  # wvect
                NoDocumento=r"\b[0-9a-zA-Z\-]{1,40}\b",  # w2vect
                NitAdquirienteMex=r"\b[A-Za-z]{4}\d{6}[A-Za-z0-9]{3}\b",
                Folio=r"\d{1,16}")



######## Pruebas Gabriel ####################
def gabriel():
    expsMalas = [
                    "y con folio de inicio igual a XXX",
                    "con rango de folio  entre el inical de AAAAA",
                    "REWEWETW  es el folio de inicio",
                    "El folio de inicio es el ERWERWREWT",
                    "En folio de inicio asignamos el QWEERE",
                    "Para folio de inicio el valor de QWERWERWER",
                    "cuyo folio de inicio es el WQERRTW",
                    "folio de inicio igual a QWERRT",
                    "El folio de inicio definido en QWERTTW",
                ]

    expsBuenas = [
                    "facturas donde el folio de inicial es 0123",
                    "y con folio de inicio igual a 000012",
                    "con rango de folio  entre el inical de 123456789",
                    "9037432  es el folio de inicio",
                    "El folio de inicio es el 002930200",
                    "En folio de inicio asignamos el 2373893",
                    "Para folio de inicio el valor de 11111111",
                    "cuyo folio de inicio es el 222222",
                    "folio de inicio igual a 78923430",
                    "El folio de inicio definido en 23432"
                ]


    grammar = r"""
                  NP: {<Folio> <sps00> <Inicio> <Es> <dato>}
                  NP: {<Folio> <sps00> <Inicio> <Es> <sps00> <dato>}
                  NP: {<dato> <Es> <da0ms0> <Folio> <sps00> <Inicio>}
                """

    field = "Folio"
    listTags = ["Inicio", "Fin", "Es"]


    for exp in expsBuenas:
        print("\n {0}".format(exp) )
        print(str(do_tagging(exp, field, listTags)))
        print(prueba(grammar, exp, field, listTags))

    # print("chunking:\n{0}".format(prueba(grammar, exp, field, listTags)))

    #print(nltk.corpus.cess_esp.readme())

#########################################################

gabriel()
