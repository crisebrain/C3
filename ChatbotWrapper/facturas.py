# from .b2bcliente import sendReq, getResponseValues, HumanResult
import sys
from gc import collect
import json
import datetime
import re
from datetime import date
sys.path.append("SearchEngine")
from SearchEngine import Regexseaker

def factura(req):
    # Ya que los elemenetos vienen en una lista deben tener un tratamiento
    # particular
    listaCampos = req.get("queryResult").get("parameters")["facturasCampos"]
    repitedItems = ["folio"]
    itemsShouldList = ["date", "date-period"]
    diccFusionado = {}

    # Fusionamos todos los diccionarios y listas, para obtener un diccionario de todo
    for element in listaCampos:
        try:
            items = list(element.items())
            key = items[0][0]

            # Evalúamos si el item es de los posibles repetidos
            if key in repitedItems:
                # Construye su nombre con respecto al tipo.
                diccFusionado.setdefault(key + items[0][1]["tipo"], items[0][1])
            elif key in itemsShouldList:
                # Fusionamos los date y date-period en diccionarios con listas.
                # Esto permite tener varias fechas a la vez.
                if not key in diccFusionado:
                    diccFusionado.setdefault(key, [element[key]])
                else:
                    diccFusionado[key].append(element[key])
            else:
                diccFusionado.update(element)
        except:
            print("WARNING: el elemento: {} , no se usó para el diccionario.".format(element))

    dicReady = preparaParametros(diccFusionado, req.get("queryResult").get("queryText"))
    print(dicReady)

    peticionStr = prepareHumanResult(dicReady)

    # Response
    dicReady.update({"returnCode": "1"})
    respuesta =  {
                    "fulfillmentText" : peticionStr,
                    "payload": dicReady
    }

    # garbage collector
    collect()

    return respuesta


def preparaParametros(dic, queryOriginal):
    dicReady = {}
    list_miss_param = []
    seaker = Regexseaker()

    # Tipo de documento
    switcherTipoDocumento = {
        "Factura": "F",
        "Nota": "N"
    }
    if dic.get("tipoDocumento"):
        addEntryToDic(dicReady, "tipoDocumento",
                      switcherTipoDocumento.get(dic.get("tipoDocumento")), 1)
    else:
        list_miss_param.append("Tipo")


    # Periodo
    # Se comenta este código porque siempre se resuelve con gramáticas.
    # Esto es porque siempre se resolverán como fechas.
    # switcherPeriodo = {
    #     "Hoy": 1,
    #     "Semana": 2,
    #     "Mes": 3
    # }
    # # Valor por default 0
    # # periodo = switcherPeriodo.get(dic.get("periodo"), 0)
    periodo = 0
    addEntryToDic(dicReady, "Periodo", periodo, 1)

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
        addEntryToDic(dicReady, "Status", status, 1)
    else:
        list_miss_param.append("Estado")

    # Prefijo
    if dic.get("prefijo"):
        prefijo = dic.get("prefijo").get("value")
        if isinstance(prefijo, float):
            prefijo = str(int(prefijo))
        elif isinstance(prefijo, str):
            prefijo = prefijo.upper().replace(" ", "")

        pattern = r"^[1-9a-zA-Z]\w{0,3}$"
        statusCode = re.search(pattern, prefijo)
        statusCode = 1 if statusCode else 0
        addEntryToDic(dicReady, "Prefijo", prefijo, statusCode)
    else:
        list_miss_param.append("Prefijo")


    # Acuse
    switcherAcuse = {
        "Aceptado": 1,
        "Rechazado": 2,
        "Pendiente": 3
    }
    acuse = []
    if dic.get("acuse"):
        acuse.append(dic.get("acuse").get("value"))
        acuse.append(1)
    else:
        list_miss_param.append("Acuse")


    # Folio Inicio
    if dic.get("folioinicial"):
        folioInicio = int(dic.get("folioinicial").get("value"))
        pattern = r"^\d{1,16}$"
        statusCode = re.search(pattern, str(folioInicio))
        statusCode = 1 if statusCode else 0
        addEntryToDic(dicReady, "FolioInicio", folioInicio, statusCode)
    else:
        list_miss_param.append("FolioInicio")

    # Folio Final
    if dic.get("foliofinal"):
        folioFinal = int(dic.get("foliofinal").get("value"))
        addEntryToDic(dicReady, "FolioFinal", folioFinal, 1)
    else:
        list_miss_param.append("FolioFinal")


    # NIT
    if dic.get("nit"):
        nit = str(int(dic.get("nit").get("value")))
        addEntryToDic(dicReady, "NITAdquiriente", nit, 1)
    else:
        list_miss_param.append("NitAdquirienteMex")


    # Cuenta
    list_miss_param.append("Cuenta")

    # Fechas
    # Ignoramos fechas de DF.
    # Primero evalúa fecha, si no funciona, realiza periodo.
    fechaTemp = seaker.seakexpresion(queryOriginal, "Fecha")
    if fechaTemp[0]["fechaInicio"] is None and fechaTemp[0]["fechaFin"] is None:
        fechaTemp = seaker.seakexpresion(queryOriginal, "Periodo")
    fechaInicio = fechaTemp[0].get("fechaInicio")
    fechaFin = fechaTemp[0].get("fechaFin")
    fechaStatus = fechaTemp[1]

    # Si existe la fecha, le pone formato ISO, sino, la deja en None
    fechaInicioStr = fechaInicio.isoformat() if fechaInicio is not None else None
    fechaFinStr = fechaFin.isoformat() if fechaFin is not None else None
    addEntryToDic(dicReady, "FechaEmisionInicio", fechaInicioStr, fechaStatus)
    addEntryToDic(dicReady, "FechaEmisionFin", fechaFinStr, fechaStatus)


    # NumeroFactura (Num. Documento)
    list_miss_param.append("NoDocumento")


    # hardcoded:
    # dicReady.setdefault("Empresa", "RICOH")

    #########################
    tipoDocumento = seaker.seakexpresion(queryOriginal, "Tipo")
    addEntryToDic(dicReady, "tipoDocumento",
                  switcherTipoDocumento.get(tipoDocumento[0]), tipoDocumento[1])

    statusT = seaker.seakexpresion(queryOriginal, "Estado")
    addEntryToDic(dicReady, "Status", switcherStatus.get(statusT[0]),
                  statusT[1])

    prefijo = seaker.seakexpresion(queryOriginal, "Prefijo")
    addEntryToDic(dicReady, "Prefijo", prefijo[0], prefijo[1])


    if True:
        pass
    else:
        acuseT = seaker.seakexpresion(queryOriginal, "Acuse")
        acuse.append(acuseT[0])
        acuse.append(acuseT[1])
    # Valor por default 0
    acuse[0] = switcherAcuse.get(acuse[0], 0)
    addEntryToDic(dicReady, "Acuse", acuse[0], acuse[1])


    folioInicio = seaker.seakexpresion(queryOriginal, "FolioInicio")
    addEntryToDic(dicReady, "FolioInicio", folioInicio[0], folioInicio[1])

    folioFinal = seaker.seakexpresion(queryOriginal, "FolioFinal")
    addEntryToDic(dicReady, "FolioFinal", folioFinal[0], folioFinal[1])

    nit = seaker.seakexpresion(queryOriginal, "NitAdquirienteMex")
    addEntryToDic(dicReady, "NITAdquiriente", nit[0], nit[1])

    cuenta = seaker.seakexpresion(queryOriginal, "Cuenta")
    addEntryToDic(dicReady, "Cuenta", cuenta[0], cuenta[1])

    numDoc = seaker.seakexpresion(queryOriginal, "NoDocumento")
    addEntryToDic(dicReady, "NumeroFactura", numDoc[0], numDoc[1])


    #########################

    print(list_miss_param)
    return dicReady

def addEntryToDic(dic, campo, value, status):
    """Status 1 correcto, status 0 incorrecto.
    """
    dic.setdefault(campo, {"value": value, "status": status})

def calcDates(listDate, listDatePeriod):
    dateStart = None
    dateEnd = None

    # Fechas individuales
    if listDate is not None:
        if len(listDate) > 0:
            i = len(listDate) - 1
            date1 = buildDate(listDate[i])

            # Evalúamos que exista otro elemento
            if i >= 1:
                i -= 1
            date2 = buildDate(listDate[i])

            # Evalúa fecha mayor
            if date1 < date2:
                dateStart = date1
                dateEnd = date2
            else:
                dateStart = date2
                dateEnd = date1

    # Periodo
    if listDatePeriod is not None:
        if len(listDatePeriod) > 0 \
            and dateStart is None and dateEnd is None:
            i = len(listDatePeriod) - 1
            dateStart = buildDate(listDatePeriod[i].get("startDate"))
            dateEnd = buildDate(listDatePeriod[i].get("endDate"))

    # Evalúamos fechas posteriores a este año
    hoy = date.today()
    if dateStart is not None and dateStart > hoy:
        dateStart = dateStart.replace(year=hoy.year)
    if dateEnd is not None and dateEnd > hoy:
        dateEnd = dateEnd.replace(year=hoy.year)

    return dateStart, dateEnd

def buildDate(dateString):
    year = int(dateString[0:4])
    month = int(dateString[5:7])
    day = int(dateString[8:10])

    return datetime.date(year, month, day)

def prepareHumanResult(dicReady: dict):
    # Print values
    peticionStr = ""
    for element in dicReady:
        if dicReady[element].get("value") is not None:# and dicReady[element]["status"] != 0:
            peticionStr += "{0}: {1}, {2} \n".format(
                element, dicReady[element]["value"], dicReady[element]["status"])

    return  peticionStr
