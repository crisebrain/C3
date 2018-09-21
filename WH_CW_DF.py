#!/home/ebraintec/anaconda3/bin/python
# -*- coding: utf-8 -*-
import json
import os
import sys
import argparse
from flask import Flask, request, make_response
from Services import makeWebhookResult

app = Flask(__name__)


@app.route("/", methods=["GET"])
def retornodummy():
    r = make_response("ItWorks")
    return r


@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='InfoManager service.')
    parser.add_argument('--port', dest='noport', metavar='NNNN', type=int,
                        help='The port number for webservice listener')
    parser.add_argument('--debug', dest='debug', metavar='N', type=int,
                        help='debug mode, 1 for turn on')
    args = parser.parse_args()
    # asignacion de puerto del webhook y modo debug
    noport = args.noport
    debug = bool(args.debug)
    # --------------------------------------------------------------------
    if args.noport is None:
        noport = 5000
    port = int(os.getenv("PORT", noport))
    print("Starting app on port %d" %port)
    app.run(debug=debug, port=port, host="0.0.0.0")
