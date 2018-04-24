from IntentTree import IntentTree, IntentNode
from .modulo_cognitivo impor cognitive_req
from time import time

class InfoManager:
    def __init__(self):
        """Creates the Info Manager for the current conference session."""
        self.conference_date = time()
        self.conference = {}

    def new_conversation(self, chatbotjson):
        """Creates new conversation Flow with the IntentTree class.
        Parameteres:
        chatbotjson: Json array with the ChatBot Id
                       and other fields.
        Outputs:
        Json with the info for the conversation nodes,
                 each node with the info about the id chatBot."""
        if self.conference == {}:
            node = cognitive_req(chatbotjson)
            conversation = self.new_conversation(node)
            self.conference.update(dict(zip([idchatBot],[conversation])))
        else:
            idchatBot =
            self.conference[]


    def new_intent(self, intent_info):
        """Creates the intentnode from the intent_info json or
        string path to json."""
        if intent_info isinstance(list):
            self.intent_info = self.load_json(intent_info)
        else:
            self.intent_info = intent_info
        self


    def search_node(self):
        print("Busca nodos")
