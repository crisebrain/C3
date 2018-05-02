from .IntentTree import IntentTree, IntentNode
import os
import json

class SessionContainer:
    def __init__(self, tree, idChatBot):
        self.addSessionTree(tree, idChatBot)

    def addSessionTree(self, tree, idChatBot):
        tree.node.assignCurrent()
        setattr(self, idChatBot, tree)
        self.current_intentTree = idChatBot

    def extractTree(self):
        return getattr(self, self.current_intentTree)

    def ShowSessionTree(self):
        print("Id : %s\n" %(self.current_intentTree))
        tree = self.extractTree()
        for i,(pre, fill, node) in enumerate(tree):
            stchain = "%s #_%d  %s  %s %s" % (pre, i, node.idField,
                                                  node.name, node.value)
            if getattr(node, "current", None) is not None:
                stchain = stchain + " --- "
            if getattr(node, "mandatory", None) is not None:
                stchain = stchain + " *** "
            print(stchain)
        print("\nmandatory: ****\ncurrent: ---")

    def WhosNextEntry(self):
        """Extracts the next field to fill."""
        tree = self.extractTree()
        name = tree.getOrderFromCurrent(pr=False)
        node = tree.find_node(name, False)
        ddata_node = node.__dict__
        ddata = {}
        for key, value in ddata_node.items():
            if key in ["idField", "msgAns", "name", "msgReq"]:
                ddata.update(dict(zip([key], [value])))
        ddata.update({"parent":node.spathlist[node.depth - 1]})
        return ddata

    def feedNextEntry(self, json_data):
        """Fill the field next to the current."""
        tree = self.extractTree()
        tree.fill_node(json_data, True)
        #setattr(self, "C_" + self.Conversation_dict["IdConference"], tree)

    def __NewSessionTree(self, conversation_dict):
        for index, intent in enumerate(conversation_dict['Session']):
            if index == 0:
                it = IntentTree(intent, conversation_dict["CreationDate"],
                                conversation_dict["IdConference"])
            else:
                it.add_node(intent)
        it.getOrderFromCurrent()
        return it

    # def updateConferences(self):
    #     with open(self.__jspath, "w") as jsf:
    #         json.dump(self.Conversation_dict, jsf, sort_keys = True,
    #                   indent = 4, ensure_ascii = True)

    # def __ConstructSessionTrees(self):
    #     conversation_dict = self.Conversation_dict["Conversation"]
    #     tree = self.__NewSessionTree(conversation_dict)
    #     setattr(self, "C_" + conversation_dict["IdConference"], tree)
    #     self.IdConference = conversation_dict["IdConference"]
