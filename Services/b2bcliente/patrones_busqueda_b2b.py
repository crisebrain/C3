# from __future__ import print_function
from .spaghetti import pos_tag
import re
from nltk import word_tokenize, RegexpParser, Tree
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import numpy as np
import json

class Regexseaker:
    def __init__(self, pathkeys=None):
        """Inicialización de la clase de busquedas.
        1 expresiones regulares para los campos utilizados
        2 carga la lista de alias para cada campo
        """
        self.patterns = dict(Cuenta=r"\b[A-Za-z]{3}\d{3}\b",
                             Prefijo=r"\b[1-9a-zA-Z]\w{0,3}\b",  # wvect
                             NoDocumento=r"\b[0-9a-zñA-ZÑ\-]{1,40}\b",  # w2vect
                             NitAdquirienteMex=r"\b[A-Za-z]{4}\d{6}[A-Za-z0-9]{3}\b",
                             datoNitCol=r"\b\d{1,32}\b",
                             Tipo=r"\b[a-zA-Z]{1,10}\b",
                             Folio=r"\d{1,16}",
                             Estado=r"[A-Za-z]",   #[a-z]{1,16}"
                             Acuse=r"[A-Za-z]",
                             Periodo=r"\b[a-zA-Z]{1,12}\b",
                             Nums=r"\b\d+\b",
                             DiasNum=r"^[0-9]{1,2}$",
                             AniosNum=r"^[0-9]{4}$",
                             Fecha=r"^$"
                             )
        if pathkeys == None:
            pathkeys = "Services/b2bcliente/facturaskeys.json"
        self.dictfacturas = json.load(open(pathkeys))
        # Services/b2bcliente/facturaskeys.json"))

    def regexextractor(self, expression, field):
        pattern = self.patterns[field]
        result = re.search(pattern=pattern, string=expression)
        if result:
            return result.group()
        else:
            return None

    def do_tagging(self, exp, field, listTags, listRegExps=None):
        """
        Para nuestras etiquetas personalizadas usamos listTags y ListRegExp.
        listTags etiqueta con base al facturaskeys.json
        listRegExp etiqueta con base a la expresiones regulares.
        """

        tokens = word_tokenize(exp)
        tagged = pos_tag(tokens)
        tagged = np.array([list(tup) for tup in tagged]).astype('|U16')

        # Inicializamos el diccionario de las etiquetas
        dicTags = {}
        for tag in listTags:
            dicTags.setdefault(tag, self.dictfacturas[tag])

        # Establecemos las etiquetas de cada palabra
        for i, token in enumerate(tokens):
            if token in self.dictfacturas[field]:
                tagged[i, 1] = str(field)
            for tag in dicTags:
                if token in dicTags[tag]:
                    tagged[i, 1] = tag
            if listRegExps is not None:
                for regExp in listRegExps:
                    if self.regexextractor(token, regExp):
                        tagged[i, 1] = regExp

        # Convertimos a tuplas y evalúamos si el dato potencialmente nos
        # interesa o no.
        mask = tagged[:, 1] == 'None'
        unknowns, = np.where(mask)
        for unknown in unknowns:
            if self.regexextractor(tokens[unknown], field) is not None:
                tagged[unknown, 1] = "dato"
            else:
                tagged[unknown, 1] = "unknown"

        return [tuple(wordtagged) for wordtagged in tagged]

    def choose_grammar(self, field):
        dgramm = dict(Prefijo=""" Q: {<dato|Nums|unknown|(nc[fm][sp]000)|Singlel>}
                                  AUX1 : {<vmip1p0> <spcms|cs>}
                                  AUX2 : {<spcms> <Calce> <sps00>}
                                  AUX3 : {<aq0cs0> <sps00|spcms>}
                                  AUX4 : {<p0300000> <vmip3s0> <cs>}
                                  AUX5 : {<vmip3s0>? <Asignar> <sps00|cs>}
                                  AUX6 : {<vsip3s0|vssp3s0|cs> <da0ms0>?}
                                  AUX : {<AUX1|AUX2|AUX3|AUX4|AUX5|AUX6>}
                                  NP: {<Prefijo> <AUX|sps00|da0ms0>? <Sustnum>? <Q|sps00>}
                                  NP: {<Q|sps00|vsip3s0> <AUX> <Prefijo>}
                              """,
                               # directas
                               # inversas
                               # añadir que se hace con sustantivos y nodos terminales
                      NoDocumento=r""" Q: {<Singlel|cc|dato|Nums|(nc[mf][sp]000)>}
                                       AUX1 : {<vmip1p0> <spcms|cs>}
                                       AUX2 : {<spcms> <Calce> <sps00>}
                                       AUX3 : {<aq0cs0> <sps00|spcms>}
                                       AUX4 : {<p0300000> <vmip3s0> <cs>}
                                       AUX5 : {<vmip3s0>? <Asignar> <sps00|cs>}
                                       AUX6 : {<vsip3s0|vssp3s0|cs> <da0ms0>?}
                                       AUX : {<AUX1|AUX2|AUX3|AUX4|AUX5|AUX6>}
                                       NP: {<Sustnum> <sps00> <da0fs0>? <(NoDocumen\w+)> <AUX|Sustnum>? <Q|sps00>}
                                       NP: {<(NoDocumen\w+)> <sps00|Pronrelativo> <Sustnum> <AUX>? <Q|sps00>}
                                       NP: {<(NoDocumen\w+)> <sps00> <Q|sps00> <AUX> <Sustnum>}
                                       NP: {<Q> <AUX> <Sustnum> <sps00> <da0fs0>? <(NoDocumen\w+)>}
                                   """,
                      NitAdquirienteMex=r""" Q: {<unknown|dato|Z|Singlel|datoNitCol>}
                                             AUX1 : {<vmip1p0> <spcms|cs>}
                                             AUX2 : {<aq0cs0> <sps00|spcms>}
                                             AUX3 : {<vmip3s0>? <Asignar> <sps00|cs>}
                                             AUX4 : {<vsip3s0|vssp3s0|cs> <da0ms0>?}
                                             AUX: {<AUX1|AUX2|AUX3|AUX4>}
                                             NP: {<(NitA\w+)> <(NitA\w+)>? <sps00> <Sustnum> <AUX>? <Q|cc>}
                                             NP: {<(NitA\w+)> <(NitA\w+)>? <sps00> <Q> <AUX> <Sustnum>}
                                             NP: {<(NitA\w+)> <(NitA\w+)>? <AUX> <Q|cc>}
                                             NP: {<(NitA\w+)> <(NitA\w+)>? <Sustnum|(vs\w+)>? <da0ms0>? <Q|cc>}
                                             NP: {<Q> <AUX> <(NitA\w+)> <(NitA\w+)>?}
                                         """,
                      Cuenta=r""" Q: {<unknown|dato|Z|Singlel>}
                                  NP: {<Cuenta> <sps00>? <Sustnum>? (<aq0cs0|sps00|Es>){0,2} <Q>}
                                  NP: {<(da0\w+)>? <Sustnum>? <sps00|da0fs0>? <Cuenta> <(vs\w+)>? <Q>}
                                  NP: {<Sustnum> <sps00> <Cuenta> <sps00> <Sustnum> <aq0cs0> <sps00> <Q>}
                                  NP: {<Sustnum> <sps00> <Cuenta> <sps00> <Q> <cs> <Sustnum>}
                                  NP: {<sps00> <Cuenta> <aq0cs0> <sps00> <Q>}
                              """,
                      Estado=r""" Q: {<Recibido|Error|Firmado|Rechazado|Aceptado|Enviado>}
                                  NP: {<Estado> <vssp3s0|sps00|vsis3s0|Es|Valor|da0ms0|cs>{0,3} <Q>}
                                  NP: {<Q> <vssp3s0|vsis3s0|Es|da0ms0|cs>{1,3} <Estado>}
                                  NP: {<Estado> <vssp3s0|sps00|vsis3s0|Es|Valor|da0ms0|cs>{0,3} <.*>}
                                  NP: {<.*> <vssp3s0|vsis3s0|Es|da0ms0|cs>{1,3} <Estado>}
                              """,
                      Acuse=r""" Q: {<Rechazado|Aceptado|Pendiente>}
                                 NP: {<Acuse> <vssp3s0|sps00|vsis3s0|Es|Valor|da0ms0|cs>{0,3} <Q>}
                                 NP: {<Q> <vssp3s0|vsis3s0|Es|da0ms0|cs>{1,3} <Acuse>}
                                 NP: {<Acuse> <vssp3s0|sps00|vsis3s0|Es|Valor|da0ms0|cs>{0,3} <.*>}
                                 NP: {<.*> <vssp3s0|vsis3s0|Es|da0ms0|cs>{1,3} <Acuse>}
                             """,
                      Folio=r""" Q: {<Es|sps00|da0ms0|unknown|Valor|cs|cc|Reciente|p0300000|dp1msp|spcms|dp1css>}
                                 NP: {<Folio> <Q>{0,3} (<tipoFolio> <Q|Prefijo>*){1,2} <dato>}
                                 NP: {<Folio> <Q>{0,3} (<dato> <Q|Prefijo>*){1,2} <tipoFolio>}
                                 NP: {<dato> <Q>{1,3} <Folio> <Q>{0,3} <tipoFolio>}
                                 NP: {<tipoFolio> <Q>{1,3} <Folio> <Q>{0,3} <dato>}
                                 NP: {<Folio> <Q>{0,3} (<tipoFolio> <Q|Prefijo>*){1,2} <.*>}
                             """,
                      Periodo=r""" DP: {<semana|dia|mes|año>}
                                   NP1: {<presente|pasado> <DP>}
                                   NP2: {<DP> <sps00>? <presente|pasado>}
                                   NP3: {<sps00> <presente|pasado>}
                                   NP4: {<spcms|da0fs0|Periodo> <DP>}
                               """,
                      Tipo=r""" Q: {<TFactura|TNota>}
                                NP: {<Tipo> <sps00> <TDocumento> <pr0cn000>? <(vs\w+)>? <Q>}
                                NP: {<TDocumento>? <pr0cn000>? <(vs\w+)>? <sps00>? <Tipo> <Q>}
                                NP: {<TDocumento> <pr0cn000>? <(vs\w+)>? <Q>}
                                NP: {<Imperativo|vmip1s0> <(da0\w+)>? <Q> <sps00>? <TCredito>?}
                                NP: {<(da0\w+)|(vs\w+)|sps00> <Q>}
                                    }<Prefijo> <(vs\w+)|sps00>?{
                                NP: {<Tipo> <sps00> <TDocumento> <pr0cn000>? <(vs\w+)>? <(.*)>}
                                NP: {<TDocumento>? <pr0cn000>? <(vs\w+)>? <sps00>? <Tipo> <(.*)>}
                            """,
                      Fecha = r"""
                                Q: {<De|Articulos|spcms|sps00|Es>}
                                I: {<Inicio|Fin> <Q>{0,2} <sps00>?}
                                NP: {<I>? <DiasNum|ao0ms0> <Q>{0,2} <Fecha> <Q>{0,2} <AniosNum|DiasNum>}
                                NP: {<I>? <Fecha> <Q>{0,2} <DiasNum|ao0ms0> <Q>{0,2} <AniosNum|DiasNum>}
                                NP: {<I>? <DiasNum|ao0ms0>? <Q>{0,2} <Fecha> <Q>{0,2} <AniosNum|DiasNum>?}
                                NP: {<I>? <Fecha> <Q>{0,2} <DiasNum|ao0ms0>? <Q>{0,2} <AniosNum|DiasNum>}
                                NP: {<I>? <DiasNum|ao0ms0> <Q>{0,2} <Fecha>}
                                """
                      )
        return dgramm[field]

    def get_posibles(self, field):
        if field in ["Prefijo", "NoDocumento", "NitAdquirienteMex", "Cuenta"]:
            return ['Fz', 'Y', 'Z', 'cc', 'dato', 'nccn000', "ncms000",
                    'ncfs000', 'sps00', 'Singlel', 'unknown', "Nums", "Es"]
        elif field == "Folio":
            return ["dato"]
        elif field == "Estado" or field == "Acuse":
            return ["dato", "vmp00sm", "ncms000", "aq0msp", "unknown", "Fz", "Y"
                    "Z", "cc"]
        elif field == "Tipo":
            return ['Fz', 'Y', 'Z', 'cc', 'dato', 'nccn000', "ncms000",
                    'ncfs000', 'sps00', 'Singlel', 'unknown', "Nums", "Es"]
        elif field == "Fecha":
            return ["Fecha", "AniosNum", "DiasNum", "Inicio", "Fin"]

    def get_tags(self, field):
        if field == "Prefijo":
            return ["Singlel", "Calce", "Asignar", "Sustnum"]
        elif field == "NoDocumento":
            return ["Singlel", "Inicio", "Sustnum", 'Prefijo', 'Folio', "Fin",
                    'Valor', 'Reciente', 'Estado', 'Recibido', 'Error', 'Firmado',
                    'Rechazado', 'Aceptado', 'Enviado', 'Pendiente', 'Acuse',
                    "Pronrelativo", "Calce", "Asignar"]
        elif field == "NitAdquirienteMex":
            return ["Singlel", "Sustnum", "Asignar", "Calce"]
        elif field == "Cuenta":
            return ["Singlel", "Sustnum"]
        elif field == "Folio":
            return ["Inicio", "Fin", "Es", "Valor", "Prefijo", "Reciente"]
        elif field == "Estado":
            return ["Es","Valor","Recibido","Error","Firmado","Rechazado",
                    "Aceptado","Enviado", "Factura"]
        elif field == "Acuse":
            return ["Es","Valor","Rechazado","Aceptado","Pendiente"]
        elif field == "Periodo":
            return ["pasado", "presente", "semana", "dia", "mes", "año"]
        elif field == "Tipo":
            return ["Prefijo", "NoDocumento", "Sustnum", "Imperativo",
                    "TDocumento", "TFactura", "TNota", "TCredito"]
        elif field == "Fecha":
            return  ["Inicio", "De", "Es", "Fin", "Articulos"]

    def regex_taglist(self, field):
        if field == "NitAdquirienteMex":
            return ["datoNitCol"]
        elif field == "NoDocumento":
            return ["Nums"]
        elif field == "Prefijo":
            return ["Nums"]
        elif field == "Fecha":
            return ["AniosNum", "DiasNum"]
        else:
            return []

    def do_chunking(self, tagged, field, posibles, grammar=None):
        if grammar is None:
            grammar = self.choose_grammar(field)
        cp = RegexpParser(grammar)
        chunked = cp.parse(tagged)
        entity = []
        unknowns = []
        subt = []
        for i, subtree in enumerate(chunked):
            if isinstance(subtree, Tree) and subtree.label() == "NP":
                if field in ["Prefijo", "NoDocumento",
                             "NitAdquirienteMex", "Cuenta",
                             "Estado", "Acuse", "Tipo"]:
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
                    subt.append(subtree)
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
            entity, code = self.__preparaFechas(entity)
            return entity, code, subt

        entity, code = self.code_validate(field, entity, unknowns,
                                          self.regex_taglist(field))
        return entity, code, subt, tagged


    def __preparaFechas(self, entity):
        import datetime
        from datetime import date

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

            # Establece la fecha al día, si no se puede la corrige.
            try:
                date = datetime.date(y, m, d)
                statusCode = 1
            except ValueError:
                date = datetime.date(y, m, 1)
                statusCode = 0  # Establece código

            # Evalúamos años posteriores
            if date.year > today.year:
                date = date.replace(year=today.year)

            return date, statusCode

        def selectCaseDate():
            nonlocal fechaInicio, fechaFin, fechaEspecifica, firstSpecificDate

            if not firstSpecificDate:
                # Caso 1: dan fecha fin, pero no de inicio.
                if fechaFin and fechaInicio is None:
                # if "fechaFin" in dicDates and not "fechaInicio" in dicDates:
                    fechaInicio = None, 1
                # Caso 2: dan fecha de inicio, pero no de fin
                elif fechaInicio and fechaFin is None:
                # elif "fechaInicio" in dicDates and not "fechaFin" in dicDates:
                    fechaFin = today, 1
            else:
                # Caso 3: fecha específica
                fechaInicio = fechaEspecifica
                fechaFin = fechaEspecifica

        def orderDate():
            nonlocal  fechaFin, fechaInicio

            # Validamos que existan las fechas y las ordenamos.
            if fechaInicio[0] and fechaFin[0] and \
                    fechaFin[0] < fechaInicio[0]:
                dateSwap = fechaInicio
                fechaInicio = fechaFin
                fechaFin = dateSwap

        fechaFin = None
        fechaInicio = None
        fechaEspecifica = None
        firstSpecificDate = False
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

        if len(entity) == 0:
            statusCode = 1
            fechaInicio = [None]
            fechaFin = [None]
        else:
            # Obtenemos fechas de las Entitys
            # Invertimos para interar desde el último elemento.
            entity.reverse()
            for fecha in entity:
                if "Fin" in fecha and fechaFin is None:
                    fechaFin = buildDate(fecha)
                elif "Inicio" in fecha and fechaInicio is None:
                    fechaInicio = buildDate(fecha)
                elif fechaEspecifica is None:
                    # Validamos si fecha específica fue la primera en ocurrir.
                    if fechaInicio is None and fechaFin is None:
                        firstSpecificDate = True
                    fechaEspecifica = buildDate(fecha)

            selectCaseDate()
            orderDate()

            # Evalúa código final
            statusCode = 0
            if fechaInicio[1] and fechaFin[1]:
                statusCode = 1

        return {"fechaInicio": fechaInicio[0], "fechaFin": fechaFin[0]}, statusCode

    def code_validate(self, field, entity, unknowns, taglist):
        # Calculo de código
        # -------------------------------------------------------------------
        if entity == []:
            code = 0
            if len(unknowns) > 1:
                entity = unknowns[-1]
            elif unknowns != []:
                entity = unknowns[0]
            else:
                entity = None
        elif len(entity) > 1:
            code = 0
            entity = entity[-1]
        else:
            entity = entity[0]
            cond = any([True if self.regexextractor(entity, tag) is not None
                        else False for tag in [field] + taglist])
            if cond:
                code = 1
            else:
                code = 0
        # -------------------------------------------------------------------
        # formato de resultado
        # -------------------------------------------------------------------
        if entity is not None:
            # Capitalizar los campos
            if field in ["Acuse", "Tipo", "Estado"]:
                # para pasar tipo de documento y no la palabra original
                if field == "Tipo":
                    if entity in self.dictfacturas["TNota"]:
                        entity = "Nota"
                    elif entity in self.dictfacturas["TFactura"]:
                        entity = "Factura"
                entity = entity.capitalize()
            # en mayusculas
            elif field in ["Prefijo", "NitAdquirienteMex",
                           "Cuenta", "NoDocumento"]:
                entity = entity.upper()
        # -------------------------------------------------------------------
        return entity, code

    def seakexpresion(self, expression, field="Cuenta", nl=7, lowerc=True):
        if lowerc:
            expression = expression.lower()
        if field in ["Prefijo", "Cuenta", "NitAdquirienteMex",
                     "Acuse", "Estado"]:
            words = self.dictfacturas[field]
            tokens = word_tokenize(expression)
            arrs = []
            # Busca palabra pivote
            for token in tokens:
                arrs.append((token, [words.index(token)+1 if token in words
                                     else False]))
            # Crea un arreglo con los indices de ocurrencias de alias
            d2arr = np.array([arr[1] for arr in arrs])
            # print(d2arr)
            # priorizacion de alias
            if any(d2arr[:, 0]):
                inds = np.argsort(d2arr[:, 0])
                mask = np.sort(d2arr[:, 0]) != 0
                # print(inds)
                inp = inds[mask][0]
                # print(inds[mask])
                if inp - nl < 0:
                    posible = " ".join(tokens[: inp + nl])
                else:
                    posible = " ".join(tokens[inp - nl: inp + nl])
            else:
                # resultado = None
                posible = None
            # print(posible)
            if posible is None:
                return (None, 1)
            taglist = self.get_tags(field)
            reglist = self.regex_taglist(field)
            tagged = self.do_tagging(posible, field, taglist, reglist)
            # print(tagged)
            posibles = self.get_posibles(field)
            return self.do_chunking(tagged, field, posibles)
        elif field in ["NoDocumento", "Tipo"]:
            taglist = self.get_tags(field)
            reglist = self.regex_taglist(field)
            tagged = self.do_tagging(expression, field, taglist, reglist)
            posibles = self.get_posibles(field)
            return self.do_chunking(tagged, field, posibles)
        elif field == "FolioInicio":
            return self.folios(expression, "Inicio")
        elif field == "FolioFinal":
            return self.folios(expression, "Fin")
        elif field == "Periodo":
            return self.chunks_period(expression, "Periodo")
        elif field == "Fecha":
            return self.__fechas(expression)

    def folios(self, phrase, tipoFolio):
        # Tipo Folio puede ser Inicio o Fin
        field = "Folio"
        # Gramática
        grammarFolio = self.choose_grammar(field)
        # Remplazos
        grammarFolio = grammarFolio.replace("tipoFolio", tipoFolio)

        listTags = self.get_tags(field)
        posibles = self.get_posibles(field)

        tagged = self.do_tagging(phrase.lower(), field, listTags)
        return self.do_chunking(tagged, field, posibles, grammarFolio)

    def __fechas(self, phrase):
        field = "Fecha"
        listRegExps = self.regex_taglist(field)
        listTags = self.get_tags(field)
        posibles = self.get_posibles(field)
        grammarFechas = self.choose_grammar(field)

        tagged = self.do_tagging(phrase.lower(), field, listTags, listRegExps)
        return self.do_chunking(tagged, field, posibles, grammarFechas)

    def chunks_period(self, exp, field):
        listTags = self.get_tags("Periodo")
        tagged = self.do_tagging(exp.lower(), "Periodo", listTags)
        grammar = self.choose_grammar("Periodo")
        cp = RegexpParser(grammar)
        chunked = cp.parse(tagged)
        dictime = {"pasado": 1, "presente": 0}
        dicinterval = {"dia": 1, "semana": 2, "mes": 3, "año": 4}
        period = dict(interval=None, time=None)
        subt = []
        for tree in chunked:
            if isinstance(tree, Tree):
                if tree.label() in ["NP1", "NP2"]:
                    for subtree in tree.subtrees(filter=lambda t: t.label() == "DP"):
                        period["interval"] = dicinterval[subtree.leaves()[0][1]]
                    for leave in tree.leaves():
                        if leave[1] in dictime.keys():
                            period["time"] = dictime[leave[1]]
                    subt.append(tree)
                elif tree.label() == "NP3":
                    for leave in tree.leaves():
                        if leave[1] in ["presente", "pasado"]:
                            period["time"] = dictime[leave[1]]
                            period["interval"] = dicinterval["dia"]
                    subt.append(tree)
                elif tree.label() == "NP4":
                    for subtree in tree.subtrees(filter=lambda t: t.label() == "DP"):
                        period["interval"] = dicinterval[subtree.leaves()[0][1]]
                        period["time"] = dictime["presente"]
                    subt.append(tree)
        # validacion para periodo, es diferente que para los otros campos
        conds = [[True] if item is not None else [False]
                 for item in period.values()]
        code, = np.logical_xor(*conds)
        code = not code
        cond = not(len(subt) > 1)
        code = code and cond
        return self.time_period(period), int(code)

    def time_period(self, period):
        result = dict(fechaInicio=None, fechaFin=None)
        if period["interval"] == 1 and period["time"] == 0:
            result["fechaInicio"] = datetime.now().date()
            result["fechaFin"] = datetime.now().date()
        if period["interval"] == 1 and period["time"] == 1:
            result["fechaInicio"] = (datetime.now() - timedelta(days=1)).date()
            result["fechaFin"] = datetime.now().date()
        if period["interval"] == 2 and period["time"] == 0:
            diacorriente = datetime.isoweekday(datetime.now())
            result["fechaInicio"] = (datetime.now() - timedelta(days=diacorriente)).date()
            result["fechaFin"] = datetime.now().date()
        if period["interval"] == 2 and period["time"] == 1:
            diacorriente = datetime.isoweekday(datetime.now())
            result["fechaInicio"] = (datetime.now() - timedelta(days=diacorriente+7)).date()
            result["fechaFin"] = result["fechaInicio"] + timedelta(days=6)
        if period["interval"] == 3 and period["time"] == 0:
            diames = datetime.now().day - 1
            result["fechaInicio"] = (datetime.now() - timedelta(days=diames)).date()
            result["fechaFin"] = datetime.now().date()
        if period["interval"] == 3 and period["time"] == 1:
            diames = datetime.now().day - 1
            primero = datetime.now() - timedelta(days=diames) - relativedelta(months=1)
            result["fechaInicio"] = primero.date()
            result["fechaFin"] = (datetime.now() - timedelta(days=diames + 1)).date()
        if period["interval"] == 4 and period["time"] == 0:
            year, weeks, weekday = datetime.isocalendar(datetime.now())
            result["fechaInicio"] = (datetime.now() - timedelta(weeks=weeks-1, days=weekday - 1)).date()
            result["fechaFin"] = datetime.now().date()
        if period["interval"] == 4 and period["time"] == 1:
            year, weeks, weekday = datetime.isocalendar(datetime.now())
            result["fechaInicio"] = (datetime.now() - relativedelta(weeks=weeks-1, days=weekday - 1, years=1)).date()
            result["fechaFin"] = result["fechaInicio"] + relativedelta(days=364)
        return result



def pruebasFolios():
    reg = Regexseaker()

    expsMalas = [
        "y con folio de inicio igual a xxxxx",
        "con rango de folio  entre el inicial de AAAAA",
        "REWEWETW  es el folio de inicio",
        "El folio de inicio es el ERWERWREWT",
        "En folio de inicio asignamos el QWEERE",
        "Para folio de inicio el valor de QWERWERWER",
        "cuyo folio de inicio es el WQERRTW",
        "folio de inicio igual a QWERRT",
        "El folio de inicio definido en QWERTTW",
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
    for phrase in expsMalas: #+ expsBuenas_FolioInicio:
        resultado = reg.seakexpresion(phrase, "FolioInicio")
        if resultado[1] == 0:
            print("Resulado: {0}\n{1}\n".format(str(resultado[:2]),resultado[3]))


def pruebasFechas():
    reg = Regexseaker()

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

    expsCasos = [
        "quiero mi facturas con fecha de inicio 3 de septiembre del 2017",
        "quiero mi facturas con fecha de fin 3 de septiembre del 2017",
        "quiero mi facturas con fecha de inicio 3 de septiembre del 2017 y fin de diciembre del 2018",
        "quiero mi facturas con fecha de 3 de septiembre del 2017",
        "quiero mi facturas con fecha de inicio 3 de septiembre del 2017 y fin de diciembre del 2018 además 1 de enero del 2018",
        "quiero mi facturas con fecha de inicio 3 de septiembre del 2017 además 1 de enero del 2018 y fin de diciembre del 2018",
        "quiero mi facturas además 1 de enero del 2018 con fecha de inicio 3 de septiembre del 2017 y fin de diciembre del 2018",
        "quiero mi facturas además 1 de enero del 2018 con 3 de septiembre del 2017 y de diciembre del 2018",
        "quiero mi facturas con además 1 de enero del 2018 y fin de diciembre del 2018",
        "quiero mi facturas con y fin de diciembre del 2018 además 1 de enero del 2018",


    ]

    for i, phrase in enumerate(expsAcordadas + expsCasos):
        resultado = reg.seakexpresion(phrase, "Fecha")
        #if resultado[1] == 0:
        print("{0}: {1} \nResultado:{2} \nEstado:{3}\n".format(
            i + 1, phrase, str(resultado[0]), resultado[1]))



if __name__ == "__main__":
    # reg = Regexseaker()
    # expr = [
    #     "Quiero facturas de estado aceptado con número de documento 33443 y el prefijo es x",
    #     "Quiero facturas de estado recibido con número de documento 33443 y el prefijo es x",
    #     "Quiero facturas de estado error con número de documento 33443 y el prefijo es x",
    #     "Quiero facturas de estado firmado con número de documento 33443 y el prefijo es x",
    #     "Quiero facturas de estado enviado con número de documento 33443 y el prefijo es x",
    #     "Quiero facturas de estado xsdsfds con número de documento 33443 y el prefijo es x",
    #     "Quiero facturas de estado 12321 con número de documento 33443 y el prefijo es x",
    #     "Quiero facturas de estado es recibido con número de documento 33443 y el prefijo es x",
    #     "Quiero facturas de estado es el que sea con número de documento 33443 y el prefijo es x",
    #     "Facturas de hoy con recibido como estado y prefijo algo",
    #     "Facturas de hoy con recibido es estado y prefijo algo",
    #     "Facturas de hoy con recibido estado y prefijo algo",
    #     "Facturas de hoy con recibido es el estado y prefijo algo"
    #     ]
    # print("\n")
    #
    # print("\n")
    # for e in expr:
    #     resultado = reg.seakexpresion(e.lower(), "Estado", nl=5)
    #     print("{0}\nEstado: {1}\n".format(e, resultado))
    # # print("NoDocumento: ", reg.seakexpresion(expr.lower(), "NoDocumento", nl=3))

    #pruebasFolios()
    # pruebasFechas()
