
# coding: utf-8

# # Instalar nltk

# In[ ]:


# Correr aquí
get_ipython().system('pip install nltk')


# In[1]:


# from __future__ import print_function
import spaghetti as sgt
import re
import nltk
import numpy as np
import json


# ### Descargar los corpus
# ```python 
# nltk.download()
# ```
# 
# ### archivos contenidos en carpeta
# - spaghetti.py
# - facturaskeys.json
# - entendimiento.ipynb

# ### definicion de palabras asociadas a los campos y de patrones de expresiones regulares

# In[180]:


dictfacturas = json.load(open("facturaskeys.json"))
print(dictfacturas)

patterns = dict(Cuenta=r"\b[A-Za-z]{3}\d{3}\b",
                Prefijo=r"\b[1-9a-zA-Z]\w{0,3}\b",  # wvect
                NoDocumento=r"\b[0-9a-zA-Z\-]{1,40}\b",  # w2vect
                NitAdquirienteMex=r"\b[A-Za-z]{4}\d{6}[A-Za-z0-9]{3}\b")


# ### NOTA: 
# 
#     Añadir al archivo facturaskeys.json los sinónimos que crean necesarios para cada campo, 
#     respetando la estructura json

# ### funciones
# 
# Nota:
# 
#     - Le hice cambios a la función do_tagged() resaltados con "##" revisar.
#     - Ya casi está terminada lo de no. de documento.
#     - Revisar los temas que añadí al notebook, son consejos y la observación sobre la definición correcta de Q.

# In[182]:


def regexextractor(expression, field):
    pattern = patterns[field]
    result = re.search(pattern=pattern, string=expression)
    if result:
        return result.group()
    else:
        return None

def do_tagging(exp, field, listTags):
    tokens = nltk.word_tokenize(exp)
    tagged = sgt.pos_tag(tokens)
    #print("tagged:",tagged)
    tagged = np.array([list(tup) for tup in tagged]).astype('|U16')

    # Inicializamos el diccionario de las etiquetas
    dicTags = {}
    for tag in listTags:
        dicTags.setdefault(tag, dictfacturas[tag])

    # Establecemos las etiquetas de cada palabra
    for i, token in enumerate(tokens):
        if token in dictfacturas[field]:
            tagged[i, 1] = str(field)
        for tag in dicTags:
            if token in dicTags[tag]:
                tagged[i, 1] = tag

    # Convertimos a tuplas y evalúamos si el dato potencialmente nos
    # interesa o no.
    mask = tagged[:, 1] == 'None'
    unknowns, = np.where(mask)
    for unknown in unknowns:
        if regexextractor(tokens[unknown], field) is not None:
            tagged[unknown, 1] = "dato"
        else:
            tagged[unknown, 1] = "unknown"
    return [tuple(wordtagged) for wordtagged in tagged]

def do_chunking(grammar, tagged, field, code):
    # añadir las condiciones que sean necesarias para contemplar
    # los posibles valores de campo
    posibles = ['Fz', 'Y', 'Z', 'cc', 'dato', 'nccn000', "ncms000",
                'ncfs000', 'sps00', 'Singlel', 'unknown']
    # posibles son los tipos de palabras que pueden representar al dato
    
    cp = nltk.RegexpParser(grammar)
    chunked = cp.parse(tagged)
    continuous_chunk = []
    entity = []
    unknowns = []
    subt = []
    for i, subtree in enumerate(chunked):
        if isinstance(subtree, nltk.Tree) and subtree.label() == "NP":
            if field in ["Prefijo", "NoDocumento", "NitAdquirienteMex", "Cuenta"]:
                #print(subtree)
                for subsubtree in subtree.subtrees(filter=lambda t: t.label() == "Q"):
                    entity += [token for token, pos in subsubtree.leaves()]
                    subt.append(subsubtree)
                unknowns += [token for token, pos in subtree.leaves()
                             if pos in posibles]
            else:
                # añadir las condiciones que sean necesarias para contemplar los posibles valores
                entity += [token for token, pos in subtree.leaves()
                           if pos in posibles]
                unknowns += [token for token, pos in subtree.leaves()
                             if pos == "unknown"]
                subt.append(subtree)
    if entity == []:
        #print(unknowns)
        code = 0
        if len(unknowns) > 1:
            entity = unknowns[-1].upper()
        elif unknowns != []:
            entity = unknowns[0].upper()
        else:
            entity = None
    elif len(entity) > 1:
        #print(entity)
        code = 0
        entity = entity[-1].upper()
    else:
        #print(entity)
        entity = entity[0].upper()
        if regexextractor(entity, field) is not None:
            code = 1
        else:
            code = 0
    return entity, code, subt, tagged


# In[183]:


do_tagging('las documento prefijo son casa', 'NoDocumento', ["Singlel"])


# ### NOTA: 
#       
#       la palabra prefijo no está en el diccionario, por lo tanto como es detectada como desconocida 
#       pero cumple con la expresión regular del campo, la asigna como posible dato

# # Ejemplo de grammar

# ```python
# grammar = r"""Q: {<dato|Z|Fz|unknown|ncfs000>}
#               T: {<dato|Fz|unknown|sps00>}
#               NP: {<Prefijo> <(vs\w+)|(nc\w+)|(wmi\w+)|(spc\w+)>* <Q>}
#               NP: {<Prefijo> <T>}
#               NP: {<Prefijo> <(vmi\w+)|(aq\w+)|unknown>? <sp\w+>? <Q>}
#               NP: {<Prefijo> <dd0fs0> <vmp00sm> <sps00> <Q>}
#               NP: {<Q> <(vs\w+)> <(da\w+)> <Prefijo>}
#               NP: {<Q> <(p030\w+)>? <vmip3s0>? <cs> <Prefijo>}
#             """
# ```
# ### Nota:
#     
#     falta definir nodos terminales

# # Para diseñar las reglas y probar
# 
# NOTA:
#     
#     Correr cada que se cambie el grammar

# In[186]:


grammar = r"""Q: {<dato|Z|Fz|unknown|ncfs000|Singlel>}
              NP: {<Prefijo> <(vs\w+)|(nc\w+)|(wmi\w+)|(spc\w+)>* <Q>}
              NP: {<Prefijo> <dato|Fz|unknown|sps00>}
              NP: {<Prefijo> <(vmi\w+)|(aq\w+)|unknown>? <sp\w+>? <Q>}
              NP: {<Prefijo> <dd0fs0> <vmp00sm> <sps00> <Q>}
              NP: {<Q|sps00> <(vs\w+)> <(da\w+)> <Prefijo>}
              NP: {<Q|sps00> <(p030\w+)>? <vmip3s0>? <cs> <Prefijo>}
            """

def prueba(exp, field): 
    tagged = do_tagging(exp.lower(), field, ["Singlel"])
    #print(tagged)
    return do_chunking(grammar, tagged, field, 1)

exp = 'de es el prefijo'
field = "Prefijo"
prueba(exp, field)


# NOTA:
#     
#     salida: (VALOR, CODIGO DE VALIDEZ, FRASE ETIQUETADA QUE CUMPLE CON GRAMMAR, FRASE ETIQUETADA)

# In[71]:


grammar = """Q: {<dato|Z|Fz|unknown|ncfs000|Singlel>}
             NP: {<Prefijo> <(vs\w+)|(nc\w+)|(wmi\w+)|(spc\w+)>* <Q>}
             NP: {<Prefijo> <dato|Fz|unknown|sps00>}
             NP: {<Prefijo> <(vmi\w+)|(aq\w+)|unknown>? <sp\w+>? <Q>}
             NP: {<Prefijo> <dd0fs0> <vmp00sm> <sps00> <Q>}
             NP: {<Q|sps00> <(vs\w+)> <(da\w+)> <Prefijo>}
             NP: {<Q|sps00> <(p030\w+)>? <vmip3s0>? <cs> <Prefijo>}
          """
cp = nltk.RegexpParser(grammar)
tagged = do_tagging(exp, "Prefijo")
chunk = cp.parse(tagged)
chunk


# # De Gerardo
# 
# Valores para agregar en facturaskeys.json
# 
# ```json
# {"Estatus": ["estado","estatus"],
#  "Acuse": ["acuse"]}
# ```
# Actualizar grammar
# 
# ```python
# 
# grammar = r"""NP: {<Estatus> <(vs\w+)|(nc\w+)|(wmi\w+)|(spc\w+)>* <dato|Z|unknown>}
#               NP: {<Estatus> <(vmi\w+)|(aq\w+)|unknown>? <sp\w+>? <dato|Z|unknown>}
#               NP: {<Estatus> <dd0fs0> <vmp00sm> <sps00> <aq0cs0> <ncms000> <pr0ms000> <aq0msp> <vmip3s0> <dato|Z|unknown>}
#               NP: {<dato|Z|unknown> <(vs\w+)> <(da\w+)> <Estatus>}
#               NP: {<dato|Z|unknown> <(p030\w+)>? <vmip3s0>? <cs> <Estatus>}
#            """
# 
# grammar = r"""NP: {<Acuse> <(vs\w+)|(nc\w+)|(wmi\w+)|(spc\w+)>* <dato|Z|unknown>}
#               NP: {<Acuse> <(vmi\w+)|(aq\w+)|unknown>? <sp\w+>? <dato|Z|unknown>}
#               NP: {<Acuse> <dd0fs0> <vmp00sm> <sps00> <aq0cs0> <ncms000> <pr0ms000> <aq0msp> <vmip3s0> <dato|Z|unknown>}
#               NP: {<dato|Z|unknown> <(vs\w+)> <(da\w+)> <Acuse>}
#               NP: {<dato|Z|unknown> <(p030\w+)>? <vmip3s0>? <cs> <Acuse>}
#            """
# ```

# # Solución No. de Documento

# In[92]:


letras = [c for c in "abcdefghijklmnñopqrstuvwxyz1234567890"]
tagged = do_tagging(" ".join(letras), "NoDocumento")
Q = '|'.join(np.unique([tag[1] for tag in tagged]))
Q


# In[187]:


frases = ["documento con numero x",
        "documento con número y",
        "documento de numero x",
        "documento de número 22",
        "documento con numero igual a x",
        "documento con número igual a e",
        "documento con aaagg como numero",
        "documento con x como número",
        "numero de documento es 100",
        "número de documento es 100",
        "con número de documento x",
        "con numero de documento a",
        "el numero de documento es y",
        "12 es el numero de documento",
        "factura con numero de",
        "factura con número a",
        "nota de numero x",
        "nota de número 22",
        "factura con numero igual a x",
        "factura con número igual a e",
        "crédito con aaagg como numero",
        "crédito con A3 como número",
        "número de crédito es 100",
        "numero de crédito es 100",
        "con número de crédito x",
        "con numero de crédito a",
        "el numero de la nota es y2",
        "12 es el numero de la nota"]

for i, frase in enumerate(frases):
    print("{0}.-".format(i),frase)
    tagged = do_tagging(frase, "NoDocumento", ["Singlel"])
    print([tag[1] for tag in tagged])


# ### Reglas gramaticales para no. de documento y solución

# In[188]:


grammar = r""" Q: {<cc|dato|Z|Singlel|unknown>}
               NP: {<(NoDocu\w+)> <sps00> <(NoDocu\w+)|ncms000> <Q|ncms000|sps00>}
               NP: {<(NoDocu\w+)> <sps00> <da0fs0>? <(NoDocu\w+)|ncms000> <aq0cs0>? <sps00|vsip3s0>? <Q|ncms000>}
               NP: {<sps00> <(NoDocu\w+)|ncms000> <aq0cs0>? <sps00|vsip3s0>? <Q|ncms000>}
               NP: {<(NoDocu\w+)> <sps00> <Q|ncms000> <cs> <(NoDocu\w+)|ncms000>}
               NP: {<Q|ncms000> <vsip3s0> <da0ms0> <(NoDocu\w+)|ncms000> <sps00> <da0fs0>? <NoDocu\w+>}
           """

posibles = ['Fz', 'Y', 'Z', 'cc', 'dato', 'nccn000', "ncms000",
            'ncfs000', 'sps00', 'Singlel', 'unknown']

exps = ["documento con numero x",
        "documento con número y",
        "documento de numero x",
        "documento de número 22",
        "documento con numero igual a x",
        "documento con número igual a e",
        "documento con aaagg como numero",
        "documento con x como número",
        "numero de documento es 100",
        "número de documento es 100",
        "con número de documento x",
        "con numero de documento a",
        "el numero de documento es y",
        "12 es el numero de documento",
        "factura con numero de",
        "factura con número a",
        "nota de numero x",
        "nota de número 22",
        "factura con numero igual a x",
        "factura con número igual a e",
        "crédito con aaagg como numero",
        "crédito con A3 como número",
        "número de crédito es 100",
        "numero de crédito es 100",
        "con número de crédito x",
        "con numero de crédito a",
        "el numero de la nota es y2",
        "12 es el numero de la nota"]

def prueba(i, exp, field, todo=True): 
    tagged = do_tagging(exp.lower(), field, ["Singlel"])
    #print(tagged)
    result = do_chunking(grammar, tagged, field, 1)
    if todo:
        print("{0}.-".format(i), exp, "\n", result)
    else:
        print("{0}.-".format(i), exp, "\n", result[:2])
    return result

for i, exp in enumerate(exps):
    prueba(i, exp, "NoDocumento", False)


# # Para Nit Adquiriente

# In[189]:


frases = ["nit con clave fafafll",
          "nit con número AAGR860628S34",
          "NIT de número x243421",
          "NIT de numero aaxr243210S01",
          "nit de clave 22",
          "nit adquiriente con numero igual a x243421",
          "nit adquiriente con número igual a aagr223455",
          "nit adquiriente con aaagg como numero",
          "nit con x como número",
          "nit clave aagr342243",
          "nit es 100",
          "nit x",
          "con nit igual a WWDA912122r44",
          "con nit adquiriente igual a aagr860628s34",
          "el nit adquiriente es y",
          "rfc con clave fafafll",
          "rfc con número AAGR860628S34",
          "rfc de número x243421",
          "rfc de numero aaxr243210'S01",
          "rfc de clave 22",
          "rfc adquiriente con numero igual a x243421",
          "rfc adquiriente con número igual a aagr223455",
          "rfc adquiriente con aaagg como numero",
          "rfc con x como número",
          "rfc clave aagr342243",
          "rfc es 100",
          "rfc x",
          "con rfc igual a WWDA912122r44",
          "con rfc adquiriente igual a aagr860628s34",
          "el rfc adquiriente es y"]

for i, frase in enumerate(frases):
    #print("{0}.-".format(i),frase)
    tagged = do_tagging(frase.lower(), "NitAdquirienteMex", ["Sust", "Singlel"])
    print("{0}.-".format(i), [tag[1] for tag in tagged])


# In[ ]:


Q: {<unknown|dato|Z|Singlel>}
NP: {<(NitA\w+)> <(NitA\w+)>? <sps00> <Sust> <aq0cs0>? <sps00>? <Q>}

['NitAdqu', 'sps00', 'Sust', 'unknown']
['NitAdqu', 'sps00', 'Sust', 'dato']
['NitAdqu', 'sps00', 'Sust', 'unknown']
['NitAdqu', 'sps00', 'Sust', 'dato']
['NitAdqu', 'sps00', 'Sust', 'Z']
['NitAdqu', 'NitAdqu', 'sps00', 'Sust', 'aq0cs0', 'sps00', 'unknown']
['NitAdqu', 'NitAdqu', 'sps00', 'Sust', 'aq0cs0', 'sps00', 'unknown']

NP: {<(NitA\w+)> <(NitA\w+)>? <sps00> <Q> <cs> <Sust>}

['NitAdqu', 'sps00', 'unknown', 'cs', 'Sust']
['NitAdqu', 'NitAdqu', 'sps00', 'unknown', 'cs', 'Sust']

NP: {<(NitA\w+)> <Sust|(vs\w+)>? <Q>}
['NitAdqu', 'Sust', 'unknown']
['NitAdqu', 'vsip3s0', 'Z']
['NitAdqu', 'unkn']

NP: {<(NitA\w+)> <(NitA\w+)>? <aq0cs0> <sps00> <Q>}
['sps00', 'NitAdqu', 'aq0cs0', 'sps00', 'dato']
['sps00', 'NitAdqu', 'NitAdqu', 'aq0cs0', 'sps00', 'dato']
['da0ms0', 'NitAdqu', 'NitAdqu', 'vsip3s0', 'cc']
['NitAdqu', 'sps00', 'Sust', 'unknown']
['NitAdquirient', 'sps00', 'Sust', 'dato']
['NitAdqu', 'sps00', 'Sust', 'unknown']
['NitAdquiriente', 'sps00', 'Sust', 'unknown']
['NitAdqu', 'sps00', 'Sust', 'Z']
['NitAdquirie', 'NitAdquirie', 'sps00', 'Sust', 'aq0cs0', 'sps00', 'unknown']
['NitAdquirie', 'NitAdquirie', 'sps00', 'Sust', 'aq0cs0', 'sps00', 'unknown']
['NitAdquirie', 'NitAdquirie', 'sps00', 'unknown', 'cs', 'Sust']
['NitAdqu', 'sps00', 'unknown', 'cs', 'Sust']
['NitAdquiri', 'Sust', 'unknown']
['NitAdqu', 'vsip3s0', 'Z']
['NitA', 'unkn']
['sps00', 'NitAdquirient', 'aq0cs0', 'sps00', 'dato']
['sps00', 'NitAdquirient', 'NitAdquirient', 'aq0cs0', 'sps00', 'dato']
['da0ms0', 'NitAdquirie', 'NitAdquirie', 'vsip3s0', 'cc']


# ### Reglas gramaticales para nit y solución

# In[190]:


grammar = r""" Q: {<unknown|dato|Z|Singlel>}
               NP: {<(NitA\w+)> <(NitA\w+)>? <sps00> <Sust> <aq0cs0>? <sps00>? <Q>}
               NP: {<(NitA\w+)> <(NitA\w+)>? <sps00> <Q> <cs> <Sust>}
               NP: {<(NitA\w+)> <(NitA\w+)>? <Sust|(vs\w+)>? <Q|cc>}
               NP: {<(NitA\w+)> <(NitA\w+)>? <aq0cs0> <sps00> <Q>}
           """

posibles = ['Fz', 'Y', 'Z', 'cc', 'dato', 'nccn000', "ncms000",
            'ncfs000', 'sps00', 'Singlel', 'unknown']

exps = ["nit con clave fafafll",
        "nit con número AAGR860628S34",
        "NIT de número x243421",
        "NIT de numero aaxr243210S01",
        "nit de clave 22",
        "nit adquiriente con numero igual a x243421",
        "nit adquiriente con número igual a aagr223455",
        "nit adquiriente con aaagg como numero",
        "nit con x como número",
        "nit clave aagr342243",
        "nit es 100",
        "nit x",
        "con nit igual a WWDA912122r44",
        "con nit adquiriente igual a aagr860628s34",
        "el nit adquiriente es y",
        "rfc con clave fafafll",
        "rfc con número AAGR860628S34",
        "rfc de número x243421",
        "rfc de numero aaxr243210'S01",
        "rfc de clave 22",
        "rfc adquiriente con numero igual a x243421",
        "rfc adquiriente con número igual a aagr223455",
        "rfc adquiriente con aaagg como numero",
        "rfc con x como número",
        "rfc clave aagr342243",
        "rfc es 100",
        "rfc x",
        "con rfc igual a WWDA912122r44",
        "con rfc adquiriente igual a aagr860628s34",
        "el rfc adquiriente es y"]

def prueba(i, exp, field, todo=True): 
    tagged = do_tagging(exp.lower(), field, ["Sust", "Singlel"])
    #print(tagged)
    result = do_chunking(grammar, tagged, field, 1)
    if todo:
        print("{0}.-".format(i), exp, "\n", result)
    else:
        print("{0}.-".format(i), exp, "\n", result[:2])
    return result

for i, exp in enumerate(exps):
    prueba(i, exp, "NitAdquirienteMex", False)


# # Para Numero de cuenta

# In[195]:


frases = ["numero de cuenta abc345",
          "el número de cuenta es Sad345",
          "cuenta con número xsa243",
          "cuenta de numero aaxr243210S01",
          "cuenta de clave 22",
          "cuenta con matrícula igual a x243421",
          "número de cuenta con número igual a aagr223455",
          "número de cuenta con 1214125 como numero",
          "cuenta 342243x",
          "la cuenta es 234342s",
          "cuenta de numero 32422a",
          "con cuenta igual a WWD224",
          "con cuenta de matricula 3424232s",
          "cuenta con numeración igual 2342211"]

for i, frase in enumerate(frases):
    #print("{0}.-".format(i),frase)
    tagged = do_tagging(frase.lower(), "Cuenta", ["Sust", "Singlel"])
    print("{0}.-".format(i), [tag[1] for tag in tagged])


# In[ ]:


Q: {<unknown|dato|Z|Singlel>}

NP: {<Cuenta> <sps00> <Sust> <Q>}
['Cuenta', 'sps00', 'Sust', 'dato']
['Cuenta', 'sps00', 'Sust', 'unknown']
['Cuenta', 'sps00', 'Sust', 'Z']
['Cuenta', 'sps00', 'Sust', 'unknown']
['sps00', 'Cuenta', 'sps00', 'Sust', 'unknown']

NP: {<Cuenta> <sps00> <Sust> <aq0cs0> <sps00>? <Q>}
['Cuenta', 'sps00', 'Sust', 'aq0cs0', 'unknown']
['Cuenta', 'sps00', 'Sust', 'aq0cs0', 'sps00', 'unknown']

NP: {<(da0\w+)>? <Sust>? <sps00|da0fs0>? <Cuenta> <(vs\w+)>? <Q>}
['Sust', 'sps00', 'Cuenta', 'dato']
['Cuenta', 'unknown']
['da0fs0', 'Cuenta', 'vsip3s0', 'unknown']
['da0ms0', 'Sust', 'sps00', 'Cuenta', 'vsip3s0', 'dato']

NP: {<Sust> <sps00> <Cuenta> <sps00> <Sust> <aq0cs0> <sps00> <Q>}
['Sust', 'sps00', 'Cuenta', 'sps00', 'Sust', 'aq0cs0', 'sps00', 'unknown']

NP: {<Sust> <sps00> <Cuenta> <sps00> <Q> <cs> <Sust>}
['Sust', 'sps00', 'Cuenta', 'sps00', 'unknown', 'cs', 'Sust']

NP: {<sps00> <Cuenta> <aq0cs0> <sps00> <Q>}
['sps00', 'Cuenta', 'aq0cs0', 'sps00', 'dato']


# ### Reglas gramaticales para numero de cuenta y solución

# In[196]:


grammar = r""" Q: {<unknown|dato|Z|Singlel>}
               NP: {<Cuenta> <sps00> <Sust> <Q>}
               NP: {<Cuenta> <sps00> <Sust> <aq0cs0> <sps00>? <Q>}
               NP: {<(da0\w+)>? <Sust>? <sps00|da0fs0>? <Cuenta> <(vs\w+)>? <Q>}
               NP: {<Sust> <sps00> <Cuenta> <sps00> <Sust> <aq0cs0> <sps00> <Q>}
               NP: {<Sust> <sps00> <Cuenta> <sps00> <Q> <cs> <Sust>}
               NP: {<sps00> <Cuenta> <aq0cs0> <sps00> <Q>}
           """

posibles = ['Fz', 'Y', 'Z', 'cc', 'dato', 'nccn000', "ncms000",
            'ncfs000', 'sps00', 'Singlel', 'unknown']

exps = ["numero de cuenta abc345",
        "el número de cuenta es Sad345",
        "cuenta con número xsa243",
        "cuenta de numero aaxr243210S01",
        "cuenta de clave 22",
        "cuenta con matrícula igual a x243421",
        "número de cuenta con número igual a aagr223455",
        "número de cuenta con 1214125 como numero",
        "cuenta 342243x",
        "la cuenta es 234342s",
        "cuenta de numero 32422a",
        "con cuenta igual a WWD224",
        "con cuenta de matricula 3424232s",
        "cuenta con numeración igual 2342211"]

def prueba(i, exp, field, todo=True): 
    tagged = do_tagging(exp.lower(), field, ["Sust", "Singlel"])
    #print(tagged)
    result = do_chunking(grammar, tagged, field, 1)
    if todo:
        print("{0}.-".format(i), exp, "\n", result)
    else:
        print("{0}.-".format(i), exp, "\n", result[:2])
    return result

for i, exp in enumerate(exps):
    prueba(i, exp, "Cuenta", False)


# ## Ejemplo de como si usan un Q con un elemento, despues no se puede utilizar el elemento por separado
# 
# 1.- Notar la diferencia en el Q

# In[255]:


tagged = do_tagging("y documento con número igual a e", "NoDocumento")
grammar = r"""Q: {<cc|dato|Z|Singlel|unknown|>}
              NP: {<cc> <(NoDocum\w+)> <sps00> <(NoDocum\w+)|ncms000> <aq0cs0> <sps00> <Q>}
           """
cp = nltk.RegexpParser(grammar)
chunked = cp.parse(tagged)
chunked


# 2.- Notar que si se le quita el 'cc' dentro del Q si encuentra la frase

# In[257]:


tagged = do_tagging("y documento con número igual a e", "NoDocumento")
grammar = r"""Q: {<dato|Z|Singlel|unknown>}
              NP: {<cc> <(NoDocum\w+)> <sps00> <(NoDocum\w+)|ncms000> <aq0cs0> <sps00> <Q|cc>}
           """
cp = nltk.RegexpParser(grammar)
chunked = cp.parse(tagged)
chunked


# ### Para que puedan avanzar más rápido en la creación de estructuras

# ```python
# ['NoDocumen', 'sps00', 'NoDocumen', 'dato']
# ['NoDocumen', 'sps00', 'ncms000', 'cc']
# ['NoDocumen', 'sps00', 'NoDocumen', 'dato']
# ['NoDocumen', 'sps00', 'ncms000', 'Z']
# ['NoDocumen', 'sps00', 'NoDocumen', 'aq0cs0', 'sps00', 'dato']
# ['NoDocumen', 'sps00', 'ncms000', 'aq0cs0', 'sps00', 'cc']
# ['NoDocumen', 'sps00', 'dato', 'cs', 'NoDocumen']
# ['NoDocumen', 'sps00', 'dato', 'cs', 'ncms000']
# ['NoDocumen', 'sps00', 'NoDocumen', 'vsip3s0', 'Z']
# ['ncms000', 'sps00', 'NoDocumen', 'vsip3s0', 'Z']
# ['sps00', 'ncms000', 'sps00', 'NoDocumen', 'dato']
# ['sps00', 'NoDocumen', 'sps00', 'NoDocumen', 'sps00']
# ```
# 
# ```python
# Q: {<dato|Z|ncms000>}
# 
# NP: {<NoDocumen> <sps00> <NoDocumen|ncms000> <Q>}
# 
# NP: {<sps00> <NoDocumen|ncms000> <sps00> <NoDocumen> <Q>}
# ```

# ## Para sacar los tipos de palabras contenidos en el corpus, por tipo

# In[139]:


from nltk.corpus import cess_esp

palabras = cess_esp.tagged_words()
palabras = np.array(palabras)

cosas = np.unique([tup[1] for tup in palabras])
dictt = {}
for key in cosas:
    dictt.update(dict(zip([key], [np.unique([palabra[0] for palabra in palabras if palabra[1] == key])])))
print(dictt)


# In[141]:


sgt.pos_tag(["n"])


# ## Ejemplo de como funciona la búsqueda de la estructura y la palabra dentro de ella

# In[250]:


tagged = sgt.pos_tag("Mi madre me ama y me canta".split())
print("Palabras Etiquetadas: ", tagged, "\n")
grammar = r"NP: {<pp1cs000> <ncfs000>}"
cp = nltk.RegexpParser(grammar)
chunked = cp.parse(tagged)
for subtree in chunked:
    if isinstance(subtree, nltk.Tree) and subtree.label() == "NP":
        print("Frase encontrada: ", subtree.label(), subtree.leaves())

