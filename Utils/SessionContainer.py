from .IntentTree import IntentTree, IntentNode
import os
import json

class SessionContainer:

    def __init__(self, CBW):
        """Class to contain the intentTree, from ChatBotWrapper CBW instance."""
        self.addSessionTree(CBW.current_intentTree,
                            CBW.current_intentTree.idChatBot)
        delattr(CBW, "current_intentTree")

    def addSessionTree(self, tree, idChatBot):
        # tree.node.assignCurrent()
        setattr(self, idChatBot, tree)
        self.current_intentTree = idChatBot
        return 0

    def extractTree(self, idChatBot=None):
        if idChatBot is None:
            return getattr(self, self.current_intentTree)
        else:
            return getattr(self, idChatBot)

    def ShowSessionTree(self):
        print("Id : %s\n" %(self.current_intentTree))
        tree = self.extractTree()
        for i,(pre, fill, node) in enumerate(tree):
            if not node.is_root:
                stchain = "%s #_%d  %s  %s" % (pre, i, node.msgReq,
                                                  node.name)# node.value)
                if getattr(node, "current", None) is not None:
                    stchain = stchain + " --- "
                if getattr(node, "mandatory", None) is not None:
                    stchain = stchain + " *** "
                print(stchain)
            # print("\n\n", node, "\n\n")
        print("\nmandatory: ****\ncurrent: ---")

    def WhosNextEntry(self):
        """Extracts the next field to fill."""
        tree = self.extractTree()
        name = tree.getOrderFromCurrent()
        node = tree.find_node(name, False)
        ddata_node = node.__dict__
        ddata = {}
        for key, value in ddata_node.items():
            if key in ["idField", "msgAns", "name", "msgReq"]:
                ddata.update(dict(zip([key], [value])))
        ddata.update({"parent":node.spathlist[node.depth - 1]}) # No va asi
        return ddata

    def feedNextEntry(self, json_data):
        """Fill the fields next to the current."""
        tree = self.extractTree()
        tree.fill_node(json_data, True)
        #setattr(self, "C_" + self.Conversation_dict["IdConference"], tree)

    def __NewSessionTree(self, conversation_dict):
        """Creates the tree from an conversation_dict.
        This function doesn't works with the dialog flow structure.
        """
        for index, intent in enumerate(conversation_dict['Session']):
            if index == 0:
                it = IntentTree(intent, conversation_dict["CreationDate"],
                                conversation_dict["IdConference"])
            else:
                it.add_node(intent)
        it.getOrderFromCurrent()
        return it
