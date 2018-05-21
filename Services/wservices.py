from .bd_busqueda import dbquery
import json

def makeWebhookResult(req):
    action = req.get("queryResult").get("action")
    try:
        if action == "VDN" or action == "saldo":
            return makeresponseAction(req, action)
        elif action == "informacion":
            return informacion(req.get("queryResult").get("parameters").get("servicio"))
        else:
            return {"payload": {"result": "Null", "returnCode": "0"},
                   "fulfillmentText": "Null"}
    except Exception as err:
        return {"payload": {"result": "Null", "returnCode": "0"},
                "fulfillmentText": "{0}".format(err)}

def makeresponseAction(req, action):
    # Carga de base de datos
    result = req.get("queryResult").get("parameters")
    
    if result.get("nombre") != "":
        coincidencias = dbquery(result.get("nombre"))
        print(json.dumps(coincidencias, indent=4))
        returnCode = calcCode(coincidencias)
    else:
        returnCode = calcCode([], True)
        coincidencias = []
        
    textresp = mensajson(coincidencias, returnCode, action, result.get("nombre"))
    resultarray = []
    for coin in coincidencias:
        resultarray.append(dict(zip(["nombre", action],
                                    [coin["Nombre"], coin[action]])))
    

    resp = {#"speech": textresp,
            "payload": {"result": resultarray, "returnCode": returnCode},
            "fulfillmentText": textresp}
            #"source": "telegram"}#req.get("queryResult").get("intent").get("displayName")}
    return resp

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
            Text = "¿Con quién desea hablar"
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
            Text = "Existen demasiadas coincidencias, necesitas ser mas especifico"
            
    elif action == "saldo":
        if valor == "":
            Text = "¿Cuál es el nombre de usuario?"
            return Text
    
        if code == 0:
           Text = "No hay referencia de esa persona. ¿Con qué otra persona te comunico?"
        
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
            Text = "Existen demasiadas coincidencias, necesitas ser mas especifico"
    return Text

def informacion(servicio):
    servicios = {
        "saldo": "Servicio de Saldo",
        "VDN": "Servicio de VDNs."
        }
    
    resp = servicios.get(servicio)
    
    return {"fulfillmentText": resp}
    
