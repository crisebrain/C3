# from __future__ import print_function
import spaghetti as sgt
import re
import nltk
import numpy as np
import json

class Regexseaker:
    def __init__(self):
        self.patterns = dict(Cuenta=r"\b[A-Za-z]{3}\d{3}\b",
                             Prefijo=r"\b[1-9a-zA-Z]\w{0,3}\b",  # wvect
                             NoDocumento=r"\b[0-9a-zA-Z\-]{1,40}\b",  # w2vect
                             NitAdquirienteMex=r"\b[A-Za-z]{4}\d{6}[A-Za-z0-9]{3}\b")
        dictfacturas = json.load(open("facturaskeys.json"))
        self.listaprefijo = dictfacturas["Prefijo"]
        self.listadocumento = dictfacturas["NoDocumento"]

    def regexextractor(self, expression, field):
        pattern = self.patterns[field]
        result = re.search(pattern=pattern, string=expression)
        if result:
            return result.group()
        else:
            return None

    def do_tagging(self, exp, field):
        listaprefijo = self.listaprefijo
        listadocumento = self.listadocumento
        tokens = nltk.word_tokenize(exp)
        tagged = sgt.pos_tag(tokens)
        tagged = np.array([list(tup) for tup in tagged])
        mask = tagged[:, 1] == None
        # Hardcode :( para serie
        if field == "Prefijo":
            for itok, token in enumerate(tagged[:, 0]):
                if token == "serie":
                    tagged[itok, 1] = "Prefijo"
        unknowns, = np.where(mask)
        for unknown in unknowns:
            if tagged[unknown, 0] in listaprefijo:
                tagged[unknown, 1] = "Prefijo"
            elif tagged[unknown, 0] in listadocumento:
                tagged[unknown, 1] = "NoDocumento"
            else:
                if self.regexextractor(tokens[unknown], field) is not None:
                    tagged[unknown, 1] = "dato"
                else:
                    tagged[unknown, 1] = "unknown"
        return [tuple(wordtagged) for wordtagged in tagged]

    def do_chunking(self, tagged, key):
        if key == "Prefijo":
            grammar = r"""NP: {<Prefijo> <(vs\w+)|(nc\w+)|(wmi\w+)|(spc\w+)>* <dato|Z>}
                          NP: {<Prefijo> <(vmi\w+)|(aq\w+)|unknown>? <sp\w+>? <dato|Z>}
                          NP: {<dato|Z> <(vs\w+)> <(da\w+)> <Prefijo>}
                          NP: {<dato|Z> <cs> <Prefijo>}
                       """
                      # r"""NP: {<Prefijo> <(vs\w+)|dato>*}"""
                              #{<dato> <nc\w+>* <Prefijo>} """
        elif key == "NoDocumento":
            grammar = r"NP: {<NoDocumento>? <nc\w+>* <sp\w+>* <nc\w+>* <dato>}"
        cp = nltk.RegexpParser(grammar)
        chunked = cp.parse(tagged)
        continuous_chunk = []
        entity = []
        for i, subtree in enumerate(chunked):
            if type(subtree) == nltk.Tree:
                print(subtree)
                entity += [token for token, pos in subtree.leaves()
                           if pos == "dato" or pos == "Z"]
        if entity == []:
            entity = None
            code = 1
        elif len(entity) > 1:
            code = 0
            entity = entity[0]
        else:
            code = 1
            entity = entity[0]
        return entity, code

    def seakexpresion(self, expression, field="Cuenta", nl=3):
        if field in ["Cuenta", "NitAdquirienteMex"]:
            return self.regexextractor(expression, field)
        elif field in ["Prefijo", "NoDocumento"]:
            if field == "Prefijo":
                words = self.listaprefijo
            elif field == "NoDocumento":
                words = self.listadocumento
            tokens = nltk.word_tokenize(expression)
            arrs = []
            for token in tokens:
                arrs.append((token, [words.index(token)+1 if token in words
                                     else False]))
            d2arr = np.array([arr[1] for arr in arrs])
            # para prefijo
            if any(d2arr[:, 0]):
                inds = np.argsort(d2arr[:, 0])
                mask = np.sort(d2arr[:, 0]) != 0
                inp = inds[mask][0]
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
            tagged = self.do_tagging(posible, field)
            print(tagged)
            return self.do_chunking(tagged, field)

if __name__ == "__main__":
    reg = Regexseaker()
    expr = "Quiero facturas de acuse recibido con número de documento 33443 y el prefijo es x"
    print("\n")
    print(expr)
    print("\n")
    print("Prefijo: ", reg.seakexpresion(expr, "Prefijo", nl=3))
    print("NoDocumento: ", reg.seakexpresion(expr, "NoDocumento", nl=3))
