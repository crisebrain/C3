from .saldos_vdns import makeresponseAction, informacion
import json
import sys
sys.path.append("Utils")
sys.path.append("ChatbotWrapper")
from logtofile import CreateLogger
from CB_DF_Facturas import factura

def makeWebhookResult(req, origin = 1):
    if origin == 1:
        originstr = "WhDF"
    else:
        originstr = "WbIM"

    if req.get("queryResult"):
        queryResult = req.get("queryResult")
        action = queryResult.get("action")
    else:
        queryResult = None
        action = req.get("action")
    
    conlog = False
    try:
        querys = CreateLogger("querys" + originstr)
        errors = CreateLogger("errors" + originstr)
        if queryResult:
            querys.logger.info(json.dumps(req.get("queryResult")) + "\n")
        conlog = True
    except (PermissionError, FileNotFoundError):
        print("\n************************* WARNING *************************")
        print("No fue posible crear correctamente los loggers del proyecto")
        print("***********************************************************\n")
    try:
        if action == "VDN" or action == "saldo":
            return makeresponseAction(req, action)
        elif action == "informacion":
            return informacion(queryResult.get("parameters").get("servicio"))
        elif action == "factura":
            return factura(req)
        # elif action == "obtieneDatos":
            # seakexpresion
        else:
            if origin == 1:
                return {"payload": {"result": "Null", "returnCode": "0"},
                        "fulfillmentText": "Null"}
            # else:
            #     return {"payload": {"result": "Null", "returnCode": "0"},
            #             "fulfillmentText": "Null"}
    except Exception as exception:
        if conlog and queryResult:
            errors.logger.info(json.dumps(queryResult) + "\n")
            errors.logger.exception(exception)
        if type(exception).__name__ == "AttributeError":
            msgerror = "El servicio de factura no ha respondido correctamente. " \
                       "Favor de reportalo con su administrador."
        else:
            nline = exception.__traceback__.tb_lineno
            cause = exception.__str__()
            msgerror = "Estimado usuario,"\
                       "Ocurrió el error: {0} en {1}".format(cause, nline)
            msgerror += "Favor de reportarlo con su administrador"
        if origin == 1:
            return {"payload": {"result": "Null", "returnCode": "0"},
                    "fulfillmentText": msgerror}
