from patrones_busqueda_b2b import Regexseaker
import pandas as pd
df = pd.read_csv("/home/ramon/Dropbox/ebraintec_pendientes/datasetprefijondoc.txt",
                 header=0, index_col=0)
frases = df.Frases.values.tolist()
totalprefs = len(df.numlabel.loc[df.numlabel == 1])
totalnodocs = len(df.numlabel.loc[df.numlabel == 0])
reg = Regexseaker()
archivo = open("prueba.txt", "w")
prefs = 0
nodocs = 0
for i, expr in enumerate(frases):
    print("\n")
    print(expr)
    print("\n")
    archivo.write("\n{0}.- {1}\n".format(i, expr))
    pref = reg.seakexpresion(expr, "Prefijo", nl=4)
    nodoc = reg.seakexpresion(expr, "NoDocumento", nl=4)
    print("Prefijo: ", pref)
    print("NoDocumento: ", nodoc)
    if pref[0] is not None and pref[1] == 1:
        prefs += 1
    if nodoc[0] is not None and nodoc[1] == 1:
        nodocs += 1
    archivo.write("Prefijo: {0} cumplidos {1} de {2}\n".format(pref,
                                                               prefs,
                                                               totalprefs))
    archivo.write("NoDocumento: {0} cumplidos {1} de {2}\n".format(nodoc,
                                                                   nodocs,
                                                                   totalnodocs))
archivo.close()
