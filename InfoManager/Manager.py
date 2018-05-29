from time import time
import re
import os
import json
import numpy as np

class InfoManager:
    """InfoManager class.
    Responsabilities:
    - Stays SessionContainer with an IntentTree loaded from pickle file (empty or
      partially filled) during "__init__".
    - Admins the adapter_DF request on "interceptIntent":
        -- identify if the intent is not fallback and feeds it (with "intentFlow").
           If intent is fallback the intent message from data will be processed by
           "Cognite_req". If the request asks for the values the function fetches
           them (wiht extractValue).
    - Feeds the correspondat intent Node with "intentFlow".
        -- Order to SessionContainer object to fill the correspondant intent Node
        -- Fetch the intents values with the SessionContainer if adapter_DF asks.
    - Fetches the valus from the contexts or id required with "extractValue".
    """
    def __init__(self, SessionContainer, makeWebhookResult,
                 rootdirectory, idChatBot=None):
        """Creates the Info Manager for the current conference session."""
        self.conference_date = time()
        self.conference = {}
        pathpicklefile = os.path.join(rootdirectory, "Sessions/Conference.pck")
        self.sc = SessionContainer(pathpicklefile, idChatBot)
        self.makeWebhookResult = makeWebhookResult
        self.sc.ShowSessionTree()

    def interceptIntent(self, jdata):  # strText, idNode
        """Text from IVR is sending to core chatbot and an intent is actioned.
        Output a jsonInput object with msgOriginal, idChatBot, idNode
        """
        sessionid = jdata.get("session").split("/")[-1]
        self.sc.reassignTree(sessionid)
        it = self.sc.extractTree()
        intentid = jdata.get("queryResult").get("intent").get("name")
        # sessionid =
        intentid = intentid.split("/")[-1]
        node = it.find_node(intentid, to_dict=False, by_field="id")
        if "fallback" not in node.name.lower():
            response = self.intentFlow(jdata, node)
        else:
            self.extractValue(jdata.get("queryResult").get("queryText"))
        print(it.currentcontextls)
        print(response)
        self.sc.updateConferencefile()
        self.sc.ShowSessionTree()
        return response

    def intentFlow(self, jdata, node):
        """Extracts the value from the msgOriginal with the extractValue
        function, then is stored into node from msgReq and msgAns taken.
        Parameters:
        jdata - query information dictionary.
        node - detected intentNode
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
                if "$" in parameter["value"]:  # local
                    # Guarda valor local
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
            it.updateContext(node.contextOut)
        response = self.outputMsg(jdata, currentNode, values, forward)
        return response


    def extractValue(self, msgOriginal):
        """Extracts the value from msgOriginal string from jdata dict."""
        # msgOriginal = jdata["msgOriginal"]
        value = msgOriginal.split(" ")[-1]
        print(value)
        print(msgOriginal)
        #jdata.update({"value":value})
        return value

    def outputMsg(self, jdata, node, values, forward):
        """formats the msgAns with the values from upper nodes."""
        # Tiene que ver con los contextos
        print(values)
        queryResult = jdata.get("queryResult")
        if forward:
            response = self.makeWebhookResult(jdata)
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
        response["fulfillmentText"] =  msgString
        return response
