from ChatbotWrapper.DF.B2B1.CB_DF_Facturas import factura
from ChatbotWrapper.DF.intentLogic import analizeReq
import json
from pprint import pprint

with open('ChatbotWrapper/DF/B2B1/FacturasVDNS.json') as f:
    specjson = json.load(f)

clave = False

def respfact(req: dict, action):
    global clave
    print(str(clave))
    print("]]]]]]from ChatbotWrapper.DF.B2B1.CB_DF_Facturas import factura
from ChatbotWrapper.DF.intentLogic import analizeReq
import json
from pprint import pprint

with open('ChatbotWrapper/DF/B2B1/FacturasVDNS.json') as f:
    specjson = json.load(f)

clave = False

def respfact(req: dict, action):
    global clave
    print(str(clave))
    print("]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]WE GOT THE ACTION: " + action)
    if action == "provee_numero_usuario":
        clave = True
        response = analizeClave(req)


    elif action == "qna":
        response = analizeReq(req, specjson)

    elif action == "soporteTecnico":
        response = {
            "fulfillmentText": specjson["dicActions"][action]
        }

    elif action == "factura":
        if clave:
            response = {
                "fulfillmentText": specjson["dicActions"][action]
            }
            #response = factura(req)
        else:
            respIntent = "El servicio de consulta de facturas está restringido a usuarios. Diga o digite su usuario o consulte a un ingeniero de soporte técnico."
            response = {
                "fulfillmentText": respIntent
            }
    elif action == "levantaTicket":
        if clave:
            response = {
                "fulfillmentText": specjson["dicActions"][action]
            }
        else:
            response = {
                "fulfillmentText": "El trámite de creación de tickets es exclusivo de usuarios registrados."
            }
    elif action == "consultaTicket":
        if clave:
            response = {
                "fulfillmentText": specjson["dicActions"][action]
            }
        else:
            response = {
                "fulfillmentText": "El trámite de consulta de tickets es exclusivo de usuarios registrados."
            }
    return response


def analizeClave(req: dict):
    numeroUsuario = req["queryResult"]["parameters"]["usuario"]
    #check if he exists on database
    #save user number in global variable for use during session
    respIntent = "Bienvenido " + str(numeroUsuario["value"])
    response = {
        "fulfillmentText": respIntent
    }
    return response
]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]WE GOT THE ACTION: " + action)
    if action == "provee_numero_usuario":
        clave = True
        response = analizeClave(req)


    elif action == "qna":
        response = analizeReq(req, specjson)
    elif action == "soporteTecnico":
        response = {
            "fulfillmentText": "lo comunicaré con el soporte técnico. Espere en la línea."
        }

    elif action == "factura":
        if clave:
            response = {
                "fulfillmentText": "tramitando su factura"
            }
            #response = factura(req)
        else:
            respIntent = "El servicio de consulta de facturas está restringido a usuarios. Diga o digite su usuario o consulte a un ingeniero de soporte técnico."
            response = {
                "fulfillmentText": respIntent
            }
    elif action == "levantaTicket":
        if clave:
            response = {
                "fulfillmentText": "levantando su ticket"
            }
        else:
            response = {
                "fulfillmentText": "El trámite de creación de tickets es exclusivo de usuarios registrados."
            }
    elif action == "consultaTicket":
        if clave:
            response = {
                "fulfillmentText": "Consultando su ticket"
            }
        else:
            response = {
                "fulfillmentText": "El trámite de consulta de tickets es exclusivo de usuarios registrados."
            }
    return response


def analizeClave(req: dict):
    numeroUsuario = req["queryResult"]["parameters"]["usuario"]
    #check if he exists on database
    #save user number in global variable for use during session
    respIntent = "Bienvenido " + str(numeroUsuario["value"])
    response = {
        "fulfillmentText": respIntent
    }
    return response
