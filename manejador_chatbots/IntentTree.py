from anytree import Node, RenderTree, ContStyle

"""Define Intent Node class and include intent fields."""
class IntentNode(Node):
    """Creates a intent node."""
    def __init__(self, parent, **kwargs):
        """Init of IntentNode by params in kwargs."""
        #super().__init__()
        self.parent = parent
        self.name = kwargs['name']
        self.idField = kwargs['idField']
        self.value = kwargs['value']
        self.accuracyPrediction = kwargs['accuracyPrediction']
        self.mandatory = kwargs['mandatory']
        self.msgReq = kwargs['msgReq']
        self.msgAns = kwargs['msgAns']


"""General Tree to manipulate all intents"""
class IntentTree(RenderTree):
    def __init__(self, nodeRoot, loadedDate, idChatBot):
        self.style=ContStyle()
        self.childiter=[nodeRoot]
        self.node = nodeRoot
        self.loadedDate = loadedDate
        self.idChatBot = idChatBot

    def add_node(self, json_data):
        node = IntentNode(self.childiter[-1], **json_data)
        self.childiter.append(node)

    def find_node(name):
        node = find(self.childiter[-1], lambda node: node.name == name)
        return node2json(node)


if __name__ == "__main__":
    uno = dict(name="Ramon", idField="1", value="3",
               accuracyPrediction="100", mandatory=True)
    node = IntentNode(None, **uno)
    print(node)
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
    # for pre, fill, node in tree:
    #     print("%s%s" % (pre, node.name))
    # print("A conversation flow:")
    # print(intent2)
