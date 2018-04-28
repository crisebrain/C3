from time import time

class InfoManager():
    def __init__(self):
        """Creates the Info Manager for the current conference session."""
        self.conference_date = time()
        self.conference = {}

    def newconsult(self, jdata):
        """Creates new conversation Flow with the IntentTree class.
        Parameteres:
        chatbotjson: Json array with the ChatBot Id
                       and other fields.
        Outputs:
        Json with the info for the conversation nodes,
                 each node with the info about the id chatBot."""
        print(jdata["msgAns"])

        # if True:
        #     jdata_new = self.chbw.interceptIntent(jdata)
        # else:
        #     jdata_new = cognitive_req(jdata)
        #
        # self.sc.feedNextEntry(jdata_new)
        # self.sc.ShowSessionTree()
