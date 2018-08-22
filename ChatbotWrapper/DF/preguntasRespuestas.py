def analizeReq(req: dict):
    value = None
    contexts = []
    respIntent = "No existe respuesta. Probablemente nadie lo sepa"
    intentName = req["queryResult"]["intent"]["displayName"]

    if req["queryResult"].get("outputContexts"):
        contexts = req["queryResult"]["outputContexts"]


    dicDuplicate = {
        "general_que_son": ["cx_interfaz", "cx_objeto", "cx_carro"]
    }

    dicResponse = {
        "interfaz_costo": "El costo varía, según lo que quieras.",
        "objeto_tipo": "Pues el tipo de objeto...",
        "general_que_son":{
            "interfaz": "Son las interfaces de usuario.",
            "objeto": "Son cosas que puede usar el usuario.",
            "carro": "Son vehículos para desplazarte."
        }
    }

    # Set type of query "que son"
    if req["queryResult"]["parameters"].get("que_son"): # TODO: hacer bien esta parte. Probablemente con un ajuste del nombre de la entity.
        value = list(req["queryResult"]["parameters"]["que_son"].keys())[0]


    # If is a intent duplicate and hasn't value. We need context.
    duplicate = dicDuplicate.get(intentName)

    if duplicate:
        if not value:
            if len(contexts) == 1:
                context = contexts[0]["name"].split("/")[-1]
                value = context[3:]
                respIntent = dicResponse[intentName][value]
            if len(contexts) > 1:
                pass # TODO
        else:
            respIntent = dicResponse[intentName][value]
    else:
        respIntent = dicResponse.get(intentName, respIntent)


    resp = {
        "fulfillmentText": respIntent
    }

    return resp
