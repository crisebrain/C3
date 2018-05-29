#!/home/ebraintec/anaconda3/bin/python
#-*- coding: utf-8 -*-
import urllib
import json
import os
from flask import Flask, request, make_response
import requests
# from Services import makeWebhookResult

def post_data(jdata, link="http://0.0.0.0:5050/infomanager"):
    r = requests.post(link, data=jdata)
    # print(json.dumps(r.json(), indent=4))
    # Ajustar salida si r no es la respuesta esperada
    return r.json()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def retornodummy():
    r = make_response("ItWorks")
    return r

@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    req = request.get_json(silent=True, force=True)
    # print(json.dumps(req, indent=4))
    res = post_data(json.dumps(req))
    res = json.dumps(res, indent=4)
    #print(json.dumps(req, indent=4))
    # print(res)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print("Starting app on port %d" %port)
    app.run(debug=True, port=port, host="0.0.0.0")
