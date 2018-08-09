#!/home/ebraintec/anaconda3/bin/python
#-*- coding: utf-8 -*-
import os
import sys
import json
from InfoManager import InfoManager, publishIntentTree
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
    print(req)
    action = req.get("action")
    if action == "obtieneDatos":
        res = im.datumCSE_Facturas(req)
    else:
    # print(json.dumps(req, indent=4))
        res = im.interceptIntent(req)
    res = json.dumps(res)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

if __name__ == "__main__":
    # Rellena el arbol con la info del CB
    if len(sys.argv) > 1:
        noport = sys.argv[1]
    else:
        noport = 5050
    with open("metadata/_NoPORT_IM.txt", "w") as fnoport:
        fnoport.write(str(noport))

    idChatBot = publishIntentTree("chatbots", "chatfase1")  # "testing-b6df8")
    im = InfoManager(rootdirectory=os.getcwd(), idChatBot=idChatBot)
    port = int(os.getenv("PORT", noport))
    print("Starting app on port %d" %port)
    app.run(debug=True, port=port, host="0.0.0.0")
