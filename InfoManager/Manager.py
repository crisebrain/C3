from time import time

class InfoManager:
    def __init__(self, SessionContainer):
        """Creates the Info Manager for the current conference session."""
        self.conference_date = time()
        self.conference = {}
        self.sc = SessionContainer()

    def newConsult(self):
        """Creates new conversation Flow with the IntentTree class.
        Parameteres:
        chatbotjson: Json array with the ChatBot Id
                       and other fields.
        Outputs:
        Json with the info for the conversation nodes,
                 each node with the info about the id chatBot."""
        jdata = self.sc.WhosNextEntry()
        return jdata

    def intentFlow(self, jdata, cbwrapper, se):
        if jdata["state"] == "valid":
            cbwrapper.showResponse(jdata)
            # self.sc.fill_node(jdata)
        elif jdata["state"] == "no_valid":
            print("ChatBotWrapper no solucionó")
            print("Buscando en bases de datos\n")
            print("Buscando con mecanismo cognitivo\n")
            jdata_ans = se(jdata)
            for intent in jdata_ans:
                cbwrapper.showResponse(intent)
                self.sc.feedNextEntry(intent)
