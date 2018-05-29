from .IntentTree import IntentTree, IntentNode
import os
import json
import pickle
import copy

class SessionContainer:
    """Admin class for the intentTree.
    Responsabilities:
    - Load the specified tree with the respective idChatBot on '__init__'
    - Show the filled intentTree with 'ShowSessionTree'
    - Feed the intent Node with the specs from infomanager on 'feedNextEntry'
    - Find the current Node with 'WhosNextEntry'
    - Fetch the context variables on 'unknownFunctionName'.
    """
    def __init__(self, pathpicklefile, idChatBot=None):
        """Class to contain the intentTree loaded from piclefile"""
        intentTree_dict = pickle.load(open(pathpicklefile, "rb"))
        tree = intentTree_dict[idChatBot][0]
        setattr(self, idChatBot, tree)
        self.current_intentTree = tree.idChatBot

    def reassingTree(self, sessionnumber):
        tree = self.extractTree()
        tree.setSession(sessionnumber)
        setattr(self, self.current_intentTree, tree)

    def extractTree(self, idChatBot=None):
        """Extracts the intent tree from the sc object."""
        return getattr(self, self.current_intentTree)

    def ShowSessionTree(self):
        """Prints the tree contained in sc object."""
        print("Id : %s\n" %(self.current_intentTree))
        tree = self.extractTree()
        for i,(pre, fill, node) in enumerate(tree):
            if not node.is_root:
                stchain = "%s #_%d  %s" % (pre, i, node.name)
                # isfilled = [True if "userValue" in param.keys() else False
                #             for param in node.parameters]
                # if any(isfilled):
                #     index = isfilled.index(True)
                #     value = node.parameters[index]["userValue"]
                #     stchain += "      %s  " % value
                if getattr(node, "msgReq", None) is not None:
                    stchain = stchain + "  {0}".format(node.msgReq)
                if getattr(node, "current", None) is not None:
                    stchain = stchain + " --- "
                print(stchain)
            else:
                print("root")
            # print("\n\n", node, "\n\n")
        print("\ncurrent: ---")

    # def WhosNextEntry(self):
    #     """Extracts the next field to fill."""
    #     tree = self.extractTree()
    #     name = tree.getOrderFromCurrent()
    #     node = tree.find_node(name, False)
    #     ddata_node = node.__dict__
    #     ddata = {}
    #     for key, value in ddata_node.items():
    #         if key in ["action", "msgAns", "name", "msgReq"]:
    #             ddata.update(dict(zip([key], [value])))
    #     ddata.update({"parent":node.spathlist[node.depth - 1]}) # No va asi
    #     return ddata

    # def feedNextEntry(self, json_data, contexts):
    #     """Feed the fields on the specified node."""
    #     tree = self.extractTree()
    #     tree.fill_node(json_data, True)
    #     #setattr(self, "C_" + self.Conversation_dict["IdConference"], tree)

    # def __NewSessionTree(self, conversation_dict):
    #     """Creates the tree from an conversation_dict.
    #     This function doesn't works with the dialog flow structure.
    #     """
    #     for index, intent in enumerate(conversation_dict['Session']):
    #         if index == 0:
    #             it = IntentTree(intent, conversation_dict["CreationDate"],
    #                             conversation_dict["IdConference"])
    #         else:
    #             it.add_node(intent)
    #     it.getOrderFromCurrent()
    #     return it
