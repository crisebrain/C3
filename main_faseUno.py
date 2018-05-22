# from SearchEngine import cognitive_req
from Utils import SessionContainer
from InfoManager import InfoManager
from ChatBotWrapper import ChatBotWrapper
from SearchEngine import cognitive_req
# from ConversationEngine import ChatBotWrapper

if __name__ == "__main__":
    # Por ahora con estas dos funciones se puede trabajar
    chbw = ChatBotWrapper("chatbots")   # Rellena el arbol con la info del CB
    im = InfoManager(SessionContainer, chbw)  # carga el arbol al contenedor SC

    # este control lo va a llevar
    # el usuario con las peticions
    i = 0
    qs = len((im.sc.extractTree()).orderlist)
    while(True):#i < qs):
    # -------------------------------------------
        json_data = chbw.interceptIntent(im)   # emular entrada de dialogflow con un json a modo
                                               # aqui me dice si el intent fue reconocido
        # im.intentFlow(json_data, chbw, cognitive_req)
        i += 1
    im.sc.ShowSessionTree()
