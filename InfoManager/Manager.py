from time import time
import requests
import subprocess
import re
import os
import json
import numpy as np
import threading
import sys
sys.path.append("Utils")
from textJumping import detect_intent_texts
from Utils import SessionContainer, constantesFacturas
sys.path.append("Services")
from Services import makeWebhookResult
sys.path.append("SearchEngine")
from SearchEngine import Regexseaker
import gc

class InfoManager:
    """InfoManager class.
    Responsabilities:
    - Stays SessionContainer with an IntentTree loaded from pickle file (empty
      or partially filled) during "__init__".
    - Admins the adapter_DF request on "interceptIntent":
        -- identify if the intent is not fallback and feeds it (with
           "intentFlow"). If intent is fallback the intent message from data
           will be processed by "Cognite_req". If the request asks for the
           values the function fetches them (wiht intentDecompose).
    - Feeds the correspondat intent Node with "intentFlow".
        -- Order to SessionContainer object to fill the correspondant intent Node
        -- Fetch the intents values with the SessionContainer if adapter_DF asks.
    - Fetches the values from the contexts or id required with "intentDecompose".
    """
    def __init__(self, rootdirectory, idChatBot=None):
        """Creates the Info Manager for the current conference session."""
        self.conference_date = time()
        self.conference = {}
        pathpicklefile = os.path.join(rootdirectory, "Sessions/Conference.pck")
        self.sc = SessionContainer(pathpicklefile, idChatBot)
        self.makeWebhookResult = makeWebhookResult
        self.sc.ShowSessionTree()
        self.info = dict()

    def interceptIntent(self, jdata):  # strText, idNode
        """Intercept the intent query info from the bot client (DF format) and
        decides which kind of treatment apply it, if the detection was
        successful the info will be sended to intentFlow method, if the intent
        was not detected the message will be used for exctract (intentDecompose)
        the possible intents, and entities staying into the original message.
        """
        projectid = jdata.get("session").split("/")[1]
        sessionid = jdata.get("session").split("/")[-1]
        intentid = jdata.get("queryResult").get("intent").get("name")
        intentid = intentid.split("/")[-1]
        self.info.update(dict(projectid=projectid, sessionid=sessionid))
        self.sc.reassignTree(sessionid, projectid)
        it = self.sc.extractTree()
        node = it.find_node(intentid, to_dict=False, by_field="id")
        if "fallback" not in node.name.lower():
            response = self.intentFlow(jdata, node)
        else:
            self.info["complexMsg"] = jdata.get("queryResult").get("queryText")
            self.intentDecompose()
        print(it.currentcontextls)
        self.sc.updateConferencefile()
        self.sc.ShowSessionTree()
        return response

    def intentFlow(self, jdata, node):
        """Extracts the value from the msgOriginal with the intentDecompose
        function, then is stored into node from msgReq and msgAns taken.
        Parameters:
        jdata - query information dictionary.
        node - detected intentNode.
        """
        queryResult = jdata.get("queryResult")
        it = self.sc.extractTree()
        inputcontext = [True if context in it.currentcontextls else False
                        for context in node.contextIn]
        values = dict()
        forward = True
        currentNode = node
        if all(inputcontext):
            parameters = node.parameters
            userdictinfo = queryResult.get("parameters")
            for parameter in parameters:
                name = parameter["name"]
                value = userdictinfo[name]
                print(value)
                if "$" in parameter["value"]:  # local
                    if jdata.get("IM_fields") is not None:
                        node.writeParameter(jdata.get("IM_fields"), name)
                    # Guarda valor local
                    else:
                        node.writeParameter(value, name)
                    values.update({parameter["value"]:value})
                elif "#" in parameter["value"]:
                    aux = parameter["value"].split(".")[0]
                    context = aux.replace("#", "").lower()
                    parameterValue = "$" + parameter["value"].split(".")[1]
                    # busca valor referenciado
                    nodereferenced = it.find_node(context,
                                                  by_field="contextOut",
                                                  to_dict=False)
                    userValue = nodereferenced.readParameter(name)
                    if userValue is not None:
                        if userValue != value:
                            nodereferenced.writeParameter(value, name)
                        values.update({parameterValue: value})
                    else:
                        node.assignCurrent()
                        currentNode = nodereferenced
                        forward = False
                        break
        else:
            currentNode = it.find_node("True", False, "current")
            if currentNode is None:
                currentNode = it.find_node("Default Fallback Intent", False,
                                           "name")  # node.children[0]
            forward = False
        if forward:
            it.inputStacklist(node)
            it.updateContext(node.contextOut)
        response = self.outputMsg(jdata, currentNode, values, forward)
        return response

    def outputMsg(self, jdata, node, values, forward):
        """formats the msgAns with the values from upper nodes."""
        # Tiene que ver con los contextos
        queryResult = jdata.get("queryResult")
        if forward:
            response = self.makeWebhookResult(jdata,2)
            if response["payload"]["returnCode"] == "0":
                msgString = node.msgAns
                pattern = r"\$\w+"
                fields = re.findall(pattern=pattern, string=msgString)
                if isinstance(fields, list):
                    for field in fields:
                        fieldw = field[1:]
                        msgString = msgString.replace(field, values[field])
                # return msgString
            else:
                msgString = response["fulfillmentText"]
                # return msgString
        else:
            msgString = node.msgAns
            # return node.msgAns
        response["fulfillmentText"] = msgString
        return response

    def datumCSE_Facturas(self, jdata):
        reg = Regexseaker()
        ndata = jdata.get("datos")
        fields = ndata.get("campos")
        phrase = ndata.get("frase")
        results = dict()
        for field in fields:
            result = reg.seakexpresion(phrase, field)
            if field in [constantesFacturas.PERIODO.value,
                         constantesFacturas.FECHA.value]:
                resdict = dict(zip(list(result[0].keys()) + ["statusField"],
                                   list(result[0].values()) + [result[1]]))
            else:
                resdict = dict(value=result[0],
                               statusField=result[1])
            results.update({field:resdict})
        response = {"campos": results,
                    "message": "Extraccion de campos",
                    "returnCode": 1}

        # TODO Revisar que este gc no esté ocultando otro problema más grave.
        # se debe revisar con un dump de memoria
        gc.collect()

        return response

    def fetchValues(self, jdata):
        """Fetch the n objects that are required on the request.
        jdata: dir object with the following fields
              agent - agent id, string assigned by dialogflow.
              session - session id, string assigned by dialogflow
              data-numberHistory - number of elements to fetch
              data-reqObject - object type (context, intent)
        """
        projectid = jdata.get("data").get("agent")
        sessionid = jdata.get("data").get("session")
        print(projectid)
        self.sc.reassignTree(sessionid, projectid)
        data = jdata.get("data")
        it = self.sc.extractTree()
        nhistory = jdata.get("data").get("numberHistory")
        reqObject = jdata.get("data").get("reqObject")
        Objects = it.fromStackList(nhistory, by_field=reqObject)
        message = ""
        returnCode = 1
        response = {"Objects": Objects,
                    "message": message,
                    "returnCode": returnCode}
        return response

    def intentDecompose(self):
        """Extracts the value from msgOriginal string from jdata dict.
        Creates a sequence in a list kind object, with the intents detected
        by the CSE classification.
        """
        # -----------------------------------------------------------------
        # simulando el cse
        # identified_list = cognite_req(msgoriginal)
        # esta lista estara construida con los intents que haya identificados
        # el cse, clasificados de acuerdo a sus nombres
        # -----------------------------------------------------------------
        it = self.sc.extractTree()
        sentencias = self.info["complexMsg"].split(",")
        intent0 = it.find_node(sentencias[0], False, "msgReq")  # "Hola"
        intent1 = it.find_node(sentencias[1], False, "msgReq")
        # -----------------------------------------------------------------
        # intents identificados, los nombres de los intents equivalen a las
        # etiquetas de clase
        identified_list = ["02 VDN", "VDN - no"]  # simulando cse
        sentencias = ["Hablale a Gabriel", "ya no quiero"]
        self.info["sentencias"] = dict(zip(identified_list, sentencias))
        nodes = []
        for intentname in identified_list:
            nodes.append(it.find_node(intentname, False, "name"))
        self.sequenceNodes = nodes
        if len(self.sequenceNodes) > 0:
            self.imControl = True
        # Para enviar la peticion de salto
        print(nodes)
        while len(self.sequenceNodes) > 0:

            self.jumpToIntent()

    def jumpToIntent(self, by="text"):
        """Send the post query to dialog flow to jump into necessary intent."""
        it = self.sc.extractTree()
        node = self.sequenceNodes.pop(0)
        if by == "event":
            events = getattr(node, "events", None)
            condicion = events is not None
            assert condicion, "No hay evento gatillo en nodo: {0}".format(node.name)
            if len(node.parameters) > 0:
                # parameters = clasifyparameters()  # encuentra entidades clasifica
                parameters = {'nombre': 'Gabriel'}
                data = {"queryInput": {"event": {'name': events[0],
                                                 'parameters': {'nombre': 'Gabriel'},
                                                 'languageCode': 'en'}},
                        "queryParams": {"timeZone": "America/Mexico_City"}}
            else:
                data = {"queryInput": {"event": {'name': events[0],
                                                 'parameters': {},
                                                 'languageCode': 'en'}},
                        "queryParams": {"timeZone": "America/Mexico_City"}}
            res = sendEvent(data, getToken(), session)
        elif by == "text":
            name = node.name
            detect_intent_texts(self.info["projectid"],
                                self.info["sessionid"],
                                [self.info["sentencias"][name]],
                                "es")
