from ChatbotWrapper.Utils import methods_DF_to_IM as IM

def analizeReq(req: dict):
    value = None
    contador = 1
    respIntent = "No existe respuesta. Probablemente nadie lo sepa"
    intentName = req["queryResult"]["intent"]["displayName"]
    session = req['session'].split("sessions/")[-1]

    dicContextHuman = {
        "cx_interfaz": "Interfaces",
        "cx_objeto": "Objetos",
        "cx_carro": "Carros"
    }

    dicEntityToContext = {
        "imss" : "cx_imss",
        "nomina" : "cx_nomina",
        "catalogo" : "cx_catalogo",
        "configuracion": "cx_configuracion",
        "miportal": "cx_miportal",
        "seguridaddelperfil" :"cx_seguridaddelperfil",
        "perfil" : "cx_perfil",
        "usuario" : "cx_usuario",
        "auditoria" : "cx_auditoria",
        "permiso" : "cx_permiso",
        "grupoempresarial" : "cx_grupoempresarial",
        "difgrupoempyrazonsocial" : "cx_difgrupoempyrazonsocial",
        "campousuario" : "cx_campousuario"
    }

    # IntentName y los contextos.
    dicDuplicate = {
        "general_que_son": ["cx_interfaz", "cx_objeto"],
        "general-modulo": ["cx_nomina", "cx_imss" , "cx_catalogo" , "cx_configuracion", "cx_miportal", "cx_seguridaddelperfil" , "cx_perfil" , "cx_usuario" , "cx_auditoria" , "cx_permiso" , "cx_grupoempresarial" , "cx_difgrupoempyrazonsocial" , "cx_campousuario"],
        "general-como": ["cx_permiso"]
    }

    # IntentName y sus respuestas.
    dicResponse = {
        "interfaz_costo": "El costo varía, según lo que quieras.",
        "objeto_tipo": "Pues el tipo de objeto...",
        "carros_marca": "es el fabricante del carro",
        "imss-servicio": "Los servicios del IMSS se refiere a los servicios que brinda la dependencia gubernamental",
        "general_que_son": {
            "interfaz": "Son las interfaces de usuario.",
            "objeto": "Son cosas que puede usar el usuario."
        },
        "general-modulo": {
            "imss": "El módulo IMSS contiene la funcionalidad general de los servicios del IMSS a los cuales se tiene acceso desde el portal.",
            "nomina": "El móduo Nómina contiene el grupo de permisos para: Captura Incidencias por Concepto, Captura Incidencias por empleado, Reversar Finiquito, Cálculo de nómina, Realizar re-apertura de finiquitos",
            "catalogo" : "El módulo Catálogos permite la administración de los 4 tipos de catalogos de que dispone el sistema que son: Puestos, Centro de Costos, Área y Sindicato. Cada uno de ellos permite la administración de  los registros del tipo que los define.",
            "configuracion": "El módulo de Configuración contiene el grupo de permisos  de Administración de Usuarios.",
            "miportal": "Mi Portal es el modulo principal del usuario y permite la visualización de la información general de su registro, notificaciones pendientes, Administración de recibos electrónicos  y de vacaciones.",
            "seguridaddelperfil" : "La seguridad del perfil se refiere a la definición de los permisos de ejecución de las actividades existentes por módulo. Los módulos disponibles son: Mi Portal, Configuración, Catálogos, IMSS  y Nómina. Para efectuar esta configuración es necesario ingresar a la sección de Configuración de Perfiles de Usuario.",
            "perfil" : "El perfil es el conjunto de permisos que indican las partes del sistema que puede visualizarse y operar.",
            "usuario" : "El Usuario es el registro del empleado que tiene facultades o permisos para realizar determinadas acciones sobre los datos del Grupo Empresarial, este registro se encuentra integrado por el identificador, nombre, perfil y rol. La descripción se refiere al nombre largo que tendrá el usuario en el sistema,  y este puede ser asociado a un empleado previamente registrado y seleccionar el tipo de perfil que más se adecúe.",
            "auditoria" : "El módulo de auditoría es el registro de bitacora de actividades en el sistema, permite efectuar consultas de los eventos mediante los filtros de: Usuario, fecha de inicio, fecha fin, tipo de operación, y tipo de componente.",
            "permiso" : "Los permisos se refieren a los partes del sistema que se podrán visualizar y operar dentro del sistema.",
            "grupoempresarial" : "Un grupo empresarial es un conjunto de empresas controladas por el mismo equipo de personas, coloca el nombre con el que identificas tu compañía o conjunto de compañías. En este campo debes capturar el nombre con el que identificas tu negocio o grupo de negocios.",
            "difgrupoempyrazonsocial" : "Un grupo empresarial es un conjunto de empresas controladas por el mismo equipo de personas, una razón social es una empresa específica, es el nombre oficial y legal que tiene cada empresa. ",
            "campousuario" : "En el campo usuario se debe ingresar un nombre o número con el que será identificada la persona."
        },
        "general-como": {
            "permiso": "Para consultar y asignar los permisos es necesario ir a Configuración-Grupo Empresarial y dar click en el elemento de la columna 'Perfiles'. Esta acción genera el listado de los perfiles existentes y permite la activación de los permisos al seleccionar algunos de los módulos presentados y efectuar la administración en la secciónd de Seguridad."
        }
    }
    #recibe respIntent y value de la entidad
    def createResp( value):
        resp = {
            "outputContexts": [{"name": req["session"] + "/contexts/" + dicEntityToContext[value],
                               "lifespanCount": 5}]
        }
        return resp

    # Set type of query "que son"
    if req['queryResult']['parameters'].keys():
        for key in req['queryResult']['parameters'].keys():
            if isinstance(req['queryResult']['parameters'][key], dict ):
                value = list(req['queryResult']['parameters'][key].keys())[0]
            else:
                value = key

    # Actualiza el IM con la petición de DF
    IM.post_data(req)

    # If is a intent duplicate and hasn't value. We need context.
    duplicate = dicDuplicate.get(intentName)

    # este if es para saber si la petición pertenece a un intent genérico
    _definedContext = False
    if duplicate:
        # Pregunta implícita. Necesita contextos.
        if not value:
            # get get history of contexts
            reqRecVal = {
                "action": "recuperaValores",
                "data": {
                    "reqObject": "context",
                    # A veces hay contextos que no nos interesan como el followup, y debemos quitarlos.
                    # Únicamente necesitamos dos.
                    "numberHistory": 4,
                    "session": session,
                    "agent": req['session'].split("/")[1],
                }
            }
            respRecupera = IM.post_data(reqRecVal)
            print(respRecupera)

            if respRecupera["returnCode"] == 1:
                # extracting useful information about history contexts
                # historyContexts = respRecupera["Objects"]
                # historyConDup = [context[0] for context in historyContexts if context[0] in dicDuplicate[intentName]]
                # Clean lista and cut to 2 contexts
                historyContexts = _cleanHistoryContext(respRecupera["Objects"].copy(), dicDuplicate[intentName], 2)

                if len(historyContexts) == 0:
                    respIntent = "¿De qué tema me hablas?"
                elif len(historyContexts) == 1:
                    respIntent = dicResponse[intentName][historyContexts[0][3:]]
                elif len(historyContexts) == 2:
                    respIntent = "¿Te refieres a {} o a {}?".format(dicContextHuman[historyContexts[0]],
                                                                  dicContextHuman[historyContexts[1]])
        # Pregunta explícita. Dan la entity en la misma pregunta.
        else:
            respIntent = dicResponse[intentName][value]
            #return createResp(respIntent, value)
            _definedContext = True

    # Caso donde primero hicieron pregunta implícita, y luego me especifican de que hablan.
    elif intentName == "general_que_son-de_que":
        respIntent = dicResponse[intentName.split("-")[0]]
        #return createResp(respIntent, value)
        _definedContext = True

    # Caso de intent específico con entity.
    else:
        respIntent = dicResponse.get(intentName, respIntent)

    resp = []

    resp = {
        "fulfillmentText": respIntent
    }
    if _definedContext:
        resp.update(createResp(value))

    print(resp)

    return resp


def _cleanHistoryContext(contexts: list, wanted: list, previousContext: int):
    """
    Limpia los contextos dejando únicamente los que nos interesan.
    Esta función también borra los followup.
    :param contexts: lista de contextos original
    :param wanted: diccionarios de contextos duplicados
    :previousContext: número máximo de contextos a buscar hacia atrás (no incluye followup)
    :return: retorna una lista sin los contextos que no nos interesan
    """
    # extracting useful information about history contexts

    historyContexts = []
    contextsTemp = []

    for context in contexts:
        if not "followup" in context[0]:
            contextsTemp.append(context)

    for context in contextsTemp[-previousContext:]:
        if context[0] in wanted:
            historyContexts.append(context[0])


    # historyContexts = [context[0] for context in contexts if context[0] in listUnwanted]
    return historyContexts


def _testRecuperaValores(number):
    listContext =[]
    if number == 1:
        listContext = [["cx_interfaz"]]
    elif number == 2:
        listContext = [["cx_interfaz"], ["cx_objeto"]]

    return {
	    "Objects": listContext,
	    "message": "Ok",
	    "returnCode": 1
    }
