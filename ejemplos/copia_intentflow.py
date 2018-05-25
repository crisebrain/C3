    queryResult = jdata.get("queryResult")
    # Extrayendo campos de query
    msgOriginal = queryResult.get("queryText")
    if "action" in queryResult.keys():
        action = queryResult.get("action")
    # Revisar como allRequiredParamsPresent está relacionado con los
    # parametros contextuales y como los voy a consultar o si es el fallback
    allRequiredParamsPresent = queryResult.get("allRequiredParamsPresent")
    # --------------------------------------------------------------------
    # extrae los nombres de los contextos del arreglo outputcontexts
    separa = lambda x: x.split("/")[-1]
    contextnames = [context["name"]
                    for context in queryResult.get("outputContexts")]
    contextnames = list(map(separa, contextnames))
    # --------------------------------------------------------------------
    parameters = [context["parameters"] for context
                  in queryResult.get("outputContexts")]
    # Extrae los parametros del arreglo outputcontext y guarda en una lista
    params = dict()
    for param in parameters:
        params.update(dict(zip(param.keys(), param.values())))
    print(params)
    parametkeys = list(params.keys())
    nodeparameters = []
    for indp, param in enumerate(node.parameters):
        indices = [True if param["name"] == key else False
                   for key in parametkeys]
        if any(indices):
            index = indices.index(True)
            param["userValue"] = params[parametkeys[index]]
            nodeparameters.append(param)
    print(nodeparameters) # considerar valor vacio
    # parameters para nodo con valor guardado
    DetectionConfidence = queryResult.get("intentDetectionConfidence")

    if allRequiredParamsPresent:
        jdata = dict(msgOriginal=msgOriginal,
                     action=action,
                     accuracyPrediction=DetectionConfidence, # no es igual
                     parameters=nodeparameters,
                     id=node.id)  # este es para que lo busque el arbol
        self.sc.feedNextEntry(jdata, dict(zip(contextnames, parameters)))
    self.sc.ShowSessionTree()
    tree = self.sc.extractTree()
    print(tree.currentcontextdict)


# leer

refparameters = nodereferenced.parameters
indices = [True if parameter["name"] == refparam["name"]
           else False for refparam in refparameters]
index = indices.index(True)
if refparameters[index][]
