# from SearchEngine import cognitive_req
from Utils import SessionContainer
from InfoManager import InfoManager
# from ConversationEngine import ChatBotWrapper

class ChatBotWrapper():
    def __init__(self, IdChatBot):
        self.publishIntenttree(IdChatBot)

    def publishIntenttree(self, IdChatBot):
        self.IdChatBot = IdChatBot
        print(IdChatBot)

    def IntentInterrupt(self, im):
        jdata = im.newConsult()
        print(jdata["msgReq"])
        jdata["name"] = None
        value = input()
        # simulacion de construccion de mensaje
        if value.isdigit():
            jdata.update({"value": value})
            jdata.update({"name": "Ampliacion"})
            jdata.update({"msgAns": "tu respuesta es {0}".format(value)})
            jdata.update({"state": "valid"})
        else:
            jdata.update({"msgAns": ""})
            jdata.update({"state": "no_valid"})
        return jdata

    def showResponse(self, jdata):
        print(jdata["msgAns"])

def cognitive_req(data):
    """
    recibe un arreglo json que contiene al menos un campo
    y cuyo campo es 'msgOriginal'
    """
    msg = data['msgReq']
    print("El mensaje original recibido es:", msg)
    value = 20000
    nodo1 = {"IdField": "credito",
             "value": 20000,
             "name": "Ampliacion",
             "acc": 98.7,
             "mandatory": "direccion",
             "txtEntrada": msg,
             "msgAns": "Si hay ampliacion por %d" %value
             }
    nodosList = [nodo1]
    return nodosList

if __name__ == "__main__":
    im = InfoManager(SessionContainer)
    IdChatBot = (im.sc.extractTree()).idChatBot
    chbw = ChatBotWrapper(IdChatBot)
    while(True):
        json_data = chbw.IntentInterrupt(im)
        im.intentFlow(json_data, chbw, cognitive_req)
        im.sc.ShowSessionTree()


# im = InfoManager(SessionContainer, ChatBotWrapper, cognitive_req)
# jdata = im.newconsult()
# im.newAnswer(jdata)
# jdata = im.newconsult()
# im.newAnswer(jdata)
# jdata = im.newconsult()
# im.newAnswer(jdata)
