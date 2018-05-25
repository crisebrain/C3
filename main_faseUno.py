# from SearchEngine import cognitive_req
import os
import json
from Utils import SessionContainer
from InfoManager import InfoManager
from ChatBotWrapper import ChatBotWrapper
from flask import Flask, request, make_response
#from SearchEngine import cognitive_req
# from ConversationEngine import ChatBotWrapper

app = Flask(__name__)

@app.route("/infomanager", methods=["POST", "GET"])
def webhook2():
    req = request.get_json(silent=True, force=True)
    # print(json.dumps(req, indent=4))
    res = im.interceptIntent(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    return r

if __name__ == "__main__":
    # Por ahora con estas dos funciones se puede trabajar
    chbw = ChatBotWrapper("chatbots", "testing-b6df8")   # Rellena el arbol con la info del CB
    idChatBot = chbw.current_intentTree
    im = InfoManager(SessionContainer,
                     rootdirectory=os.getcwd(),
                     idChatBot=idChatBot)  # carga el arbol al contenedor SC
    port = int(os.getenv("PORT", 5050))
    print("Starting app on port %d" %port)
    app.run(debug=True, port=port, host="0.0.0.0")

    # # este control lo va a llevar
    # # el usuario con las peticions
    # i = 0
    # qs = len((im.sc.extractTree()).orderlist)
    # while(True):#i < qs):
    # # -------------------------------------------
    #     json_data = chbw.interceptIntent(im)   # emular entrada de dialogflow con un json a modo
    #                                            # aqui me dice si el intent fue reconocido
    #     # im.intentFlow(json_data, chbw, cognitive_req)
    #     i += 1
    # im.sc.ShowSessionTree()
