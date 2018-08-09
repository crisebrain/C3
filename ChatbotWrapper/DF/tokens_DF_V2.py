# -*- coding: utf-8 -*-
import json
import os
import sys
import subprocess

from flask import Flask, request, make_response

app = Flask(__name__)


@app.route("/", methods=["GET"])
def retornodummy():
    r = make_response("ItWorks")
    return r


@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = getToken(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r


def getToken(req: dict):
    print("{} - {} request token for {} agent.".format(req["client"], req["session"], req["agent"]))

    # Obtenemos token de google (Ver documentación de como generar el token)
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"])
    token = token.decode("utf-8").strip()

    print("{} - {} token: {}".format(req["client"], req["session"], token))


    return {"token": token, "returnCode": 1}


if __name__ == "__main__":
    if len(sys.argv) > 1:
        portnumber = int(sys.argv[1])
    else:
        portnumber = 6000
    port = int(os.getenv("PORT", portnumber))
    print("Starting token server on port %d" %port)
    app.run(debug=True, port=port, host="0.0.0.0")
