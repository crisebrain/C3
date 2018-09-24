import json
from Utils.logtofile import CreateLogger


def makeWebhookResult(req, origin = 1):
    if origin == 1:
        from ChatbotWrapper.DF import preguntasRespuestas
        from ChatbotWrapper.CB_DF_Facturas import factura
        from ChatbotWrapper.Utils import methods_DF_to_IM as IM
        originstr = "WhDF"
    else:
        from .saldos_vdns import makeresponseAction, informacion
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
        if origin ==1:
            # Cada servicio es responsable de construir su propio retorno
            # de error, parecido a esto;
            # return {"payload": {"result": "Null", "returnCode": "0"},
            #         "fulfillmentText": "Null"}
            if action == "factura":
                return factura(req)
            elif action == "preguntasRespuestas":
                return preguntasRespuestas.analizeReq(req)
            else:
                response = IM.post_data(req)
                return response
        else:
            if action == "VDN" or action == "saldo":
                return makeresponseAction(req, action)
            elif action == "informacion":
                return informacion(queryResult.get("parameters").get("servicio"))
            else:
                return {"payload": {"result": "Null", "returnCode": "0"},
                        "fulfillmentText": "Null"}

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
        return {"payload": {"result": "Null", "returnCode": "0"},
                "fulfillmentText": msgerror}
