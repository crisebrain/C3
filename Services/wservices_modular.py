from .saldos_vdns import makeresponseAction, informacion
from .facturas import factura, dudasFacturasCampos

import json
import sys
sys.path.append("Utils")
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
            return factura(req)
        else:
            return {"payload": {"result": "Null", "returnCode": "0"},
                   "fulfillmentText": "Null"}
    except Exception as exception:
        errors.logger.info(json.dumps(req.get("queryResult")) + "\n")
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
