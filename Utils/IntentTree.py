from anytree import (Node, RenderTree, ContStyle,
                     find, PreOrderIter, findall)
import numpy as np

"""Defines Intent Node class and include intent fields."""
class IntentNode(Node):
    """Creates a intent node."""
    def __init__(self, parent, **kwargs):
        """Init of IntentNode by params in kwargs.
        Parameters:
        parent : Parent Node.
        kwargs : dictionary object with the parameters for
                 IntentNode
                 - id
                 - name
                 - accuracyPrediction
                 - msgReq
                 - msgAns
                 - parameters
                 - contextIn
                 - contextOut
                 - action
                 - events
        binding fields are marked with *
        """
        self.parent = parent
        self.spathlist = list()
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.__assignpath()

    def __assignpath(self):
        for nodeparent in self.path:
            self.spathlist.append(nodeparent.name)

    def writeParameter(self, value, name):
        """Write the UserValue into node."""
        parameters = self.parameters
        indices = [True if param["name"] == name else False
                   for param in parameters]
        index = indices.index(True)
        parameters[index]["userValue"] = value
        self.parameters = parameters

    def readParameter(self, name):
        """Read the userValue if exists, else return None."""
        parameters = self.parameters
        indices = [True if param["name"] == name else False
                   for param in parameters]
        index = indices.index(True)
        parameter = parameters[index]
        if "userValue" not in parameter.keys():
            return None
        elif parameter["userValue"] == "":
            return None
        else:
            return parameter["userValue"]

    def updateNode(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def assignCurrent(self):
        self.current = "True"

    def dropCurrent(self):
        delattr(self, "current")

    def toDict(self, keys):
        """keys - list kind object."""
        node_dict = self.__dict__
        dictionary = dict()
        for key in keys:
            dictionary.update({key: node_dict.get(key, "")})
        return dictionary


"""General Tree to manipulate all intents"""
class IntentTree(RenderTree):
    def __init__(self, json_data, loadedDate, idChatBot):
        """Creates the node structure for the conversation with the root.
        Parameters:
        ------------------------------------------------------------------
        json_data - json object or dictionary with the parameters.
        loadedDate - Date for the conversation.
        idChatBot - Id for current chatBot conference.
        ------------------------------------------------------------------
        Attributes:
        node - Root node.
        currentcontextls - context list for the tree
        loadedDate - str Date-Time
        idChatBot - Id for the current ChatBot. ProjectId for DialogFlow
        sessionid - Id for the session, created when the firs request from
                    dialog flow is send.
        """
        self.style=ContStyle()
        if "parent" in json_data:
            _ = json_data.pop("parent")
        self.node = IntentNode(None, **json_data)
        self.childiter = list
        self.orderlist = list()
        self.inputlist = list()
        self.currentcontextls = list()  # self.node]
        self.loadedDate = loadedDate
        self.idChatBot = idChatBot

    def setSession(self, sessionid):
        setattr(self, "sessionid", sessionid)

    def add_node(self, json_data, current=False):
        """Add a node to the intent tree.
        Parameters
        json_data : Dictionary with the data for the node. Have to include
                    the parent field with the name of the parent.
        current : The field "current" is useful at the new node adding by
                  the intent Analysis.
        """
        if "parent" in json_data:
            parent = json_data.pop("parent")
        # if isinstance(parent, str):
        parent = self.find_node(parent, False, "name")
        node = IntentNode(parent, **json_data)
        if current:
            node.assignCurrent()
            befnode = self.find_node(self.orderlist[self.index - 1], False)
            delattr(befnode, "current")
            print("deleting current attribute for {0}".format(befnode.name))
                # ------------------------------------------------------------
                # Si ya existe el nombre y el idField solo reasignar campos.
                # ------------------------------------------------------------
        # elif isinstance(parent, int):
        #     parent = self.find_node(self.nodels[parent].name, False)
        #     node = IntentNode(parent, **json_data)
        # self.nodels.append(node)
        # self.__LevelOrderlist()

    def fill_node(self, json_data, current=False):
        """Fill the current Node with the new contained fields in json_data.
        If exists, Updates the value attribute and adds the msgOriginal
        to current Node, and set "current" for the next node in the order
        list.
        """
        intentid = json_data["id"]
        node = self.find_node(intentid, False, "id")
        pastnode = self.find_node("True", False, "current")
        if pastnode is not None:
            pastnode.dropCurrent()
        node.updateNode(**json_data)
        node.assignCurrent()

    def find_node(self, value, to_dict=True, by_field="name"):
        """Find a node by an arbitrary "field" attribute.

        Parameters:
        value - string value to compare.
        to_dict - Bolean condition to ask for the node or
                  the text dictionary.
        by_field - string attribute.

        Returns:
        node - IntentNode object or dictionary with attributes
               as elements.
        """
        if by_field == "contextOut":
            def la(node):
                attr = getattr(node, by_field, None)
                if attr is not None:
                    if value in attr:
                        return True
        else:
            la = lambda x: getattr(x, by_field, None) == value
        node = find(self.node, la)
        if to_dict and node:
            return node.__dict__
        else:
            return node

    def updateContext(self, contexts):
        for context in contexts:
            if context not in self.currentcontextls:
                self.currentcontextls.append(context)

    def getOrderFromCurrent(self):
        """Get the name for the current node according to orderlist.
        """
        node = find(self.node,
                    lambda node: getattr(node, "current", None) is not None)
        index = self.orderlist.index(node.name)
        self.index = index
        return self.orderlist[index]

    def inputStacklist(self, lastnode):
        """Creates the node list of intentnodes with the input order.
        """
        idnode = lastnode.id
        indices = [True if idnode == node.id else False
                   for node in self.inputlist]
        if any(indices):
            index = indices.index(True)
            _ = self.inputlist.pop(index)
            self.inputlist.append(lastnode)
        else:
            self.inputlist.append(lastnode)

    def fromStackList(self, n_objects, by_field="intent"):
        if by_field == "intent":
            nodes = self.inputlist[-n_objects:]
            attributes = ["id", "name", "msgAns", "parameters",
                          "contextIn", "contextOut", "action",
                          "events"]
            objects = [node.toDict(attributes) for node in nodes]
        elif by_field == "context":
            mask = [True if node.contextOut != [] else False
                       for node in self.inputlist]
            contextOutArray = []
            for i, element in enumerate(mask):
                if element:
                    contextOutArray.append(self.inputlist[i].contextOut)
            objects = contextOutArray[-n_objects:]
        return objects
