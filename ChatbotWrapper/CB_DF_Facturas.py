from gc import collect
import json
import datetime
import re
import requests
from datetime import date
from Utils import constantesFacturas as CF

def post_data(jdata, link="http://localhost:5050/infomanager"):
    r = requests.post(link, data=jdata)
    # Ajustar salida si r no es la respuesta esperada
    return r.json()


def factura(req):
    # Ya que los elementos vienen en una lista deben tener un tratamiento
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
    list_miss_param = [
        CF.TIPO_DOCUMENTO.value,
        CF.PERIODO.value,
        CF.STATUS.value,
        CF.PREFIJO.value,
        CF.ACUSE.value,
        CF.FOLIO_INICIAL.value,
        CF.FOLIO_FINAL.value,
        CF.NIT.value,
        CF.CUENTA.value,
        #CF.FECHA.value,
        CF.NO_DOCUMENTO.value
    ]

    # _tipoDocumento(dic, dicReady, list_miss_param)
    # _periodo(dicReady)
    # _estatus(dic, dicReady, list_miss_param)
    # _prefijo(dic, dicReady, list_miss_param)
    # _acuse(dic, list_miss_param)
    # _folioInicial(dic, dicReady, list_miss_param)
    # _folioFinal(dic, dicReady, list_miss_param)
    # _nit(dic, dicReady, list_miss_param)
    # _cuenta(list_miss_param)
    # #_fechas(dicReady, queryOriginal)
    # _numFactura(list_miss_param)



    #
    #
    # print(dicReady)
    # for key in dicReady:
    #     print("{0} {1}".format(key, dicReady[key]))
    #



    # hardcoded:
    # dicReady.setdefault("Empresa", "RICOH")


    # ######################### Anterior ####################
    # seaker = Regexseaker()
    #
    # prefijo = seaker.seakexpresion(queryOriginal, "Prefijo")
    # setEntryInDic(dicReady, "Prefijo", prefijo[0], prefijo[1])
    #

    #
    # folioInicio = seaker.seakexpresion(queryOriginal, "FolioInicio")
    # setEntryInDic(dicReady, "FolioInicio", folioInicio[0], folioInicio[1])
    #
    # folioFinal = seaker.seakexpresion(queryOriginal, "FolioFinal")
    # setEntryInDic(dicReady, "FolioFinal", folioFinal[0], folioFinal[1])
    #
    # nit = seaker.seakexpresion(queryOriginal, "NitAdquirienteMex")
    # setEntryInDic(dicReady, "NITAdquiriente", nit[0], nit[1])
    #
    # cuenta = seaker.seakexpresion(queryOriginal, "Cuenta")
    # setEntryInDic(dicReady, "Cuenta", cuenta[0], cuenta[1])
    #
    # numDoc = seaker.seakexpresion(queryOriginal, "NoDocumento")
    # setEntryInDic(dicReady, "NumeroFactura", numDoc[0], numDoc[1])
    #
    #
    # #########################


    req = {
        "action": "obtieneDatos",
        "datos": {
            "frase": queryOriginal,
            "campos": list_miss_param
        }
    }

    resp = {
        "campos": {
                    CF.TIPO_DOCUMENTO.value: {"value": "Factura",
                           "statusField": 1
                           },
                    CF.PERIODO.value: {"value": CF.PERIODO.value,
                                                "statusField": 1
                                                },
                    CF.STATUS.value: {"value": "Recibido",
                                         "statusField": 1
                                         },
                    CF.PREFIJO.value: {"value": "ABCD",
                                         "statusField": 1
                                         },
                    CF.ACUSE.value: {"value": "Pendiente",
                                         "statusField": 1
                                         },
                    CF.FOLIO_INICIAL.value: {"value": 123456,
                                         "statusField": 1
                                         },
                    CF.FOLIO_FINAL.value: {"value": 987654,
                                         "statusField": 1
                                         },
                    CF.NIT.value: {"value": "OOMA890909AS3",
                                         "statusField": 1
                                         },
                    CF.CUENTA.value: {"value": "ABC123",
                                         "statusField": 1
                                         },
                    CF.NO_DOCUMENTO.value: {"value": "ABC-2343",
                                         "statusField": 1
                                         }
                    },
        "message": "Mensaje",
        "returnCode": 1
    }

    for field in list_miss_param:
        field_resp = resp["campos"][field]
        _setEntryInDic(dicReady, field,
                       field_resp["value"], field_resp["statusField"])
        # TODO: Caso de fechas y periodo

    _mapValues(dicReady)


    print(req)
    return dicReady


def _numFactura(list_miss_param):
    # NumeroFactura (Num. Documento)
    list_miss_param.append(CF.NO_DOCUMENTO.value)


def _fechas(dicReady, queryOriginal):
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
    setEntryInDic(dicReady, "FechaEmisionInicio", fechaInicioStr, fechaStatus)
    setEntryInDic(dicReady, "FechaEmisionFin", fechaFinStr, fechaStatus)


def _cuenta(list_miss_param):
    # Cuenta
    list_miss_param.append(CF.CUENTA.value)


def _nit(dic, dicReady, list_miss_param):
    # NIT
    if dic.get(CF.NIT.value):
        nit = str(int(dic.get(CF.NIT.value).get("value")))
        _setEntryInDic(dicReady, CF.NIT.value, nit, 1)
    else:
        list_miss_param.append(CF.NIT.value)


def _folioFinal(dic, dicReady, list_miss_param):
    # Folio Final
    if dic.get(CF.FOLIO_FINAL.value):
        folioFinal = int(dic.get(CF.FOLIO_FINAL.value).get("value"))
        _setEntryInDic(dicReady, CF.FOLIO_FINAL.value, folioFinal, 1)
    else:
        list_miss_param.append(CF.FOLIO_FINAL.value)


def _folioInicial(dic, dicReady, list_miss_param):
    # Folio Inicio
    if dic.get(CF.FOLIO_INICIAL.value):
        folioInicio = int(dic.get(CF.FOLIO_INICIAL.value).get("value"))
        pattern = r"^\d{1,16}$"
        statusCode = re.search(pattern, str(folioInicio))
        statusCode = 1 if statusCode else 0
        _setEntryInDic(dicReady, CF.FOLIO_INICIAL.value, folioInicio, statusCode)
    else:
        list_miss_param.append(CF.FOLIO_INICIAL.value)


def _acuse(dic, list_miss_param):
    # Acuse
    switcherAcuse = {
        "Aceptado": 1,
        "Rechazado": 2,
        "Pendiente": 3
    }
    acuse = []
    if dic.get(CF.ACUSE.value):
        acuse.append(dic.get(CF.ACUSE.value).get("value"))
        acuse.append(1)
    else:
        list_miss_param.append(CF.ACUSE.value)


def _prefijo(dic, dicReady, list_miss_param):
    # Prefijo
    if dic.get(CF.PREFIJO.value):
        prefijo = dic.get(CF.PREFIJO.value).get("value")
        if isinstance(prefijo, float):
            prefijo = str(int(prefijo))
        elif isinstance(prefijo, str):
            prefijo = prefijo.upper().replace(" ", "")

        pattern = r"^[1-9a-zA-Z]\w{0,3}$"
        statusCode = re.search(pattern, prefijo)
        statusCode = 1 if statusCode else 0
        _setEntryInDic(dicReady, CF.PREFIJO.value, prefijo, statusCode)
    else:
        list_miss_param.append(CF.PREFIJO.value)


def _estatus(dic, dicReady, list_miss_param):
    # Estatus
    switcherStatus = {
        "Recibido": 1,
        "Error": 6,
        "Firmado": 22,
        "Rechazado": 23,
        "Aceptado": 24,
        "Enviado": 25
    }
    if dic.get(CF.STATUS.value):
        status = switcherStatus.get(dic.get(CF.STATUS.value).get("value"))
        _setEntryInDic(dicReady, CF.STATUS.value, status, 1)
    else:
        list_miss_param.append(CF.STATUS.value)


def _periodo(dicReady):
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
    _setEntryInDic(dicReady, CF.PERIODO.value, periodo, 1)


def _tipoDocumento(dic, dicReady, list_miss_param):
    # Tipo de documento
    switcherTipoDocumento = {
        "Factura": "F",
        "Nota": "N"
    }
    if dic.get(CF.TIPO_DOCUMENTO.value):
        _setEntryInDic(dicReady, CF.TIPO_DOCUMENTO.value,
                       switcherTipoDocumento.get(dic.get(CF.TIPO_DOCUMENTO.value)), 1)
    else:
        list_miss_param.append(CF.TIPO_DOCUMENTO.value)


def _setEntryInDic(dic: dict, campo: str, value, status: int):
    """Status 1 correcto, status 0 incorrecto.
    """
    dic[campo] = {"value": value, "status": status}


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


def _mapValues(dic: dict):
    def tipoDocumento(value):
        switcherTipoDocumento = {
            "Factura": "F",
            "Nota": "N"
        }
        return switcherTipoDocumento[value]

    def periodo(value):
        switcherPeriodo = {
            "Hoy": 1,
            "Semana": 2,
            "Mes": 3
        }
        # Valor por default 0
        # switcherPeriodo.get(value, 0)
        return 0

    def estatus(value):
        switcherStatus = {
            "Recibido": 1,
            "Error": 6,
            "Firmado": 22,
            "Rechazado": 23,
            "Aceptado": 24,
            "Enviado": 25
        }
        return switcherStatus[value]

    def acuse(value):
        switcherAcuse = {
            "Aceptado": 1,
            "Rechazado": 2,
            "Pendiente": 3
        }
        # Valor por default 0
        return switcherAcuse.get(value, 0)

    fields_to_map = {
        CF.TIPO_DOCUMENTO.value: tipoDocumento,
        CF.PERIODO.value: periodo,
        CF.STATUS.value: estatus,
        CF.ACUSE.value: acuse
    }

    for field in dic.keys():
        if field in fields_to_map.keys():
            dic[field]["value"] = fields_to_map[field](dic[field]["value"])


def prepareHumanResult(dicReady: dict):
    # Print values
    peticionStr = ""
    for element in dicReady:
        if dicReady[element].get("value") is not None:# and dicReady[element]["status"] != 0:
            peticionStr += "{0}: {1}, {2} \n".format(
                element, dicReady[element]["value"], dicReady[element]["status"])

    return  peticionStr
