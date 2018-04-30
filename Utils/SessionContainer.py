from .IntentTree import IntentTree, IntentNode
import os
import json

class SessionContainer:
    def __init__(self):
        folder = "Sessions"
        if not os.path.exists(folder):
            os.mkdir(folder)
        assert os.path.exists(folder), """No existe Directorio 'Sessions',
        Creando directorio, favor de proporcionar archivo json"""

        jspath = os.path.join(folder, "Conference.json")
        assert os.path.exists(jspath), """Directorio 'Sessions' Vacio,
        favor de proporcionar archivo json"""

        print("Cargando archivo {0}".format(jspath))
        with open(jspath, "r") as jfile:
            self.Conversation_dict = json.load(jfile)
        self.__jspath = jspath
        if self.Conversation_dict["Conversation"] is not None:
            self.__ConstructSessionTrees()

    def WhosNextEntry(self):
        """Extracts the next field to fill."""
        tree = self.extractTree()
        name = tree.getOrderFromCurrent(pr=False)
        node = tree.find_node(name, False)
        ddata_node = node.__dict__
        ddata = {}
        for key, value in ddata_node.items():
            if key in ["IdField", "msgAns", "name", "msgReq"]:
                ddata.update(dict(zip([key], [value])))
        ddata.update({"parent":node.spathlist[node.depth - 1]})
        return ddata

    def feedNextEntry(self, json_data):
        """Fill the field next to the current."""
        tree = self.extractTree()
        tree.fill_node(json_data, True)
        #setattr(self, "C_" + self.Conversation_dict["IdConference"], tree)

    def addSessionTree(self, conversation_dict):
        tree = self.__NewSessionTree(conversation_dict)
        setattr(self, "C_" + conversation_dict["IdConference"], tree)
        self.Conversation_dict["Conversation"] = conversation_dict
        self.updateConferences()

    def extractTree(self):
        return self.__getSessionTree(self.IdConference)

    def ShowSessionTree(self):
        IdConference = self.IdConference
        print("Id : %s\n" %(IdConference))
        it = self.__getSessionTree(IdConference)
        IdField = it.node.IdField
        for i,(pre, fill, node) in enumerate(it):
            stchain = "%s #_%d CB_%s  %s : %s" % (pre, i, node.IdField,
                                                  node.name, node.value)
            if getattr(node, "current", None) is not None:
                stchain = stchain + " --- "
            if getattr(node, "mandatory", None) is not None:
                stchain = stchain + " *** "
            print(stchain)
        print("\nmandatory: ****\ncurrent: ---")

    def updateConferences(self):
        with open(self.__jspath, "w") as jsf:
            json.dump(self.Conversation_dict, jsf, sort_keys = True,
                      indent = 4, ensure_ascii = True)

    def __ConstructSessionTrees(self):
        conversation_dict = self.Conversation_dict["Conversation"]
        tree = self.__NewSessionTree(conversation_dict)
        setattr(self, "C_" + conversation_dict["IdConference"], tree)
        self.IdConference = conversation_dict["IdConference"]

    def __getSessionTree(self, IdConference):
        IdConference = "C_" + IdConference
        it = getattr(self, IdConference)
        return it

    def __NewSessionTree(self, conversation_dict):
        for index, intent in enumerate(conversation_dict['Session']):
            if index == 0:
                it = IntentTree(intent, conversation_dict["CreationDate"],
                                conversation_dict["IdConference"])
            else:
                it.add_node(intent)
        it.getOrderFromCurrent()
        return it
