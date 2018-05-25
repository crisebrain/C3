#-*- coding: utf-8 -*-
import os
import json
import pickle
from ConversationEngine import traductor_df
from Utils import IntentTree

"""Class to manage the conversation and publish the IntentTree"""
class ChatBotWrapper:

    def __init__(self, chatbots_folder, idChatBot=None):
        self.publishIntentTree(chatbots_folder, idChatBot)

    def publishIntentTree(self, chatbots_folder, idChatBot=None):
        """Consult and publish the current IntentTree using the chatbots folder.
        Here a project id is supplied to retrieve all intents from core
        and build the IntentTree. At the end self.current_intentTree must
        be updated and the tree saved it into session.
        """
        intentTree_list = traductor_df(chatbots_folder, IntentTree)
        # Traduce de json intents a intentTree
        pickle.dump(intentTree_list, open('Sessions/Conference.pck','wb'))
        if idChatBot is None:
            self.current_intentTree = intentTree_list[0].idChatBot
        else:
            indices = [True if idChatBot == tree.idChatBot else False
                       for tree in intentTree_list]
            tree = intentTree_list[indices.index(True)]
            self.current_intentTree = tree.idChatBot
        print("Created intentTree for %s" %self.current_intentTree)
