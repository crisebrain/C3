
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

# In[2]:


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

# In[94]:


def regexextractor(expression, field):
    pattern = patterns[field]
    result = re.search(pattern=pattern, string=expression)
    if result:
        return result.group()
    else:
        return None

def do_tagging(exp, field):
    tokens = nltk.word_tokenize(exp)
    tagged = sgt.pos_tag(tokens)
    tagged = np.array([list(tup) for tup in tagged]).astype(str)
    mask = tagged[:, 1] == 'None'
    for i, token in enumerate(tokens):
        if token in dictfacturas[field]:
            tagged[i, 1] = str(field)
    unknowns, = np.where(mask)
    for unknown in unknowns:
        if tagged[unknown, 0] in dictfacturas[field]:
            tagged[unknown, 1] = field
        else:
            if regexextractor(tokens[unknown], field) is not None:
                tagged[unknown, 1] = "dato"
            else:
                tagged[unknown, 1] = "unknown"
    return [tuple(wordtagged) for wordtagged in tagged]

def do_chunking(grammar, tagged, field, code):
    cp = nltk.RegexpParser(grammar)
    chunked = cp.parse(tagged)
    continuous_chunk = []
    entity = []
    unknowns = []
    subt = []
    for i, subtree in enumerate(chunked):
        if isinstance(subtree, nltk.Tree):
            # añadir las condiciones que sean necesarias para contemplar los posibles valores
            posibles = ["dato", "Z", "ncfs000", "ncms000", "ncfs000"]
            entity += [token for token, pos in subtree.leaves()
                       if pos in posibles]
            unknowns += [token for token, pos in subtree.leaves()
                         if pos == "unknown"]
            subt.append(subtree)
    if entity == []:
        code = 0
        if len(unknowns) > 1:
            entity = unknowns[-1].upper()
        elif unknowns != []:
            entity = unknowns[0].upper()
        else:
            entity = None
    elif len(entity) > 1:
        code = 0
        entity = entity[-1].upper()
    else:
        entity = entity[0].upper()
        if regexextractor(entity, field) is not None:
            code = 1
        else:
            code = 0
    return entity, code, subt, tagged


# In[47]:


do_tagging('las documento prefijo son casa', 'NoDocumento')


# ### NOTA: 
#       
#       la palabra prefijo no está en el diccionario, por lo tanto como es detectada como desconocida 
#       pero cumple con la expresión regular del campo, la asigna como posible dato

# # Ejemplo de grammar

# ```python
# grammar = r"""NP: {<Prefijo> <(vs\w+)|(nc\w+)|(wmi\w+)|(spc\w+)>* <dato|Z|unknown>}
#               NP: {<Prefijo> <(vmi\w+)|(aq\w+)|unknown>? <sp\w+>? <dato|Z|unknown>}
#               NP: {<Prefijo> <dd0fs0> <vmp00sm> <sps00> <dato|Z|unknown>}
#               NP: {<dato|Z|unknown> <(vs\w+)> <(da\w+)> <Prefijo>}
#               NP: {<dato|Z|unknown> <(p030\w+)>? <vmip3s0>? <cs> <Prefijo>}
#            """
# ```
# ### Nota:
#     
#     falta definir nodos terminales

# # Para diseñar las reglas y probar
# 
# NOTA:
#     
#     Correr cada que se cambie el grammar

# In[110]:


grammar = r"""NP: {<Prefijo> <(vs\w+)|(nc\w+)|(wmi\w+)|(spc\w+)>* Q}
              NP: {<Prefijo> <(vmi\w+)|(aq\w+)|unknown>? <sp\w+>? Q}
              NP: {<Prefijo> <dd0fs0> <vmp00sm> <sps00> Q}
              NP: {Q <(vs\w+)> <(da\w+)> <Prefijo>}
              NP: {Q <(p030\w+)>? <vmip3s0>? <cs> <Prefijo>}
              Q: {<dato|Z|unknown|ncfs000|ncms000>}
            """

def prueba(exp, field): 
    tagged = do_tagging(exp.lower(), field)
    return do_chunking(grammar, tagged, field, 1)


# NOTA:
#     
#     salida: (VALOR, CODIGO DE VALIDEZ, FRASE ETIQUETADA QUE CUMPLE CON GRAMMAR, FRASE ETIQUETADA)

# In[112]:


exp = 'escuela es el prefijo'
field = "Prefijo"
prueba(exp, field)

