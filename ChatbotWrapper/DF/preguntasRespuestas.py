from ChatbotWrapper.Utils import methods_DF_to_IM as IM

def analizeReq(req: dict):
    value = None
    respIntent = "No existe respuesta. Probablemente nadie lo sepa"
    intentName = req["queryResult"]["intent"]["displayName"]

    dicContextHuman = {
        "cx_interfaz": "Interfaces",
        "cx_objeto": "Objetos",
        "cx_carro": "Carros"
    }

    # IntentName y los contextos.
    dicDuplicate = {
        "general_que_son": ["cx_interfaz", "cx_objeto"],
        "general-modulo": ["cx_nomina", "cx_imss"]
    }

    # IntentName y sus respuestas.
    dicResponse = {
        "interfaz_costo": "El costo varía, según lo que quieras.",
        "objeto_tipo": "Pues el tipo de objeto...",
        "carros_marca": "es el fabricante del carro",
        "imss-servicios": "El IMSS tiene varios servicios.",
        "general_que_son": {
            "interfaz": "Son las interfaces de usuario.",
            "objeto": "Son cosas que puede usar el usuario."
        },
        "general-modulo": {
            "imss": "El módulo IMSS contiene la funcionalidad general de los servicios del IMSS a los cuales se tiene acceso desde el portal.",
            "nomina": "El módulo nómina, bla, bla, bla."
        }
    }

    # Set type of query "que son"
    if req['queryResult']['parameters'].keys():
        for key in req['queryResult']['parameters'].keys():
            value = list(req['queryResult']['parameters'][key].keys())[0]

    # IM.updateIM(req, {"algo": 1})
    IM.post_data(req)

    # If is a intent duplicate and hasn't value. We need context.
    duplicate = dicDuplicate.get(intentName)

    if duplicate:
        # Pregunta implícita. Necesita contextos.
        if not value:
            # get get history of contexts
            reqRecVal = {
                "action": "recuperaValores",
                "data": {
                    "reqObject": "context",
                    # A veces hay contextos que no nos interesan como el followup, y debemos quitarlos.
                    # Únicamente necesitamos dos.
                    "numberHistory": 4,
                    "session": req['session'].split("sessions/")[-1],
                    "agent": req['session'].split("/")[1],
                }
            }
            respRecupera = IM.post_data(reqRecVal)
            print(respRecupera)

            if respRecupera["returnCode"] == 1:
                # extracting useful information about history contexts
                # historyContexts = respRecupera["Objects"]
                # historyConDup = [context[0] for context in historyContexts if context[0] in dicDuplicate[intentName]]
                # Clean lista and cut to 2 contexts
                historyContexts = _cleanHistoryContext(respRecupera["Objects"].copy(), dicDuplicate[intentName], 2)

                if len(historyContexts) == 0:
                    respIntent = "¿De qué tema me hablas?"
                elif len(historyContexts) == 1:
                    respIntent = dicResponse[intentName][historyContexts[0][3:]]
                elif len(historyContexts) == 2:
                    respIntent = "¿Te refieres a {} o a {}?".format(dicContextHuman[historyContexts[0]],
                                                                  dicContextHuman[historyContexts[1]])
        # Pregunta explícita. Dan la entity en la misma pregunta.
        else:
            respIntent = dicResponse[intentName][value]

    # Caso donde primero hicieron pregunta implícita, y luego me especifican de que hablan.
    elif intentName == "general_que_son-de_que":
        respIntent = dicResponse[intentName.split("-")[0]][value]

    else:
        respIntent = dicResponse.get(intentName, respIntent)


    resp = {
        "fulfillmentText": respIntent
    }

    print(resp)

    return resp


def _cleanHistoryContext(contexts: list, wanted: list, previousContext: int):
    """
    Limpia los contextos dejando únicamente los que nos interesan.
    Esta función también borra los followup.
    :param contexts: lista de contextos original
    :param wanted: diccionarios de contextos duplicados
    :previousContext: número máximo de contextos a buscar hacia atrás (no incluye followup)
    :return: retorna una lista sin los contextos que no nos interesan
    """
    # extracting useful information about history contexts

    historyContexts = []
    contextsTemp = []

    for context in contexts:
        if not "followup" in context[0]:
            contextsTemp.append(context)

    for context in contextsTemp[-previousContext:]:
        if context[0] in wanted:
            historyContexts.append(context[0])


    # historyContexts = [context[0] for context in contexts if context[0] in listUnwanted]
    return historyContexts


def _testRecuperaValores(number):
    listContext =[]
    if number == 1:
        listContext = [["cx_interfaz"]]
    elif number == 2:
        listContext = [["cx_interfaz"], ["cx_objeto"]]

    return {
	    "Objects": listContext,
	    "message": "Ok",
	    "returnCode": 1
    }
