from ChatbotWrapper.Utils import methods_DF_to_IM as IM
import json
from pprint import pprint

with open('ChatbotWrapper/DF/preguntasRespuestas.json') as f:
    specjson = json.load(f)

#===============================================================================================================
#===============================================================================================================
#===============================================================================================================
#===============================================================================================================

contextsHistory = []

def analizeReq(req: dict):
    value = None
    contador = 1
    respIntent = "No existe respuesta. Probablemente nadie lo sepa"
    #print("RRRRRRRRRRRRRRRRRRRRRRRRRRRR-- " + str(req) +" --RRRRRRRRRRRRRRRRRRRRRRRRRRRR")
    intentName = req["queryResult"]["intent"]["displayName"]
    session = req['session'].split("sessions/")[-1]


    #cuando hay que mencionar la entidad en lenguaje natural a partir de los contextos recordados
    #para mencionarlo en una frase, de aquí se extrae
    dicContextToEntityPhrase = specjson["dicContextToEntityPhrase"]
    #cuando el usuario te da el contexto, se usa este dic para parsear la entidad al contexto
    dicEntityToContext = specjson["dicEntityToContext"]
    # IntentName y los contextos.
    dicDuplicate = specjson["dicDuplicate"]
    # IntentName y sus respuestas.
    dicResponse = specjson["dicResponse"]

    #===============================================================================================================
    #===============================================================================================================
    #recibe respIntent y value de la entidad
    #/////
    #===============================================================================================================
    #===============================================================================================================

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
    print("¿¿ value: " + str(value))
    print("¿¿ intentName: " + str(intentName))
    duplicate = dicDuplicate.get(intentName)
    print("¿¿ dicDuplicate: " + str(duplicate))
    ###print("THIS IS WHAT WE GOT ON DUPLICATE  " + str(duplicate))

    # este if es para saber si la petición pertenece a un intent genérico
    _definedContext = False
    if duplicate:
        print("DUPLICATE IF ENTERED")
        # Pregunta implícita. Necesita contextos.
        #if not value:
        if value == "que_son":
            print("QUE_SON IF ENTERED")
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
            #print("!!!!!!!!!!!!!!!" + str(respRecupera))

#==================================================================================
            if respRecupera["returnCode"] == 1:
                print("RETURN CODE IF ENTERED")
                #print("---EL INTENTNAME " + intentName + "-----dicDuplicate[intentName]  " + str(dicDuplicate[intentName]))
                #historyContexts = _cleanHistoryContext(respRecupera["Objects"].copy(), dicDuplicate[intentName], 2)
                #if len(historyContexts) == 0:
                #    respIntent = "¿A qué te refieres?"
                #elif len(historyContexts) == 1:
                #    respIntent = dicResponse[intentName][historyContexts[0][3:]]
                #elif len(historyContexts) == 2:
                #    respIntent = "¿Te refieres a {} o a {}?".format(dicContextToEntityPhrase [historyContexts[0]], dicContextToEntityPhrase [historyContexts[1]])
                if len(contextsHistory) >= 2:
                    print(">= 2 CONTEXT HISTORY IF ENTERED")
                    print("we got overhere")
                    respIntent = "¿Te refieres a {} o a {}?".format(dicContextToEntityPhrase[contextsHistory[len(contextsHistory) - 2]], dicContextToEntityPhrase[contextsHistory[len(contextsHistory) - 1]])
                else:
                    print("== 0 CONTEXT HISTORY IF ENTERED")
                    respIntent = "¿A qué te refieres?"
                #elif len(contextsHistory) == 1:
                    #print("== 1 CONTEXT HISTORY IF ENTERED")
                    #respIntent = dicResponse[intentName][contextsHistory[0][3:]]
        # Pregunta explícita. Dan la entity en la misma pregunta.
        else:
            print("EXPLICITY CASE ATTENDED " + str(dicResponse[intentName][value]))
            respIntent = dicResponse[intentName][value]
            contextsHistory.append(dicEntityToContext[value])
            print(str(contextsHistory))
            #return createResp(respIntent, value)
            _definedContext = True

    # Caso donde primero hicieron pregunta implícita, y luego me especifican de que hablan.
    elif intentName == "general_que_son-de_que":
        print("IMPLICITY CASE ATTENDED " + str(dicResponse[intentName.split("-")[0]]))
        respIntent = dicResponse[intentName.split("-")[0]][value]
        contextsHistory.append(dicEntityToContext[value])
        print(str(contextsHistory))
        #return createResp(respIntent, value)
        _definedContext = True

    # Caso de intent específico con entity.
    else:
        print("---------------------WE GOT HERE----------------------")
        #respIntent = dicResponse.get(intentName, respIntent)
        respIntent = dicResponse[intentName]
        contextsHistory.append(dicEntityToContext[value])
        print(str(contextsHistory))

    resp = []

    resp = {
        "fulfillmentText": respIntent
    }
    if _definedContext:
        resp.update(createResp(value, req, dicEntityToContext))

    print(resp)
    print(" ")
    print(" ")
    print(" ")
    return resp

#===============================================================================================================
#===============================================================================================================
#===============================================================================================================
#===============================================================================================================
#"recibe respIntent y value de la entidad" entre comillas
def createResp(value, req, dicEntityToContext):
    resp = {
        "outputContexts": [{"name": req["session"] + "/contexts/" + dicEntityToContext[value],
                           "lifespanCount": 5}]
    }
    return resp

#===============================================================================================================
#===============================================================================================================
#===============================================================================================================
#===============================================================================================================

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

    #print(str(contexts))

    for context in contexts:
        print("+" + str(context[0]))
        if not "followup" in context[0]:
            contextsTemp.append(context)

    #for context in contextsTemp[-previousContext:]:
    #    print("an iteration")
    #    if context[0] in wanted:
    #        historyContexts.append(context[0])



    # historyContexts = [context[0] for context in contexts if context[0] in listUnwanted]
    #return wanted
    return historyContexts


#===============================================================================================================
#===============================================================================================================
#===============================================================================================================
#===============================================================================================================


#def _testRecuperaValores(number):
#    listContext =[]
#    if number == 1:
#        listContext = [["cx_interfaz"]]
#    elif number == 2:
#        listContext = [["cx_interfaz"], ["cx_objeto"]]
#
#    return {
#        "Objects": listContext,
#        "message": "Ok",
#        "returnCode": 1
#    }
