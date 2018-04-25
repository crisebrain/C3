from time import time
from ConversationTree import IntentNode, IntentTree
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
