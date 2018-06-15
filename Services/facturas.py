from .b2bcliente import sendReq, getResponseValues, HumanResult
import json

def dudasFacturasCampos(campo):
    entrada = "Para factura, "
    campos = {
        "documento": entrada + "el campo Tipo Documento como su nombre lo indica "
                    "hace referencia a las variantes de documento con que cuenta "
                    "el sistema, en este momento se encuentran disponibles "
                    "documentos de tipo Factura o Nota de Crédito.",
        "estado": entrada + "el campo Estatus indica los posibles estados en los "
                    "cuales se encuetra el documento, siendo estos: "
                    "Recibido, Firmado, Aceptado, Rechazado, Error o Enviado.",
        "prefijo": entrada + "el campo Serie (Prefijo) identifica los documentos "
                    "por un nivel general de organización, en este caso se "
                    "representa mediante un valor alfanumérico, por ejemplo puede "
                    "ser la serie B.",
        "acuse": entrada + "el campo Acuse indica el estado de recepción del "
                    "documento pudiendo ser Aceptado, Rechazado o Pendiente.",
        "numero": entrada + "el campo Número de Factura se refiere al identificador "
                    "específico del documento, este valor acepta números y letras. ",
        "periodo": entrada + "el campo Periodo hace referencia a valores de "
                    "tiempo predefinidos, siendo estos: Hoy, Semana y Mes."
        }
    resp = campos.get(campo)
    return {"fulfillmentText": resp}


def factura(parametros):
    # Ya que los elemenetos vienen en una lista deben tener un tratamiento
    # particular
    listaCampos = parametros["facturasCampos"]
    diccFusionado = {}

    # Fusionamos todos los diccionarios
    for dicc in listaCampos:
        diccFusionado.update(dicc)

    dicReady = preparaParametros(diccFusionado)
    print(dicReady)

    # Caso que no traiga ninguna restricción. Consulta muy amplia.
    # if not(estado or prefijo or periodo or numFactura or acuse):
    #
    #     # TODO: Implementar caso de que traiga valores inválidos
    #
    #     respuesta = "Debe acotar su consulta, ya que el resultado puede ser muy" \
    #                 " grande. Puede delimitarla con los campos:" \
    #                 "\nTipo de documento," \
    #                 "\nEstado," \
    #                 "\nSerie," \
    #                 "\nPeriodo," \
    #                 "\nAcuse," \
    #                 "\nNumero de Factura"
    #
    #     return {"fulfillmentText" : respuesta}

    # servicio de factura
    req = sendReq(dicReady)
    findedFac = HumanResult(getResponseValues(req.content))
    print(findedFac)

    peticionStr = ""
    for elemento in dicReady:
        if dicReady[elemento] is not None:
            peticionStr += elemento + ": {0} \n".format(dicReady[elemento])

    peticionStr += ".\n----------------Resultados:-------------------\n" + findedFac

    respuesta =  {
                    "fulfillmentText" : peticionStr,
                    "payload": {
                        "resultIn": dicReady ,
                        "resultOut": getResponseValues(req.content)
                    }
    }
    
    print(respuesta)

    return respuesta


def preparaParametros(dic):
    dicReady = {}

    # Obtenemos los valores y los preparamos
    dicReady.setdefault("Factura", dic.get("tipoDocumento"))

    dicReady.setdefault("Periodo", dic.get("periodo"))

    if dic.get("status"):
        dicReady.setdefault("Status", dic.get("status").get("value"))

    # TODO: Corregir los upper para NONE.
    if dic.get("prefijo"):
        prefijo = dic.get("prefijo").get("value")
        if not isinstance(prefijo, str):
            dicReady.setdefault("Prefijo", str(int(prefijo)))
        else:
            dicReady.setdefault("Prefijo", prefijo.upper())

    if dic.get("acuse"):
        dicReady.setdefault("Acuse", dic.get("acuse").get("value"))

    if dic.get("numeroFactura"):
        numfactura = dic.get("numeroFactura").get("value").get("value")
        if not isinstance(numfactura, str):
            dicReady.setdefault("NumeroFactura", str(int(numfactura)))
        else:
            dicReady.setdefault("NumeroFactura", numFactura.upper())

    # hardcoded:
    dicReady.setdefault("Empresa", "RICOH")
    dicReady.setdefault("FechaEmisionInicio", None)
    dicReady.setdefault("FechaEmisionFin", None)
    dicReady.setdefault("Cuenta", None)
    dicReady.setdefault("FolioInicio", None)
    dicReady.setdefault("FolioFin", None)
    dicReady.setdefault("NITAdquiriente", None)

    return dicReady