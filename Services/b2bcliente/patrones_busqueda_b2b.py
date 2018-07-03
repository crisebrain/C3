# from __future__ import print_function
from .spaghetti import pos_tag
import re
from nltk import word_tokenize, RegexpParser, Tree
from gc import collect
import numpy as np
import json

class Regexseaker:
    def __init__(self):
        """Inicialización de la clase de busquedas.
        1 expresiones regulares para los campos utilizados
        2 carga la lista de alias para cada campo
        """
        self.patterns = dict(Cuenta=r"\b[A-Za-z]{3}\d{3}\b",
                             Prefijo=r"\b[1-9a-zA-Z]\w{0,3}\b",  # wvect
                             NoDocumento=r"\b[0-9a-zA-Z\-]{1,40}\b",  # w2vect
                             NitAdquirienteMex=r"\b[A-Za-z]{4}\d{6}[A-Za-z0-9]{3}\b",
                             Folio=r"\d{1,16}",
                             Estado=r"[A-Za-z]",   #[a-z]{1,16}"
                             Acuse=r"[A-Za-z]")
        self.dictfacturas = json.load(open("Services/b2bcliente/facturaskeys.json"))
        # Services/b2bcliente/facturaskeys.json"))

    def regexextractor(self, expression, field):
        pattern = self.patterns[field]
        result = re.search(pattern=pattern, string=expression)
        if result:
            return result.group()
        else:
            return None

    def do_tagging(self, exp, field, listTags, listRegExps=None):
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
        dgramm = dict(Prefijo=r"""Q: {<dato|Z|Fz|unknown|ncfs000|Singlel>}
                                  NP: {<Prefijo> <(vs\w+)|(nc\w+)|(wmi\w+)|(spc\w+)>* <Q>}
                                  NP: {<Prefijo> <dato|Fz|unknown|sps00>}
                                  NP: {<Prefijo> <(vmi\w+)|(aq\w+)|unknown>? <sp\w+>? <Q>}
                                  NP: {<Prefijo> <dd0fs0> <vmp00sm> <sps00> <Q>}
                                  NP: {<Q|sps00> <(vs\w+)> <(da\w+)> <Prefijo>}
                                  NP: {<Q|sps00> <(p030\w+)>? <vmip3s0>? <cs> <Prefijo>}
                               """,
                               # directas
                               # inversas
                               # añadir que se hace con sustantivos y nodos terminales
                      NoDocumento=r""" Q: {<cc|dato|Z|Singlel|unknown>}
                                       NP: {<(NoDocu\w+)> <sps00> <(NoDocu\w+)|ncms000> <Q|ncms000|sps00>}
                                       NP: {<(NoDocu\w+)> <sps00> <da0fs0>? <(NoDocu\w+)|ncms000> <aq0cs0>? <sps00|vsip3s0>? <Q|ncms000>}
                                       NP: {<sps00>? <(NoDocu\w+)|ncms000> <aq0cs0>? <sps00|vsip3s0>? <Q|ncms000>}
                                       NP: {<(NoDocu\w+)> <sps00> <Q|ncms000> <cs> <(NoDocu\w+)|ncms000>}
                                       NP: {<Q|ncms000> <vsip3s0> <da0ms0> <(NoDocu\w+)|ncms000> <sps00> <da0fs0>? <NoDocu\w+>}
                                       NP: {<Q> <p0300000> <vmip3s0> <cs> <NoDocumento>}
                                       NP: {<NoDocumento> <Q>}
                                   """,
                      NitAdquirienteMex=r""" Q: {<unknown|dato|Z|Singlel>}
                                             NP: {<(NitA\w+)> <(NitA\w+)>? <sps00> <Sust> <aq0cs0>? <sps00>? <Q>}
                                             NP: {<(NitA\w+)> <(NitA\w+)>? <sps00> <Q> <cs> <Sust>}
                                             NP: {<(NitA\w+)> <(NitA\w+)>? <Sust|(vs\w+)>? <da0ms0>? <Q|cc>}
                                             NP: {<(NitA\w+)> <(NitA\w+)>? <aq0cs0> <sps00> <Q>}
                                         """,
                      Cuenta=r""" Q: {<unknown|dato|Z|Singlel>}
                                  NP: {<Cuenta> <sps00> <Sust> <Q>}
                                  NP: {<Cuenta> <sps00> <Sust> <aq0cs0> <sps00>? <Q>}
                                  NP: {<(da0\w+)>? <Sust>? <sps00|da0fs0>? <Cuenta> <(vs\w+)>? <Q>}
                                  NP: {<Sust> <sps00> <Cuenta> <sps00> <Sust> <aq0cs0> <sps00> <Q>}
                                  NP: {<Sust> <sps00> <Cuenta> <sps00> <Q> <cs> <Sust>}
                                  NP: {<sps00> <Cuenta> <aq0cs0> <sps00> <Q>}
                              """,
                      Estado=r""" Q: {<Recibido|Error|Firmado|Rechazado|Aceptado|Enviado>}
                                   NP: {<Estado> <vssp3s0|unknown|vssp3s0|sps00>* <Q>}
                                   NP: {<Estado> <vsis3s0|vmp00sm|sps00|Es|Valor>* <Q>}
                                   NP: {<Q> <sps00|ncms000|Es|da0ms0>* <Estado>}
                               """,
                      Acuse=r"""Q: {<Rechazado|Aceptado|Pendiente>}
                                NP: {<Acuse> <vssp3s0|unknown|vssp3s0|sps00>* <Q>}
                                NP: {<Acuse> <vsis3s0|vmp00sm|sps00|Es|Valor>* <Q>}
                                NP: {<Q> <sps00|ncms000|Es|da0ms0>* <Acuse>}
                             """,
                      Folio=r""" Q: {<Es|sps00|da0ms0|unknown|Valor|cs|cc|Reciente|p0300000|dp1msp|spcms|dp1css>}
                                 NP: {<Folio> <Q>* (<tipoFolio> <Q|Prefijo>*){1,2} <dato>}
                                 NP: {<Folio> <Q>* (<dato> <Q|Prefijo>*){1,2} <tipoFolio>}
                                 NP: {<dato> <Q>+ <Folio> <Q>* <tipoFolio>}
                                 NP: {<tipoFolio> <Q>* <Folio> <Q>* <dato>}
                             """)
        return dgramm[field]

    def get_posibles(self, field):
        if field in ["Prefijo", "NoDocumento", "NitAdquirienteMex", "Cuenta"]:
            return ['Fz', 'Y', 'Z', 'cc', 'dato', 'nccn000', "ncms000"
                    'ncfs000', 'sps00', 'Singlel', 'unknown']
        elif field == "Folio":
            return ["dato"]
        elif field == "Estado" or field == "Acuse":
            return ["dato","Recibido","Error","Firmado","Rechazado",
                    "Aceptado","Enviado","Pendiente"]

    def get_tags(self, field):
        if field == "Prefijo":
            return ["Singlel"]
        elif field == "NoDocumento":
            return ["Singlel"]
        elif field == "NitAdquirienteMex":
            return ["Singlel", "Sust"]
        elif field == "Cuenta":
            return ["Singlel", "Sust"]
        elif field == "Folio":
            return ["Inicio", "Fin", "Es", "Valor", "Prefijo", "Reciente"]
        elif field == "Estado":
            return ["Es","Valor","Recibido","Error","Firmado","Rechazado",
                    "Aceptado","Enviado"]
        elif field == "Acuse":
            return ["Es","Valor","Rechazado","Aceptado","Pendiente"]

    def do_chunking(self, tagged, field, code, posibles, grammar=None):
        if grammar is None:
            grammar = self.choose_grammar(field)
        cp = RegexpParser(grammar)
        chunked = cp.parse(tagged)
        continuous_chunk = []
        entity = []
        unknowns = []
        subt = []
        for i, subtree in enumerate(chunked):
            if isinstance(subtree, Tree) and subtree.label() == "NP":
                if field in ["Prefijo", "NoDocumento",
                             "NitAdquirienteMex", "Cuenta",
                             "Estado", "Acuse"]:
                    #print(subtree)
                    for subsubtree in subtree.subtrees(filter=lambda t: t.label() == "Q"):
                        entity += [token for token, pos in subsubtree.leaves()]
                        subt.append(subsubtree)
                    unknowns += [token for token, pos in subtree.leaves()
                                 if pos in posibles]
                else:
                    # añadir las condiciones que sean necesarias para contemplar
                    # los posibles valores
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
            if self.regexextractor(entity, field) is not None:
                code = 1
            else:
                code = 0
        return entity, code, subt, tagged

    def seakexpresion(self, expression, field="Cuenta", nl=5, lowerc=True):
        if lowerc:
            expression = expression.lower()
        if field in ["Prefijo", "NoDocumento", "Cuenta", "NitAdquirienteMex",
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
            else:
                code = 1
            # codigo 1 es para busqueda de campo exitosa
            # inocente hasta que se demuestre lo contrario
            taglist = self.get_tags(field)
            tagged = self.do_tagging(posible, field, taglist)
            # print(tagged)
            collect()
            posibles = self.get_posibles(field)
            return self.do_chunking(tagged, field, code, posibles)
        elif field == "FolioInicio":
            return self.folios(expression, "Inicio")
        elif field == "FolioFinal":
            return  self.folios(expression, "Fin")

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
        return self.do_chunking(tagged, field, 1, posibles, grammarFolio)


if __name__ == "__main__":
    reg = Regexseaker()
    #expr = "Quiero facturas de acuse recibido con número de documento 33443 y el prefijo es x"
    #expr = "Hola, me ayudas con las facturas donde ABCD ES el valor definido para el prefijo"
    #expr = "Hola, me ayudas con las facturas donde ABCD ES el prefijo"
    # expr = "Por favor con las facturas donde ABCD ES el prefijo, perdon el prefijo es XXXX"
    expr = "quiero facturas de hoy y ayer con número de factura escuela con prefijo aaas gracias"
    print("\n")
    print(expr)
    print("\n")
    print("Prefijo: ", reg.seakexpresion(expr.lower(), "Prefijo", nl=5))
    # print("NoDocumento: ", reg.seakexpresion(expr.lower(), "NoDocumento", nl=3))
