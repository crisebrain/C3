from anytree import Node, RenderTree, ContStyle, find
from time import time

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
        for key, value in kwargs.items():
            setattr(self, key, value)


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
        loadedDate - Date into float time
        idChatBot - Id for the current ChatBot
        """
        self.style=ContStyle()
        self.node = IntentNode(None, **json_data)
        self.childiter = list
        self.nodels=[self.node]
        self.loadedDate = loadedDate
        self.idChatBot = idChatBot

    def add_node(self, json_data, parent=None):
        """Add a node to the intent tree.
        Parameters
        json_data : Dictionary with the data for the node.
        parent : parent Node, if None (Default) the parent will be the rootnode.
                 If parent is a string, the node will be searched by find_node
                 method using the name attribute. If it's an integer the parent
                 will be assigned by the position on the nodels list.
        """
        if parent == None:
            parent = self.node
            node = IntentNode(parent, **json_data)
        elif isinstance(parent, str):
            parent = self.find_node(parent, False)
            node = IntentNode(parent, **json_data)
        elif isinstance(parent, int):
            parent = self.find_node(self.nodels[parent].name, False)
            node = IntentNode(parent, **json_data)
        self.nodels.append(node)

    def find_node(self, name, to_dict=True):
        """Find a node by the str name attribute."""
        node = find(self.node, lambda node: node.name == name)
        if to_dict:
            return node.__dict__
        else:
            return node


if __name__ == "__main__":

    # root = IntentNode(name="Saludo", parent=None, idField="nombre",
    #                   value="Francis", accuracyPrediction=None, mandatory=True,
    #                   msgReq="Hola, mi nombre es Francis",
    #                   msgAns="Bienvenida Francis, que puedo hacer por tí hoy?")
    # intent1 = IntentNode(name="ConsultaSaldo", parent=root, idField=None,
    #                      value=None, accuracyPrediction=None, mandatory=False,
    #                      msgReq="Quiero consultar mi saldo",
    #                      msgAns="Puedes proporcionarme tu número de cuenta?")
    # intent2 = IntentNode(name="NumCuenta", parent=intent1, idField="num_cuenta",
    #                      value="010101", accuracyPrediction=None,
    #                      mandatory=True,
    #                      msgReq="Claro, el número de cuenta es 010101",
    #                      msgAns="Muchas gracias, tu saldo es de 300 y vence mañana.")
    # tree = IntentTree(root, loadedDate="22/04/2018", idChatBot=1)


    # Para poder adjuntar los nodos de manera automatizada revisar
    # IntentTree.add_node()

    droot = {"name":"Saludo", "idField":"nombre", "value":"Ramon",
             "accuracyPrediction":"100", "mandatory":"True",
             "msgReq":"Hola, mi nombre es Francis",
             "msgAns":"Bienvenida Francis, que puedo hacer por tí hoy?"}

    int1 = {"name":"ConsultaSaldo", "value":"13",
            # idField=None, value=None, accuracyPrediction=None
            "mandatory":"False",
            "msgReq":"Quiero consultar mi saldo",
            "msgAns":"Puedes proporcionarme tu número de cuenta?"}

    int2 = {"name":"Numcuenta", "idField":"num_cuenta", "value":"34322",
            "mandatory":"True",
            "msgReq":"Claro, el número de cuenta es 010101",
            "msgAns":"Muchas gracias, tu saldo es de 300 y vence mañana."}

    int3 = {"name":"Sexo", "value":"Masculino",
            "msgAns":"Buenos días caballero, ¿en que puedo ayudarlo?"}

    int4 = {"name":"TarjetaCredito", "idField":"credito",
            "value":"0913234112",
            "accuracyPrediction":"80",
            "msgReq":"Claro, el número de cuenta es 0913234112",
            "msgAns":"Su saldo es -100, Pague por las buenas"}

    it = IntentTree(droot, time(), '0901')
    ## El arbol de nodos se crea con un diccionario para el nodo raiz
    it.add_node(int1, "Saludo")
    # Los demas nodos se pueden ir adjuntando con el nombre del nodo padre
    # o con la posicion en la lista nodels o None por Default
    it.add_node(int2, "ConsultaSaldo")
    it.add_node(int3, "Saludo")
    it.add_node(int4, -2)

    print("\nArbol de conversacion:\n")
    for pre, fill, node in it:
        print("%s%s" % (pre, node.name))
    print("\nUn flujo de conversacion:\n")
    print(it.nodels[-1])
    print("\nBusqueda de nodo\n")
    print(it.find_node(name="ConsultaSaldo", to_dict=True))
