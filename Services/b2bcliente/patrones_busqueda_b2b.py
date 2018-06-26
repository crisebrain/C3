# from __future__ import print_function
import spaghetti as sgt
import re
import nltk
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
                             NitAdquirienteMex=r"\b[A-Za-z]{4}\d{6}[A-Za-z0-9]{3}\b")
        self.dictfacturas = json.load(open("facturaskeys.json"))

    def regexextractor(self, expression, field):
        pattern = self.patterns[field]
        result = re.search(pattern=pattern, string=expression)
        if result:
            return result.group()
        else:
            return None

    def do_tagging(self, exp, field):
        lista = self.dictfacturas[field]
        tokens = nltk.word_tokenize(exp)
        tagged = sgt.pos_tag(tokens)
        tagged = np.array([list(tup) for tup in tagged])
        mask = tagged[:, 1] == None
        # Hardcode :( para serie
        for i, token in enumerate(tokens):
            if token in self.dictfacturas[field]:
                tagged[i, 1] = field
        unknowns, = np.where(mask)
        for unknown in unknowns:
            if tagged[unknown, 0] in lista:
                tagged[unknown, 1] = field
            else:
                if self.regexextractor(tokens[unknown], field) is not None:
                    tagged[unknown, 1] = "dato"
                else:
                    tagged[unknown, 1] = "unknown"
        return [tuple(wordtagged) for wordtagged in tagged]

    def do_chunking(self, tagged, field, code):
        if field == "Prefijo":
            # directas
            # inversas
            # añadir que se hace con sustantivos y nodos terminales
            grammar = r"""NP: {<Prefijo> <(vs\w+)|(nc\w+)|(wmi\w+)|(spc\w+)>* <dato|Z|unknown>}
                          NP: {<Prefijo> <(vmi\w+)|(aq\w+)|unknown>? <sp\w+>? <dato|Z|unknown>}
                          NP: {<Prefijo> <dd0fs0> <vmp00sm> <sps00> <dato|Z|unknown>}
                          NP: {<dato|Z|unknown> <(vs\w+)> <(da\w+)> <Prefijo>}
                          NP: {<dato|Z|unknown> <(p030\w+)>? <vmip3s0>? <cs> <Prefijo>}
                       """
                      # r"""NP: {<Prefijo> <(vs\w+)|dato>*}"""
                              #{<dato> <nc\w+>* <Prefijo>} """
        elif field == "NoDocumento":
            grammar = r"""NP: {<NoDocumento> <(nc\w+)|(sp\w+)|(vs)\w+>* <dato|Z>}
                          NP: {<NoDocumento|(ncm\w+)> <(vm\w+)|(vs\w+)|(aq\w+)>* <cs|(sps\w+)|(spc\w+)>? <dato|Z>}
                          NP: {<NoDocumento> <(vm\w+)|(vs\w+)>* <cs|spcms>? <dato|Z>}
                          NP: {<dato|Z> <vsip3s0|cs> <ncms000>? <da0ms0|(sps\w+)>? <NoDocumento|ncms000>}
                          NP: {<dato|Z> <(p0\w+)> <vm\w+> <cs> <NoDocumento>}
                       """
                       #NP: {<dato> <vsip3s0|cs> <NoDocumento>}

        cp = nltk.RegexpParser(grammar)
        chunked = cp.parse(tagged)
        continuous_chunk = []
        entity = []
        unknowns = []
        subt = []
        for i, subtree in enumerate(chunked):
            if type(subtree) == nltk.Tree:
                print(subtree)
                entity += [token for token, pos in subtree.leaves()
                           if pos == "dato" or pos == "Z"]
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
            entity = entity
        else:
            code = 1
            entity = entity[0].upper()
        return entity, code, subt, tagged

    def seakexpresion(self, expression, field="Cuenta", nl=3):
        if field in ["Cuenta", "NitAdquirienteMex"]:
            return self.regexextractor(expression, field)
        elif field in ["Prefijo", "NoDocumento"]:
            words = self.dictfacturas[field]
            tokens = nltk.word_tokenize(expression)
            arrs = []
            # Busca palabra pivote
            for token in tokens:
                arrs.append((token, [words.index(token)+1 if token in words
                                     else False]))
            # Crea un arreglo con los indices de ocurrencias de alias
            d2arr = np.array([arr[1] for arr in arrs])
            print(d2arr)
            # priorizacion de alias
            if any(d2arr[:, 0]):
                inds = np.argsort(d2arr[:, 0])
                mask = np.sort(d2arr[:, 0]) != 0
                print(inds)
                inp = inds[mask][0]
                print(inds[mask])
                if inp - nl < 0:
                    posible = " ".join(tokens[: inp + nl])
                else:
                    posible = " ".join(tokens[inp - nl: inp + nl])
            else:
                # resultado = None
                posible = None
            print(posible)
            if posible is None:
                return (None, 1)
            else:
                code = 1
            # codigo 1 es para busqueda de campo exitosa
            # inocente hasta que se demuestre lo contrario
            tagged = self.do_tagging(posible, field)
            print(tagged)
            return self.do_chunking(tagged, field, code)

if __name__ == "__main__":
    reg = Regexseaker()
    #expr = "Quiero facturas de acuse recibido con número de documento 33443 y el prefijo es x"
    #expr = "Hola, me ayudas con las facturas donde ABCD ES el valor definido para el prefijo"
    #expr = "Hola, me ayudas con las facturas donde ABCD ES el prefijo"
    expr = "Por favor con las facturas donde ABCD ES el prefijo, perdon el prefijo es XXXX"
    print("\n")
    print(expr)
    print("\n")
    print("Prefijo: ", reg.seakexpresion(expr.lower(), "Prefijo", nl=5))
    # print("NoDocumento: ", reg.seakexpresion(expr.lower(), "NoDocumento", nl=3))
