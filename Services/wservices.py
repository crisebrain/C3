from .bd_busqueda import dbquery
from .b2bcliente import sendReq, getResponseValues
import json

def makeWebhookResult(req):
    action = req.get("queryResult").get("action")
    try:
        if action == "VDN" or action == "saldo":
            return makeresponseAction(req, action)
        elif action == "informacion":
            return informacion(req.get("queryResult").get("parameters").get("servicio"))
        elif action == "dudasFacturasCampos":
            return dudasFacturasCampos(req.get("queryResult").get("parameters").get("campo"))
        elif action == "factura":
            return factura(req.get("queryResult").get("parameters"))
        else:
            return {"payload": {"result": "Null", "returnCode": "0"},
                   "fulfillmentText": "Null"}
    except Exception as err:
        return {"payload": {"result": "Null", "returnCode": "0"},
                "fulfillmentText": "{0}".format(err)}

def makeresponseAction(req, action):
    # Carga de base de datos
    result = req.get("queryResult").get("parameters")

    nombre = construyeNombre(result)


    if nombre != "":
        coincidencias = dbquery(nombre)
        print(json.dumps(coincidencias, indent=4))
        returnCode = calcCode(coincidencias)
    else:
        returnCode = calcCode([], True)
        coincidencias = []

    textresp = mensajson(coincidencias, returnCode, action, nombre)
    resultarray = []
    for coin in coincidencias:
        resultarray.append(dict(zip(["nombre", action],
                                    [coin["Nombre"], coin[action]])))


    resp = {
            "payload": {"result": resultarray, "returnCode": returnCode},
            "fulfillmentText": textresp
    }



    respContext = evaluaContextos(returnCode, action, nombre, req.get("session"))

    if respContext:
        resp.update(respContext)

    return resp


def construyeNombre(parametros):
    import numpy as np
    listaNombre = parametros.get("nombre")

    # Obtenemos los nombres que vengan, se consideran valores repetidos
    keys = [list(dicc.keys()) for dicc in listaNombre]
    unicos = np.unique(np.array(keys).reshape(-1, ))
    dicNombres = dict(zip(unicos, [""]*len(unicos)))
    for dicc in listaNombre:
        for unico in unicos:
            if unico in dicc.keys():
                dicNombres[unico] = " ".join([dicNombres[unico].strip(), dicc[unico].strip()])

    # Concatenamos los nombres
    nombre = "" + str(dicNombres.setdefault("nombre", "")) + " "\
             + str(dicNombres.setdefault("apellido", "")) + " "\
             + str(dicNombres.setdefault("nombresExtras", ""))

    return nombre.strip()


def evaluaContextos(code, action, valor, session):
    if action == "VDN" and code == 1 and valor:
        return {"outputContexts": [
            {
                "name": session + "/contexts/0-2vdn-followup",
                "lifespanCount": 0
            },
            {
                "name": session + "/contexts/0-2vdn-followup-2",
                "lifespanCount": 0
            }
        ]}

    if action == "saldo" and code == 1 and valor:
        return {"outputContexts": [
            {
                "name": session + "/contexts/0-1saldo-followup",
                "lifespanCount": 0
            },
            {
                "name": session + "/contexts/0-1saldo-followup-2",
                "lifespanCount": 0
            }
        ]}


def calcCode(array, empty=False):
    if not empty:
        ncoincidencias = len(array)
        if ncoincidencias == 0: #No encontró a nadie
            code = 0
        elif ncoincidencias == 1: #Encontró a alguien
            code = 1
        elif ncoincidencias < 4: # Encontró menos de 3 personas
            code = 2
        else:
            code = 3 # Encontró más de 3 personas
        return code
    else:
        return 1

def mensajson(array, code, action, valor):
    if action == "VDN":
        if valor == "":
            Text = "¿Con quién desea hablar?"
            return Text

        if code == 0:
            Text = "No hay referencia de esa persona. ¿Con qué otra persona te comunico?"

        elif code == 1:
            elem = array[0]
            Text = "Será transferido con {0} {1} y tel: {2}.".format(elem["Nombre"],
                                                        elem["Apellido"],
                                                        elem["VDN"])
            Text += "\nHasta luego."

        elif code == 2:
            textnames = [elem["Nombre"] + " " + elem["Apellido"] for elem in array]
            textnames = ' o '.join(textnames)
            Text = "¿A cual persona te refieres? a {0}".format(textnames)

        else:
            Text = "Existen demasiadas coincidencias, necesitas ser mas específico"

    elif action == "saldo":
        if valor == "":
            Text = "¿Cuál es el nombre de usuario?"
            return Text

        if code == 0:
           Text = "No hay referencia de esa persona. ¿Con qué otra persona te comunico?"

        elif code == 1:
            elem = array[0]
            Text = "El saldo de {0} {1} es {2} pesos".format(elem["Nombre"],
                                                            elem["Apellido"],
                                                            elem["saldo"])
            Text += "\n¿Deseas algo más?"

        elif code == 2:
            textnames = [elem["Nombre"] + " " + elem["Apellido"] for elem in array]
            textnames = ' o '.join(textnames)
            Text = "¿A cual persona te refieres? a {0}".format(textnames)

        else:
            Text = "Existen demasiadas coincidencias, necesitas ser mas específico"
    return Text

def informacion(servicio):
    servicios = {
        "saldo": "Servicio de Saldo",
        "VDN": "Servicio de VDNs."
        }

    resp = servicios.get(servicio)

    return {"fulfillmentText": resp}


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
    #print(json.dumps(parametros, indent=4))
    estado = None
    tipoDocumento = None
    periodo = None
    prefijo = None
    acuse = None
    numFactura = None

    # Ya que los elemenetos vienen en una lista deben tener un
    # tratamiento algo particular
    listaCampos = parametros["facturasCampos"]
    diccFusionado = {}

    # Fusionamos todos los diccionarios
    for dicc in listaCampos:
        diccFusionado.update(dicc)

    # Obtenemos los valores
    tipoDocumento = diccFusionado.get("tipoDocumento")
    periodo = diccFusionado.get("periodo")
    if diccFusionado.get("status"):
        estado = diccFusionado.get("status").get("value")
    if diccFusionado.get("prefijo"):
        prefijo = diccFusionado.get("prefijo").get("value")
    if diccFusionado.get("acuse"):
        acuse = diccFusionado.get("acuse").get("value")
    if diccFusionado.get("numeroFactura"):
        numfactura = diccFusionado.get("numeroFactura").get("value").get("value")
        if not isinstance(numfactura, str):
            numFactura = str(int(numfactura))

    # Caso que no traiga ninguna restricción. Consulta muy amplia
    if not(estado or prefijo or periodo or numFactura or acuse):

        # TODO: Implementar caso de que traiga valores inválidos


        respuesta = "Debe acotar su consulta, ya que el resultado puede ser muy" \
                    " grande. Puede delimitarla con los campos:" \
                    "\nTipo de documento," \
                    "\nEstado," \
                    "\nSerie," \
                    "\nPeriodo," \
                    "\nAcuse," \
                    "\nNumero de Factura"

        return {"fulfillmentText" : respuesta}

    diccFinal = {
            "Empresa": "RICOH",
            "Periodo": periodo,
            "FechaEmisionInicio": "",
            "FechaEmisionFin": "",
            "Status": estado,
            "NumeroFactura": numFactura,
            "Factura": tipoDocumento,
            "Cuenta": "",
            "Cuenta": "",
            "Prefijo": prefijo,
            "FolioInicio": "",
            "FolioFin" : "",
            "Acuse": acuse,
            "NITAdquiriente": ""
    }

    # servicio de factura
    req = sendReq(diccFinal)
    msg = getResponseValues(req.content)
    print(msg)

    peticionstr = ("\nTipo documento: {0}" +
                  "\nEstado: {1}" +
                  "\nPeriodo {2}" +
                  "\nNumero de Factura: {3}" +
                  "\nPrefijo {4}" +
                  "\nAcuse {5}\n").format(tipoDocumento, estado,
                                        periodo, numFactura, prefijo, acuse)}

    return {"fulfillmentText" : peticionstr + msg}
