#import dialogflow
import os
import json
import pickle
from ConversationEngine import traductor_df
from Utils import IntentTree

"""Class to manage the conversation and publish the IntentTree"""
class ChatBotWrapper:

    def publishIntentTree(self, chatbots_folder):
        """Consult and publish the current IntentTree using the chatbots folder.
        Here a project id is supplied to retrieve all intents from core
        and build the IntentTree. At the end self.current_intentTree must
        be updated and the tree saved it into session
        """
        intentTree_list = traductor_df(chatbots_folder, IntentTree)
        self.current_intentTree = intentTree_list[0]
        pickle.dump(intentTree_list, open('Sessions/Conference.pck','wb'))


    def generateAnswer(self, jsonGenerateAnswer):
        """Read msgAnswer from the idIntentTree-idNode for current intent.

        If the idIntentTree equals to idChatBot for the current_intentTree,
        then find the idNode and load msgAnswer. Else, publishIntentTree
        with the new idChatBot and find idNode to load msgAnswer.
        The output is sending to the IVR as a text string.
        """
        print("Chatbot:  \n", jsonGenerateAnswer["msgAnsd"])

    def interceptIntent(self, im):  # strText, idNode
        """Text from IVR is sending to core chatbot and an intent is actioned.
        Output a jsonInput object with msgOriginal, idChatBot, idNode
        """
        jdata = im.newConsult()
        # IVR
        print("Usuario:  ")
        msgOriginal = input()
        # IVR
        # print(jdata["msgAns"])
        jdata.update({"msgOriginal": msgOriginal})
        # simulacion de construccion de mensaje
        # ******* Operaciones de chatbotWrapper para deteccion de *******
        # ************* mensajes, simulada con el if ********************
        if msgOriginal is not None:
            jdata.update({"state": "valid"})
        else:
            jdata.update({"state": "no_valid"})
        return jdata
        # ***************************************************************

    def listAllAvailableChatbots(self):
        """Check all available chatbots on the core and assign them an id."""

    def manageConversation(self):
        """intercept the intent that it is actioned and change it by the
        one received from GI."""

    def __init__(self, chatbots_folder):
        self.publishIntentTree(chatbots_folder)
