#!/home/ebraintec/anaconda3/bin/python
# -*- coding: utf-8 -*-
import json
import os
import sys
import subprocess

from flask_cors import CORS
from flask import Flask, request, make_response
from datetime import datetime
from Utils.logtofile import CreateLogger
import time

_CERT_FILE = "/home/ebraintec/certificados/misitio_crt.pem"
_KEY_FILE = "/home/ebraintec/certificados/misitio_key.pem"
_GCLOUD_FILE = "/home/ebraintec/bin/google-cloud-sdk/bin/gcloud"

# Paths for json files
_DICT_AGENT_CLIENT = {
    "facturasvoz-estable": {
        "paginaWeb": "/home/ebraintec/Keys_DF/facturasvoz-estable-ae59624e7be6_cliente.json"
    }
    # TODO: generar key para saltos en im y tomar en cuenta la variable de
    # ambiente con el path de gclod
}

# Dict Tokens
_dicTokens = {}


app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def retornodummy():
    r = make_response("ItWorks")
    return r


@app.route("/getToken", methods=["POST", "GET"])
def webhook():
    try:
        req = request.get_json(silent=True, force=True)
        res = getToken(req)
    except Exception as err:
        if conlog:
            errors.logger.info("\n" + str(request.headers) + "\n"+ str(request.__dict__))
            errors.logger.exception(err)
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
    print("{} - {} requesting token for {} agent.".format(req["client"], req["session"], req["agent"]))
    if conlog:
        querys.logger.info(json.dumps(req) + "\n")
    # Verifica si el token existe en caché y sigue siendo válido
    token = _getCachedToken(req["agent"], req["client"])

    if not token:
        _setJson(req["agent"], req["client"])
        # Obtenemos token de google (Ver documentación de como generar el token)
        token = subprocess.check_output([_GCLOUD_FILE, "auth", "application-default", "print-access-token"])
        token = token.decode("utf-8").strip()
        _setTokenCached(req["agent"], req["client"], token)


    print("{} - {} token: {}".format(req["client"], req["session"], token))

    return {"token": token, "returnCode": 1}


def _setJson(agent: str, client: str):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = _DICT_AGENT_CLIENT[agent][client]


def _getCachedToken(agent: str, client: str):
    now = datetime.now()

    if agent in _dicTokens and client in _dicTokens[agent] \
            and (now - _dicTokens[agent][client]["time"]).seconds < 3500:
        return _dicTokens[agent][client]["token"]
    else:
        return None


def _setTokenCached(agent: str, client: str, token: str):
    now = datetime.now()

    # Build new dictonary for tokens
    if not _dicTokens.get(agent):
        _dicTokens[agent] = {}

    _dicTokens[agent] = {
        client: {
            "time": now,
            "token": token
        }
    }


def _test():
    req = {"agent": "facturasvoz-estable",
           "client": "paginaWeb",
           "session": "session1"}

    for i in range(2):
        getToken(req)
        time.sleep(2)
        print(_dicTokens)



if __name__ == "__main__":
    # _test()

    if len(sys.argv) > 1:
        portnumber = int(sys.argv[1])
    else:
        portnumber = 6010
    port = int(os.getenv("PORT", portnumber))

    print("Starting token server on port %d" %port)
    conlog = False
    # Iniciar loggers
    try:
        querys = CreateLogger("querysToken")
        errors = CreateLogger("errorsToken")
        conlog = True
    except (PermissionError, FileNotFoundError):
        print("\n************************* WARNING *************************")
        print("No fue posible crear correctamente los loggers del proyecto")
        print("***********************************************************\n")
    # -------------------------------------------------------------------------
    app.run(debug=True, port=port, host="0.0.0.0",
            ssl_context=(_CERT_FILE, _KEY_FILE))
