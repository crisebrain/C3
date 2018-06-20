from .b2bcliente import sendReq, getResponseValues, HumanResult
from .b2bcliente import Regexseaker
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


def factura(req):
    # Ya que los elemenetos vienen en una lista deben tener un tratamiento
    # particular
    listaCampos = req.get("queryResult").get("parameters")["facturasCampos"]
    repitedItems = ["folio"]
    diccFusionado = {}

    # Fusionamos todos los diccionarios
    for dicc in listaCampos:
        items = list(dicc.items())

        # Evalúamos si el item es de los posibles repetidos
        if items[0][0] in repitedItems:
            # Construye su nombre con respecto al tipo.
            diccFusionado.setdefault(items[0][0] + items[0][1]["tipo"], items[0][1])
        else:
            diccFusionado.update(dicc)


    dicReady = preparaParametros(diccFusionado, req.get("queryResult").get("queryText"))
    print(dicReady)

    peticionStr = ""
    for elemento in dicReady:
        if dicReady[elemento] is not None:
            peticionStr += elemento + ": {0} \n".format(dicReady[elemento])

    respuesta =  {
                    "fulfillmentText" : peticionStr,
                    "payload": dicReady

    }

    return respuesta


def preparaParametros(dic, queryOriginal):
    dicReady = {}
    seaker = Regexseaker()

    # Tipo de documento
    if dic.get("tipoDocumento") == "Factura":
        dicReady.setdefault("Factura", "F")
    elif dic.get("tipoDocumento") == "Nota":
        dicReady.setdefault("Factura", "N")

    # Periodo
    switcherPeriodo = {
        "Hoy": 1,
        "Semana": 2,
        "Mes": 3
    }
    # Valor por default 0
    periodo = switcherPeriodo.get(dic.get("periodo"), 0)
    dicReady.setdefault("Periodo", periodo)


    # Estatus
    switcherStatus = {
        "Recibido": 1,
        "Error": 6,
        "Firmado": 22,
        "Rechazado": 23,
        "Aceptado": 24,
        "Enviado": 25
    }
    if dic.get("status"):
        status = switcherStatus.get(dic.get("status").get("value"))
        dicReady.setdefault("Status", status)


    # TODO: Corregir los upper para NONE.
    if dic.get("prefijo"):
        prefijo = dic.get("prefijo").get("value")
        if not isinstance(prefijo, str):
            dicReady.setdefault("Prefijo", str(int(prefijo)))
        else:
            dicReady.setdefault("Prefijo", prefijo.upper())


    # Acuse
    switcherAcuse = {
        "Aceptado": 1,
        "Rechazado": 2,
        "Pendiente": 3
    }
    acuse = ""
    if dic.get("acuse"):
        acuse = dic.get("acuse").get("value")
    # Valor por default 0
    dicReady.setdefault("Acuse", switcherAcuse.get(acuse, 0))


    # Folio
    if dic.get("folioinicial"):
        dicReady.setdefault("FolioInicio", dic.get("folioinicial").get("value"))
    if dic.get("foliofinal"):
        dicReady.setdefault("FolioFinal", dic.get("foliofinal").get("value"))

    # NIT
    if dic.get("nit"):
        dicReady.setdefault("NITAdquiriente", dic.get("nit").get("value"))
    else:
        dicReady.setdefault("NITAdquiriente", seaker.seakexpresion(queryOriginal, "NitAdquirienteMex"))


    # Código que indica el valor inválido.
    # if dicReady.get("NITAdquiriente") is None:
    #     import re
    #     patternNIT = re.search(r"nit", queryOriginal)
    #     temp = queryOriginal[patternNIT.end():len(queryOriginal)]
    #     dicReady["NITAdquiriente"] = "Valor invalido: " + temp




    # Cuenta
    dicReady.setdefault("Cuenta", seaker.seakexpresion(queryOriginal, "Cuenta"))


    # hardcoded:
    # dicReady.setdefault("Empresa", "RICOH")
    dicReady.setdefault("FechaEmisionInicio", None)
    dicReady.setdefault("FechaEmisionFin", None)
    # NumeroFactura (Num. Documento)
    dicReady.setdefault("NumeroFactura", None)


    return dicReady

def addEntryToDic(dic, campo, value, status):
    dic.setdefault(campo, {"value": value, "status": status})