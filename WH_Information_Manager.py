#!/home/ebraintec/anaconda3/bin/python
#-*- coding: utf-8 -*-
import os
import sys
import json
from InfoManager import InfoManager, publishIntentTree, update_Agents
from flask import Flask, request, make_response
#from SearchEngine import cognitive_req

app = Flask(__name__)

@app.route("/", methods=["GET"])
def retornodummy():
    r = make_response("ItWorks")
    return r

@app.route("/infomanager", methods=["POST", "GET"])
def webhook2():
    req = request.get_json(silent=True, force=True)
    action = req.get("action")
    if action == "obtieneDatos":
        res = im.datumCSE_Facturas(req)
    elif action == "recuperaValores":
        res = im.fetchValues(req)
    else:
        # print(json.dumps(req, indent=4))
        res = im.interceptIntent(req)
    res = json.dumps(res)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

def readnumport():
    with open("metadata/_NoPORT_IM.temp", "r") as fnoport:
        numport = int(fnoport.read().strip())
    return numport

def writenumport(numport):
    with open("metadata/_NoPORT_IM.temp", "w") as fnoport:
        fnoport.write(str(numport))
    return 0


if __name__ == "__main__":
    idChatBot = "hs-preguntasrespuestas"
    if len(sys.argv) == 2:
        noport = sys.argv[1]
        _ = writenumport(noport)
    elif len(sys.argv) > 2:
        noport = sys.argv[1]
        _ = writenumport(noport)
        idChatBot = sys.argv[2]
    else:
        try:
            noport = readnumport()
        except FileNotFoundError:
            noport = 5050
            _ = writenumport(noport)
    # Rellena el arbol con la info del CB
    update_Agents()
    idChatBot = publishIntentTree("chatbots", idChatBot)  # "testing-b6df8")
    im = InfoManager(rootdirectory=os.getcwd(), idChatBot=idChatBot)
    port = int(os.getenv("PORT", noport))
    print("Starting app on port %d" %port)
    app.run(debug=True, port=port, host="0.0.0.0")
