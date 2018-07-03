#!/home/ebraintec/anaconda3/bin/python
#-*- coding: utf-8 -*-
import urllib
import json
import os
import sys
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
    #print(json.dumps(req, indent=4))
    # aqui se necesita pasar la funcion creadora de
    # logfile porque los imports relativos no lo permiten
    res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    # print(r)
    return r


if __name__ == "__main__":
    portnumber = sys.argv[1]
    port = int(os.getenv("PORT", portnumber))
    print("Starting app on port %d" %port)
    app.run(debug=True, port=port, host="0.0.0.0")
