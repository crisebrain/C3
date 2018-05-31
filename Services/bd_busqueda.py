import pandas as pd
import json
import re
import os

def joinnames(nameString):
    if not isinstance(nameString, str):
        stname = " ".join(nameString)
        array = [word.strip() for word in stname.split(" ")
                 if re.match(pattern=r"\w+", string=word)]
        stname = " ".join(array)
    else:
        array = [word.strip() for word in nameString.split(" ")
                 if re.match(pattern=r"\w+", string=word)]
        stname = " ".join(array)
    return normaliza(stname)

def normaliza(data):
    import unicodedata
    normal = unicodedata.normalize('NFKD', data).encode('ASCII', 'ignore')
    return normal.decode()

class BDbusquedas:
    def __init__(self):
        pathfile = os.getcwd()
        # pathfile = os.path.join(pathfile, "Services", "basedatosficticia.txt")
        pathfile = os.path.join(pathfile,
                                "Services",
                                "DataSetExtensiones_utf8.csv")
        self.BD = pd.read_csv(pathfile, header=0)
        # self.BD = pd.read_csv(pathfile, header=0, encoding="ISO-8859-1")

    def comparaPalabras(self, stringinput, stringname):
        wordlist = stringinput.lower().split(" ")
        coincidencias = [True if word in stringname else False
                         for word in wordlist]
        return True if all(coincidencias) else False

    def busqueda(self, valor):
        valor = joinnames(valor)
        Nombres = self.BD[["Nombre", "Apellido"]].apply(func=joinnames, axis=1)
        # print(Nombres)
        posibles = self.BD.iloc[[self.comparaPalabras(valor, n)
                                 for n in Nombres.str.lower().values]]
        # posiblesc = self.BD.iloc[[True if n in valor.lower() else False
                                #   for n in Nombres.str.lower().values]]
        # posibles = pd.concat([posibles, posiblesc])
        resultado = json.loads(posibles.drop(["Id"],
                               axis=1).to_json(orient="table"))
        return resultado["data"]

def dbquery(valor):
    bdbusqueda = BDbusquedas()
    return bdbusqueda.busqueda(valor)
