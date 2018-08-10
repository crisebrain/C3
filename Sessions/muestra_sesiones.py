import os
import sys
import pickle
sys.path.append("..")
from Utils import SessionContainer

def menu(keys, sesion=False):
    if sys.platform == 'linux':
        os.system('clear')
    else:
        os.system('cls')
    if not sesion:
        print ("Selecciona el tipo de chatbot")
        for i, key in enumerate(keys):
            print ("\t{0} - chat: {1}".format(i+1, key))
    else:
        print ("Selecciona la sesion")
        for i, key in enumerate(keys):
            if key is not None:
                print ("\t{0} - chat: {1}".format(i+1, key))
            else:
                print ("\t{0} - chat: Plantilla".format(i+1))
    print ("\t0 - salir")

if __name__ == "__main__":
    sesiones = pickle.load(open("Conference.pck", "rb"))
    chatnames = [key for key in sesiones.keys()]
    idsesiones = dict()
    for key in chatnames:
        trees = sesiones[key]
        ids = [getattr(tree, "sessionid", None) for tree in trees]
        idsesiones.update(dict(zip([key], [ids])))
    while True:
        menu(chatnames)
        opcionMenu = input("inserta un numero valor >> ")
        if int(opcionMenu) <= len(chatnames)  and opcionMenu != "0":
            indname = chatnames[int(opcionMenu)-1]
            # carga el arreglo de chatbots con el nombre seleccionado
            sc = SessionContainer("Conference.pck", indname)
            menu(idsesiones[indname], True)
            opcion2 = input("inserta un numero valor >> ")
            if int(opcion2) <= len(idsesiones[indname]):
                indlist = int(opcion2)-1
                sesion = idsesiones[indname][indlist]
                # muestra el arbol correspondiente a la sesion elegida
                sc.reassignTree(sesion)
                sc.ShowSessionTree()
            input("\npulsa una tecla para continuar")
        elif opcionMenu=="0":
            break
        else:
            print ("")
            input("No has pulsado ninguna opción correcta..." \
                  "\npulsa una tecla para continuar")
