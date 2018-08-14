# -*- coding: utf-8 -*-
import json
import os
import sys
import subprocess
from flask_cors import CORS
from flask import Flask, request, make_response

CERT_FILE = "/home/gabriel/Documentos/Certificados/misitio_crt.pem"
KEY_FILE = "/home/gabriel/Documentos/Certificados/misitio_key.pem"

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def retornodummy():
    r = make_response("ItWorks")
    return r


@app.route("/getToken", methods=["POST", "GET"])
def webhook():
    req = request.get_json(silent=True, force=True)
    try:
        res = getToken(req)
    except:
        res = {
            "token": str(sys.exc_info()),
            "returnCode": 0
        }
    finally:
        res = json.dumps(res, indent=4)
        r = make_response(res)
        r.headers["Content-Type"] = "application/json"
        return r


def getToken(req: dict):
    print("{} - {} request token for {} agent.".format(req["client"], req["session"], req["agent"]))

    _setJson(req["agent"], req["client"])

    # Obtenemos token de google (Ver documentación de como generar el token)
    token = subprocess.check_output(["gcloud", "auth", "application-default", "print-access-token"])
    token = token.decode("utf-8").strip()

    print("{} - {} token: {}".format(req["client"], req["session"], token))

    return {"token": token, "returnCode": 1}


def _setJson(agent: str, client: str):
    # Paths for json files
    DICT_AGENT_CLIENT = {
        "facturasvoz-estable": {
            "paginaWeb": "/home/gabriel/Documentos/Keys_DF/facturasvoz-estable-ae59624e7be6_cliente.json"
        }
    }

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = DICT_AGENT_CLIENT[agent][client]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        portnumber = int(sys.argv[1])
    else:
        portnumber = 6010
    port = int(os.getenv("PORT", portnumber))

    print("Starting token server on port %d" %port)
    app.run(debug=True, port=port, host="0.0.0.0",
            ssl_context=(CERT_FILE, KEY_FILE))
