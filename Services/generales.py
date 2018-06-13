import numpy as np

def construyeNombre(parametros):
    listaNombre = parametros.get("nombre")
    # Obtenemos los nombres que vengan, se consideran valores repetidos
    keys = [list(dicc.keys()) for dicc in listaNombre]
    unicos = np.unique(np.array(keys).reshape(-1, ))
    dicNombres = dict(zip(unicos, [""]*len(unicos)))
    for dicc in listaNombre:
        for unico in unicos:
            if unico in dicc.keys():
                dicNombres[unico] = " ".join([dicNombres[unico].strip(),
                                              dicc[unico].strip()])
    # Concatenamos los nombres
    nombre = "" + str(dicNombres.setdefault("nombre", "")) + " "\
             + str(dicNombres.setdefault("apellido", "")) + " "\
             + str(dicNombres.setdefault("nombresExtras", ""))

    return nombre.strip()
