import re
import pandas as pd

class Regexseaker:
    def __init__(self):
        self.patterns = dict(Cuenta=r"\b[A-Za-z]{3}\d{3}\b",  # paloma
                             #Prefijo=pendiente,              # tache
                             NoDocumento=r"\b[A-Za-z\-0-9]{3}\b",  # tache
                             NitAdquirienteMex=r"\b[A-Za-z]{4}\d{6}[A-Za-z]{6}\w\d\b") # paloma

    def seakexpresion(self, expression, field="Cuenta"):
        pattern = self.patterns[field]
        result = re.search(pattern=pattern, string=expression)
        if result:
            return result.group()
        else:
            return None

    def seakkey(self, expression, key):
        kpatterns = dict(Cuenta=r"\b[Cc]uenta\b",
                         # "Prefijo": pendiente,
                         NoDocumento=r"\b(numero)?\b(de)?\b[Dd]ocumento\b",
                         NitAdquirienteMex=r"\b[Aa]dquiriente\b")
        pattern = kpatterns[key]
        expression = expression.lower()
        result = re.search(pattern=pattern, string=expression)
        if result:
            return result.group()
        else:
            return None

if __name__ == "__main__":
    seaker = Regexseaker()
    prueba = "coada sasa a-1 prefijo uno12 com- 1-2 RAMON AAGR860628HDFPRM01 AOp122"
    for c in ["Cuenta", "NoDocumento", "NitAdquirienteMex"]:
        print(seaker.seakexpresion(prueba, c))
    #
    # frases = pd.read_csv("../../frases.txt",
    #                      header=None, index_col=0)
    # seaker = Regexseaker()
    # resultados = []
    # for frase in frases.values:
    #     encontradas = {}
    #     for c in ["Cuenta", "NoDocumento", "NitAdquirienteMex"]:
    #         ff = seaker.seakkey(frase[0], c)
    #         if ff is not None:
    #             print(c, ff)
    #         encontradas[c] = seaker.seakexpresion(frase[0], c)
    #     resultados.append(encontradas)
    # print(resultados)
