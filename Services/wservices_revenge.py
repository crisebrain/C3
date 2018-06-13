from .bd_busqueda import dbquery
from .b2bcliente import sendReq, getResponseValues, HumanResult
import json
import sys
sys.path.append("../Utils")
from logtofile import CreateLogger

def makeWebhookResult(req):
    action = req.get("queryResult").get("action")
    querys = CreateLogger("querys")
    querys.logger.info(json.dumps(req.get("queryResult")) + "\n")
    errors = CreateLogger("errors")
    try:
        if action == "VDN" or action == "saldo":
            return makeresponseAction(req, action)
        elif action == "informacion":
            return informacion(req.get("queryResult").get("parameters").get("servicio"))
        elif action == "dudasFacturasCampos":
            return dudasFacturasCampos(req.get("queryResult").get("parameters").get("campo"))
        elif action == "factura":
            return factura(req.get("queryResult").get("parameters"))
        else:
            return {"payload": {"result": "Null", "returnCode": "0"},
                   "fulfillmentText": "Null"}
    except Exception as exception:
        errors.logger.exception(exception)
        errors.logger.info(json.dumps(req.get("queryResult")) + "\n")
        if type(exception).__name__ == "AttributeError":
            msgerror = "El servicio de factura no ha respondido correctamente. " \
                       "Favor de reportalo con su administrador."
        else:
            nline = exception.__traceback__.tb_lineno
            cause = exception.__str__()
            msgerror = "Estimado usuario,"\
                       "Ocurrió el error: {0} en {1}".format(cause, nline)
            msgerror += "Favor de reportarlo con su administrador"

        return {"payload": {"result": "Null", "returnCode": "0"},
                "fulfillmentText": msgerror}

def makeresponseAction(req, action):
    """Creates the response json object to send as answer to the webhook.
    Parameters:
    req - json request object with the petition.
    action - string with the action to process as webservices. "VDN", "Saldo" o
             "factura"
    Output:
    resp - json object with the response to send by webhook to DF.
           includes the fields:
           "payload": {"result": result Array like of the query,
                       "returnCode": error code of the query},
           "fulfillmentText": TextString
    """
    # Carga de base de datos
    result = req.get("queryResult").get("parameters")

    nombre = construyeNombre(result)

    if nombre != "":
        coincidencias = dbquery(nombre)
        print(json.dumps(coincidencias, indent=4))
        returnCode = calcCode(coincidencias)
    else:
        returnCode = calcCode([], True)
        coincidencias = []

    textresp = mensajson(coincidencias, returnCode, action, nombre)
    resultarray = []
    for coin in coincidencias:
        resultarray.append(dict(zip(["nombre", action],
                                    [coin["Nombre"], coin[action]])))


    resp = {"payload": {"result": resultarray, "returnCode": returnCode},
            "fulfillmentText": textresp}
            # "followupEventInput": {"name": "salida",
            #                "parameters": {"prueba": "1"},
            #                "languageCode": "es"}}

    respContext = evaluaContextos(returnCode, action,
                                  nombre, req.get("session"))

    if respContext:
        resp.update(respContext)

    return resp

def evaluaContextos(code, action, valor, session):
    if action == "VDN" and code == 1 and valor:
        outputContexts = [{"name": session + "/contexts/0-2vdn-followup",
                           "lifespanCount": 0},
                          {"name": session + "/contexts/0-2vdn-followup-2",
                           "lifespanCount": 0}]
    if action == "saldo" and code == 1 and valor:
        outputContexts = [{"name": session + "/contexts/0-1saldo-followup",
                           "lifespanCount": 0},
                          {"name": session + "/contexts/0-1saldo-followup-2",
                           "lifespanCount": 0}]
        return {"outputContexts": outputContexts}

def calcCode(array, empty=False):
    if not empty:
        ncoincidencias = len(array)
        if ncoincidencias == 0: #No encontró a nadie
            code = 0
        elif ncoincidencias == 1: #Encontró a alguien
            code = 1
        elif ncoincidencias < 4: # Encontró menos de 3 personas
            code = 2
        else:
            code = 3 # Encontró más de 3 personas
        return code
    else:
        return 1

def mensajson(array, code, action, valor):
    if action == "VDN":
        if valor == "":
            Text = "¿Con quién desea hablar?"
            return Text

        if code == 0:
            Text = "No hay referencia de esa persona. ¿Con qué otra persona te comunico?"

        elif code == 1:
            elem = array[0]
            Text = "Será transferido con {0} {1} y tel: {2}.".format(elem["Nombre"],
                                                        elem["Apellido"],
                                                        elem["VDN"])
            Text += "\nHasta luego."

        elif code == 2:
            textnames = [elem["Nombre"] + " " + elem["Apellido"] for elem in array]
            textnames = ' o '.join(textnames)
            Text = "¿A cual persona te refieres? a {0}".format(textnames)

        else:
            Text = "Existen demasiadas coincidencias, necesitas ser mas específico"

    elif action == "saldo":
        if valor == "":
            Text = "¿Cuál es el nombre de usuario?"
            return Text

        if code == 0:
           Text = "No hay referencia de ese usuario. Si necesita el saldo de " \
                  "alguien más sólo díga el nombre de usuario correcto."

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
            Text = "Existen demasiadas coincidencias, necesitas ser mas específico"
    return Text

def informacion(servicio):
    servicios = {
        "saldo": "Servicio de Saldo",
        "VDN": "Servicio de VDNs."
        }

    resp = servicios.get(servicio)

    return {"fulfillmentText": resp}
