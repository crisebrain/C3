from anytree import Node, RenderTree, ContStyle

"""Define Intent Node class and include intent fields."""
class IntentNode(Node):    
    def __init__(self, name, parent, idField, value, accuracyPrediction, mandatory, msgReq, msgAns):
        """Init of IntentNode."""
        #super().__init__()
        self.name = name
        self.parent = parent
        self.idField= idField
        self.value = value
        self.accuracyPrediction = accuracyPrediction
        self.obligatorio = mandatory
        self.msgReq = msgReq
        self.msgAns = msgAns

"""General Tree to manipulate all intents"""
class IntentTree(RenderTree):
    def __init__(self, nodeRoot, loadedDate, idChatBot):
      self.style=ContStyle()
      self.childiter=list
      self.node = nodeRoot
      self.loadedDate = loadedDate
      self.idChatBot = idChatBot		

if __name__ == "__main__":
    root = IntentNode(name="Saludo", parent=None, idField="nombre", value="Francis", accuracyPrediction=None, mandatory=True, msgReq="Hola, mi nombre es Francis", msgAns="Bienvenida Francis, que puedo hacer por tí hoy?")
    intent1 = IntentNode(name="ConsultaSaldo", parent=root, idField=None, value=None, accuracyPrediction=None, mandatory=False, msgReq="Quiero consultar mi saldo", msgAns="Puedes proporcionarme tu número de cuenta?")
    intent2 = IntentNode(name="NumCuenta", parent=intent1, idField="num_cuenta", value="010101", accuracyPrediction=None, mandatory=True, msgReq="Claro, el número de cuenta es 010101", msgAns="Muchas gracias, tu saldo es de 300 y vence mañana.")
    tree = IntentTree(root, loadedDate="22/04/2018", idChatBot=1)
    for pre, fill, node in tree:
        print("%s%s" % (pre, node.name))
    print("A conversation flow:")
    print(intent2)