import pandas as pd
import json

class BDbusquedas:
    def __init__(self):
        self.BD = pd.read_csv("basedatosficticia.txt", header=0)

    def busqueda(self, valor):
        posibles = self.BD.loc[self.BD.Nombre == valor]
        resultado = json.loads(posibles.drop(["Id"], axis=1).to_json(orient="table"))["data"]
        return resultado
