from anytree import (Node, RenderTree, ContStyle,
                     find, PreOrderIter)

"""Defines Intent Node class and include intent fields."""
class IntentNode(Node):
    """Creates a intent node."""
    def __init__(self, parent, **kwargs):
        """Init of IntentNode by params in kwargs.
        Parameters:
        parent : Parent Node.
        kwargs : dictionary object with the parameters for
                 IntentNode
                 -name *,
                 -idField *
                 -value *
                 -accuracyPrediction
                 -mandatory
                 -msgReq
                 -msgAns.
        binding fields are marked with *
        """
        #super().__init__()
        self.parent = parent
        self.spathlist = list()
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.__assignpath()

    def __assignpath(self):
        for nodeparent in self.path:
            self.spathlist.append(nodeparent.name)

    def updateNode(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    # AssignCurrent solo para el ejemplo
    def assignCurrent(self):
        self.current = "True"

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
        nodels - node list for the tree
        loadedDate - str Date-Time
        idChatBot - Id for the current ChatBot
        """
        self.style=ContStyle()
        if "parent" in json_data:
            _ = json_data.pop("parent")
        self.node = IntentNode(None, **json_data)
        self.childiter = list
        self.orderlist = list()
        self.nodels=[self.node]
        self.loadedDate = loadedDate
        self.idChatBot = idChatBot

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
        # if current:
            # json_data.update({"current": "True"})
            # _ = self.getOrderFromCurrent(mandatory=False)
        if isinstance(parent, str):
            parent = self.find_node(parent, False)
            node = IntentNode(parent, **json_data)
            if current:
                node.assignCurrent()
                befnode = self.find_node(self.orderlist[self.index - 1], False)
                delattr(befnode, "current")
                print("deleting current attribute for {0}".format(befnode.name))
                # ------------------------------------------------------------
                # Si ya existe el nombre y el idField solo reasignar campos.
                # ------------------------------------------------------------
        elif isinstance(parent, int):
            parent = self.find_node(self.nodels[parent].name, False)
            node = IntentNode(parent, **json_data)
        self.nodels.append(node)
        self.__LevelOrderlist()

    def fill_node(self, json_data, current=False):
        name = json_data["name"]
        idField = json_data["idField"]
        node = find(self.node,
                    lambda nod: nod.name == name)# and nod.idField == idField)
        if node is not None:
            delattr(node, "current")
            # print("deleting current attribute for {0}".format(node.name))
            nextnode = self.find_node(self.orderlist[self.index + 1], False)
            setattr(nextnode, "current", "True")
            _ = json_data.pop("parent")
            node.updateNode(**json_data)
        else:
            self.add_node(json_data, current)

    def find_node(self, value, to_dict=True, by_field="name"):
        """Find a node by the str name attribute."""
        if by_field == "name":
            node = find(self.node, lambda node: node.name == value)
        # elif by_field == "idField":
        #     node = find(self.node, lambda node: getattr(node, "idField", None) == value)
        else:
            node = find(self.node, lambda node: getattr(node, by_field, None) == value)
        if to_dict and node:
            return node.__dict__
        else:
            return node

    def getOrderFromCurrent(self, mandatory=False, pr=True):
        node = find(self.node, lambda node: getattr(node, "current", None) is not None)
        index = self.orderlist.index(node.name)
        self.index = index
        if pr:
            for i, nodename in enumerate(self.orderlist):
                if i == index + 1:
                    print("-->%s"%nodename)
                else:
                    print("%s"%nodename)
        return self.orderlist[index]

    def __LevelOrderlist(self):
        self.orderlist = [node.name for node in PreOrderIter(self.node)]
