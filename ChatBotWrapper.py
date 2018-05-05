#import dialogflow
import os
import json
from time import time
from Utils import IntentTree
import pickle

"""Class to manage the conversation and publish the IntentTree"""
class ChatBotWrapper:

    def publishIntentTree(self, chatbots_folder):
        """Consult and publish the current IntentTree using the chatbots folder.
        Here a project id is supplied to retrieve all intents from core
        and build the IntentTree. At the end self.current_intentTree must
        be updated and the tree saved it into session
        """
        chatbots = os.listdir(chatbots_folder)
        intentTree_list = []
        for chat in chatbots:
            intents = os.listdir(os.path.join(chatbots_folder,chat,'intents'))
            agent_data = json.load(open(os.path.join(chatbots_folder,chat,'agent.json')))
            id_chatbot = agent_data['googleAssistant']['project']
            # divide the json objects between intents and usersays
            intents_usersays = []
            intents_copy = intents.copy()
            for f in intents_copy:
                if '_usersays_' in f:
                    intents_usersays.append(f)
                    intents.remove(f)
                if 'Fallback' in f:
                    intents.remove(f)
            # parsing Intents and Usersays to IntentTree
            intents_jsons = []
            intents_ids = {}
            for intent in range(len(intents)):
                intent_data = json.load(open(os.path.join(chatbots_folder,chat,'intents',intents[intent])))
                intent_usersay = json.load(open(os.path.join(chatbots_folder,chat,'intents',intents_usersays[intent])))
                # normal intent
                if not intent_data['fallbackIntent']:
                    intents_ids[intent_data['id']]=intent_data['name']
                    msgReq = intent_usersay[0]['data'][0]['text']
                    msgAns = intent_data['responses'][0]['messages'][0]['speech']
                    id_field = None
                    if len(intent_data['responses'][0]['parameters'])>0:
                        id_field = intent_data['responses'][0]['parameters'][0]['name']
                    build_json = {"name":intent_data['name'], "parent": None,
                                  "idField":id_field, "value":None,
                                  "accuracyPrediction":0, "mandatory":False,
                                  "msgReq":msgReq,"msgAns":msgAns}
                    # check if it is the root node
                    if 'parentId' not in intent_data.keys():
                        it = IntentTree(build_json, time(), id_chatbot)
                    else:
                        build_json['parent']=intent_data['parentId']
                        intents_jsons.append(build_json)
            i = 0
            while len(intents_jsons)>0:
                jsonObj=intents_jsons[i]
                if it.find_node(value=intents_ids[jsonObj['parent']], to_dict=False):
                    jsonObj['parent']=intents_ids[jsonObj['parent']]
                    it.add_node(jsonObj)
                    intents_jsons.remove(jsonObj)
                    i=0
                else:
                    i=i+1
            intentTree_list.append(it)
        # keep as current tree the first one and save all IntentTrees in the list to Sessions
        self.current_intentTree = intentTree_list[0]
        pickle.dump(intentTree_list,open('./Sessions/Conference.pck','wb'))

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
