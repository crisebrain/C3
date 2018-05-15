import pandas as pd
import json
import re

def joinnames(array):
    stname = " ".join(array)
    return stname


class BDbusquedas:
    def __init__(self):
        self.BD = pd.read_csv("basedatosficticia.txt", header=0)

    def busqueda(self, valor):
        valor = valor.strip()
        Nombres = self.BD[["Nombre", "Apellido"]].apply(func=joinnames, axis=1)
        posibles = self.BD.iloc[[True if valor.lower() in n else False for n in Nombres.str.lower().values]]
        # posiblesc = self.BD.iloc[[True if n in valor.lower() else False for n in Nombres.str.lower().values]]
        # posibles = pd.concat([posibles, posiblesc])
        resultado = json.loads(posibles.drop(["Id"], axis=1).to_json(orient="table"))["data"]
        return resultado

# print(valor)
# if len(valor.split(" ")) == 1:
#     if valor.lower() in self.BD.Nombre.str.lower().values:
#         posibles = self.BD.loc[self.BD.Nombre.str.lower() == valor.lower()]
#         resultado = json.loads(posibles.drop(["Id"], axis=1).to_json(orient="table"))["data"]
#     elif valor.lower() in self.BD.Apellido.str.lower().values:
#         posibles = self.BD.loc[self.BD.Apellido.str.lower() == valor.lower()]
#         resultado = json.loads(posibles.drop(["Id"], axis=1).to_json(orient="table"))["data"]
#     else:
#         resultado = []
# elif len(valor.split(" ")) == 2:
#     cad = valor.split(" ")
#     posibles = self.BD.loc[self.BD.Nombre.str.lower() == cad[0].lower()]
#     posibles2 = posibles.loc[posibles.Apellido.str.lower() == cad[1].lower()]
#     resultado = json.loads(posibles2.drop(["Id"], axis=1).to_json(orient="table"))["data"]
