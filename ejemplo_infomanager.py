# from SearchEngine import cognitive_req
from Utils import SessionContainer
from InfoManager import InfoManager
from ChatBotWrapper import ChatBotWrapper
# from ConversationEngine import ChatBotWrapper

def cognitive_req(data):
    """
    recibe un arreglo json que contiene al menos un campo
    y cuyo campo es 'msgOriginal'
    """
    msg = data['msgReq']
    print("El mensaje original recibido es:", msg)
    value = 20000
    nodo1 = {"idField": "credito",
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
    chbw = ChatBotWrapper("chatbots")
    im = InfoManager(SessionContainer, chbw)
    i = 0
    qs = len((im.sc.extractTree()).orderlist)
    ids = ["name", "action", "provider_name", "affiliation"]
    while(i < qs):
        json_data = chbw.interceptIntent(im)
        if i < qs - 1:
            json_data.update({"idvalue":ids[i]})
            im.intentFlow(json_data, chbw, cognitive_req)
        else:
            break
        i += 1
    im.sc.ShowSessionTree()


# im = InfoManager(SessionContainer, ChatBotWrapper, cognitive_req)
# jdata = im.newconsult()
# im.newAnswer(jdata)
# jdata = im.newconsult()
# im.newAnswer(jdata)
# jdata = im.newconsult()
# im.newAnswer(jdata)
