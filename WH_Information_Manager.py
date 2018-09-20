#!/home/ebraintec/anaconda3/bin/python
#-*- coding: utf-8 -*-
import os
import sys
import json
import argparse
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
    parser = argparse.ArgumentParser(description='InfoManager service.')
    parser.add_argument('--port', dest='noport', metavar='NNNN', type=int,
                        help='The port number for webservice listener')
    parser.add_argument('--agent', dest='agentid', metavar='string', type=str,
                        help='The agent id to default set')
    args = parser.parse_args()
    agentid = args.agentid
    noport = args.noport
    if args.agentid is None:
        agentid = "hs-preguntasrespuestas"
    if args.noport is None:
        try:
            noport = readnumport()
        except FileNotFoundError:
            noport = 5050
    _ = writenumport(noport)
    # Rellena el arbol con la info del CB
    if update_Agents() == 0:
        print("WARNING: Error updating agents\n")
    agentid = publishIntentTree("chatbots", agentid)  # "testing-b6df8")
    im = InfoManager(rootdirectory=os.getcwd(), idChatBot=agentid)
    port = int(os.getenv("PORT", noport))
    print("Starting app on port %d" %port)
    app.run(debug=False, port=port, host="0.0.0.0")
