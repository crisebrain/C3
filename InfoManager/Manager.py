from time import time
import re

class InfoManager:
    def __init__(self, SessionContainer, ChatBotWrapper):
        """Creates the Info Manager for the current conference session."""
        self.conference_date = time()
        self.conference = {}
        self.sc = SessionContainer(ChatBotWrapper.current_intentTree,
                                   ChatBotWrapper.current_intentTree.idChatBot)

    def newConsult(self):
        """Creates new conversation Flow with the IntentTree class.
        Parameteres:
        chatbotjson: Json array with the ChatBot Id
                       and other fields.
        Outputs:
        Json with the info for the conversation nodes,
                 each node with the info about the id chatBot."""
        jdata = self.sc.WhosNextEntry()
        jdata["msgAns"] = self.outputMsg(jdata["msgAns"])
        return jdata

    def intentFlow(self, jdata, cbwrapper, se):
        if jdata["state"] == "valid":
            cbwrapper.generateAnswer(jdata)
            self.sc.feedNextEntry(jdata)

            # self.sc.fill_node(jdata)
        elif jdata["state"] == "no_valid":
            print("ChatBotWrapper no solucionó")
            print("Buscando en bases de datos\n")
            print("Buscando con mecanismo cognitivo\n")
            jdata_ans = se(jdata)
            for intent in jdata_ans:
                cbwrapper.generateAnswer(intent)
                self.sc.feedNextEntry(intent)

    def outputMsg(self, msgString):
        pattern = r"\$\w+"
        fields = re.findall(pattern=pattern, string=msgString)
        if isinstance(fields, list):
            for field in fields:
                fieldw = field[1:]
                tree = self.sc.extractTree()
                node = tree.find_node(fieldw, False, "idvalue")
                msgString = msgString.replace(field, node.value)
        return msgString
            # tree.find_node()
