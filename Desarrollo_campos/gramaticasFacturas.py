import spaghetti as sgt
import re
import nltk
import numpy as np
import json
#pip install cucco==1.0.0
from cucco import Cucco
normEsp = Cucco(language='es')
norms = ['remove_accent_marks']


def regexextractor(expression, field):
    pattern = patterns[field]
    result = re.search(pattern=pattern, string=expression)
    if result:
        retorno = result.group()
        if( retorno.startswith('cerrad')) : retorno = 'cerrado'
        elif( retorno.startswith('firmad')) : retorno = 'firmado'
        elif( retorno.startswith('enviad')) : retorno = 'enviado'
        elif( retorno.startswith('cancela')) : retorno = 'cancelado'
        elif( retorno.startswith('acepta')) : retorno = 'aceptado'
        elif( retorno.startswith('erro')) : retorno = 'error'
        return retorno
    else:
        return None

def do_tagging(exp, field, listTags):
    tokens = nltk.word_tokenize( [normEsp.normalize(exp),norms][0])
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
    #print('chunked:',chunked)
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

######### Programa  ##############
dictfacturas = json.load(open("facturaskeys.json"))
#print("Diccionario:\n{0}\n\n".format(str(dictfacturas)))

patterns = dict(Cuenta=r"\b[A-Za-z]{3}\d{3}\b",
                Prefijo=r"\b[1-9a-zA-Z]\w{0,3}\b",  # wvect
                NoDocumento=r"\b[0-9a-zA-Z\-]{1,40}\b",  # w2vect
                NitAdquirienteMex=r"\b[A-Za-z]{4}\d{6}[A-Za-z0-9]{3}\b",
                Folio=r"\d{1,16}",
                Estados_valores=r"\bcerrad\w{0,30}|firmad\w{0,30}|enviad\w{0,30}|cancela\w{0,30}|acepta\w{0,30}|erro\w{0,30}\b",
                Acuse_valores=r"\bpendient\w{0,30}|rechaz\w{0,30}|acepta\w{0,30}\b")



######## Pruebas Gabriel ####################
def gabriel():

    expsMalas_11_FolioInicio = [
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

    expsBuenas_5_Estatus = [
                "con estatus igual a Cerrado",
                "Cerrado",
                "Que han sido canceladas",
                "Que fueron recibidas",
                "Que ya han sido canceladas",
                "Que tienen el estatus de aceptado",
                "y cerrado como estatus",

    ]
    expsBuenas_11_FolioInicio = [
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

    expsBuenas_12_FolioFin = [
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

    grammar_11_FolioInicio = r"""
                  NP: {<Folio> <Inicio> <dato>}
                  NP: {<Folio> <Inicio> <Es> <dato>}
                  NP: {<Folio> <Inicio> <aq0cs0> <dato>}
                  NP: {<Folio> <Inicio> <dato>}
                  NP: {<dato> <Folio> <Inicio>}
                  NP: {<Folio> <Inicio> <unknown> <dato>}
                  NP: {<Folio> <Inicio> <ncms000> <dato>}
                  NP: {<Folio> <Inicio> <vmp00sm> <dato>}
                  NP: {<Folio> <unknown> <aq0cs0> <Inicio> <dato>}
                  NP: {<dato> <unknown> <Folio> <Inicio>}
                  NP: {<Inicio> <Folio> <dato>}
                  NP: {<Folio> <Inicio> <ncfs000> <dato>}
                  NP: {<Folio> <Inicio> <Inicio> <dato>}
                  NP: {<Folio> <Inicio> <Inicio> <vmp00sm><dato>}
                  NP: {<Folio> <dato> <Inicio> }
                  NP: {<vmip3p0> <Folio> <dato> }
                """
    grammar_12_FolioFin = r"""
                  NP: {<Folio> <Fin> <aq0cs0> <dato>}
                  NP: {<Folio> <Fin> <dato>}
                  NP: {<Folio> <Fin> <unknown> <dato>}
                  NP: {<dato> <Folio> <Fin> }
                  NP: {<Folio> <Fin> <vmp00sm> <dato>}
                  NP: {<Folio> <Fin> <Fin> <dato>}
                  NP: {<Folio> <Fin> <Fin> <unknown> <dato>}
                  NP: {<dato> <unknown> <Folio> <Fin>}
                  NP: {<Folio> <dato> <Fin>}
                  NP: {<Fin> <Folio> <unknown> <dato>}
                  NP: {<Fin> <Folio> <dato> }
                  NP: {<Folio> <Fin> <unknown> <ncms000> <dato>}
                  NP: {<dato> <ncms000> <Folio> <Fin> }
                """
    grammar_05_Estatus = r"""
                  NP: {<Folio> <Fin> <aq0cs0> <dato>}
                """
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    #for exp in expsBuenas_5_Estatus:
    for exp in expsBuenas_11_FolioInicio:
    #for exp in expsBuenas_12_FolioFin:
        #print(' 05. evalua Estatus :',prueba(grammar_05_Estatus, exp, "Estados_valores", ["Estado"]),'\n')
        print('11. evalua Folio Inicio :',prueba(grammar_11_FolioInicio, exp, "Folio", ["Inicio"]),'\n')
        #print('12. evalua Folio Fin :',prueba(grammar_12_FolioFin, exp, "Folio", ["Fin"]),'\n')


    # print("chunking:\n{0}".format(prueba(grammar, exp, field, listTags)))

    #print(nltk.corpus.cess_esp.readme())

###########################################################
gabriel()
