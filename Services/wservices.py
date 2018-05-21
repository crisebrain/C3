from .bd_busqueda import dbquery
import json

def makeWebhookResult(req):
    action = req.get("queryResult").get("action")
    try:
        if action == "VDN" or action == "saldo":
            return makeresponseAction(req, action)
        else:
            return {"payload": {"result": "Null", "returnCode": "0"},
                   "fulfillmentText": "Null"}
    except Exception as err:
        return {"payload": {"result": "Null", "returnCode": "0"},
                "fulfillmentText": "Null"}

def makeresponseAction(req, action):
    # Carga de base de datos
    result = req.get("queryResult").get("parameters")
    coincidencias = dbquery(result.get("nombre"))
    print(json.dumps(coincidencias, indent=4))
    returnCode = calcCode(coincidencias)
    textresp = mensajson(coincidencias, returnCode, action)
    resultarray = []
    for coin in coincidencias:
        resultarray.append(dict(zip(["nombre", action],
                                    [coin["Nombre"], coin[action]])))

    resp = {#"speech": textresp,
            "payload": {"result": resultarray, "returnCode": returnCode},
            "fulfillmentText": textresp}
            #"source": "telegram"}#req.get("queryResult").get("intent").get("displayName")}
    return resp

def calcCode(array):
    ncoincidencias = len(array)
    if ncoincidencias == 0:
        code = 0
    elif ncoincidencias == 1:
        code = 1
    elif ncoincidencias < 4:
        code = 2
    else:
        code = 3
    return code

def mensajson(array, code, action):
    if action == "VDN":
        if code == 0:
            Text = "No hay referencia de esa persona"
        elif code == 1:
            elem = array[0]
            Text = "El telefono de {0} {1} es {2}.".format(elem["Nombre"],
                                                          elem["Apellido"],
                                                          elem["VDN"])
            Text += "\n¿Deseas algo más?"
        elif code == 2:
            textnames = [elem["Nombre"] + " " + elem["Apellido"] for elem in array]
            textnames = ' o '.join(textnames)
            Text = "¿A cual persona te refieres? a {0}".format(textnames)
        else:
            Text = "Tengo {0} coincidencias, necesitas ser mas especifico".format(len(array))
    elif action == "saldo":
        if code == 0:
            Text = "No hay referencia de esa persona"
        elif code == 1:
            elem = array[0]
            Text = "El saldo de {0} {1} es {2} pesos".format(elem["Nombre"],
                                                             elem["Apellido"],
                                                             elem["saldo"])
            Text += "\n¿Deseas algo más?"
        elif code == 2:
            textnames = [elem["Nombre"] + " " + elem["Apellido"] for elem in array]
            textnames = ' o '.join(textnames)
            Text = "¿A cual persona te refieres? a {0}".format(textnames)
        else:
            Text = "Tengo {0} coincidencias, necesitas ser mas especifico".format(len(array))
    return Text
