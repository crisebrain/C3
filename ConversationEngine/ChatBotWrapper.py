"""Class to manage the conversation and publish the IntentTree"""
class ChatBotWrapper:

    def publishIntentTree(self, IdChatBot):
        self.IdChatBot = IdChatBot
        """Consult and publish the current Intent by the Chatbot Id.

        Here a chatbot id is supplied to retrieve all intents from core
        and build the IntentTree. At the end self.current_intentTree must
        be updated and the tree saved it into session
        """

    def generateAnswer(self, jsonGenerateAnswer):
        """Read msgAnswer from the idIntentTree-idNode for current intent.

        If the idIntentTree equals to idChatBot for the current_intentTree,
        then find the idNode and load msgAnswer. Else, publishIntentTree
        with the new idChatBot and find idNode to load msgAnswer.
        The output is sending to the IVR as a text string.
        """

    def interceptIntent(self):  # strText, idNode
        """Text from IVR is sending to core chatbot and an intent is actioned.
        Output a jsonInput object with msgOriginal, idChatBot, idNode
        """
        respuesta = input()
        return {"name":"Ampliacion", "value": respuesta,
                "IdChatBot":self.IdChatBot, "msgAns":"Tu respuesta es {0}".format(respuesta)}

    def listAllAvailableChatbots(self):
        """Check all available chatbots on the core and assign them an id."""

    def manageConversation(self):
        """intercept the intent that it is actioned and change it by the
        one received from GI."""

    def __init__(self, IdChatBot):
        self.publishIntentTree(IdChatBot)
