import spaghetti as sgt
import re
import nltk
import numpy as np
import json

# pip install cucco==1.0.0
from cucco import Cucco
normEsp = Cucco(language='es')
norms = ['remove_accent_marks']

def regexextractor(expression, field):
    pattern = patterns[field]
    result = re.search(pattern=pattern, string=expression)
    if result:
        return result.group()
    else:
        return None

def do_tagging(exp, field, listTags):
    tokens = nltk.word_tokenize( [normEsp.normalize(exp),norms][0])
    # tokens = nltk.word_tokenize(exp)
    tagged = sgt.pos_tag(tokens)
    #print("tagged:",tagged)
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
    print('chunked:',chunked)
    continuous_chunk = []
    entity = []
    unknowns = []
    subt = []
    for i, subtree in enumerate(chunked):
        if isinstance(subtree, nltk.Tree) and subtree.label() == "NP":
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


#def testRegex():
    #print(regexextractor2("El estatus es de cancelaweewwewewewewe", "estados_valores"))


def folios(phrase, tipoFolio):
    # Tipo Folio puede ser Inicio o Fin

    # Gramática
    grammarFolio = r"""
                  NP: {<Folio> <tipoFolio> <Es> <dato>}
                  NP: {<Folio> <tipoFolio> <aq0cs0> <dato>}
                  NP: {<dato> <unknown|ncms000|aq0cs0|vmp00sm>* <Folio> <tipoFolio>}
                  NP: {<Folio> <tipoFolio>+ <unknown|ncms000|aq0cs0|vmp00sm>* <dato>}
                  NP: {<Folio> <unknown> <aq0cs0> <tipoFolio> <dato>}
                  NP: {<dato> <unknown> <Folio> <tipoFolio>}
                  NP: {<tipoFolio> <Folio> <unknown|ncms000|aq0cs0|vmp00sm>? <dato>}
                  NP: {<Folio> <tipoFolio> <ncfs000> <dato>}
                  NP: {<Folio> <tipoFolio> <tipoFolio> <vmp00sm><dato>}
                  NP: {<Folio> <dato> <tipoFolio> }
                  NP: {<vmip3p0> <Folio> <dato> }
                """

    grammarFolio = grammarFolio.replace("tipoFolio", tipoFolio)
    listTags = ["Inicio", "Fin", "Es"]

    return prueba(grammarFolio, phrase, "Folio", listTags)




def pruebasFolios():
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
        "con estatus igual a Cerrado",
        "Cerrado",
        "Que han sido canceladas",
        "Que fueron recibidas",
        "Que ya han sido canceladas",
        "Que tienen el estatus de aceptado",
        "y cerrado como estatus",

    ]

    expsBuenas_FolioInicio = [
        "facturas donde el folio de inicial es 0123",
        "y con folio de inicio igual a 000012",
        "con rango de folio  entre el inicial de 123456789",
        "9037432  es el folio de inicio",
        "El folio de inicio es el 002930200",
        "En folio de inicio asignamos el 2373893",
        "Para folio de inicio el valor de 11111111",
        "cuyo folio de inicio es el 222222",
        "folio de inicio igual a 78923430",
        "El folio de inicio definido en 23432",
        "con folio inicial igual a 568768",
        "con folio inicial  de  709898798",
        "el folio inicial es el  689778",
        "folio inicial de 6987687",
        "folio Inicial definido en 79876767878 ",
        "23432 es el folio de inicio",
        "y asignamos 56987 como folio inicial",
        "cuyo folio mas reciente de inicio es el 5687",
        "6987898 es el ultimo folio de inicio",
        "el folio inicial es el 6987879",
        "tenemos un folio de inicialización de 679876",
        "y donde 6987867 es el folio de inicio definido",
        "con folio inicial asignado de 569876",
        "folio de inicialización de 69879879",
        "folio de inicio asignado a 5986987",
        "dame las facturas con folio de inicio igual a 6987987",
        "con comienzo de folio en 69887",
        "con inicialización de folio o folio de inicio de 69979",
        "Ademas de que el folio de comienzo de serie es el 60978",
        "el folio de comienzo es el 7098",
        "y un folio inicial o de inicio de 709098",
        "con folio con principio de serie de 698987",
        "dame las facturas que principian con el folio 09900909",
        "Quiero las facturas con inicialización de folio en 97980990",
        "Requiero las facturas cerradas pero que inicien con el folio 6899879",
        "por favor factoras con inicialización de folio en 89989",
        "notas de credito cuyo folio inicial es el 9889897979",
        "908908908 como folio de inicialización",
        "908908908 como folio de inicio",
        "908908908 es el folio de inicio",
        "dame las facturas que inician con el folio 987879797897",
        "quiero facturas con folio inicial o de inicio definido en  6999897979",
        "necesito las facturas donde el folio de comienzo es 433554",
        "necesito las facturas que comienzan con el folio 7998989",
        "solicito las facturas cuo folio de inicia empieza en 7898908",
        "quiero facturas que empiezan con el folio 68799889",
        "el folio 79898798 es el de inicio"
    ]

    expsBuenas_FolioFin = [
        "con folio de finalización igual a 69898",
        "el folio de finalizado es 6980987",
        "el folio de fin es el 698798",
        "con folio de fin en 6987",
        "el folio de finalizacion es 98798787",
        "en folio de finalización asignamos 6988",
        "con folio de finalizado igual a 232343",
        " y el folio final de 65656",
        "el folio de finalización es el 12342",
        "con folio de finalización de 98573",
        "en folio de finalización ponemos 2334",
        "y 87664 como folio de finalización",
        "el folio final es 42445",
        "con folio de finalización definido en 42455",
        "el folio de finalización es 62564",
        "en folio de finalización asignamos el 9873",
        "9877 es el folio de finalización",
        "53457 es el folio de finalizado",
        "y con folio de finalización o de fin en 69887",
        "el folio final es igual a 2334544",
        "el folio termina en 6798",
        "con folio final definido a 698787",
        "y un folio de finalización igual a 23443",
        "asi como un folio de fin de 6797898989",
        "56987987 es el folio de finalización",
        "56987987 es el folio de finalización",
        "56987987 es el folio de cierre",
        "como folio de cierre o de fin ponemos el 698987",
        "el folio de fin es el 798988",
        "679897 es el ultimo folio de finalizado",
        "el reciente folio de finalizado es el 9898787",
        "el folio 79898798 es el de finalización",
        "como finalización de folio ponemos el 698988",
        "y con folio de fin definido en 69887",
        "como folio de finalizado se tiene el 69898",
        "en folio de finalizado asignamoe el valor 609898",
        "para el folio de finalizado ponemos 435665",
        "9880708 es el valor del folio de final",
        "11111 es nuestro folio de finalización",
        "11111 es mi folio de finalización",
        "mi folio de finalización es el 222222",
        "nuestro valor de finalización en folio es el 697988",
        "folio de finalizado es 689080880",
        "para folio de finalizado asignamos el 67879799",
        "en el cierre de folio ponemos el 68808080808",
    ]


    # for phrase in expsBuenas_FolioInicio:
    #     print("Resulado: {0}\n".format(str(folios(phrase, "Inicio"))))

    for phrase in expsBuenas_FolioFin:
        print("Resulado: {0}\n".format(str(folios(phrase, "Fin"))))




########################## Programa  #############################
dictfacturas = json.load(open("facturaskeys.json"))
#print("Diccionario:\n{0}\n\n".format(str(dictfacturas)))

patterns = dict(Cuenta=r"\b[A-Za-z]{3}\d{3}\b",
                Prefijo=r"\b[1-9a-zA-Z]\w{0,3}\b",  # wvect
                NoDocumento=r"\b[0-9a-zA-Z\-]{1,40}\b",  # w2vect
                NitAdquirienteMex=r"\b[A-Za-z]{4}\d{6}[A-Za-z0-9]{3}\b",
                Folio=r"\d{1,16}",
                Estados_valores=r"\bcerrad\w{0,30}|firmad\w{0,30}|enviad\w{0,30}|cancela\w{0,30}|acepta\w{0,30}|erro\w{0,30}\b",
                Acuse_valores=r"\bpendient\w{0,30}|rechaz\w{0,30}|acepta\w{0,30}\b")



###################### Pruebas Gabriel ##########################
def gabriel():
    pruebasFolios()

    #print(nltk.corpus.cess_esp.readme())

gabriel()
