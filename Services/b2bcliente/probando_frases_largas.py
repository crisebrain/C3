from patrones_busqueda_b2b import Regexseaker
import pandas as pd
df = pd.read_csv("/home/ramon/Dropbox/ebraintec_pendientes/frasescompuestas_prefijo_nodoc_25062018.csv",
                 header=0, index_col=0)
frases = df.Frases.values.tolist()
totalprefs = len(df.Prefijo.loc[df.Prefijo == 1])
totalnodocs = len(df.NoDocumento.loc[df.NoDocumento == 1])
reg = Regexseaker()
archivo = open("prueba_largas.txt", "w")
prefs = 0
nodocs = 0
dpref = {"inc":[], "cump":[]}
ddoc = {"inc":[], "cump":[]}
for i, expr in enumerate(frases):
    print("\n")
    print(expr)
    print("\n")
    archivo.write("\n{0}.- {1}\n".format(i, expr))
    pref = reg.seakexpresion(expr.lower(), "Prefijo", nl=4)
    nodoc = reg.seakexpresion(expr.lower(), "NoDocumento", nl=4)
    print("Prefijo: ", pref[:2])
    print("NoDocumento: ", nodoc[:2])
    if pref[0] is not None and pref[1] == 1:
        prefs += 1
        dpref["cump"].append(pref[2])
    else:
        try:
            dpref["inc"].append(pref[3])
        except IndexError:
            dpref["inc"].append([])
    if nodoc[0] is not None and nodoc[1] == 1:
        nodocs += 1
        ddoc["cump"].append(nodoc[2])
    else:
        try:
            ddoc["inc"].append(nodoc[3])
        except IndexError:
            ddoc["inc"].append([])
    archivo.write("Prefijo: {0} cumplidos {1} de {2}\n".format(pref[:2],
                                                               prefs,
                                                               totalprefs))
    archivo.write("NoDocumento: {0} cumplidos {1} de {2}\n".format(nodoc[:2],
                                                                   nodocs,
                                                                   totalnodocs))
print("\nincumplidas pref:\n")
for c in dpref["inc"]:
    print(c)
print("\nincumplidas doc:\n")
for c in ddoc["inc"]:
    print(c)
archivo.close()
