import os
import json
from time import time

def get_json_list(intent_dict, mode, pathfile):
    json_array = []
    for filename in intent_dict[mode]:
        pfile = os.path.join(pathfile, filename)
        data = json.load(open(pfile, "r"))
        json_array.append(data)
    return json_array

def get_files_list(chatbots_folder):
    chatbots = os.listdir(chatbots_folder)
    botnames = {}
    for chat in chatbots:
        intfolder = os.path.join(chatbots_folder, chat, "intents")
        intents_usersays =[f for f in os.listdir(intfolder) if "_usersays_" in f]
        intents = [f for f in os.listdir(intfolder) if "_usersays_" not in f]
        botnames.update({chat:{"usersays": intents_usersays,
                               "intents": intents}})
    return botnames

def traductor_df(chatbots_folder, IntentTree):
    # Json files names
    botnames = get_files_list(chatbots_folder)
    # Json files loading ...
    json_intents = {}
    for botname, intents in botnames.items():
        intents_mode = {}
        for mode in intents.keys():
            pathfile = os.path.join(chatbots_folder, botname, "intents")
            intents_mode.update({mode:get_json_list(intents, mode, pathfile)})
        agent_data = json.load(open(os.path.join(chatbots_folder,
                                                 botname,
                                                 "agent.json")))
        idChatBot = agent_data["googleAssistant"]["project"]
        intents_mode.update({"idChatBot": idChatBot})
        json_intents.update({botname:intents_mode})

    # json to nodes
    intentTree_dict = {}
    for botname, botintgroup in botnames.items():
        botnodes = []
        intents_ids = {}
        it = IntentTree({"name":json_intents[botname]["idChatBot"]},
                        time(), json_intents[botname]["idChatBot"])
        intents_ids["root"] = json_intents[botname]["idChatBot"]
        for nint, intent in enumerate(json_intents[botname]["intents"]):
            # if not intent["fallbackIntent"]:
            intents_ids[intent["id"]] = intent["name"]
            # Para dialogflow sólo importa una de las posibles respuestas
            # Para otros provedores se construye una lista de strings con
            # las posibles respuestas por si llegara a haber.
            if len(intent["events"]) > 0:
                events = intent["events"]
            else:
                events = None
            msgAns = intent["responses"][0]["messages"][0]["speech"]
            # Busca si el intent tiene su llamado mediante una frase
            # del usuario en el arreglo _usersays_, añade msgReq
            # si lo hay
            contextIn = [context.lower() for context in intent["contexts"]]
            # preguntar por el lifespan
            contextOut = [d["name"].lower() for d
                          in intent["responses"][0]["affectedContexts"]]
            parameters = intent["responses"][0]["parameters"]
            ques = [True if botintgroup["intents"][nint][:-5] in elem else False
                    for elem in botintgroup["usersays"]]
            if any(ques):
                qind = ques.index(True)
                usersay_intent = json_intents[botname]["usersays"][qind]
                # Se pueden añadir varios mesgReq
                msgReq = usersay_intent[0]["data"][0]["text"]
            else:
                msgReq=None
            action = None
            if "action" in intent["responses"][0].keys():
                action = intent["responses"][0]["action"]
            build_json = {"name": intent["name"],
                          "id": intent["id"],
                          "parent": None,
                          "action": action,
                          "accuracyPrediction":0, #"mandatory":False,
                          "contextIn": contextIn,
                          "contextOut": contextOut,
                          "msgReq": msgReq,
                          "msgAns": msgAns,
                          "parameters": parameters,
                          "events": events}
            # En dialogflow no necesariamente hay un intent root
            # por lo que se define un root arbitrario
            # con el id del chatbot
            if "parentId" not in intent.keys():
                build_json["parent"] = "root"
            else:
                build_json["parent"] = intent["parentId"]
            # Descomentar para que los intents en el intentTree sólo sean
            # considerados en el árbol cuando haya llamadas por webhook
            # --------------------------------------------------------------
            # if intent["webhookUsed"] != True:
            #     continue
            # --------------------------------------------------------------
            botnodes.append(build_json)
        i = 0
        while len(botnodes) > 0 :
            intent = botnodes[i]
            pa = it.find_node(value=intents_ids[intent["parent"]], to_dict=False)
            if pa is not None:
                intent["parent"] = intents_ids[intent["parent"]]
                it.add_node(intent)
                botnodes.remove(intent)
                i = 0
            else:
                i += 1
        intentTree_dict.update({json_intents[botname]["idChatBot"]:[it]})
    # pick.dump(intentTree_list, open("./Sessions/Conference.pck", "wb"))
    return intentTree_dict

if __name__ == "__main__":
    print("Uno")
