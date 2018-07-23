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
    list_params = [
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


    req = {
        "action": "obtieneDatos",
        "datos": {
            "frase": queryOriginal,
            "campos": list_params
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

    for field in list_params:
        field_resp = resp["campos"][field]
        _setEntryInDic(dicReady, field,
                       field_resp["value"], field_resp["statusField"])
        # TODO: Caso de fechas y periodo

    _mapValues(dicReady)


    print(req)
    return dicReady


def _setEntryInDic(dic: dict, campo: str, value, status: int):
    """Status 1 correcto, status 0 incorrecto.
    """
    dic[campo] = {"value": value, "status": status}


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
