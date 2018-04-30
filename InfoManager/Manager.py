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
        print(jdata["msgAns"])
        return jdata

    def intentFlow(self, jdata, cbwrapper, se):
        cbwrapper.(jdata)
        chbw = self.cbw(jdata["IdField"])
        if True:
            jdata_new = chbw.interceptIntent()
        else:
            jdata_new = self.se(jdata)
        self.sc.feedNextEntry(jdata_new)
        self.sc.ShowSessionTree()
