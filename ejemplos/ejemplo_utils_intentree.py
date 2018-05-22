from time import time
from Utils import IntentNode, IntentTree

session = [{"name":"Saludo", "IdField":"nombre",
            "parent": "None",
            "value":"Ramon", "accuracyPrediction":"100",
            "mandatory":"True",
            "msgReq":"Hola, mi nombre es Francis",
            "msgAns":"Bienvenida Francis, que puedo hacer por tí hoy?"},
           {"parent": "Saludo", "IdField":"saludo",
            "name":"ConsultaSaldo", "value":"13", # idField=None, value=None, accuracyPrediction=None
            "mandatory":"False", "msgReq":"Quiero consultar mi saldo",
            "msgAns":"Puedes proporcionarme tu número de cuenta?"},
           {"name":"Numcuenta", "IdField":"num_cuenta",
            "parent": "Saludo",
            "value":"34322", "mandatory":"True",
            "msgReq":"Claro, el número de cuenta es 010101",
            "msgAns":"Muchas gracias, tu saldo es de 300 y vence mañana."},
           {"parent": "Saludo", "IdField":"num_cuenta",
            "name":"Sexo", "value":"Masculino",
            "msgAns":"Buenos días caballero, ¿en que puedo ayudarlo?"},
           {"parent": "Numcuenta",
            "name":"TarjetaCredito", "IdField":"credito",
            "value":"0913234112", "accuracyPrediction":"80",
            "msgReq":"Claro, el número de cuenta es 0913234112",
            "msgAns":"Su saldo es -100, Pague por las buenas"}]

## El arbol de nodos se crea con un diccionario para el nodo raiz
for i in range(len(session)):
    if i == 0:
        it = IntentTree(session[i], loadedDate="23-04-2018",
                        idChatBot="01312")
    else:
        it.add_node(session[i])

print("\nArbol de conversacion:\n")
for pre, fill, node in it:
    print("%s%s" % (pre, node.name))
print("\nUn flujo de conversacion:\n")
print(it.nodels[-1])
print("\nBusqueda de nodo\n")
print(it.find_node(value="ConsultaSaldo", to_dict=True))
