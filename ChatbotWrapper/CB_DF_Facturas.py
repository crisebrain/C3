from gc import collect
from ChatbotWrapper.Utils import methods_DF_to_IM as IM
from Utils import constantesFacturas as CF

STATUS_FIELD = "statusField"
RETURN_CODE = "returnCode"
MESSAGE = "message"
CAMPOS = "campos"


def factura(req: dict):
    """
    Función principal de esta clase. Se encarga de llevar la lógica del
    negocio.

    :param req: Petición de DF.
    :return: Respuesta construida hacia DF
    """

    # diccFusionado = _prepareJsonDF(req)

    dicReady, returnCode, message = _prepareParameters(req.get("queryResult").get("queryText"))
    print("\nDicReady:\n{0}".format(dicReady))

    peticionStr = _prepareHumanResult(dicReady)

    # Response
    respuesta = {
        "fulfillmentText": peticionStr,
        "payload": {
            "data:": dicReady,
            RETURN_CODE: returnCode
        }
    }

    # TODO: únicamente para pruebas. Borra cuando no sea necesario.
    # _updateValues(req.copy(), dicReady.copy())

    # garbage collector
    collect()

    return respuesta


def _updateValues(req: dict, fields: dict):
    """
    Esta función únicamente es de prueba, para probar que el IM guarde los
    valores que se le han pasado.
    """
    fields["date"] = [fields[CF.FECHA_INICIAL.value]["value"],
                      fields[CF.FECHA_FINAL.value]["value"]]
    del fields[CF.FECHA_INICIAL.value]
    del fields[CF.FECHA_FINAL.value]
    IM.updateIM(req, fields)


def _prepareJsonDF(req: dict):
    """
    Función que procesa el json de entrada de DF y le da tratamiento para ser
    más amigable a la hora de extraer valores.

    :param req: Petición de DF.
    :return: Diccionario construido con los valores de DF.
    """

    # Ya que los elementos vienen en una lista deben tener un tratamiento
    # particular
    listaCampos = req.get("queryResult").get("parameters")["facturasCampos"]
    repitedItems = ["folio"]
    itemsShouldList = ["date", "date-period"]
    diccFusionado = {}
    # Fusionamos todos los diccionarios y listas, para obtener un diccionario
    # de todos los parámetros de DF.
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
    return diccFusionado


def _prepareParameters(queryOriginal: str):
    """
    Función que prepara los parámetros de salida para el cliente. Esta función
    se encarga de llamar a las funciones auxiliares, para obtener datos,
    construir el diccionario y mapear valores.

    :param dic: Diccionario de los parámetros de DF.
    :param queryOriginal: Lo que el usuario ingreso a DF.
    :return: Diccionario listo para ser añadido al json final, código de Retorno y mensaje genérico.
    """
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
        CF.FECHA.value,
        CF.NO_DOCUMENTO.value
    ]

    resp = IM.extractData(queryOriginal, list_params)

    _buildFinalDic(dicReady, list_params, resp)

    _mapValues(dicReady)

    return dicReady, resp[RETURN_CODE], resp[MESSAGE]


def _getDummyResp():
    """
    Retorna un json dummy estilo respuesta IM para procesar.

    :return: json dummy
    """
    resp = {
        CAMPOS: {
            CF.TIPO_DOCUMENTO.value: {"value": "Factura",
                                      STATUS_FIELD: 1
                                      },
            CF.PERIODO.value: {CF.FECHA_INICIAL.value: None,
                               CF.FECHA_FINAL.value: None,
                               STATUS_FIELD: 1
                               },
            CF.STATUS.value: {"value": "Recibido",
                              STATUS_FIELD: 1
                              },
            CF.PREFIJO.value: {"value": "ABCD",
                               STATUS_FIELD: 1
                               },
            CF.ACUSE.value: {"value": "Pendiente",
                             STATUS_FIELD: 1
                             },
            CF.FOLIO_INICIAL.value: {"value": 123456,
                                     STATUS_FIELD: 1
                                     },
            CF.FOLIO_FINAL.value: {"value": 987654,
                                   STATUS_FIELD: 1
                                   },
            CF.NIT.value: {"value": "OOMA890909AS3",
                           STATUS_FIELD: 1
                           },
            CF.CUENTA.value: {"value": "ABC123",
                              STATUS_FIELD: 1
                              },
            CF.NO_DOCUMENTO.value: {"value": "ABC-2343",
                                    STATUS_FIELD: 1
                                    },
            CF.FECHA.value: {CF.FECHA_INICIAL.value: "2000-01-01",
                             CF.FECHA_FINAL.value: "2010-12-24",
                             STATUS_FIELD: 1
                             }
        },
        MESSAGE: "Mensaje",
        RETURN_CODE: 1
    }
    return resp


def _buildFinalDic(dicReady: dict, list_params: list, resp: dict):
    """
    Función que prepara los parámetros de salida para el cliente. Esta
    función es la encarga de construir la estructura general del json para
    clientes de terceros.

    :param dicReady: Diccionario donde se guardarán los resultados.
    :param list_params: Parámetros que se incluirán en el diccionario
    :param resp: Respuesta del IM
    """
    # Construimos diccionario de salida
    for field in list_params:
        field_resp = resp[CAMPOS][field]

        if field == CF.FECHA.value or field == CF.PERIODO.value:
            # Si el field es fecha, entonces sobreescribe por ser el de mayor
            # prioridad, siempre y cuando traiga una fecha válida.
            # Si no existe el campo, cualquiera puede guardar
            # (Sería periodo).
            if field == CF.FECHA.value and \
                    (field_resp.get(CF.FECHA_INICIAL.value) or
                     field_resp.get(CF.FECHA_FINAL.value)):
                _setEntryInDic(dicReady, CF.FECHA_INICIAL.value,
                               field_resp[CF.FECHA_INICIAL.value],
                               field_resp[STATUS_FIELD])
                _setEntryInDic(dicReady, CF.FECHA_FINAL.value,
                               field_resp[CF.FECHA_FINAL.value],
                               field_resp[STATUS_FIELD])
            elif not dicReady.get(CF.FECHA_INICIAL.value):
                _setEntryInDic(dicReady, CF.FECHA_INICIAL.value,
                               field_resp[CF.FECHA_INICIAL.value],
                               field_resp[STATUS_FIELD])
                _setEntryInDic(dicReady, CF.FECHA_FINAL.value,
                               field_resp[CF.FECHA_FINAL.value],
                               field_resp[STATUS_FIELD])
        else:
            _setEntryInDic(dicReady, field,
                           field_resp["value"], field_resp[STATUS_FIELD])
    # Hardoced value
    _setEntryInDic(dicReady, CF.PERIODO.value, 0, 1)


def _setEntryInDic(dic: dict, campo: str, value, status: int):
    """
    Función que construye la estructura de cada campo en el json para el cliente.

    :param dic: Diccionario donde se guardarán los campos
    :param campo: nombre del campo
    :param value: valor del campo
    :param status: código de estado del campo: 1 correcto, status 0 incorrecto.
    """
    dic[campo] = {"value": value, "status": status}


def _mapValues(dic: dict):
    """
    Función que se encarga de mapear los valores ingresados por el usuario,
    a los valores requeridos por el cliente.

    :param dic: Diccionario donde se guardarán los resultados
    """

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

    for field, values in dic.items():
        if field in fields_to_map.keys() and values["value"]:
            values["value"] = fields_to_map[field](values["value"])


def _prepareHumanResult(dicReady: dict):
    """
    Función que regresa una salida amigable del json de salida al cliente.

    :param dicReady: Diccionario que será integrado al json final
    :return: String con la salida amigable.
    """
    peticionStr = ""
    for element in dicReady:
        if dicReady[element].get("value") is not None:  # and dicReady[element]["status"] != 0:
            peticionStr += "{0}: {1}, {2} \n".format(
                element, dicReady[element]["value"], dicReady[element]["status"])

    return peticionStr
