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
        json_root = cognitive_req(chatbotjson)
        idchatBot = chatbotjson['idChatBot']
        conversation = IntentTree(json_root,
                                  time(), idchatBot)
        self.conference.update(dict(zip([idchatBot],[conversation])))

    def new_intent(self, intent_info):
        """Creates the intent node from the intent_info json or
        string path to json."""
        if isinstance(intent_info, str):
            intent_info = self.load_json(intent_info)
        self.conference[ChatBotWrapper.current_idChatBot].add_node(intent_info,
                                                                   parent)
