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
    """Listener method for POST request to connect the InfoManager."""
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
    """Reads the port number stored in _NoPORT_IM.temp."""
    with open("metadata/_NoPORT_IM.temp", "r") as fnoport:
        numport = int(fnoport.read().strip())
    return numport

def writenumport(numport):
    """Writes the port number into _NoPORT_IM.temp."""
    with open("metadata/_NoPORT_IM.temp", "w") as fnoport:
        fnoport.write(str(numport))
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='InfoManager service.')
    parser.add_argument('--port', dest='noport', metavar='NNNN', type=int,
                        help='The port number for webservice listener')
    parser.add_argument('--agent', dest='agentid', metavar='string', type=str,
                        help='The agent id to default set')
    parser.add_argument('--debug', dest='debug', metavar='N', type=int,
                        help='debug mode, 1 for turn on')
    # asignacion de puerto del webhook e id de agente para construccion por
    # defecto de arbol en conference (puede cambiar)
    args = parser.parse_args()
    agentid = args.agentid
    noport = args.noport
    debug = bool(args.debug)
    # -------------------------------------------------------------------
    if args.agentid is None:
        agentid = "hs-preguntasrespuestas"
    if args.noport is None:
        try:
            noport = readnumport()
        except FileNotFoundError:
            noport = 5050
    _ = writenumport(noport)
    # Descarga los agentes cuyas llaves esten listadas en keyfiles_path.json
    if update_Agents() == 0:
        print("WARNING: Error updating agents\n")
    # Crea los esqueletos de los arboles en el conference.pck
    agentid = publishIntentTree("chatbots", agentid)
    # Crea la instancia del infomanager
    im = InfoManager(rootdirectory=os.getcwd(), idChatBot=agentid)
    # Levanta listener para el webhook del infomanager
    port = int(os.getenv("PORT", noport))
    print("Starting app on port %d" %port)
    app.run(debug=debug, port=port, host="0.0.0.0")
