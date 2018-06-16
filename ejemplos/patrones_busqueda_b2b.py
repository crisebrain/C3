import re

class Regexseaker:
    def __init__(self):
        self.patterns = dict(Cuenta=r"\b[A-Za-z]{3}\d{3}\b",
                             # "Prefijo": pendiente,
                             NoDocumento=r"\b[A-Za-z\-0-9]{3}\b",
                             NitAdquirienteMex=r"\b[A-Z]{4}\d{6}[A-Za-z]{6}\d{2}\b")

    def seakexpresion(self, expression, field="Cuenta"):
        pattern = self.patterns[field]
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
