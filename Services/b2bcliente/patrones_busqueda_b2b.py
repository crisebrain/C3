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
                                 NP: {<Folio> <Q>* (<tipoFolio> <Q|Prefijo>*){1,2} <dato>}
                                 NP: {<Folio> <Q>* (<dato> <Q|Prefijo>*){1,2} <tipoFolio>}
                                 NP: {<dato> <Q>+ <Folio> <Q>* <tipoFolio>}
                                 NP: {<tipoFolio> <Q>* <Folio> <Q>* <dato>}
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
                                NP: {<I> <DiasNum|ao0ms0> <Q>{0,2} <Fecha> <Q>{0,2} <AniosNum|DiasNum>}
                                NP: {<I> <Fecha> <Q>{0,2} <DiasNum|ao0ms0> <Q>{0,2} <AniosNum|DiasNum>}
                                NP: {<I> <DiasNum|ao0ms0>? <Q>{0,2} <Fecha> <Q>{0,2} <AniosNum|DiasNum>?}
                                NP: {<I> <Fecha> <Q>{0,2} <DiasNum|ao0ms0>? <Q>{0,2} <AniosNum|DiasNum>}
                                NP: {<I> <DiasNum|ao0ms0> <Q>{0,2} <Fecha>}
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
            return entity, code

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

        def missingDate():
            nonlocal fechaInicio, fechaFin

            # Caso 1: dan fecha fin, pero no de inicio.
            if fechaFin and fechaInicio is None:
                fechaInicio = None, 1
            # Caso 2: dan fecha de inicio, pero no de fin
            elif fechaInicio and fechaFin is None:
                fechaFin = today, 1

            # if fechaFin is None:
            #     fechaFin = fechaInicio
            # elif fechaInicio is None:
            #     fechaInicio = fechaFin

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
            # Invertimos para interar desde el último elemento
            entity.reverse()
            for fecha in entity:
                if "Fin" in fecha and fechaFin is None:
                    fechaFin = buildDate(fecha)
                elif "Inicio" in fecha and fechaInicio is None:
                    fechaInicio = buildDate(fecha)

            missingDate()
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


if __name__ == "__main__":
    reg = Regexseaker()
    expr = [
        "Quiero facturas de estado aceptado con número de documento 33443 y el prefijo es x",
        "Quiero facturas de estado recibido con número de documento 33443 y el prefijo es x",
        "Quiero facturas de estado error con número de documento 33443 y el prefijo es x",
        "Quiero facturas de estado firmado con número de documento 33443 y el prefijo es x",
        "Quiero facturas de estado enviado con número de documento 33443 y el prefijo es x",
        "Quiero facturas de estado xsdsfds con número de documento 33443 y el prefijo es x",
        "Quiero facturas de estado 12321 con número de documento 33443 y el prefijo es x",
        "Quiero facturas de estado es recibido con número de documento 33443 y el prefijo es x",
        "Quiero facturas de estado es el que sea con número de documento 33443 y el prefijo es x",
        "Facturas de hoy con recibido como estado y prefijo algo",
        "Facturas de hoy con recibido es estado y prefijo algo",
        "Facturas de hoy con recibido estado y prefijo algo",
        "Facturas de hoy con recibido es el estado y prefijo algo"
        ]
    print("\n")

    print("\n")
    # for e in expr:
    #     resultado = reg.seakexpresion(e.lower(), "Estado", nl=5)
    #     print("{0}\nEstado: {1}\n".format(e, resultado))


    expFechas = [
        "quiero mi facturas con fecha de inicio 3 de septiembre del 2000",
        "quiero mi facturas con fecha de inicio 3 de septiembre del 2020",
        "quiero mi facturas con fecha de fin 3 de septiembre del 2000",
        "quiero mi facturas con fecha de fin 3 de septiembre del 2020"
        ]
    for e in expFechas:
        resultado = reg.seakexpresion(e, "Fecha")
        print("{0}\nFecha: {1}\n".format(e, resultado))

    # print("NoDocumento: ", reg.seakexpresion(expr.lower(), "NoDocumento", nl=3))
