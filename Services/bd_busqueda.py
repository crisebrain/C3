import pandas as pd
import json
import re
import os

def joinnames(array):
    stname = " ".join(array)
    return stname

def normaliza(data):
    import unicodedata
    normal = unicodedata.normalize('NFKD', data).encode('ASCII', 'ignore')
    return normal.decode()

class BDbusquedas:
    def __init__(self):
        pathfile = os.getcwd()
        # pathfile = os.path.join(pathfile, "Services", "basedatosficticia.txt")
        pathfile = os.path.join(pathfile, "Services", "DataSetExtensiones_utf8.csv")
        self.BD = pd.read_csv(pathfile, header=0)
        # self.BD = pd.read_csv(pathfile, header=0, encoding="ISO-8859-1")

    def busqueda(self, valor):
        valor = valor.strip()
        valor = normaliza(valor)
        Nombres = self.BD[["Nombre", "Apellido"]].apply(func=joinnames, axis=1)
        posibles = self.BD.iloc[[True if valor.lower() in n else False for n in Nombres.str.lower().values]]
        # posiblesc = self.BD.iloc[[True if n in valor.lower() else False for n in Nombres.str.lower().values]]
        # posibles = pd.concat([posibles, posiblesc])
        resultado = json.loads(posibles.drop(["Id"], axis=1).to_json(orient="table"))["data"]
        return resultado

def dbquery(valor):
    bdbusqueda = BDbusquedas()
    return bdbusqueda.busqueda(valor)
