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


# Para nuestras etiquetas personalizadas usamos listTags y ListRegExp.
# listTags etiqueta con base al facturaskeys.json
# listRegExp etiqueta con base a la expresiones regulares.
def do_tagging(exp, field, listTags, listRegExps=None):
    tokens = nltk.word_tokenize(exp)
    tagged = sgt.pos_tag(tokens)
    tagged = np.array([list(tup) for tup in tagged]).astype('|U16')

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
        if listRegExps is not None:
            for regExp in listRegExps:
                if regexextractor(token, regExp):
                    tagged[i, 1] = regExp

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


def do_chunking(tagged, field, posibles, grammar=None):
    if grammar is None:
        grammar = choice_grammar(field)
    cp = nltk.RegexpParser(grammar)
    chunked = cp.parse(tagged)
    entity = []
    unknowns = []
    subt = []

    for i, subtree in enumerate(chunked):
        if isinstance(subtree, nltk.Tree) and subtree.label() == "NP":
            if field in ["Prefijo", "NoDocumento", "NitAdquirienteMex", "Cuenta"]:
                # print(subtree)
                for subsubtree in subtree.subtrees(filter=lambda t: t.label() == "Q"):
                    entity += [token for token, pos in subsubtree.leaves()]
                    subt.append(subsubtree)
                unknowns += [token for token, pos in subtree.leaves()
                             if pos in posibles]
            elif field == "Fecha":
                fecha = {}
                for token, tag in subtree.leaves():
                    if tag in posibles:
                        fecha.setdefault(tag, token)
                entity.append(fecha)
            else:
                # añadir las condiciones que sean necesarias para contemplar
                # los posibles valores
                entity += [token for token, pos in subtree.leaves()
                           if pos in posibles]
                unknowns += [token for token, pos in subtree.leaves()
                             if pos == "unknown"]
                subt.append(subtree)

    # Prepara fechas
    if field == "Fecha":
        entity, code = preparaFechas(entity)
        return entity, code

    entity, code = code_validate(field, entity, unknowns,
                                 regex_taglist(field))
    return entity, code, subt, tagged


def preparaFechas(entity):
    import datetime
    from datetime import date

    fechaFin = None
    fechaInicio = None
    today = date.today()
    numberMonth = {
        "enero": 1,
        "febrero": 2,
        "marzo": 3,
        "abril": 4,
        "mayo": 5,
        "junio": 6,
        "julio": 7,
        "agosto": 8,
        "septiembre": 9,
        "octubre": 10,
        "noviembre": 11,
        "diciembre": 12
    }

    def buildDate(fechaDic):
        diasNum = {
            "primero": 1,
            "segundo": 2,
            "tercero": 3,
            "cuarto": 4,
            "quinto": 5,
            "sexto": 6,
            "séptimo": 7,
            "octavo": 8,
            "noveno": 9
        }

        y = today.year if fechaDic.get("AniosNum") is None else int(fechaDic["AniosNum"])
        m = today.month if fechaDic.get("Fecha") is None else fechaDic["Fecha"]
        m = numberMonth[m]

        d = fechaDic.get("DiasNum")
        if d is None:
            d = 1
        elif d in diasNum:
            d = diasNum[d]
        else:
            d = int(d)

        try:
            date = datetime.date(y, m, d)
            statusCode = 1
        except ValueError:
            date = datetime.date(y, m, 1)
            statusCode = 0  # Establece código

        return date, statusCode

    entity.reverse()
    for fecha in entity:
        if "Fin" in fecha and fechaFin is None:
            fechaFin = buildDate(fecha)
        elif "Inicio" in fecha and fechaInicio is None:
            fechaInicio = buildDate(fecha)

    # Evalúa código final
    statusCode = 0
    if fechaInicio[1] and fechaFin[1]:
        statusCode = 1

    return {"fechaInicio": fechaInicio[0], "fechaFin": fechaFin[0]}, statusCode


def code_validate(field, entity, unknowns, taglist):
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
        cond = any([True if regexextractor(entity, tag) is not None
                    else False for tag in [field] + taglist])
        if cond:
            code = 1
        else:
            code = 0
    return entity, code


def regex_taglist(field):
    if field == "NitAdquirienteMex":
        return ["datoNitCol"]
    else:
        return []


def prueba(grammar, exp, field, listTags, listRegExps, posibles):
    tagged = do_tagging(exp.lower(), field, listTags, listRegExps)

    return do_chunking(tagged, field, posibles, grammar)


def folios(phrase, tipoFolio):
    # Tipo Folio puede ser Inicio o Fin

    # Gramática
    # Q = "Es|sps00|da0ms0|unknown|Valor|cs|cc|Reciente|p0300000|dp1msp|spcms|dp1css"

    grammarFolio = r"""
    Q: {<unknown>}
                  R: {<Es|sps00|da0ms0|unknown|Valor|cs|cc|Reciente|p0300000|dp1msp|spcms|dp1css>}

                  NP: {<Folio> <Q>* (<tipoFolio> <Q|Prefijo>*){1,2} <dato|unknown>}
                  NP: {<Folio> <Q>* (<dato> <Q|Prefijo>*){1,2} <tipoFolio>}
                  NP: {<dato> <Q>* <Folio> <Q>* <tipoFolio>}
                  NP: {<tipoFolio> <Q>* <Folio> <Q>* <dato>}
                """

    # Remplazos
    # grammarFolio = grammarFolio.replace("Q", Q)
    grammarFolio = grammarFolio.replace("tipoFolio", tipoFolio)
    listTags = ["Inicio", "Fin", "Es", "Valor", "Prefijo", "Reciente"]

    return prueba(grammarFolio, phrase, "Folio", listTags)


def pruebasFolios():
    expsMalas = [
        "y con folio de inicio igual a xxxxx"
        # "con rango de folio  entre el inicial de AAAAA",
        # "REWEWETW  es el folio de inicio",
        # "El folio de inicio es el ERWERWREWT",
        # "En folio de inicio asignamos el QWEERE",
        # "Para folio de inicio el valor de QWERWERWER",
        # "cuyo folio de inicio es el WQERRTW",
        # "folio de inicio igual a QWERRT",
        # "El folio de inicio definido en QWERTTW",
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
    #     resultado = folios(phrase, "Inicio")
    #     if resultado[1] == 0:
    #         print("Resulado: {1}\n{0}\n\n".format(str(resultado[0:2]), resultado[2]))
    #
    # for phrase in expsBuenas_FolioFin:
    #     resultado = folios(phrase, "Fin")
    #     if resultado[1] == 0:
    #         print("Resulado: {1}\n{0}\n\n".format(str(resultado[0:2]), resultado[2]))

    # for phrase in expsBuenas_FolioFin:
    #     print("Resulado: {0}\n".format(str(folios(phrase, "Fin"))))

    for phrase in expsMalas:
        resultado = folios(phrase, "Inicio")
        # if resultado[1] == 0:
        print("Resulado: {1}\n{0}\n\n".format(str(resultado[0:2]), resultado[2]))


def fechas(phrase):
    # R = "<Es> <Desde> <da0ms0>"
    grammarFolio = r"""
                Q: {<De|Articulos|spcms|sps00|Es>}
                I: {<Inicio|Fin> <Q>{0,2} <sps00>?}
                NP: {<I> <DiasNum|ao0ms0> <Q>{0,2} <Fecha> <Q>{0,2} <AniosNum|DiasNum>}
                NP: {<I> <Fecha> <Q>{0,2} <DiasNum|ao0ms0> <Q>{0,2} <AniosNum|DiasNum>}
                NP: {<I> <DiasNum|ao0ms0>? <Q>{0,2} <Fecha> <Q>{0,2} <AniosNum|DiasNum>?}
                NP: {<I> <Fecha> <Q>{0,2} <DiasNum|ao0ms0>? <Q>{0,2} <AniosNum|DiasNum>}
                NP: {<I> <DiasNum|ao0ms0> <Q>{0,2} <Fecha>}
                """

    listTags = ["Inicio", "De", "Desde", "Es", "Fin", "Articulos"]
    listRegExps = ["AniosNum", "DiasNum"]
    posibles = ["Fecha", "AniosNum", "DiasNum", "Inicio", "Fin"]

    return prueba(grammarFolio, phrase, "Fecha", listTags, listRegExps, posibles)


def pruebasFechas():
    exps = [
        # "con fecha inicial del 15 de Febrero del 2017 , es todo gracias",
        # " cuya fecha inicial es desde el 1 de febrero del 2017",
        # "posteriores al primero de febrero del 2018",
        # "entre el 15 de noviembre del 17",
        # "con periodo del 1 de Marzo del 2017 ",
        # " desde marzo del 2017",
        # "posteriores al 24 de Septiembre",
        # "de Marzo primero del 2017",
        # "de noviembre ",
        # "desde Abril del 2017 ",
        # "a partir de la segunda semena de enero del año pasado",
        # "comprendidas en el periodo de Enero del 2017",
        # " generadas a partir del 6 de Noviembre del año pasado",
        # "generados desde el 8 de Abril del presente año",
        # " generadas desde el 5 del presente mes",
        # "con fecha del 5 de Abril del 2017",
        # "que oscilen entre el 4 de Junio",
        # "comprendidos entre Abril 7",
        # "con rango de fechas comprendido entre Abril 5",
        # "que datan del 4 de Abril del 2018",
        # "desde el último de marzo del 2017",
        # "entre el 23 de Junio del 2016",
        # "con fecha de inicio del 12 de Marzo del 2016",
        # "pero emitidas en Noviembre 17 del año pasado",
        # "pero cuyas fechas se encuentren entre el 1 de Diciembre",
        # "Del 1 de marzo",
        # "Del 3 de Mayo del año pasado ",
        # " entre el 5 de Marzo del 2018",
        # "que esten entre el día actual ",
        # "pero que tambien sean anteriores al 12 de Marzo del 18, esta claro",
        # "pero que sean anteriores al 14 de Junio",
        # "y el 24 de Febrero del 2018",
        # "al 5 de Noviembre",
        # "al mes actual",
        # "anteriores al 7 de Noviembre",
        # "hasta el mes pasado",
        # "anteriores a Enero del presente año",
        # "a Marzo del mismo año",
        # " al 6 de Noviembre del año pasado",
        # "y Septiembre 14 del año pasado",
        # "y Marzo 19 del presente año",
        # "previos al 15 de Enero del 2018",
        # "anteriores a Abril 9 de este año",
        # "hasta el día de hoy",
        # "y el primero de Marzo del año pasado",
        # "y fecha de fin del 13 de Noviembre del presente año",
        # "anteriores al 5 de Marzo del 2017",
        # "pero que sean previas al 15 de Marzo de este año.",
        # " y el 15 de Febrero del año pasado",
        # " y que sean previas al 6 de Noviembre de este año",
        # "al 9 de Noviembre del 2016",
        # "al 19 de Enero del presente año",
        # " previas al 5 de noviembre de este año",
        # "y el 6 de Enero del 2017",
        # "y posteriores al 14 de Diciembre"
        "facturas con fecha de inicio es 21 de febrero del 2009 y de fin 15 de marzo del 2018, gracias. y fecha de fin 24 de diciembre del 2000"
    ]

    expsAcordadas = [
        "fecha inicial del 5 de enero del 2015",
        "fecha inicial del 9 de Diciembre del 2013",
        "fecha de inicio al 12 de Marzo del 2013",
        "fecha de inicio al 12 de Noviembre del 2015",
        "fecha de comienzo del primero de enero del 2015",
        "fecha de comienzo del 21 de Enero del 2013",
        "fecha inicio de marzo del 2015",
        "fecha principio en Julio del 2015",
        "con periodo de inicio de Septiembre 23 del 2016",
        "iniciando en Septiembre 27 del 2012",
        "Con comienzo en Julio 23",
        "Con comienzo en Julio 45",
        "Iniciando el 14 de Mayo",
        "iniciando el 12 de Febrero",
        "inicia Del primero de enero",

        "Fecha final del 3 de Noviembre del 2017",
        "y finalizando al 4 de Marzo del 2014",
        "finalizando el 12 de Agosto de 1980",
        "concluyendo el 23 de Febrero de 1988",
        "y terminando el 12 de Julio de 1990",
        "concluyendo en Octubre 23",
        "con fecha de finalización a Septiembre del 2016",
        "hasta el 12 de Marzo",
        "la fecha de fin es el 12 de Abril",
        "terminando el 23 de diciembre del 2030",
        "y la fecha final es el 23 de Octubre",
        "fecha de conclusión de Noviembre 18",
        "Terminando el 12 Marzo del 2015",
        "y fecha de conclusión de documentos al 23 de Noviembre"
    ]

    for phrase in exps:
        resultado = fechas(phrase)
        # if resultado[1] == 0:
        print("Resulado: {1}\n{0}\n\n".format(str(resultado[0:2]), resultado[2]))


########################## Programa  #############################
dictfacturas = json.load(open("facturaskeys.json"))
# print("Diccionario:\n{0}\n\n".format(str(dictfacturas)))

patterns = dict(Cuenta=r"\b[A-Za-z]{3}\d{3}\b",
                Prefijo=r"\b[1-9a-zA-Z]\w{0,3}\b",  # wvect
                NoDocumento=r"\b[0-9a-zA-Z\-]{1,40}\b",  # w2vect
                NitAdquirienteMex=r"\b[A-Za-z]{4}\d{6}[A-Za-z0-9]{3}\b",
                Folio=r"\d{1,16}",
                Estados_valores=r"\bcerrad\w{0,30}|firmad\w{0,30}|enviad\w{0,30}|cancela\w{0,30}|acepta\w{0,30}|erro\w{0,30}\b",
                Acuse_valores=r"\bpendient\w{0,30}|rechaz\w{0,30}|acepta\w{0,30}\b",
                DiasNum=r"^[0-9]{1,2}$",
                AniosNum=r"^[0-9]{4}$",
                Fecha=r"^$"
                )


###################### Pruebas Gabriel ##########################
def gabriel():
    pruebasFechas()
    # pruebasFolios()

    # print(nltk.corpus.cess_esp.readme())


gabriel()
