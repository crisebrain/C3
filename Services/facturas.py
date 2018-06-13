
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
                dicNombres[unico] = " ".join([dicNombres[unico].strip(),
                                              dicc[unico].strip()])

    # Concatenamos los nombres
    nombre = "" + str(dicNombres.setdefault("nombre", "")) + " "\
             + str(dicNombres.setdefault("apellido", "")) + " "\
             + str(dicNombres.setdefault("nombresExtras", ""))

    return nombre.strip()

def factura(parametros):
    estado = None
    tipoDocumento = None
    periodo = None
    prefijo = None
    acuse = None
    numFactura = None
    # Ya que los elemenetos vienen en una lista deben tener un tratamiento
    # particular
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
        if not isinstance(prefijo, str):
            prefijo = str(int(prefijo))
        else:
            prefijo = prefijo.upper()
    if diccFusionado.get("acuse"):
        acuse = diccFusionado.get("acuse").get("value")
    if diccFusionado.get("numeroFactura"):
        numfactura = diccFusionado.get("numeroFactura").get("value").get("value")
        if not isinstance(numfactura, str):
            numFactura = str(int(numfactura))
        else:
            numfactura = [c if c.isdigit() else c.upper() for c in numfactura]
            numfactura = "".join(numfactura)
    # Caso que no traiga ninguna restricción. Consulta muy amplia
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

    diccFinal = {"Empresa": "RICOH",
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
                 "NITAdquiriente": ""}

    # servicio de factura
    req = sendReq(diccFinal)
    msg = HumanResult(getResponseValues(req.content))
    print(msg)
    mostrar = [tipoDocumento, estado, periodo, numFactura, prefijo, acuse]
    simostrar = [True if var is not None else False for var in mostrar]
    formatos = ["\nTipo documento: ", "\nEstado: ", "\nPeriodo ",
                "\nNumero de Factura: ", "\nPrefijo ", "\nAcuse "]
    peticionstr = ""
    for i, var in enumerate(mostrar):
        if simostrar[i]:
            peticionstr += formatos[i] + "{0}".format(var)
    peticionstr += ".\n-----------------------------------\n" + msg
    respuesta =  {"fulfillmentText" : peticionstr,
                  "payload": { "resultIn": {"periodo": periodo,
                                            "estado": estado,
                                            "numFactura": numFactura,
                                            "prefijo": prefijo,
                                            "acuse": acuse,
                                            "factura": tipoDocumento},
                  "resultOut": getResponseValues(req.content)}}
    return respuesta
